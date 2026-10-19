"""Statistical factor model from PCA eigenportfolios (Avellaneda & Lee, 2010).

Every ``refit_every`` days we take the last ``window`` days of returns, compute
the correlation matrix's top ``k`` eigenvectors, and turn each into an
*eigenportfolio* (weights v_j / sigma_i). The returns of those portfolios are
the factors F_t. Each stock is regressed on the factors over the window,

    r_it = beta_i' F_t + e_it,

and the *residual* e_it is the idiosyncratic part of the move - the piece a
market-neutral statistical-arbitrage book is trying to predict. Loadings,
idiosyncratic variances and k-means "peer clusters" are kept for each refit so
the portfolio can neutralise factor exposure later.

Everything for the days after refit date R uses parameters estimated with data
up to and including R only, so there is no look-ahead.
"""
from __future__ import annotations

import bisect
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from ..utils import LOG


@dataclass
class FactorSnapshot:
    date: pd.Timestamp
    tickers: list[str]
    eigen_weights: np.ndarray      # n x k   (eigenportfolio weights)
    loadings: np.ndarray           # n x k   (betas on factor returns)
    idio_var: np.ndarray           # n       (daily residual variance)
    explained: np.ndarray          # k       (share of variance per eigenvector)
    clusters: np.ndarray           # n       (k-means peer group id)


@dataclass
class FactorModel:
    residuals: pd.DataFrame
    factor_returns: pd.DataFrame
    snapshots: list[FactorSnapshot] = field(default_factory=list)

    def snapshot_at(self, date) -> FactorSnapshot | None:
        """Latest snapshot estimated on or before ``date``."""
        dates = [s.date for s in self.snapshots]
        i = bisect.bisect_right(dates, pd.Timestamp(date)) - 1
        return self.snapshots[i] if i >= 0 else None

    def cluster_panel(self, index: pd.DatetimeIndex, columns) -> pd.DataFrame:
        """Peer-cluster label for each (date, ticker), valid from a refit until the next."""
        col_pos = {c: i for i, c in enumerate(columns)}
        vals = np.full((len(index), len(columns)), np.nan)
        for i, s in enumerate(self.snapshots):
            a = index.searchsorted(s.date)
            b = index.searchsorted(self.snapshots[i + 1].date) if i + 1 < len(self.snapshots) else len(index)
            cols = [col_pos[t] for t in s.tickers if t in col_pos]
            vals[a:b, cols] = s.clusters[[j for j, t in enumerate(s.tickers) if t in col_pos]]
        return pd.DataFrame(vals, index=index, columns=columns)


def fit_factor_model(
    ret: pd.DataFrame,
    n_factors: int = 15,
    window: int = 252,
    refit_every: int = 21,
    n_clusters: int = 20,
    min_coverage: float = 0.9,
    seed: int = 0,
) -> FactorModel:
    dates = ret.index
    cols = ret.columns
    R = ret.to_numpy(dtype=float)
    T, N = R.shape
    resid = np.full((T, N), np.nan)
    fret = np.full((T, n_factors), np.nan)
    snaps: list[FactorSnapshot] = []

    refit_idx = list(range(window - 1, T, refit_every))
    for r_i, t0 in enumerate(refit_idx):
        W = R[t0 - window + 1 : t0 + 1]
        coverage = np.isfinite(W).mean(axis=0)
        ok = (coverage >= min_coverage) & np.isfinite(R[t0])
        if ok.sum() < max(3 * n_factors, 30):
            continue
        Wk = W[:, ok]
        mu = np.nanmean(Wk, axis=0)
        sd = np.nanstd(Wk, axis=0)
        sd[sd == 0] = np.nan
        Z = np.nan_to_num((Wk - mu) / sd)
        k = min(n_factors, ok.sum() - 1, window - 1)
        # SVD of the standardized window = eigen-decomposition of correlation
        _, S, Vt = np.linalg.svd(Z, full_matrices=False)
        V = Vt[:k].T                                   # n_ok x k
        explained = (S[:k] ** 2) / (S ** 2).sum()
        Q = V / np.nan_to_num(sd, nan=1.0)[:, None]    # eigenportfolio weights
        # sign convention: the first eigenportfolio should be long the market
        if Q[:, 0].sum() < 0:
            Q[:, 0] *= -1
        Wf = np.nan_to_num(Wk) @ Q                     # window factor returns
        # OLS of each stock on the factors over the window
        X = np.column_stack([np.ones(len(Wf)), Wf])
        Y = np.nan_to_num(Wk - 0)
        coef, *_ = np.linalg.lstsq(X, Y, rcond=None)
        B = coef[1:].T                                 # n_ok x k
        in_resid = Y - X @ coef
        idio_var = np.maximum(in_resid.var(axis=0), 1e-8)

        clusters = _kmeans_labels(B, n_clusters, seed + r_i)
        snaps.append(FactorSnapshot(dates[t0], list(cols[ok]), Q, B, idio_var, explained, clusters))

        # out-of-sample residuals for the days until the next refit
        t_end = refit_idx[r_i + 1] if r_i + 1 < len(refit_idx) else T - 1
        P = R[t0 + 1 : t_end + 1][:, ok]
        if len(P):
            Fp = np.nan_to_num(P) @ Q
            fret[t0 + 1 : t_end + 1, :k] = Fp
            e = P - Fp @ B.T
            block = resid[t0 + 1 : t_end + 1]
            block[:, ok] = e
            resid[t0 + 1 : t_end + 1] = block

    LOG.info("factor model: %d refits, %d factors", len(snaps), n_factors)
    return FactorModel(
        residuals=pd.DataFrame(resid, index=dates, columns=cols),
        factor_returns=pd.DataFrame(fret, index=dates, columns=[f"PC{i+1}" for i in range(n_factors)]),
        snapshots=snaps,
    )


def _kmeans_labels(B: np.ndarray, n_clusters: int, seed: int) -> np.ndarray:
    """Group stocks whose factor loadings point the same way (peer groups)."""
    from sklearn.cluster import KMeans

    n = len(B)
    k = max(1, min(n_clusters, n // 5))
    if k == 1:
        return np.zeros(n, dtype=int)
    X = B[:, 1:] if B.shape[1] > 1 else B  # drop the market factor: it moves everyone
    X = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)
    return KMeans(n_clusters=k, n_init=3, random_state=seed).fit_predict(X)
