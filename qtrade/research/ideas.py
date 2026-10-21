"""The ideas lab: new candidate signals, tested as they are written.

Each idea is a function ``(md, ctx, facts) -> panel`` registered with ``@idea``
under a theme and the wave it was added in. ``python -m qtrade.research.zoo
--group ideas`` computes every idea, normalises it like any other signal, and
scores its IC at the job's horizon in 2006-2014 and 2015-2026 plus the
break-even cost of trading it; the results land in best_correlations.csv.
Positive values should mean "expected to outperform" where the literature has
a view; the sign actually found is what the report shows.
"""
from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd

IDEAS: dict[str, tuple[str, int, Callable]] = {}


def idea(theme: str, wave: int):
    def wrap(fn):
        IDEAS[fn.__name__] = (theme, wave, fn)
        return fn
    return wrap


def _pit(facts, tag, md, annual=False):
    from ..data.fundamentals import point_in_time

    if facts is None:
        return None
    return point_in_time(facts, tag, md.dates, md.tickers, annual).shift(1)   # usable the day after filing


# =============================================================================
# wave 1: momentum variants
# =============================================================================
@idea("momentum", 1)
def sharpe_mom(md, ctx, facts):
    """12-1 month return divided by its volatility: momentum per unit of risk."""
    r = ctx.log_ret
    return (r.rolling(231, min_periods=200).sum().shift(21)) / (r.rolling(252, min_periods=200).std() * np.sqrt(252))


@idea("momentum", 1)
def frog_in_pan(md, ctx, facts):
    """Da-Gurun-Warachka: momentum built from many small moves persists more than
    momentum from a few jumps. sign(12-1 return) x (share of down days - share of up days)."""
    r = ctx.ret.shift(21)
    past = r.rolling(231, min_periods=200)
    pos = (r > 0).rolling(231, min_periods=200).mean()
    neg = (r < 0).rolling(231, min_periods=200).mean()
    return -np.sign(past.sum()) * (neg - pos)


@idea("momentum", 1)
def mom_consistency(md, ctx, facts):
    """Share of the last 12 months with a positive return."""
    m = ctx.log_ret.rolling(21).sum()
    months = pd.concat([m.shift(21 * k) > 0 for k in range(1, 13)], keys=range(12))
    return months.groupby(level=1).mean().reindex(m.index)


@idea("momentum", 1)
def cluster_rel_mom(md, ctx, facts):
    """6-1 month return relative to the stock's k-means peer group."""
    r6 = ctx.log_ret.rolling(105, min_periods=90).sum().shift(21)
    cl = ctx.clusters
    out = r6.copy() * np.nan
    for c in np.unique(cl.stack().dropna()):
        m = cl == c
        g = r6.where(m)
        out = out.where(~m, g.sub(g.mean(axis=1), axis=0))
    return out


@idea("momentum", 1)
def stock_tsmom(md, ctx, facts):
    """Each stock's own trend: sign of its 12-month return, scaled by inverse vol."""
    r = ctx.log_ret
    return np.sign(r.rolling(252, min_periods=200).sum()) / (r.rolling(63, min_periods=40).std() + 1e-4)


# =============================================================================
# wave 1: trend shape
# =============================================================================
@idea("trend", 1)
def ma50_200(md, ctx, facts):
    """50-day vs 200-day moving average (golden/death cross distance)."""
    p = md.close
    return np.log(p.rolling(50, min_periods=40).mean() / p.rolling(200, min_periods=150).mean())


@idea("trend", 1)
def macd(md, ctx, facts):
    """MACD (12/26-day EMA gap) relative to price."""
    p = md.close
    return (p.ewm(span=12, min_periods=26).mean() - p.ewm(span=26, min_periods=26).mean()) / p


@idea("trend", 1)
def dist_from_high(md, ctx, facts):
    """Drawdown from the 252-day high (0 at the high)."""
    return md.close / md.close.rolling(252, min_periods=200).max() - 1


# =============================================================================
# wave 1: volatility and higher moments
# =============================================================================
@idea("volatility", 1)
def vol_change(md, ctx, facts):
    """Minus log(21-day vol / 252-day vol): falling volatility."""
    r = ctx.ret
    return -np.log(r.rolling(21, min_periods=15).std() / r.rolling(252, min_periods=200).std())


@idea("volatility", 1)
def idio_skew(md, ctx, facts):
    """Minus the skewness of residual returns over 126 days (lottery stocks underperform)."""
    return -ctx.resid.rolling(126, min_periods=90).skew()


