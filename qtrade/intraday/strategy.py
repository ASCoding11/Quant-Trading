"""Intraday reversal: walk-forward model, portfolio rule and bar-by-bar backtest.

Timeline within a session (5-minute bars, 78 per day)::

    close of bar b      features use bars 0..b of today and earlier days only
    open of bar b+1     trade toward the target at that price, paying costs
    ...                 from the open of bar ``flat_bar + 1`` (15:45) the target
                        is zero; anything still open is closed at the close

No position is ever held overnight, so there is no gap risk and no borrow fee.

The model is a ridge regression refit every month on the previous
``train_months``. Ridge only needs X'X and X'y, which add up across months,
so each month's sums are computed once and the rolling window is a sum of
twelve small matrices.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..utils import LOG
from .bars import DayBars
from .features import FEATURES, History, day_features, day_target, exec_prices, history


# -----------------------------------------------------------------------------
# costs and the portfolio rule (shared with the live trader)
# -----------------------------------------------------------------------------
def unit_cost(adv: np.ndarray, sigma: np.ndarray, icfg, trade_dollars: np.ndarray | float | None = None,
              n_bars: int = 78) -> np.ndarray:
    """Cost per dollar traded: half-spread by liquidity tier + slippage + sqrt impact."""
    adv = np.nan_to_num(adv, nan=0.0)
    hs = np.full(adv.shape, np.nan)
    for threshold, bps in sorted(icfg.spread_tiers, key=lambda x: -x[0]):
        hs = np.where(np.isnan(hs) & (adv >= threshold), bps / 1e4, hs)
    hs = np.nan_to_num(hs, nan=max(b for _, b in icfg.spread_tiers) / 1e4)
    if trade_dollars is None:
        trade_dollars = icfg.gross * icfg.aum / max(2 * (icfg.n_side or 100), 1)
    q = np.abs(trade_dollars)
    sig_d = np.nan_to_num(sigma, nan=0.001) * np.sqrt(n_bars)
    impact = icfg.impact_coef * sig_d * np.sqrt(q / np.where(adv > 0, adv, np.inf))
    return hs + icfg.slippage_bps / 1e4 + impact


def target_weights(score: np.ndarray, sigma: np.ndarray, adv: np.ndarray, w_cur: np.ndarray,
                   icfg, ic: float, n_bars: int = 78) -> np.ndarray:
    """Dollar-neutral target weights (fractions of capital) from one bar's forecast.

    Weights are proportional to score / volatility. With ``n_side`` only the
    strongest names are opened, and a held name is kept while it stays in the
    top/bottom 2 x n_side (so names don't churn in and out). A cost-aware
    no-trade band (same derivation as the daily optimizer) leaves a position
    alone when moving it would cost more than the forecast is worth.
    """
    N = len(score)
    ok = np.isfinite(score) & np.isfinite(sigma) & (sigma > 0)
    w_out = np.where(ok, 0.0, w_cur)               # untradable names can't be changed
    if ok.sum() < 10 or ic <= 0:
        return w_out
    idx = np.nonzero(ok)[0]
    z = score[idx]
    z = (z - z.mean()) / (z.std() + 1e-12)
    sig = sigma[idx]
    G = icfg.gross
    if icfg.n_side and len(idx) > 2 * icfg.n_side:
        k = icfg.n_side
        rank = np.argsort(np.argsort(z))           # 0 = most negative
        n = len(idx)
        held_long, held_short = w_cur[idx] > 0, w_cur[idx] < 0
        longs = (rank >= n - k) | (held_long & (rank >= n - 2 * k))
        shorts = (rank < k) | (held_short & (rank < 2 * k))
        longs &= z > 0
        shorts &= z < 0
        raw = np.zeros(len(idx))
        raw[longs] = z[longs] / sig[longs]
        raw[shorts] = z[shorts] / sig[shorts]
        w = np.zeros(len(idx))
        if longs.any() and shorts.any():
            w[longs] = raw[longs] / raw[longs].sum() * G / 2
            w[shorts] = raw[shorts] / -raw[shorts].sum() * G / 2
        sel = longs | shorts
    else:
        raw = z / sig
        raw = raw - raw.mean()
        w = raw / np.abs(raw).sum() * G
        sel = np.ones(len(idx), dtype=bool)
    # no-trade band: half-width s_eff * c / var, with s_eff the scaling of the Kelly book
    h = icfg.horizon_bars
    var = sig ** 2 * h
    w_full = ic * z / (sig * np.sqrt(h))
    s_eff = G / max(np.abs(w_full[sel]).sum(), 1e-12)
    c = unit_cost(adv[idx], sig, icfg, n_bars=n_bars) * icfg.cost_aversion
    half = s_eff * c / var
    w = np.clip(w_cur[idx], w - half, w + half)
    w_out[idx] = w
    return w_out


# -----------------------------------------------------------------------------
# walk-forward model
# -----------------------------------------------------------------------------
@dataclass
class MonthStats:
    XtX: np.ndarray
    Xty: np.ndarray
    yty: float
    n: int


def _training_rows(X: np.ndarray, y: np.ndarray, icfg) -> tuple[np.ndarray, np.ndarray]:
    rows = slice(max(icfg.start_bar, 0), icfg.flat_bar)
    Xs, ys = X[rows].reshape(-1, X.shape[-1]), y[rows].reshape(-1)
    ok = np.isfinite(Xs[:, 0]) & np.isfinite(ys)
    return Xs[ok].astype(np.float64), ys[ok].astype(np.float64)


def fit_ridge(stats: list[MonthStats], ridge: float) -> tuple[np.ndarray, float]:
    """Coefficients and in-sample correlation from summed monthly statistics."""
    XtX = sum(s.XtX for s in stats)
    Xty = sum(s.Xty for s in stats)
    yty = sum(s.yty for s in stats)
    n = sum(s.n for s in stats)
    coef = np.linalg.solve(XtX + ridge * n * np.eye(len(Xty)), Xty)
    denom = np.sqrt(max(coef @ XtX @ coef, 1e-18) * max(yty, 1e-18))
    return coef, float(coef @ Xty / denom)


class Session:
    """Inputs for one day, sliced from the full arrays."""

    def __init__(self, bars: DayBars, hist: History, d: int):
        self.open, self.close = bars.open[d], bars.close[d]
        self.volume, self.vwap = bars.volume[d], bars.vwap[d]
        self.sigma, self.adv = hist.sigma[d], hist.adv[d]
        self.prev_close, self.vol_base = hist.prev_close[d], hist.vol_base[d]

    def features(self) -> np.ndarray:
        return day_features(self.open, self.close, self.volume, self.vwap, self.prev_close,
                            self.sigma, self.vol_base)


def walk_forward(bars: DayBars, hist: History, icfg) -> tuple[np.ndarray, pd.DataFrame, dict]:
    """Out-of-sample forecasts (D x B x N), the monthly fit log, and a final model."""
    D, B, N = bars.close.shape
    months = bars.days.to_period("M")
    uniq = months.unique()
    stats: dict = {}
    for m in uniq:                                  # pass 1: monthly sufficient statistics
        F = len(FEATURES)
        XtX, Xty, yty, n = np.zeros((F, F)), np.zeros(F), 0.0, 0
        for d in np.nonzero(months == m)[0]:
            s = Session(bars, hist, d)
            X, y = _training_rows(s.features(), day_target(s.open, s.close, s.sigma, icfg.horizon_bars), icfg)
            XtX += X.T @ X
            Xty += X.T @ y
            yty += float(y @ y)
            n += len(y)
        stats[m] = MonthStats(XtX, Xty, yty, n)
    pred = np.full((D, B, N), np.nan, dtype=np.float32)
    log = []
    for j, m in enumerate(uniq):                    # pass 2: forecast each month with earlier months
        train = [stats[p] for p in uniq[max(0, j - icfg.train_months):j] if stats[p].n > 0]
        if len(train) < icfg.min_train_months:
            continue
        coef, ic = fit_ridge(train, icfg.ridge)
        for d in np.nonzero(months == m)[0]:
            X = Session(bars, hist, d).features()
            pred[d] = np.einsum("bnf,f->bn", np.nan_to_num(X), coef).astype(np.float32)
            pred[d][~np.isfinite(X[..., 0])] = np.nan
        log.append({"month": str(m), "train_months": len(train), "ic_in_sample": ic,
                    **{f: c for f, c in zip(FEATURES, coef)}})
        LOG.info("intraday model %s: trained on %d months, in-sample IC %.4f", m, len(train), ic)
    final_stats = [stats[p] for p in uniq[-icfg.train_months:] if stats[p].n > 0]
    final = {}
    if final_stats:
        coef, ic = fit_ridge(final_stats, icfg.ridge)
        final = {"features": FEATURES, "coef": coef.tolist(), "ic_in_sample": ic,
                 "trained_through": str(bars.days[-1].date()), "tickers": bars.tickers}
    return pred, pd.DataFrame(log), final


# -----------------------------------------------------------------------------
# backtest
# -----------------------------------------------------------------------------
def run_backtest(bars: DayBars, hist: History, pred: np.ndarray, icfg, ic_by_day: np.ndarray,
                 frictionless: bool = False) -> pd.DataFrame:
    """Bar-by-bar simulation; one row per session."""
    D, B, N = bars.close.shape
    equity = icfg.aum
    rows = []
    for d in range(D):
        if not np.isfinite(pred[d]).any():
            continue
        Qf, can = exec_prices(bars.open[d], bars.close[d])
        sigma, adv = hist.sigma[d], hist.adv[d]
        h = np.zeros(N)                     # dollars held
        pnl = cost = traded = gross_sum = 0.0
        n_trades = 0
        for k in range(1, B + 1):           # decision point k: open of bar k (k = B: the close)
            with np.errstate(invalid="ignore", divide="ignore"):
                r = np.nan_to_num(Qf[k] / Qf[k - 1] - 1)
            pnl += float(h @ r)
            h = h * (1 + r)
            gross_sum += np.abs(h).sum()
            b = k - 1                       # the bar whose close was just seen
            e_now = equity + pnl - cost
            if k > icfg.flat_bar or k == B:
                w_t = np.zeros(N)
            elif b >= icfg.start_bar and (b - icfg.start_bar) % icfg.rebalance_every == 0:
                w_t = target_weights(pred[d, b], sigma, adv, h / e_now, icfg, ic_by_day[d], B)
            else:
                continue
            new_h = np.where(can[k], w_t * e_now, h)
            if k == B:
                new_h[:] = 0.0              # anything without a closing print is closed at its last price
            dq = new_h - h
            if np.any(dq != 0):
                n_trades += int((np.abs(dq) > 1e-9).sum())
                traded += np.abs(dq).sum()
                if not frictionless:
                    cost += float((np.abs(dq) * unit_cost(adv, sigma, icfg, dq, B)).sum())
            h = new_h
        ret = (pnl - cost) / equity
        rows.append({"date": bars.days[d], "ret": ret, "pre_cost": pnl / equity, "cost": cost / equity,
                     "turnover": traded / equity, "avg_gross": gross_sum / B / equity,
                     "trades": n_trades, "ic": ic_by_day[d]})
        equity *= 1 + ret
    return pd.DataFrame(rows).set_index("date")


def realized_daily_ic(bars: DayBars, hist: History, pred: np.ndarray, icfg) -> np.ndarray:
    """Out-of-sample IC of each day's forecasts, known only after that day."""
    D = len(bars.days)
    out = np.full(D, np.nan)
    for d in range(D):
        if not np.isfinite(pred[d]).any():
            continue
        y = day_target(bars.open[d], bars.close[d], hist.sigma[d], icfg.horizon_bars)
        rows = slice(icfg.start_bar, icfg.flat_bar)
        p, t = pred[d, rows].ravel(), y[rows].ravel()
        ok = np.isfinite(p) & np.isfinite(t)
        if ok.sum() > 100:
            out[d] = np.corrcoef(p[ok], t[ok])[0, 1]
    return out


def ic_for_sizing(daily_ic: np.ndarray, prior: float = 0.02, prior_days: int = 60,
                  lookback: int = 120) -> np.ndarray:
    """Shrunk trailing out-of-sample IC available at the start of each day."""
    out = np.full(len(daily_ic), prior)
    for d in range(len(daily_ic)):
        h = daily_ic[max(0, d - lookback):d]
        h = h[np.isfinite(h)]
        out[d] = max((h.sum() + prior * prior_days) / (len(h) + prior_days), 0.0)
    return out


def prepare(bars: DayBars, icfg):
    hist = history(bars, icfg.vol_days)
    pred, log, final = walk_forward(bars, hist, icfg)
    daily_ic = realized_daily_ic(bars, hist, pred, icfg)
    return hist, pred, log, final, daily_ic
