"""A synthetic intraday market with planted short-term reversal, for tests and
the offline demo. Bar returns = market factor + idiosyncratic noise, where each
stock gives back a fraction of its last bar's idiosyncratic move."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .bars import DayBars, bars_per_day


def make_intraday(n_stocks: int = 60, n_days: int = 300, bar_minutes: int = 5, reversal: float = 0.15,
                  seed: int = 0) -> DayBars:
    rng = np.random.default_rng(seed)
    B = bars_per_day(bar_minutes)
    days = pd.bdate_range("2020-01-02", periods=n_days)
    ivol = rng.uniform(0.0008, 0.002, n_stocks)
    base_vol = rng.lognormal(9, 0.8, n_stocks)
    shape = 1.5 + np.cos(np.linspace(0, 2 * np.pi, B))          # U-shaped intraday volume
    O = np.empty((n_days, B, n_stocks), np.float32)
    C, V, W = np.empty_like(O), np.empty_like(O), np.empty_like(O)
    px = rng.uniform(20, 300, n_stocks)
    for d in range(n_days):
        px = px * np.exp(rng.normal(0, 0.006, n_stocks))         # overnight gap
        eps_prev = np.zeros(n_stocks)
        for b in range(B):
            mkt = rng.normal(0, 0.0006)
            eps = rng.normal(0, 1, n_stocks) * ivol
            r = mkt + eps - reversal * eps_prev
            eps_prev = eps
            o = px
            c = o * np.exp(r)
            O[d, b], C[d, b] = o, c
            W[d, b] = (o + c) / 2
            V[d, b] = base_vol * shape[b] * np.exp(rng.normal(0, 0.4, n_stocks)) * (1 + 50 * np.abs(eps))
            px = c * np.exp(rng.normal(0, ivol * 0.1))           # tiny gap to the next bar's open
    return DayBars(days, [f"S{i:03d}" for i in range(n_stocks)], O, C, V, W, bar_minutes)
