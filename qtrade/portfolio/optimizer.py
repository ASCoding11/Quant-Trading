"""From forecasts to positions.

1. Forecast -> expected return (Grinold's "alpha = IC x volatility x score"):

       alpha_i = IC_hat * sigma_i * z_i

   z_i is the model's cross-sectional z-score, sigma_i the stock's daily
   idiosyncratic volatility, and IC_hat the model's recently *realised*
   information coefficient, shrunk toward a prior (see ``realized_ic``).

2. Kelly-optimal market-neutral weights. Maximising expected log growth
   ``w'alpha - 1/2 w' Sigma w`` subject to  C'w = 0  (C = [1, B]: zero net
   dollars and zero exposure to every PCA factor) gives

       w* = D^-1 (alpha - C lam),   lam = (C' D^-1 C)^-1 C' D^-1 alpha

   where D is the diagonal idiosyncratic variance. Because the constraints
   remove all factor exposure, factor covariance drops out of the problem.

3. Leverage = min(fractional Kelly, volatility target, gross cap).

4. Transaction-cost no-trade band (see ``construct``), then per-name caps,
   re-projecting onto the neutral subspace after clipping.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

TRADING_DAYS = 252


@dataclass
class SizingInfo:
    scale: float
    binding: str          # which limit set the leverage: kelly / vol / gross
    predicted_vol: float  # annualised, after scaling
    gross: float
    net: float


def neutral_kelly(alpha: np.ndarray, var: np.ndarray, C: np.ndarray) -> np.ndarray:
    """w* = D^-1 (alpha - C lam) with C'w* = 0."""
    Dinv = 1.0 / var
    CtDinv = C.T * Dinv
    lam = np.linalg.lstsq(CtDinv @ C, CtDinv @ alpha, rcond=None)[0]
    return Dinv * (alpha - C @ lam)


def project_neutral(w: np.ndarray, C: np.ndarray) -> np.ndarray:
    """Remove any exposure to the columns of C (least-squares projection)."""
    coef = np.linalg.lstsq(C, w, rcond=None)[0]
    return w - C @ coef


def construct(
    z: np.ndarray,
    sigma: np.ndarray,
    loadings: np.ndarray | None,
    ic_hat: float,
    cfg,
    risk_scale: float = 1.0,
    w_cur: np.ndarray | None = None,
    tcost: np.ndarray | None = None,
    holding_periods: float = 1.0,
) -> tuple[np.ndarray, SizingInfo]:
    """Target weights (fractions of equity) for the stocks in ``z``.

    With ``w_cur`` and ``tcost`` (cost per unit of weight traded, in return
    units) each name solves the cost-aware problem

        max  a w - (g/2) d w^2 - c |w - w0|

    whose answer is a *no-trade band*: keep w0 if it lies within
    [(a - c)/(g d), (a + c)/(g d)], otherwise trade just to the nearest edge.
    Small, uncertain edges are therefore never paid for twice.

    A position is typically held for several forecast horizons, so the
    one-off cost is amortised over ``holding_periods`` (estimated by the
    caller from the forecast's autocorrelation: L = 1 / (1 - rho)).
    """
    p = cfg.portfolio
    h = cfg.model.horizon
    n = len(z)
    cap = p.max_weight if not p.max_names else max(p.max_weight, 1.5 * p.max_gross / p.max_names)
    if n < 10 or ic_hat <= 0:
        return np.zeros(n), SizingInfo(0.0, "no_edge", 0.0, 0.0, 0.0)
    sigma = np.clip(sigma, 0.003, 0.15)
    var_d = sigma ** 2
    var = var_d * h                      # variance over the forecast horizon
    use_factors = loadings is not None and p.factor_neutral
    C = np.column_stack([np.ones(n), loadings]) if use_factors else np.ones((n, 1))
    if p.weighting == "rank":
        # diagnostic alternative: weights proportional to the score itself
        var = np.full(n, var.mean())
        alpha = ic_hat * np.sqrt(var) * z
    else:
        alpha = ic_hat * sigma * np.sqrt(h) * z
    w_full = neutral_kelly(alpha, var, C)

    pred_vol = np.sqrt((w_full ** 2 * var_d).sum() * TRADING_DAYS)
    gross = np.abs(w_full).sum()
    scales = {
        "kelly": p.kelly_fraction,
        "vol": p.target_vol / pred_vol if pred_vol > 0 else 0.0,
        "gross": p.max_gross / gross if gross > 0 else 0.0,
    }
    binding = min(scales, key=scales.get)
    s = scales[binding] * risk_scale

    # cost-free target: scale, then cap names and refill exposure on the rest
    intended_gross = min(s * gross, p.max_gross)
    vol_cap = p.target_vol * risk_scale
    w = w_full * s
    for _ in range(12):
        w = project_neutral(np.clip(w, -cap, cap), C)
        g = np.abs(w).sum()
        v = np.sqrt((w ** 2 * var_d).sum() * TRADING_DAYS)
        up = min(intended_gross / g if g > 0 else 1.0, vol_cap / v if v > 0 else 1.0)
        if up < 1.01:
            break
        w = w * up
    w = np.clip(w, -cap, cap)

    if w_cur is not None and tcost is not None and s > 0:
        # no-trade band of half-width s_eff*c/var around the target, where
        # s_eff is the realised scaling of the Kelly portfolio (risk aversion 1/s_eff)
        s_eff = np.abs(w).sum() / gross if gross > 0 else s
        c = np.nan_to_num(tcost, nan=0.0) * p.cost_aversion / max(holding_periods, 1.0)
        half = s_eff * c / var
        w = np.clip(w_cur, w - half, w + half)
        w = project_neutral(np.clip(w, -cap, cap), C)

    w = np.clip(w, -cap, cap)
    g = np.abs(w).sum()
    if g > p.max_gross:
        w *= p.max_gross / g
    info = SizingInfo(
        scale=s, binding=binding,
        predicted_vol=float(np.sqrt((w ** 2 * var_d).sum() * TRADING_DAYS)),
        gross=float(np.abs(w).sum()), net=float(w.sum()),
    )
    return w, info


def realized_ic(ic_hist: np.ndarray, prior: float, prior_days: int) -> float:
    """Bayesian-shrunk estimate of the forecast's daily IC.

    Treat the prior as ``prior_days`` pseudo-observations at ``prior``, so a
    short or noisy track record is pulled toward the prior and a model whose
    edge has gone away is sized down - to zero if its IC turns negative.
    """
    h = ic_hist[np.isfinite(ic_hist)]
    est = (h.sum() + prior * prior_days) / (len(h) + prior_days)
    return float(max(est, 0.0))


def trade_toward(w_cur: np.ndarray, w_tgt: np.ndarray, rate: float, band: float) -> np.ndarray:
    """Partial adjustment (Garleanu-Pedersen): move ``rate`` of the way to the
    target each day, and skip trades smaller than ``band``. Exits are never
    delayed below the band (a target of exactly 0 is honoured)."""
    step = rate * (w_tgt - w_cur)
    new = w_cur + step
    small = np.abs(new - w_cur) < band
    new[small] = w_cur[small]
    exit_ = (w_tgt == 0) & (np.abs(new) < band)
    new[exit_] = 0.0
    return new
