"""Intraday signals, computed one session at a time.

Everything for bar b of day d uses only bars 0..b of day d plus *earlier* days
(volatility and volume baselines), so the backtest and the live trader call
exactly the same functions. Returns are measured against the cross-sectional
average (the "market" move in that bar), and scaled by each stock's own
5-minute volatility, so a 30 bp move means more in a sleepy utility than in a
chip stock.

Signals (positive = expected to outperform over the next half hour):

rev_1        minus the last bar's relative return
rev_3        minus the last 15 minutes' relative return
rev_12       minus the last hour's relative return
day_ret      the relative return since the open (its sign is learned)
gap          minus the overnight gap (previous close -> today's open)
vwap_dev     minus the distance from today's running VWAP
abn_vol      volume in the last 15 minutes vs. the usual volume at this time of day
rev3_lowvol  15-minute reversal, stronger when it happened on light volume

The model sees each signal three times, once per third of the session, so it
can weight the open, midday and close differently.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .bars import DayBars

BASE_FEATURES = ["rev_1", "rev_3", "rev_12", "day_ret", "gap", "vwap_dev", "abn_vol", "rev3_lowvol"]
N_BUCKETS = 3
FEATURES = [f"{f}@{k}" for k in ("open", "mid", "close") for f in BASE_FEATURES]


@dataclass
class History:
    """Per-day baselines built from *previous* days only."""
    sigma: np.ndarray        # D x N   std of 5-minute log returns
    adv: np.ndarray          # D x N   median daily dollar volume
    vol_base: np.ndarray     # D x B x N  average volume in each bar slot
    prev_close: np.ndarray   # D x N   last close of the previous session


def _ffill_bars(x: np.ndarray) -> np.ndarray:
    """Forward-fill along the bar axis (axis -2 of B x N or D x B x N)."""
    out = x.copy()
    for b in range(1, out.shape[-2]):
        prev = out[..., b - 1, :]
        cur = out[..., b, :]
        out[..., b, :] = np.where(np.isfinite(cur), cur, prev)
    return out


def history(bars: DayBars, vol_days: int = 20) -> History:
    D, B, N = bars.close.shape
    px = _ffill_bars(bars.close)
    with np.errstate(invalid="ignore", divide="ignore"):
        lr = np.diff(np.log(px), axis=1)
        n_ok = np.isfinite(lr).sum(axis=1)
        dvar = np.where(n_ok >= B // 2, np.nanmean(lr ** 2, axis=1), np.nan)      # D x N
        dollar = np.nansum(np.nan_to_num(bars.close) * bars.volume, axis=1)        # D x N
    dollar[np.isfinite(px[:, -1]) == False] = np.nan  # noqa: E712  (no trading that day)
    mp = max(5, vol_days // 2)
    sigma = np.sqrt(pd.DataFrame(dvar).rolling(vol_days, min_periods=mp).mean().shift(1).to_numpy())
    adv = pd.DataFrame(dollar).rolling(vol_days, min_periods=mp).median().shift(1).to_numpy()
    # mean volume per slot over the previous vol_days sessions
    v = np.nan_to_num(bars.volume).astype(np.float64)
    cs = np.cumsum(v, axis=0)
    base = np.full(v.shape, np.nan, dtype=np.float32)
    for d in range(1, D):
        lo = max(0, d - vol_days)
        tot = cs[d - 1] - (cs[lo - 1] if lo > 0 else 0)
        base[d] = tot / (d - lo)
    last = px[:, -1, :]
    prev_close = np.vstack([np.full((1, N), np.nan), last[:-1]]).astype(np.float32)
    return History(sigma.astype(np.float32), adv.astype(np.float32), base, prev_close)


def _cs_demean(x: np.ndarray) -> np.ndarray:
    with np.errstate(invalid="ignore"):
        return x - np.nanmean(x, axis=-1, keepdims=True)


def _cs_z(x: np.ndarray) -> np.ndarray:
    with np.errstate(invalid="ignore", divide="ignore"):
        mu = np.nanmean(x, axis=-1, keepdims=True)
        sd = np.nanstd(x, axis=-1, keepdims=True)
        return np.clip((x - mu) / np.where(sd > 0, sd, np.nan), -4, 4)


def day_features(open_: np.ndarray, close: np.ndarray, volume: np.ndarray, vwap: np.ndarray,
                 prev_close: np.ndarray, sigma: np.ndarray, vol_base: np.ndarray) -> np.ndarray:
    """B x N x len(FEATURES) features for one session (NaN = not tradable at that bar)."""
    B, N = close.shape
    px = _ffill_bars(close)
    anchor = np.where(np.isfinite(open_[0]), open_[0], prev_close)
    ext = np.vstack([anchor[None], px])
    b = np.arange(B)[:, None]
    sig = np.where(sigma > 0, sigma, np.nan)[None, :]
    valid = np.isfinite(px) & np.isfinite(sig) & np.isfinite(anchor)[None]

    def ret_k(k):
        lag = np.maximum(np.arange(B) + 1 - k, 0)
        return ext[1:] / ext[lag] - 1

    with np.errstate(invalid="ignore", divide="ignore"):
        f = {}
        f["rev_1"] = -_cs_demean(ret_k(1)) / sig
        f["rev_3"] = -_cs_demean(ret_k(3)) / (sig * np.sqrt(np.minimum(3, b + 1)))
        f["rev_12"] = -_cs_demean(ret_k(12)) / (sig * np.sqrt(np.minimum(12, b + 1)))
        f["day_ret"] = _cs_demean(px / anchor - 1) / (sig * np.sqrt(b + 1))
        gap = np.broadcast_to(anchor / prev_close - 1, (B, N))
        f["gap"] = -_cs_demean(np.where(valid, gap, np.nan)) / (sig * np.sqrt(6))
        vv = np.nan_to_num(volume)
        pv = np.cumsum(np.nan_to_num(vwap) * vv, axis=0)
        cum_vwap = pv / np.where(np.cumsum(vv, axis=0) > 0, np.cumsum(vv, axis=0), np.nan)
        f["vwap_dev"] = -_cs_demean(px / cum_vwap - 1) / (sig * np.sqrt(b + 1))
        v3 = np.cumsum(vv, axis=0)
        v3 = v3 - np.vstack([np.zeros((3, N)), v3[:-3]])
        bc = np.cumsum(np.nan_to_num(vol_base), axis=0)
        b3 = bc - np.vstack([np.zeros((3, N)), bc[:-3]])
        f["abn_vol"] = _cs_demean(np.log((v3 + 1) / (b3 + 1)))
        z = {k: _cs_z(np.where(valid, x, np.nan)) for k, x in f.items()}
        z["rev3_lowvol"] = _cs_z(z["rev_3"] * -np.tanh(np.nan_to_num(z["abn_vol"])))
    X = np.stack([np.nan_to_num(z[k]) for k in BASE_FEATURES], axis=-1).astype(np.float32)
    X[~valid] = np.nan
    return expand_time_of_day(X)


def expand_time_of_day(X: np.ndarray) -> np.ndarray:
    """B x N x F -> B x N x (3F): each feature active only in its third of the day."""
    B, N, F = X.shape
    bucket = np.minimum(np.arange(B) * N_BUCKETS // B, N_BUCKETS - 1)
    out = np.zeros((B, N, F * N_BUCKETS), dtype=np.float32)
    for k in range(N_BUCKETS):
        rows = bucket == k
        out[rows, :, k * F:(k + 1) * F] = X[rows]
    out[~np.isfinite(X[..., 0])] = np.nan
    return out


def exec_prices(open_: np.ndarray, close: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Trade prices at the B+1 decision points of a session: the open of each
    bar, then the closing price. Returns (forward-filled prices, tradable mask)."""
    Q = np.vstack([open_, close[-1:]])
    can = np.isfinite(Q)
    Qf = Q.copy()
    for k in range(1, len(Qf)):
        Qf[k] = np.where(can[k], Qf[k], Qf[k - 1])
    return Qf, can


def day_target(open_: np.ndarray, close: np.ndarray, sigma: np.ndarray, horizon: int) -> np.ndarray:
    """Training label for bar b: relative return from the open of bar b+1 to the
    open of bar b+1+horizon (or the close), in units of 5-minute volatility."""
    B = open_.shape[0]
    Qf, can = exec_prices(open_, close)
    k0 = np.arange(B) + 1
    k1 = np.minimum(k0 + horizon, B)
    with np.errstate(invalid="ignore", divide="ignore"):
        r = Qf[k1] / Qf[k0] - 1
        r[~can[k0]] = np.nan
        h = np.maximum(k1 - k0, 1)[:, None]
        y = _cs_demean(r) / (np.where(sigma > 0, sigma, np.nan)[None] * np.sqrt(h))
    return np.clip(y, -5, 5)
