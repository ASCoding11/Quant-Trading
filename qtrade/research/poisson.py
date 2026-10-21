"""Poisson models for the things that arrive as counts.

A "jump" is a day on which a stock's factor-residual return is beyond 3 times
its trailing volatility. Jumps, like news articles, are discrete events, and a
Poisson model is the natural first description of how often they happen.

1. Market jump counts N_t (stocks jumping on day t):
   * overdispersion: var/mean = 1 for a Poisson process; >> 1 means jumps
     cluster in time
   * INGARCH(1,1): lambda_t = w + a N_{t-1} + b lambda_{t-1}, a self-exciting
     Poisson model (a discrete-time Hawkes process). a + b near 1 = jump
     storms persist. Scored on out-of-sample predictive log-likelihood vs. a
     constant-rate Poisson.
   * Poisson HMM: hidden regimes with their own jump rate. Walk-forward,
     scored like the Gaussian HMM (crash calibration, reversal IC by regime).
2. Stock jump intensities (Gamma-Poisson shrinkage toward the cross-section):
   crash_risk (down-jump rate) and jump_skew (up minus down rate).
3. After a jump: average market-relative return over the next 1-10 days,
   split by direction and (if news data exists) whether there was news.
4. news_surprise: 3-day article count vs. the stock's own expected Poisson
   rate, as a Pearson residual (N - lambda) / sqrt(lambda).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import gammaln

from ..utils import LOG, rank_ic

SPLIT = "2015-01-01"


# -----------------------------------------------------------------------------
# jumps
# -----------------------------------------------------------------------------
def jump_panels(ctx, k: float = 3.0) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(up, down) jump indicators from factor residuals vs. trailing vol (known at the close)."""
    e = ctx.resid
    sd = e.rolling(63, min_periods=40).std().shift(1)
    z = e / sd
    tr = ctx.tradable
    return (z > k).where(tr), (z < -k).where(tr)