@idea("volatility", 1)
def coskew(md, ctx, facts):
    """Minus co-skewness with the market: stocks that crash with the market should pay more."""
    r = ctx.ret
    m = ctx.market_ret
    md_ = m - m.rolling(252, min_periods=200).mean()
    num = (r.sub(r.rolling(252, min_periods=200).mean())).mul(md_ ** 2, axis=0).rolling(252, min_periods=200).mean()
    den = r.rolling(252, min_periods=200).std().mul((md_ ** 2).rolling(252, min_periods=200).mean(), axis=0)
    return num.div(den.where(den > 0))


# =============================================================================
# wave 1: liquidity
# =============================================================================
@idea("liquidity", 1)
def amihud_change(md, ctx, facts):
    """Minus the change in illiquidity (last month vs last year)."""
    x = (ctx.ret.abs() / ctx.dollar_volume.where(ctx.dollar_volume > 0))
    return -np.log(x.rolling(21, min_periods=15).mean() / x.rolling(252, min_periods=200).mean())


@idea("liquidity", 1)
def obv_divergence(md, ctx, facts):
    """On-balance volume trend minus price trend over 63 days (volume leading price)."""
    v = np.sign(ctx.ret) * md.volume
    obv = v.rolling(63, min_periods=40).sum() / md.volume.rolling(63, min_periods=40).sum()
    return obv - np.tanh(ctx.log_ret.rolling(63, min_periods=40).sum() * 5)


# =============================================================================
# wave 1: fundamentals - growth, profitability, financing
# =============================================================================
@idea("fundamental", 1)
def earnings_growth(md, ctx, facts):
    ni = _pit(facts, "NetIncomeLoss", md, annual=True)
    if ni is None:
        return None
    prev = ni.shift(252)
    return (ni - prev) / prev.abs().where(prev.abs() > 0)


@idea("fundamental", 1)
def revenue_growth(md, ctx, facts):
    rev = _pit(facts, "Revenues", md, annual=True)
    if rev is None:
        return None
    rev = rev.fillna(_pit(facts, "RevenueFromContractWithCustomerExcludingAssessedTax", md, annual=True))
    return np.log(rev / rev.shift(252))


@idea("fundamental", 1)
def roe(md, ctx, facts):
    ni, eq = _pit(facts, "NetIncomeLoss", md, annual=True), _pit(facts, "StockholdersEquity", md)
    if ni is None:
        return None
    return (ni / eq).where(eq > 0)


@idea("fundamental", 1)
def low_leverage(md, ctx, facts):
    li, a = _pit(facts, "Liabilities", md), _pit(facts, "Assets", md)
    if li is None:
        return None
    return -(li / a)


@idea("fundamental", 1)
def net_buyback(md, ctx, facts):
    """Minus the 1-year change in shares outstanding (issuers underperform, buyers outperform)."""
    sh = _pit(facts, "dei:EntityCommonStockSharesOutstanding", md)
    if sh is None:
        return None
    return -np.log(sh / sh.shift(252))


@idea("fundamental", 1)
def rd_intensity(md, ctx, facts):
    rd, a = _pit(facts, "ResearchAndDevelopmentExpense", md, annual=True), _pit(facts, "Assets", md)
    if rd is None:
        return None
    return rd / a


@idea("fundamental", 1)
def cash_ratio(md, ctx, facts):
    c, a = _pit(facts, "CashAndCashEquivalentsAtCarryingValue", md), _pit(facts, "Assets", md)
    if c is None:
        return None
    return c / a


def compute_ideas(md, ctx, data_dir: str = "data", waves: set[int] | None = None) -> tuple[dict, dict]:
    """All ideas as normalised panels, plus their themes."""
    from pathlib import Path

    from ..signals import normalize_signal
    from ..utils import LOG

    facts = None
    fpath = Path(data_dir) / "fundamentals" / "fundamentals.parquet"
    if fpath.exists():
        from ..data.fundamentals import load_fundamentals

        facts = load_fundamentals(fpath.parent)
    out, themes = {}, {}
    for name, (theme, wave, fn) in IDEAS.items():
        if waves and wave not in waves:
            continue
        try:
            raw = fn(md, ctx, facts)
        except Exception as exc:
            LOG.warning("idea %s failed: %s", name, exc)
            continue
        if raw is None:
            continue
        out[name] = normalize_signal(raw, ctx.tradable)
        themes[name] = f"idea:{theme} (wave {wave})"
    return out, themes
