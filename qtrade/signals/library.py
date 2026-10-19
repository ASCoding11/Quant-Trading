"""The signal library.

Each function maps a :class:`FeatureContext` to a dates x tickers panel whose
row ``t`` uses only data up to the close of day ``t``. Signs are chosen so that
a *positive* value is the direction the academic literature associates with
*higher* future returns - but the models re-learn every weight from data, so a
signal that has stopped working simply gets a small or negative weight.

Families
--------
mean_reversion   short-horizon reversal, the classic stat-arb engine
momentum         medium-horizon trend continuation
volume           liquidity and abnormal-volume effects
volatility       low-risk anomalies and lottery-like payoffs
microstructure   information hidden in open/high/low/close bars
seasonality      calendar patterns in individual stocks
structure        peer groups, Kalman-filtered trends, autocorrelation
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..features.context import FeatureContext
from ..utils import rolling_beta, safe_div
from .registry import signal

LN2 = np.log(2.0)


# =============================================================================
# Mean reversion
# =============================================================================
@signal("mean_reversion", "Minus yesterday's return (1-day reversal)")
def rev_1d(c: FeatureContext):
    return -c.ret


@signal("mean_reversion", "Minus the last 5 days' return (weekly reversal, Lehmann 1990)")
def rev_5d(c: FeatureContext):
    return -c.log_ret.rolling(5, min_periods=4).sum()


@signal("mean_reversion", "Minus the last month's return (monthly reversal, Jegadeesh 1990)")
def rev_21d(c: FeatureContext):
    return -c.log_ret.rolling(21, min_periods=15).sum()


@signal("mean_reversion", "Minus yesterday's PCA-residual return, scaled by idiosyncratic vol")
def resid_rev_1d(c: FeatureContext):
    return -safe_div(c.resid, c.resid.rolling(63, min_periods=30).std())


@signal("mean_reversion", "Minus the 5-day PCA-residual return, scaled by idiosyncratic vol")
def resid_rev_5d(c: FeatureContext):
    s = c.resid.rolling(5, min_periods=4).sum()
    return -safe_div(s, c.resid.rolling(63, min_periods=30).std() * np.sqrt(5))


@signal("mean_reversion", "Ornstein-Uhlenbeck s-score of cumulative residuals (Avellaneda-Lee)")
def ou_sscore(c: FeatureContext, window: int = 60):
    # Fit X_{t+1} = a + b X_t + eps on the cumulative residual X over a rolling
    # window. The s-score (X_t - m) / sigma_eq is invariant to where the
    # cumulative sum starts, so a single global cumsum can be used.
    e = c.resid.fillna(0.0)
    X = e.cumsum().where(c.resid.notna())
    Xl = X.shift(1)
    mp = int(window * 0.8)
    mx, my = Xl.rolling(window, min_periods=mp).mean(), X.rolling(window, min_periods=mp).mean()
    cov = (X * Xl).rolling(window, min_periods=mp).mean() - mx * my
    var = (Xl * Xl).rolling(window, min_periods=mp).mean() - mx * mx
    b = safe_div(cov, var)
    a = my - b * mx
    resid_var = ((X * X).rolling(window, min_periods=mp).mean() - my * my) - b * cov
    m = safe_div(a, 1 - b)
    sigma_eq = np.sqrt(safe_div(resid_var.clip(lower=0), 1 - b * b))
    s = safe_div(X - m, sigma_eq)
    # only trust fast mean reversion: half-life under ~30 trading days
    fast = (b > 0) & (b < np.exp(-1 / 30))
    return -s.where(fast).clip(-4, 4)


@signal("mean_reversion", "Minus distance from the 20-day moving average in std units (Bollinger)")
def bollinger_z(c: FeatureContext):
    p = c.md.close
    return -safe_div(p - p.rolling(20, min_periods=15).mean(), p.rolling(20, min_periods=15).std())


@signal("mean_reversion", "Minus (RSI-14 minus 50): oversold stocks bounce")
def rsi_14(c: FeatureContext):
    up = c.ret.clip(lower=0).ewm(alpha=1 / 14, min_periods=14).mean()
    dn = (-c.ret).clip(lower=0).ewm(alpha=1 / 14, min_periods=14).mean()
    rsi = 100 - 100 / (1 + safe_div(up, dn))
    return -(rsi - 50)


@signal("mean_reversion", "Minus today's overnight gap (gaps tend to fade)")
def overnight_rev(c: FeatureContext):
    return -c.overnight


@signal("mean_reversion", "Minus today's open-to-close move")
def intraday_rev(c: FeatureContext):
    return -c.intraday


@signal("mean_reversion", "Reversal that only fires on low-volume moves (Campbell-Grossman-Wang)")
def low_volume_rev(c: FeatureContext):
    abn = np.log(safe_div(c.md.volume.rolling(5, min_periods=3).mean(),
                          c.md.volume.rolling(63, min_periods=40).mean()))
    r5 = c.log_ret.rolling(5, min_periods=4).sum()
    return -r5 * np.exp(-abn.clip(-2, 2))


# =============================================================================
# Momentum
# =============================================================================
@signal("momentum", "12-month return skipping the last month (Jegadeesh-Titman)")
def mom_12_1(c: FeatureContext):
    lp = np.log(c.md.close)
    return lp.shift(21) - lp.shift(252)


@signal("momentum", "6-month return skipping the last month")
def mom_6_1(c: FeatureContext):
    lp = np.log(c.md.close)
    return lp.shift(21) - lp.shift(126)


@signal("momentum", "Residual momentum: 12-1 month sum of PCA residuals / their vol (Blitz et al.)")
def resid_mom(c: FeatureContext):
    s = c.resid.shift(21).rolling(231, min_periods=150).sum()
    return safe_div(s, c.resid.shift(21).rolling(231, min_periods=150).std() * np.sqrt(231))


@signal("momentum", "Price relative to its 52-week high (George-Hwang)")
def high_52w(c: FeatureContext):
    return safe_div(c.md.close, c.md.high.rolling(252, min_periods=200).max())


@signal("momentum", "3-month trend x R-squared of log-price on time (smooth trends persist)")
def trend_quality(c: FeatureContext):
    lp = np.log(c.md.close)
    t = pd.Series(np.arange(len(lp), dtype=float), index=lp.index)
    r2 = lp.rolling(63, min_periods=50).corr(t) ** 2
    return (lp - lp.shift(63)) * r2


@signal("momentum", "Momentum acceleration: last 3 months minus the 3 months before")
def mom_accel(c: FeatureContext):
    lp = np.log(c.md.close)
    return (lp - lp.shift(63)) - (lp.shift(63) - lp.shift(126))


@signal("momentum", "Cumulative 21-day overnight return (overnight momentum, Lou-Polk-Skouras)")
def overnight_mom(c: FeatureContext):
    return np.log1p(c.overnight).rolling(21, min_periods=15).sum()


@signal("momentum", "Minus cumulative 21-day intraday return (intraday reversal)")
def intraday_rev_21(c: FeatureContext):
    return -np.log1p(c.intraday).rolling(21, min_periods=15).sum()


@signal("momentum", "Peer-group (k-means on PCA loadings) 1-month return: industry momentum")
def cluster_mom(c: FeatureContext):
    r21 = c.log_ret.rolling(21, min_periods=15).sum()
    return _cluster_mean(r21, c.clusters)


# =============================================================================
# Volume / liquidity
# =============================================================================
@signal("volume", "Log ratio of 5-day to 63-day volume (attention / abnormal volume)")
def abn_volume(c: FeatureContext):
    return np.log(safe_div(c.md.volume.rolling(5, min_periods=3).mean(),
                           c.md.volume.rolling(63, min_periods=40).mean()))


@signal("volume", "Log Amihud illiquidity |r| / $volume (illiquidity premium)")
def amihud(c: FeatureContext):
    x = safe_div(c.ret.abs(), c.dollar_volume)
    return np.log(x.rolling(21, min_periods=15).mean() * 1e9 + 1e-12)


@signal("volume", "Minus log ratio of 21-day to 252-day $volume (crowding)")
def turnover_trend(c: FeatureContext):
    dv = c.dollar_volume
    return -np.log(safe_div(dv.rolling(21, min_periods=15).mean(), dv.rolling(252, min_periods=150).mean()))


@signal("volume", "Rolling correlation of returns and volume changes, negated")
def vol_price_corr(c: FeatureContext):
    dv = np.log(c.md.volume.replace(0, np.nan)).diff()
    return -c.ret.rolling(21, min_periods=15).corr(dv)


@signal("volume", "Minus log market cap proxy: log of 63-day median $volume (size effect)")
def size_proxy(c: FeatureContext):
    return -np.log(c.dollar_volume.rolling(63, min_periods=40).median())


# =============================================================================
# Volatility / risk
# =============================================================================
@signal("volatility", "Minus 63-day realized volatility (low-volatility anomaly)")
def low_vol(c: FeatureContext):
    return -c.vol_63


@signal("volatility", "Minus 63-day idiosyncratic volatility (Ang et al. 2006)")
def idio_vol(c: FeatureContext):
    return -c.resid.rolling(63, min_periods=40).std()


@signal("volatility", "Minus the largest daily return over 21 days (MAX effect, Bali et al.)")
def max_effect(c: FeatureContext):
    return -c.ret.rolling(21, min_periods=15).max()


@signal("volatility", "Minus 63-day return skewness (lottery stocks underperform)")
def neg_skew(c: FeatureContext):
    return -c.ret.rolling(63, min_periods=40).skew()


@signal("volatility", "Minus 252-day market beta (betting against beta, Frazzini-Pedersen)")
def bab(c: FeatureContext):
    return -c.beta_252


@signal("volatility", "Minus downside beta: beta measured on down-market days only")
def downside_beta(c: FeatureContext):
    down = c.market_ret < 0
    return -rolling_beta(c.ret.where(down, np.nan), c.market_ret.where(down), 252)


@signal("volatility", "Minus volatility of volatility (stability premium)")
def vol_of_vol(c: FeatureContext):
    return -safe_div(c.vol_21.rolling(63, min_periods=40).std(), c.vol_21.rolling(63, min_periods=40).mean())


# =============================================================================
# Microstructure (OHLC bars)
# =============================================================================
def _parkinson(c: FeatureContext) -> pd.DataFrame:
    return np.log(safe_div(c.md.high, c.md.low)) ** 2 / (4 * LN2)


@signal("microstructure", "Minus short/long Parkinson range-volatility ratio (vol expansion)")
def range_vol_ratio(c: FeatureContext):
    pk = _parkinson(c)
    return -np.log(safe_div(pk.rolling(5, min_periods=3).mean(), pk.rolling(63, min_periods=40).mean()))


@signal("microstructure", "Minus 5-day close-location value: closes near the high fade")
def close_location(c: FeatureContext):
    h, l, cl = c.md.high, c.md.low, c.md.close
    clv = safe_div((cl - l) - (h - cl), h - l)
    return -clv.rolling(5, min_periods=3).mean()


@signal("microstructure", "Corwin-Schultz bid-ask spread estimate (liquidity provision premium)")
def cs_spread(c: FeatureContext):
    return c.spread


@signal("microstructure", "Garman-Klass volatility relative to close-to-close volatility")
def gk_ratio(c: FeatureContext):
    h, l, o, cl = c.md.high, c.md.low, c.md.open, c.md.close
    gk = 0.5 * np.log(safe_div(h, l)) ** 2 - (2 * LN2 - 1) * np.log(safe_div(cl, o)) ** 2
    gkv = np.sqrt(gk.clip(lower=0).rolling(21, min_periods=15).mean())
    return -np.log(safe_div(gkv, c.vol_21))


# =============================================================================
# Seasonality
# =============================================================================
@signal("seasonality", "Average return over the next month in each of the past 5 years (Heston-Sadka)")
def same_month(c: FeatureContext):
    lp = np.log(c.md.close)
    parts = [lp.shift(252 * k - 21) - lp.shift(252 * k) for k in range(1, 6)]
    stack = np.stack([p.to_numpy() for p in parts])
    cnt = np.isfinite(stack).sum(axis=0)
    with np.errstate(invalid="ignore"):
        mean = np.nanmean(np.where(cnt >= 2, stack, np.nan), axis=0)
    return pd.DataFrame(mean, index=lp.index, columns=lp.columns)


@signal("seasonality", "Average residual return on the same weekday as tomorrow, past year")
def weekday_seasonality(c: FeatureContext):
    e = c.resid
    acc = None
    n = None
    for k in range(1, 53):
        x = e.shift(5 * k - 1)
        acc = x.fillna(0) if acc is None else acc + x.fillna(0)
        n = x.notna().astype(float) if n is None else n + x.notna()
    return safe_div(acc, n.where(n >= 26))


@signal("seasonality", "Turn-of-month exposure: beta x (days to month end <= 3)")
def turn_of_month(c: FeatureContext):
    # Is the next business day one of the last 2 or first 3 business days of
    # its month? Uses only the calendar, which is known in advance.
    idx = c.ret.index
    nxt = (idx + pd.offsets.BDay(1)).values.astype("datetime64[D]")
    month_start = (idx + pd.offsets.BDay(1)).to_period("M").start_time.values.astype("datetime64[D]")
    month_end = (idx + pd.offsets.BDay(1)).to_period("M").end_time.normalize().values.astype("datetime64[D]")
    from_start = np.busday_count(month_start, nxt)
    to_end = np.busday_count(nxt, month_end + np.timedelta64(1, "D")) - 1
    flag = pd.Series(((from_start <= 2) | (to_end <= 1)).astype(float), index=idx)
    return c.beta_252.mul(flag * 2 - 1, axis=0)


# =============================================================================
# Structure: peers, filters, autocorrelation
# =============================================================================
@signal("structure", "Peer-group 5-day return minus own 5-day return (lagging peers catch up)")
def peer_gap(c: FeatureContext):
    r5 = c.log_ret.rolling(5, min_periods=4).sum()
    return _cluster_mean(r5, c.clusters) - r5


@signal("structure", "Peer-group return yesterday (lead-lag within peer groups)")
def peer_lead(c: FeatureContext):
    return _cluster_mean(c.ret, c.clusters)


@signal("structure", "Kalman-filtered local-linear-trend slope of log price / volatility")
def kalman_trend(c: FeatureContext):
    return safe_div(kalman_slope(np.log(c.md.close)), c.vol_63)


@signal("structure", "Lag-1 autocorrelation x last return: continue trends, fade noise")
def autocorr_signal(c: FeatureContext):
    ac = c.ret.rolling(63, min_periods=40).corr(c.ret.shift(1))
    return ac * safe_div(c.ret, c.vol_63)


@signal("structure", "Minus correlation with the market over 63 days (diversifier premium)")
def market_corr(c: FeatureContext):
    return -c.ret.rolling(63, min_periods=40).corr(c.market_ret)


# =============================================================================
# helpers
# =============================================================================
def _cluster_mean(x: pd.DataFrame, clusters: pd.DataFrame) -> pd.DataFrame:
    """Mean of ``x`` within each stock's peer cluster on each day."""
    X = x.to_numpy(dtype=float)
    C = clusters.reindex_like(x).to_numpy()
    out = np.full_like(X, np.nan)
    labels = np.unique(C[np.isfinite(C)])
    for lab in labels:
        m = (C == lab) & np.isfinite(X)
        s = np.where(m, X, 0.0).sum(axis=1)
        n = m.sum(axis=1)
        mean = np.where(n >= 3, s / np.maximum(n, 1), np.nan)
        out = np.where(C == lab, mean[:, None], out)
    return pd.DataFrame(out, index=x.index, columns=x.columns)


