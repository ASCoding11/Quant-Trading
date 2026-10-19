"""Performance statistics, including overfitting-aware Sharpe ratios.

Probabilistic Sharpe Ratio (Bailey & Lopez de Prado, 2012)
    PSR(SR*) = Phi( (SR - SR*) sqrt(n - 1) / sqrt(1 - g3 SR + (g4 - 1)/4 SR^2) )
    the probability the true Sharpe exceeds SR*, accounting for sample
    length, skewness g3 and kurtosis g4 of the returns.

Deflated Sharpe Ratio (Bailey & Lopez de Prado, 2014)
    PSR evaluated at the Sharpe you would expect from the *best of N
    worthless strategies*:
    SR* = sqrt(V[SR_n]) ((1 - e) Phi^-1(1 - 1/N) + e Phi^-1(1 - 1/(N e)))
    with e = Euler-Mascheroni constant. Testing many models and reporting
    the best inflates Sharpe; DSR corrects for that.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

TD = 252
EULER = 0.5772156649


def sharpe(r: pd.Series) -> float:
    r = r.dropna()
    return float(r.mean() / r.std() * np.sqrt(TD)) if r.std() > 0 else 0.0


def max_drawdown(r: pd.Series) -> float:
    eq = (1 + r.fillna(0)).cumprod()
    return float((eq / eq.cummax() - 1).min())


def drawdown_series(r: pd.Series) -> pd.Series:
    eq = (1 + r.fillna(0)).cumprod()
    return eq / eq.cummax() - 1


def probabilistic_sharpe(r: pd.Series, sr_star: float = 0.0) -> float:
    """sr_star is annualised; computation is in per-period units."""
    r = r.dropna()
    n = len(r)
    if n < 30 or r.std() == 0:
        return float("nan")
    sr = r.mean() / r.std()
    g3 = stats.skew(r)
    g4 = stats.kurtosis(r, fisher=False)
    sr0 = sr_star / np.sqrt(TD)
    denom = np.sqrt(max(1 - g3 * sr + (g4 - 1) / 4 * sr ** 2, 1e-12))
    return float(stats.norm.cdf((sr - sr0) * np.sqrt(n - 1) / denom))


def deflated_sharpe(r: pd.Series, trial_sharpes: list[float]) -> float:
    """``trial_sharpes``: annualised Sharpes of every variant that was tried."""
    N = len(trial_sharpes)
    if N < 2:
        return probabilistic_sharpe(r, 0.0)
    v = np.var(trial_sharpes, ddof=1)
    sr_star = np.sqrt(v) * ((1 - EULER) * stats.norm.ppf(1 - 1 / N) + EULER * stats.norm.ppf(1 - 1 / (N * np.e)))
    return probabilistic_sharpe(r, sr_star)


def summarize(r: pd.Series, daily: pd.DataFrame | None = None, benchmark: pd.Series | None = None) -> dict:
    r = r.dropna()
    years = len(r) / TD
    eq = (1 + r).prod()
    downside = r[r < 0].std() * np.sqrt(TD)
    out = {
        "start": str(r.index[0].date()), "end": str(r.index[-1].date()), "years": round(years, 2),
        "cagr": eq ** (1 / years) - 1 if years > 0 else np.nan,
        "ann_return": r.mean() * TD,
        "ann_vol": r.std() * np.sqrt(TD),
        "sharpe": sharpe(r),
        "sortino": r.mean() * TD / downside if downside > 0 else np.nan,
        "max_drawdown": max_drawdown(r),
        "calmar": (eq ** (1 / years) - 1) / abs(max_drawdown(r)) if max_drawdown(r) < 0 else np.nan,
        "hit_rate": (r > 0).mean(),
        "skew": stats.skew(r),
        "kurtosis": stats.kurtosis(r),
        "best_day": r.max(), "worst_day": r.min(),
        "psr_vs_0": probabilistic_sharpe(r, 0.0),
    }
    if daily is not None:
        out.update({
            "avg_gross": daily["gross"].mean(), "avg_net": daily["net"].mean(),
            "ann_turnover": daily["turnover"].mean() * TD,
            "ann_cost_drag": daily["cost"].mean() * TD,
            "ann_borrow_drag": daily["borrow"].mean() * TD,
            "avg_long_names": daily["long_names"].mean(), "avg_short_names": daily["short_names"].mean(),
            "share_overnight_pnl": daily["pnl_overnight"].sum() / (daily["pnl_overnight"].sum() + daily["pnl_intraday"].sum()),
        })
    if benchmark is not None:
        b = benchmark.reindex(r.index).fillna(0)
        beta = np.cov(r, b)[0, 1] / b.var() if b.var() > 0 else np.nan
        out["beta_to_market"] = beta
        out["corr_to_market"] = float(np.corrcoef(r, b)[0, 1])
    return {k: (float(v) if isinstance(v, (np.floating, float, int, np.integer)) and not isinstance(v, bool) else v)
            for k, v in out.items()}


def annual_returns(r: pd.Series) -> pd.Series:
    return (1 + r).groupby(r.index.year).prod() - 1


def monthly_table(r: pd.Series) -> pd.DataFrame:
    m = (1 + r).groupby([r.index.year, r.index.month]).prod() - 1
    tbl = m.unstack()
    tbl.columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][: tbl.shape[1]]
    return tbl


def rolling_sharpe(r: pd.Series, window: int = 252) -> pd.Series:
    return r.rolling(window).mean() / r.rolling(window).std() * np.sqrt(TD)
