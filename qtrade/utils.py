"""Shared numerical helpers.

Conventions used throughout the package
---------------------------------------
* A *panel* is a ``pandas.DataFrame`` indexed by trading date (rows) with one
  column per ticker. Every signal, prediction and weight lives in this shape.
* A value stored at row ``t`` may only use information available at the
  **close of day t**. Nothing in this package is allowed to look forward;
  ``tests/test_no_lookahead.py`` enforces that for every signal.
"""
from __future__ import annotations

import logging
import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import ndtri

LOG = logging.getLogger("qtrade")

TRADING_DAYS = 252


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )
    for noisy in ("matplotlib", "yfinance", "urllib3", "peewee"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


# ---------------------------------------------------------------------------
# Cross-sectional transforms (applied row by row, i.e. across stocks per day)
# ---------------------------------------------------------------------------
def cs_winsorize(df: pd.DataFrame, lower: float = 0.01, upper: float = 0.99) -> pd.DataFrame:
    """Clip each row to its own [lower, upper] quantiles."""
    lo = df.quantile(lower, axis=1)
    hi = df.quantile(upper, axis=1)
    return df.clip(lower=lo, upper=hi, axis=0)


def cs_zscore(df: pd.DataFrame, winsor: float | None = 0.01) -> pd.DataFrame:
    """Winsorize then z-score each row (mean 0, std 1 across stocks)."""
    if winsor:
        df = cs_winsorize(df, winsor, 1 - winsor)
    mu = df.mean(axis=1)
    sd = df.std(axis=1).replace(0, np.nan)
    return df.sub(mu, axis=0).div(sd, axis=0)


def cs_rank_gauss(df: pd.DataFrame) -> pd.DataFrame:
    """Map each row to Gaussian scores through its ranks (robust to outliers)."""
    ranks = df.rank(axis=1, pct=True)
    n = df.notna().sum(axis=1)
    # shift ranks into (0, 1) open interval: (rank*n - 0.5) / n
    u = (ranks.mul(n, axis=0) - 0.5).div(n, axis=0)
    return pd.DataFrame(ndtri(u.to_numpy(dtype=float)), index=df.index, columns=df.columns)


def cs_demean(df: pd.DataFrame) -> pd.DataFrame:
    return df.sub(df.mean(axis=1), axis=0)


def safe_div(a, b):
    with np.errstate(divide="ignore", invalid="ignore"):
        out = a / b
    if isinstance(out, (pd.DataFrame, pd.Series)):
        return out.replace([np.inf, -np.inf], np.nan)
    return np.where(np.isfinite(out), out, np.nan)


def rank_ic(pred: np.ndarray, target: np.ndarray, min_names: int = 20) -> np.ndarray:
    """Daily Spearman rank correlation between two (T, N) arrays, vectorised."""
    ok = np.isfinite(pred) & np.isfinite(target)
    a = pd.DataFrame(np.where(ok, pred, np.nan)).rank(axis=1).to_numpy()
    b = pd.DataFrame(np.where(ok, target, np.nan)).rank(axis=1).to_numpy()
    n = ok.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        a = a - np.nanmean(a, axis=1, keepdims=True)
        b = b - np.nanmean(b, axis=1, keepdims=True)
        num = np.nansum(a * b, axis=1)
        den = np.sqrt(np.nansum(a * a, axis=1) * np.nansum(b * b, axis=1))
        ic = num / den
    ic[n < min_names] = np.nan
    return ic


# ---------------------------------------------------------------------------
# Rolling helpers that operate on whole panels at once
# ---------------------------------------------------------------------------
def rolling_sum(df: pd.DataFrame, window: int, min_periods: int | None = None) -> pd.DataFrame:
    return df.rolling(window, min_periods=min_periods or window).sum()


def rolling_mean(df: pd.DataFrame, window: int, min_periods: int | None = None) -> pd.DataFrame:
    return df.rolling(window, min_periods=min_periods or max(2, window // 2)).mean()


def rolling_std(df: pd.DataFrame, window: int, min_periods: int | None = None) -> pd.DataFrame:
    return df.rolling(window, min_periods=min_periods or max(3, window // 2)).std()


def rolling_beta(y: pd.DataFrame, x: pd.Series, window: int) -> pd.DataFrame:
    """Rolling OLS slope of each column of ``y`` on the series ``x``."""
    mp = max(20, window // 2)
    xm = x.rolling(window, min_periods=mp).mean()
    ym = y.rolling(window, min_periods=mp).mean()
    xym = y.mul(x, axis=0).rolling(window, min_periods=mp).mean()
    xxm = (x * x).rolling(window, min_periods=mp).mean()
    cov = xym - ym.mul(xm, axis=0)
    var = xxm - xm * xm
    return cov.div(var, axis=0)


# ---------------------------------------------------------------------------
# I/O: parquet when pyarrow is installed, pickle otherwise
# ---------------------------------------------------------------------------
def _has_parquet() -> bool:
    try:
        import pyarrow  # noqa: F401

        return True
    except ImportError:  # pragma: no cover
        return False


def save_frame(df: pd.DataFrame, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if _has_parquet():
        path = path.with_suffix(".parquet")
        df.to_parquet(path)
    else:  # pragma: no cover
        path = path.with_suffix(".pkl")
        df.to_pickle(path)
    return path


def load_frame(path: str | Path) -> pd.DataFrame | None:
    path = Path(path)
    for suffix in (".parquet", ".pkl"):
        p = path.with_suffix(suffix)
        if p.exists():
            return pd.read_parquet(p) if suffix == ".parquet" else pd.read_pickle(p)
    return None


def save_pickle(obj, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "wb") as fh:
        pickle.dump(obj, fh, protocol=pickle.HIGHEST_PROTOCOL)
    os.replace(tmp, path)


def load_pickle(path: str | Path):
    path = Path(path)
    if not path.exists():
        return None
    with open(path, "rb") as fh:
        return pickle.load(fh)