def kalman_slope(logp: pd.DataFrame, q_level: float = 1e-2, q_slope: float = 1e-4) -> pd.DataFrame:
    """Local-linear-trend Kalman filter run on every stock at once.

    State s_t = [level, slope];  level_{t+1} = level_t + slope_t + w1,
    slope_{t+1} = slope_t + w2;  observation y_t = level_t + v,  Var(v) = 1.
    Only the ratio of noise variances matters for the gain, so measurement
    noise is normalised to 1. Missing prices skip the update step.
    """
    Y = logp.to_numpy(dtype=float)
    T, N = Y.shape
    F = np.array([[1.0, 1.0], [0.0, 1.0]])
    Q = np.diag([q_level, q_slope])
    s = np.zeros((N, 2))
    P = np.tile(np.eye(2) * 1e3, (N, 1, 1))
    started = np.zeros(N, dtype=bool)
    out = np.full((T, N), np.nan)
    for t in range(T):
        y = Y[t]
        obs = np.isfinite(y)
        # initialise level at the first observation
        new = obs & ~started
        s[new, 0] = y[new]
        started |= obs
        # predict
        s = s @ F.T
        P = F @ P @ F.T + Q
        # update (H = [1, 0])
        S = P[:, 0, 0] + 1.0
        K = P[:, :, 0] / S[:, None]
        innov = np.where(obs, y - s[:, 0], 0.0)
        s = s + K * innov[:, None]
        upd = obs[:, None, None]
        P = np.where(upd, P - K[:, :, None] * P[:, 0:1, :], P)
        out[t] = np.where(started & obs, s[:, 1], np.nan)
    return pd.DataFrame(out, index=logp.index, columns=logp.columns)
