"""Transaction-cost model.

cost of trading Q dollars of stock i =
    |Q| * (commission + slippage + half_spread_i)        crossing the bid-ask spread
  + |Q| * c * sigma_i * sqrt(|Q| / ADV_i)                square-root market impact

Half-spreads come from liquidity tiers (21-day median dollar volume): quoted
half-spreads for the most liquid US stocks are around a basis point, and wider
for smaller names. The tiers in ``CostConfig`` are deliberately a little
conservative. Impact follows the empirical square-root law (Almgren et al.
2005; Toth et al. 2011). Short positions also pay an annual borrow fee.
"""
from __future__ import annotations

import numpy as np


def half_spread(adv: np.ndarray, cfg) -> np.ndarray:
    """Half-spread (as a fraction) for each stock from its dollar-volume tier."""
    adv = np.nan_to_num(adv, nan=0.0)
    out = np.full(adv.shape, np.nan)
    for threshold, bps in sorted(cfg.costs.spread_tiers, key=lambda x: -x[0]):
        out = np.where(np.isnan(out) & (adv >= threshold), bps / 1e4, out)
    return np.nan_to_num(out, nan=max(b for _, b in cfg.costs.spread_tiers) / 1e4)


def trade_cost(dollars: np.ndarray, adv: np.ndarray, sigma: np.ndarray, cfg) -> np.ndarray:
    c = cfg.costs
    q = np.abs(dollars)
    adv_ = np.where(np.isfinite(adv) & (adv > 0), adv, np.inf)
    sig = np.nan_to_num(sigma, nan=0.02)
    impact = c.impact_coef * sig * np.sqrt(q / adv_)
    fixed = (c.commission_bps + c.slippage_bps) / 1e4 + half_spread(adv, cfg)
    return q * (fixed + impact)


def unit_cost(adv: np.ndarray, sigma: np.ndarray, equity: float, cfg) -> np.ndarray:
    """Approximate cost per unit of weight traded, for the optimizer's no-trade
    band, evaluated at a typical trade of half the per-name cap."""
    typical = 0.5 * cfg.portfolio.max_weight * equity
    dollars = np.full(np.shape(adv), typical)
    return trade_cost(dollars, adv, sigma, cfg) / typical


def borrow_cost(dollars: np.ndarray, cfg) -> float:
    shorts = np.clip(-dollars, 0, None).sum()
    return shorts * cfg.costs.borrow_bps_annual / 1e4 / 252
