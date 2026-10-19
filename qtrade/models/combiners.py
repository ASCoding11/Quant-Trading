"""Signal combiners: models that turn ~45 weak signals into one forecast.

Every model is trained on a stacked panel of (day, stock) rows where the
features are that day's cross-sectionally z-scored signals (plus the market
regime probabilities) and the target is the stock's *next-period return,
ranked across stocks and mapped to Gaussian scores*. Ranking makes the target
robust to fat tails and removes market moves, which a market-neutral book
does not trade anyway.

Models
------
ridge          linear, L2 penalty chosen on a time-ordered holdout
elastic_net    linear, L1+L2 - zeroes out useless signals
regime_ridge   ridge on signal x regime-probability interactions, so each
               signal's weight can differ by hidden market regime
kernel_ridge   ridge on random Fourier features (Rahimi-Recht), an
               approximation to Gaussian-kernel regression - nonlinear
gbm            histogram gradient-boosted trees - nonlinear with interactions
ic_weighted    Grinold-style: weight each signal by its information ratio
               (mean / std of its daily rank IC) over the training window
"""
from __future__ import annotations

import numpy as np


class BaseModel:
    name = "base"
    uses_regime = False

    def fit(self, X: np.ndarray, y: np.ndarray, R: np.ndarray, day: np.ndarray) -> "BaseModel":
        raise NotImplementedError

    def predict(self, X: np.ndarray, R: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def weights(self) -> np.ndarray | None:
        """Per-signal weights for reporting (linear models only)."""
        return None


# -----------------------------------------------------------------------------
# helpers
# -----------------------------------------------------------------------------
def _ridge_solve(XtX: np.ndarray, Xty: np.ndarray, lam: float, n: int) -> np.ndarray:
    p = XtX.shape[0]
    return np.linalg.solve(XtX + lam * n * np.eye(p), Xty)


def _holdout_split(day: np.ndarray, frac: float = 0.2, embargo: int = 5):
    """Time-ordered split: the last ``frac`` of days validate, with a gap."""
    days = np.unique(day)
    cut = days[int(len(days) * (1 - frac))]
    train = day < cut - embargo
    valid = day >= cut
    return train, valid


def _corr(a: np.ndarray, b: np.ndarray) -> float:
    a = a - a.mean()
    b = b - b.mean()
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 0 else 0.0


def _choose_ridge(X, y, day, grid=(1e-3, 1e-2, 1e-1, 1.0, 10.0)) -> float:
    tr, va = _holdout_split(day)
    if tr.sum() < 1000 or va.sum() < 1000:
        return 1e-1
    XtX = X[tr].T @ X[tr]
    Xty = X[tr].T @ y[tr]
    best, best_lam = -np.inf, grid[0]
    for lam in grid:
        b = _ridge_solve(XtX, Xty, lam, tr.sum())
        score = _corr(X[va] @ b, y[va])
        if score > best:
            best, best_lam = score, lam
    return best_lam


def _subsample(n: int, k: int, rng: np.random.Generator) -> np.ndarray:
    return np.arange(n) if n <= k else np.sort(rng.choice(n, k, replace=False))


# -----------------------------------------------------------------------------
# models
# -----------------------------------------------------------------------------
class RidgeModel(BaseModel):
    name = "ridge"

    def fit(self, X, y, R, day):
        X = X.astype(np.float64)
        self.lam = _choose_ridge(X, y, day)
        self.coef = _ridge_solve(X.T @ X, X.T @ y, self.lam, len(y))
        return self

    def predict(self, X, R):
        return X @ self.coef

    def weights(self):
        return self.coef


class ElasticNetModel(BaseModel):
    name = "elastic_net"

    def __init__(self, max_rows: int = 400_000, seed: int = 0):
        self.max_rows = max_rows
        self.rng = np.random.default_rng(seed)

    def fit(self, X, y, R, day):
        from sklearn.linear_model import ElasticNet

        idx = _subsample(len(y), self.max_rows, self.rng)
        self.m = ElasticNet(alpha=2e-3, l1_ratio=0.5, fit_intercept=False, max_iter=2000, tol=1e-4)
        self.m.fit(X[idx], y[idx])
        return self

    def predict(self, X, R):
        return X @ self.m.coef_

    def weights(self):
        return self.m.coef_


class RegimeRidgeModel(BaseModel):
    """y ~ sum_k p_k(t) * (x' b_k): each regime gets its own signal weights."""

    name = "regime_ridge"
    uses_regime = True

    def __init__(self, max_rows: int = 600_000, seed: int = 0):
        self.max_rows = max_rows
        self.rng = np.random.default_rng(seed)

    @staticmethod
    def _expand(X, R):
        return (X[:, :, None] * R[:, None, :]).reshape(len(X), -1)

    def fit(self, X, y, R, day):
        idx = _subsample(len(y), self.max_rows, self.rng)
        Z = self._expand(X[idx], R[idx]).astype(np.float64)
        self.lam = _choose_ridge(Z, y[idx], day[idx])
        self.coef = _ridge_solve(Z.T @ Z, Z.T @ y[idx], self.lam, len(idx))
        self.K = R.shape[1]
        return self

    def predict(self, X, R):
        return self._expand(X, R) @ self.coef

    def regime_weights(self) -> np.ndarray:
        """signals x regimes matrix of weights."""
        return self.coef.reshape(-1, self.K)

    def weights(self):
        return self.regime_weights().mean(axis=1)


class KernelRidgeModel(BaseModel):
    """Random Fourier features: z(x) = sqrt(2/D) cos(Wx + b) approximates an RBF
    kernel, so ridge on z is approximately Gaussian-kernel ridge regression."""

    name = "kernel_ridge"
    uses_regime = True

    def __init__(self, n_features: int = 256, max_rows: int = 300_000, seed: int = 0):
        self.D = n_features
        self.max_rows = max_rows
        self.rng = np.random.default_rng(seed)

    def _phi(self, X, R):
        Z = np.hstack([X, R]).astype(np.float32)
        return np.hstack([np.sqrt(2.0 / self.D) * np.cos(Z @ self.W + self.b), X]).astype(np.float64)

    def fit(self, X, y, R, day):
        p = X.shape[1] + R.shape[1]
        bandwidth = np.sqrt(p)  # median-distance heuristic for unit-variance inputs
        self.W = (self.rng.standard_normal((p, self.D)) / bandwidth).astype(np.float32)
        self.b = self.rng.uniform(0, 2 * np.pi, self.D).astype(np.float32)
        idx = _subsample(len(y), self.max_rows, self.rng)
        Z = self._phi(X[idx], R[idx])
        self.lam = _choose_ridge(Z, y[idx], day[idx])
        self.coef = _ridge_solve(Z.T @ Z, Z.T @ y[idx], self.lam, len(idx))
        return self

    def predict(self, X, R):
        out = np.empty(len(X))
        for i in range(0, len(X), 200_000):  # chunk to bound memory
            out[i : i + 200_000] = self._phi(X[i : i + 200_000], R[i : i + 200_000]) @ self.coef
        return out


class GBMModel(BaseModel):
    name = "gbm"
    uses_regime = True

    def __init__(self, max_rows: int = 400_000, seed: int = 0):
        self.max_rows = max_rows
        self.rng = np.random.default_rng(seed)
        self.seed = seed

    def fit(self, X, y, R, day):
        from sklearn.ensemble import HistGradientBoostingRegressor

        idx = _subsample(len(y), self.max_rows, self.rng)
        self.m = HistGradientBoostingRegressor(
            max_iter=150, learning_rate=0.05, max_leaf_nodes=15, min_samples_leaf=1000,
            l2_regularization=1.0, max_bins=64, early_stopping=False, random_state=self.seed,
        )
        self.m.fit(np.hstack([X[idx], R[idx]]), y[idx])
        return self

    def predict(self, X, R):
        return self.m.predict(np.hstack([X, R]))


class ICWeightedModel(BaseModel):
    name = "ic_weighted"

    def fit(self, X, y, R, day):
        days = np.unique(day)
        ics = np.zeros((len(days), X.shape[1]))
        order = np.argsort(day, kind="stable")
        Xs, ys, ds = X[order], y[order], day[order]
        bounds = np.searchsorted(ds, days)
        bounds = np.append(bounds, len(ds))
        for i in range(len(days)):
            a, b = bounds[i], bounds[i + 1]
            if b - a < 10:
                continue
            xx = Xs[a:b] - Xs[a:b].mean(axis=0)
            yy = ys[a:b] - ys[a:b].mean()
            den = np.sqrt((xx ** 2).sum(axis=0) * (yy ** 2).sum()) + 1e-12
            ics[i] = (xx * yy[:, None]).sum(axis=0) / den
        mean, sd = ics.mean(axis=0), ics.std(axis=0) + 1e-9
        tstat = mean / sd * np.sqrt(len(days))
        # information ratio, shrunk to zero when not statistically distinct
        self.coef = (mean / sd) * np.clip(1 - 4 / np.maximum(tstat ** 2, 1e-9), 0, 1)
        self.ic_mean = mean
        return self

    def predict(self, X, R):
        return X @ self.coef

    def weights(self):
        return self.coef


def build_model(name: str, cfg) -> BaseModel:
    m = cfg.model
    return {
        "ridge": lambda: RidgeModel(),
        "elastic_net": lambda: ElasticNetModel(m.gbm_max_rows, m.seed),
        "regime_ridge": lambda: RegimeRidgeModel(seed=m.seed),
        "kernel_ridge": lambda: KernelRidgeModel(m.rff_features, seed=m.seed),
        "gbm": lambda: GBMModel(m.gbm_max_rows, m.seed),
        "ic_weighted": lambda: ICWeightedModel(),
    }[name]()
