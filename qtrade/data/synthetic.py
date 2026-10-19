"""A synthetic stock market with *known* hidden structure.

Used by the test-suite and by ``qtrade demo`` so the whole pipeline can be run
without an internet connection. The generator plants:

* a 3-state hidden Markov regime (calm / normal / crisis) that changes factor
  volatility, drift and cross-stock correlation - the HMM should recover it;
* a K-factor return structure - PCA should recover it;
* short-term reversal in idiosyncratic returns and a slow-moving persistent
  alpha (momentum) - the signals and models should find both.

Because the true structure is known, tests can check that each component
actually does its job, which is impossible with real data alone.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .market import MarketData

REGIMES = {  # (factor vol multiplier, market drift per day, idio vol multiplier)
    0: (0.6, 0.0006, 0.8),   # calm bull market
    1: (1.0, 0.0002, 1.0),   # normal
    2: (2.6, -0.0015, 1.6),  # crisis
}
TRANSITION = np.array([
    [0.985, 0.014, 0.001],
    [0.010, 0.980, 0.010],
    [0.002, 0.038, 0.960],
])


def make_market(
    n_stocks: int = 120,
    n_days: int = 2520,
    n_factors: int = 5,
    reversal: float = 0.06,
    alpha_strength: float = 0.0004,
    late_listing_frac: float = 0.15,
    seed: int = 0,
    start: str = "2006-01-02",
) -> tuple[MarketData, pd.Series]:
    """Return (market data, true regime series)."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(start, periods=n_days)
    tickers = [f"S{i:04d}" for i in range(n_stocks)]

    # --- hidden regime path -------------------------------------------------
    states = np.zeros(n_days, dtype=int)
    states[0] = 1
    for t in range(1, n_days):
        states[t] = rng.choice(3, p=TRANSITION[states[t - 1]])
    fvol_mult = np.array([REGIMES[s][0] for s in states])
    drift = np.array([REGIMES[s][1] for s in states])
    ivol_mult = np.array([REGIMES[s][2] for s in states])

    # --- factor structure ---------------------------------------------------
    betas = rng.normal(0, 0.6, (n_stocks, n_factors))
    betas[:, 0] = rng.uniform(0.6, 1.4, n_stocks)  # market factor
    fvol = np.array([0.010] + [0.005] * (n_factors - 1))
    f = rng.standard_normal((n_days, n_factors)) * fvol * fvol_mult[:, None]
    f[:, 0] += drift

    # --- idiosyncratic returns with planted predictability ------------------
    idio_vol = rng.uniform(0.010, 0.025, n_stocks)
    noise = rng.standard_normal((n_days, n_stocks)) * idio_vol * ivol_mult[:, None]
    slow_alpha = np.zeros((n_days, n_stocks))
    eps = np.zeros((n_days, n_stocks))
    for t in range(1, n_days):
        slow_alpha[t] = 0.995 * slow_alpha[t - 1] + rng.standard_normal(n_stocks) * alpha_strength * 0.1
        eps[t] = noise[t] - reversal * eps[t - 1] + slow_alpha[t]

    ret = f @ betas.T + eps
    ret = np.clip(ret, -0.5, 0.5)

    # split each day into overnight and intraday pieces
    frac_overnight = rng.uniform(0.2, 0.5, (n_days, n_stocks))
    overnight = ret * frac_overnight
    intraday = (1 + ret) / (1 + overnight) - 1

    close = np.empty_like(ret)
    open_ = np.empty_like(ret)
    p0 = rng.uniform(20, 200, n_stocks)
    prev = p0
    for t in range(n_days):
        open_[t] = prev * (1 + overnight[t])
        close[t] = open_[t] * (1 + intraday[t])
        prev = close[t]
    span = np.abs(rng.standard_normal((n_days, n_stocks))) * idio_vol * 0.6
    high = np.maximum(open_, close) * (1 + span)
    low = np.minimum(open_, close) * (1 - span * rng.uniform(0.5, 1.0, (n_days, n_stocks)))

    base_vol = rng.lognormal(13.5, 1.0, n_stocks)
    volume = base_vol * np.exp(0.3 * rng.standard_normal((n_days, n_stocks))) * (
        1 + 8 * np.abs(eps) / idio_vol
    )

    frames = {k: pd.DataFrame(v, index=dates, columns=tickers)
              for k, v in dict(open=open_, high=high, low=low, close=close, volume=volume).items()}

    # some companies list partway through the sample
    n_late = int(late_listing_frac * n_stocks)
    late = rng.choice(n_stocks, n_late, replace=False)
    for j in late:
        cut = rng.integers(n_days // 5, n_days // 2)
        for df in frames.values():
            df.iloc[:cut, j] = np.nan

    return MarketData(**frames), pd.Series(states, index=dates, name="true_regime")
