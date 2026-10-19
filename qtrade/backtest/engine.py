"""Event-by-event daily backtest with realistic execution.

Each day t:
  close of t     forecasts and target weights are computed from data <= t
  open of t+1    overnight P&L on yesterday's book; trade toward the target at
                 the opening price, paying spread + impact
  close of t+1   intraday P&L on the new book; short positions pay borrow

Stocks that fail to print a price cannot be traded that day; after five
missing days in a row the position is written off at its last price.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..features.context import FeatureContext
from ..portfolio.decider import Decider
from ..portfolio.optimizer import trade_toward
from ..utils import LOG
from .costs import borrow_cost, trade_cost


@dataclass
class BacktestResult:
    daily: pd.DataFrame          # one row per day: returns, exposures, costs...
    weights: pd.DataFrame        # end-of-day weights (fractions of equity)
    ic: pd.Series                # realised daily rank IC of the traded forecast
    name: str = "strategy"

    @property
    def returns(self) -> pd.Series:
        return self.daily["ret"]


def run_backtest(
    ctx: FeatureContext,
    pred: np.ndarray,
    fwd_ret: np.ndarray,
    cfg,
    start: pd.Timestamp | None = None,
    name: str = "strategy",
    record_weights: bool = True,
) -> BacktestResult:
    md = ctx.md
    dates = md.dates
    T, N = pred.shape
    O = md.open.to_numpy()
    Cl = md.close.to_numpy()
    p = cfg.portfolio
    dec = Decider(ctx, pred, fwd_ret, cfg)
    sigma, adv = dec.sigma, dec.adv

    t0 = int(np.argmax(np.isfinite(pred).any(axis=1)))
    if start is not None:
        t0 = max(t0, int(dates.searchsorted(pd.Timestamp(start))))
    equity = cfg.costs.aum
    peak = equity
    dd_mode = False
    w = np.zeros(N)                   # weights at today's close
    missing = np.zeros(N, dtype=int)
    rows = []
    W = np.zeros((T, N), dtype=np.float32) if record_weights else None

    for t in range(t0, T - 1):
        # ---------- decision at close t (data <= t only) ----------
        d = dec.decide(t, w, equity, p.drawdown_scale if dd_mode else 1.0)
        w_tgt, info, ic_hat, hold_L = d.weights, d.info, d.ic_hat, d.holding_periods

        # ---------- open of t+1: overnight P&L, then trade ----------
        o1, c1 = O[t + 1], Cl[t + 1]
        priced = np.isfinite(o1) & np.isfinite(c1) & np.isfinite(Cl[t])
        missing = np.where(priced, 0, missing + 1)
        overnight = np.where(priced, o1 / Cl[t] - 1, 0.0)
        intraday = np.where(priced, c1 / o1 - 1, 0.0)
        overnight = np.nan_to_num(overnight)
        intraday = np.nan_to_num(intraday)

        hold = w * equity
        pnl_on = (hold * overnight).sum()
        hold = hold * (1 + overnight)
        eq_open = equity + pnl_on
        w_open = hold / eq_open if eq_open > 0 else hold * 0

        # names with no price cannot trade; long-missing names are written off
        w_new = trade_toward(w_open, w_tgt, p.trade_rate, p.no_trade_band)
        w_new[~priced] = w_open[~priced]
        if p.whole_shares and eq_open > 0:
            px = np.where(priced, o1, np.nan)
            shares = np.trunc(np.nan_to_num(w_new * eq_open / px))
            w_new = np.where(priced, shares * np.nan_to_num(px) / eq_open, w_new)
        dead = missing >= 5
        w_new[dead] = 0.0

        trade_dollars = (w_new - w_open) * eq_open
        trade_dollars[dead] = 0.0
        cost = trade_cost(trade_dollars, adv[t], sigma[t], cfg).sum()
        hold_new = w_new * eq_open

        # ---------- close of t+1 ----------
        pnl_id = (hold_new * intraday).sum()
        borrow = borrow_cost(hold_new, cfg)
        new_equity = eq_open + pnl_id - cost - borrow
        ret = new_equity / equity - 1
        hold_close = hold_new * (1 + intraday)
        w = hold_close / new_equity if new_equity > 0 else hold_close * 0
        equity = new_equity

        peak = max(peak, equity)
        dd = equity / peak - 1
        if dd < -p.drawdown_limit:
            dd_mode = True
        elif dd > -p.drawdown_limit / 2:
            dd_mode = False

        if W is not None:
            W[t + 1] = w
        rows.append({
            "date": dates[t + 1], "ret": ret, "equity": equity,
            "gross": np.abs(w).sum(), "net": w.sum(),
            "long_names": int((w > 1e-6).sum()), "short_names": int((w < -1e-6).sum()),
            "turnover": np.abs(trade_dollars).sum() / max(eq_open, 1e-9),
            "cost": cost / max(equity, 1e-9), "borrow": borrow / max(equity, 1e-9),
            "pnl_overnight": pnl_on / max(equity, 1e-9), "pnl_intraday": pnl_id / max(equity, 1e-9),
            "ic_hat": ic_hat, "holding_periods": hold_L, "scale": info.scale, "binding": info.binding,
            "predicted_vol": info.predicted_vol, "drawdown": dd, "dd_mode": dd_mode,
        })

    daily = pd.DataFrame(rows).set_index("date")
    weights = pd.DataFrame(W, index=dates, columns=md.tickers).loc[daily.index] if W is not None else None
    LOG.info("backtest %-12s %s -> %s  final equity %.0f", name, daily.index[0].date(),
             daily.index[-1].date(), equity)
    return BacktestResult(daily=daily, weights=weights, ic=pd.Series(dec.ic, index=dates), name=name)