def gamma_poisson_rate(events: pd.DataFrame, window: int = 252, prior_days: float = 252) -> pd.DataFrame:
    """Shrunk daily event rate per stock: (count + a) / (exposure + b), with the
    prior mean set to the cross-sectional average rate that day."""
    cnt = events.rolling(window, min_periods=window // 2).sum()
    expo = events.notna().rolling(window, min_periods=window // 2).sum()
    pooled = cnt.sum(axis=1) / expo.sum(axis=1)
    a = pooled * prior_days
    return cnt.add(a, axis=0).div(expo + prior_days)


# -----------------------------------------------------------------------------
# INGARCH(1,1): self-exciting Poisson counts
# -----------------------------------------------------------------------------
def ingarch_filter(n: np.ndarray, w: float, a: float, b: float) -> np.ndarray:
    lam = np.empty(len(n))
    lam[0] = max(np.nanmean(n), 1e-3)
    for t in range(1, len(n)):
        prev = n[t - 1] if np.isfinite(n[t - 1]) else lam[t - 1]
        lam[t] = w + a * prev + b * lam[t - 1]
    return lam


def poisson_ll(n: np.ndarray, lam: np.ndarray) -> np.ndarray:
    lam = np.maximum(lam, 1e-9)
    return n * np.log(lam) - lam - gammaln(n + 1)


def fit_ingarch(n: np.ndarray) -> tuple[float, float, float]:
    ok = np.isfinite(n)
    m = np.nanmean(n)

    def nll(p):
        w, a, b = np.exp(p[0]), 1 / (1 + np.exp(-p[1])), 1 / (1 + np.exp(-p[2]))
        if a + b >= 0.999:
            return 1e12
        lam = ingarch_filter(n, w, a, b)
        return -poisson_ll(n[ok], lam[ok]).sum()

    best = None
    for a0, b0 in ((0.3, 0.5), (0.1, 0.8), (0.5, 0.3)):
        x0 = [np.log(m * (1 - a0 - b0)), np.log(a0 / (1 - a0)), np.log(b0 / (1 - b0))]
        r = minimize(nll, x0, method="Nelder-Mead", options={"maxiter": 2000, "xatol": 1e-6, "fatol": 1e-6})
        if best is None or r.fun < best.fun:
            best = r
    p = best.x
    return float(np.exp(p[0])), float(1 / (1 + np.exp(-p[1]))), float(1 / (1 + np.exp(-p[2])))


# -----------------------------------------------------------------------------
# Poisson HMM
# -----------------------------------------------------------------------------
class PoissonHMM:
    """Hidden Markov model whose regimes differ in their event rate."""

    def __init__(self, k: int = 3, n_iter: int = 200, seed: int = 0):
        self.K, self.n_iter = k, n_iter
        self.rng = np.random.default_rng(seed)

    def _logB(self, n):
        out = np.zeros((len(n), self.K))
        ok = np.isfinite(n)
        out[ok] = poisson_ll(n[ok, None], self.rates[None, :])
        return out

    def _forward(self, logB):
        T = len(logB)
        alpha = np.empty((T, self.K))
        scale = np.empty(T)
        m = logB.max(axis=1, keepdims=True)
        B = np.exp(logB - m)
        a = self.pi * B[0]
        for t in range(T):
            if t:
                a = (alpha[t - 1] @ self.A) * B[t]
            scale[t] = a.sum()
            alpha[t] = a / scale[t]
        return alpha, scale, B

    def fit(self, n: np.ndarray, warm: "PoissonHMM | None" = None) -> "PoissonHMM":
        x = n[np.isfinite(n)]
        if warm is not None:
            self.rates, self.A, self.pi = warm.rates.copy(), warm.A.copy(), warm.pi.copy()
        else:
            self.rates = np.quantile(x, np.linspace(0.2, 0.95, self.K)) + 0.1
            self.A = np.full((self.K, self.K), 0.05 / max(self.K - 1, 1))
            np.fill_diagonal(self.A, 0.95)
            self.pi = np.full(self.K, 1 / self.K)
        prev = -np.inf
        for _ in range(self.n_iter):
            logB = self._logB(x)
            alpha, scale, B = self._forward(logB)
            beta = np.empty_like(alpha)
            beta[-1] = 1
            for t in range(len(x) - 2, -1, -1):
                beta[t] = (self.A @ (B[t + 1] * beta[t + 1])) / scale[t + 1]
            g = alpha * beta
            g /= g.sum(axis=1, keepdims=True)
            xi = self.A * (alpha[:-1].T @ ((B[1:] * beta[1:]) / scale[1:, None]))
            self.A = xi / xi.sum(axis=1, keepdims=True)
            self.pi = g[0] + 1e-6
            self.pi /= self.pi.sum()
            self.rates = (g * x[:, None]).sum(axis=0) / (g.sum(axis=0) + 1e-9) + 1e-6
            ll = np.log(scale).sum() + logB.max(axis=1).sum()
            if ll - prev < 1e-6 * abs(ll):
                break
            prev = ll
        order = np.argsort(self.rates)                         # state 0 = calmest
        self.rates, self.pi = self.rates[order], self.pi[order]
        self.A = self.A[np.ix_(order, order)]
        return self

    def filter(self, n: np.ndarray) -> np.ndarray:
        return self._forward(self._logB(n))[0]

    def predictive_ll(self, n: np.ndarray) -> np.ndarray:
        alpha = self.filter(n)
        prior = np.vstack([self.pi[None], alpha[:-1] @ self.A])
        return np.log((prior * np.exp(self._logB(n))).sum(axis=1))


def walk_forward_poisson_hmm(n: pd.Series, k: int, refit_every: int = 252, min_history: int = 756):
    x = n.to_numpy(dtype=float)
    T = len(x)
    first = int(np.argmax(np.isfinite(x)))
    probs = np.full((T, k), np.nan)
    pll = np.full(T, np.nan)
    prev = None
    refits = list(range(first + min_history, T, refit_every))
    for i, r in enumerate(refits):
        hmm = PoissonHMM(k).fit(x[first:r + 1], warm=prev)
        end = refits[i + 1] if i + 1 < len(refits) else T - 1
        a = hmm.filter(x[first:end + 1])
        probs[r + 1:end + 1] = a[r + 1 - first:]
        pll[r + 1:end + 1] = hmm.predictive_ll(x[first:end + 1])[r + 1 - first:]
        prev = hmm
    return pd.DataFrame(probs, index=n.index), pd.Series(pll, index=n.index), prev


# -----------------------------------------------------------------------------
# the study
# -----------------------------------------------------------------------------
def run(md, ctx, out: Path, news_counts: pd.DataFrame | None = None) -> tuple[dict, dict]:
    up, down = jump_panels(ctx)
    n_up = up.sum(axis=1)
    n_dn = down.sum(axis=1)
    N = (n_up + n_dn).where(ctx.resid.notna().sum(axis=1) > 50)
    lines = ["## Poisson models of jumps and news", ""]
    res = {}

    # 1a. overdispersion
    disp = {}
    for name, s in (("all jumps", N), ("up jumps", n_up.where(N.notna())), ("down jumps", n_dn.where(N.notna()))):
        s = s.dropna()
        disp[name] = {"mean_per_day": s.mean(), "variance": s.var(), "var_over_mean": s.var() / s.mean()}
    dtab = pd.DataFrame(disp).T
    res["dispersion"] = float(dtab.loc["all jumps", "var_over_mean"])
    lines += ["### Do jumps cluster? (Poisson: variance / mean = 1)", "", dtab.round(2).to_markdown(), ""]

    # 1b. INGARCH: fit on 2004-2014, score both periods out of sample
    x = N.to_numpy(dtype=float)
    idx = N.index
    tr = (idx < SPLIT) & np.isfinite(x)
    w, a, b = fit_ingarch(np.where(idx < SPLIT, x, np.nan)[: tr.nonzero()[0][-1] + 1])
    lam = ingarch_filter(x, w, a, b)
    const = np.nanmean(x[tr])
    ok = np.isfinite(x)
    rows = []
    for per, m in (("2004-2014 (fit)", (idx < SPLIT) & ok), ("2015-2026 (out of sample)", (idx >= SPLIT) & ok)):
        rows.append({"period": per, "ll_ingarch": poisson_ll(x[m], lam[m]).mean(),
                     "ll_constant_rate": poisson_ll(x[m], np.full(m.sum(), const)).mean(),
                     "corr(predicted, actual)": np.corrcoef(lam[m], x[m])[0, 1]})
    itab = pd.DataFrame(rows)
    res["ingarch"] = {"w": w, "a": a, "b": b, "persistence": a + b}
    lines += [f"### Self-exciting jumps: INGARCH(1,1) lambda_t = {w:.2f} + {a:.3f} N_t-1 + {b:.3f} lambda_t-1", "",
              f"Persistence a + b = **{a + b:.3f}** (1 = jump storms never die out; the half-life of a shock is "
              f"{np.log(0.5) / np.log(a + b) if 0 < a + b < 1 else float('nan'):.1f} days).", "",
              itab.round(4).to_markdown(index=False), ""]

    # 1c. Poisson HMM vs. crash calibration and reversal IC
    mkt = ctx.market_ret
    fwd5 = mkt[::-1].rolling(5).sum()[::-1].shift(-1)
    event = (fwd5 < -0.03).astype(float).where(fwd5.notna())
    from ..signals import compute_signals

    rev = compute_signals(ctx, ["rev_5d"])["rev_5d"].to_numpy()
    o = md.open
    fwd = (o.shift(-6) / o.shift(-1) - 1).where(ctx.tradable).to_numpy()
    rev_ic = pd.Series(rank_ic(rev, fwd), index=md.dates)
    hrows = []
    for k in (2, 3):
        P, pll, last = walk_forward_poisson_hmm(N, k)
        row = {"states": k, "rates (jumps/day)": np.round(last.rates, 1).tolist(),
               "expected_days_in_state": np.round(1 / (1 - np.diag(last.A)), 1).tolist()}
        for per, m in (("1st", idx < SPLIT), ("2nd", idx >= SPLIT)):
            m = m & P.notna().all(axis=1).to_numpy()
            Pm = P[m].to_numpy()
            row[f"pred_ll_{per}"] = float(np.nanmean(pll[m]))
            # crash probability from per-state frequencies learned on 2004-2014
            ftr = (idx < SPLIT) & P.notna().all(axis=1).to_numpy() & event.notna().to_numpy()
            f_k = (P[ftr].to_numpy() * event[ftr].to_numpy()[:, None]).sum(0) / P[ftr].to_numpy().sum(0)
            p_ev = Pm @ f_k
            y = event[m].to_numpy()
            okk = np.isfinite(y)
            base = event[ftr].mean()
            row[f"brier_skill_{per}"] = 1 - np.mean((p_ev[okk] - y[okk]) ** 2) / np.mean((base - y[okk]) ** 2)
            ric = rev_ic[m].to_numpy()
            okr = np.isfinite(ric)
            for tag, j in (("calm", 0), ("stormy", k - 1)):
                wj = Pm[okr, j]
                row[f"rev_ic_{tag}_{per}"] = float((wj * ric[okr]).sum() / wj.sum()) if wj.sum() > 1 else np.nan
        hrows.append(row)
    htab = pd.DataFrame(hrows)
    lines += ["### Poisson HMM on daily jump counts (walk-forward)", "",
              "Compare brier_skill and rev_ic with the Gaussian HMM table: same tests, different symptoms.", "",
              htab.round(4).to_markdown(index=False), ""]

    # 2. stock-level jump intensity signals
    lam_up = gamma_poisson_rate(up)
    lam_dn = gamma_poisson_rate(down)
    signals = {"crash_risk": -lam_dn, "jump_skew": -(lam_up - lam_dn), "jump_intensity": -(lam_up + lam_dn)}

    # 3. what happens after a jump
    ar = ctx.ret.sub(mkt, axis=0)
    has_news = None
    if news_counts is not None:
        has_news = news_counts.reindex_like(up).fillna(0).rolling(2).sum() > 0
    ev_rows = []
    car = {h: ar[::-1].rolling(h).sum()[::-1].shift(-1) for h in (1, 3, 5, 10)}   # days t+1..t+h
    for name, ev in (("up jump", up), ("down jump", down)):
        groups = [("all", ev == 1)]
        if has_news is not None:
            groups += [("with news", (ev == 1) & has_news), ("no news", (ev == 1) & ~has_news)]
        for g, m in groups:
            for per, sel in (("1st", ar.index < SPLIT), ("2nd", ar.index >= SPLIT)):
                mm = m[sel]
                row = {"event": name, "news": g, "period": per, "events": int(mm.sum().sum())}
                for h, c in car.items():
                    v = c[sel].where(mm).stack()
                    row[f"car_{h}d_bp"] = v.mean() * 1e4
                    if h == 5:
                        row["t_5d"] = v.mean() / v.std() * np.sqrt(len(v)) if len(v) > 10 else np.nan
                ev_rows.append(row)
    etab = pd.DataFrame(ev_rows)
    lines += ["### After a jump: market-relative return over the next days (bp)", "",
              "Negative after an up jump (or positive after a down jump) = reversal; same sign = drift.", "",
              etab.round(2).to_markdown(index=False), ""]

    # 4. news surprise
    if news_counts is not None:
        c = news_counts.reindex_like(up).fillna(0.0).where(ctx.tradable.reindex_like(up))
        lam_n = gamma_poisson_rate(c.shift(3), window=250, prior_days=60) * 3        # expected 3-day count
        c3 = c.rolling(3).sum()
        signals["news_surprise"] = -((c3 - lam_n) / np.sqrt(lam_n.clip(lower=0.05)))

    pd.DataFrame({"N": N, "lambda_ingarch": lam}).to_csv(out / "poisson_jump_counts.csv")
    etab.to_csv(out / "poisson_after_jumps.csv", index=False)
    htab.to_csv(out / "poisson_hmm.csv", index=False)
    (out / "poisson.md").write_text("\n".join(lines) + "\n")
    LOG.info("poisson: dispersion %.1f, INGARCH persistence %.3f", res["dispersion"], a + b)
    return res, signals
