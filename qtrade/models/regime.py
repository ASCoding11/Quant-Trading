"""Walk-forward market-regime probabilities from the Gaussian HMM.

At each refit date R the HMM is re-estimated on all market-state data up to R
(expanding window, warm-started from the previous fit). Filtered probabilities
for the days after R - until the next refit - come from that model's forward
recursion, which only ever looks backwards. Before the first fit every regime
gets equal probability.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..utils import LOG
from .hmm import GaussianHMM


def walk_forward_regimes(
    state: pd.DataFrame,
    n_states: int = 3,
    refit_every: int = 252,
    min_history: int = 756,
    n_init: int = 5,
    max_iter: int = 200,
    seed: int = 0,
    vol_column: str = "log_rvol",
) -> tuple[pd.DataFrame, list[tuple[pd.Timestamp, GaussianHMM]]]:
    X_all = state.to_numpy(dtype=float)
    T = len(X_all)
    probs = np.full((T, n_states), 1.0 / n_states)
    valid = np.isfinite(X_all).all(axis=1)
    first = int(np.argmax(valid)) if valid.any() else T
    sort_col = list(state.columns).index(vol_column) if vol_column in state.columns else None

    fits: list[tuple[pd.Timestamp, GaussianHMM]] = []
    prev: GaussianHMM | None = None
    refits = list(range(first + min_history, T, refit_every))
    for i, r in enumerate(refits):
        train = X_all[first : r + 1]
        # standardise with training statistics only
        mu = np.nanmean(train, axis=0)
        sd = np.nanstd(train, axis=0) + 1e-12
        hmm = GaussianHMM(n_states, n_init=n_init if prev is None else 2,
                          max_iter=max_iter, seed=seed + i)
        hmm.fit((train - mu) / sd, warm=prev, sort_by=sort_col)
        hmm.mu_, hmm.sd_ = mu, sd
        end = refits[i + 1] if i + 1 < len(refits) else T - 1
        # filter from the start of history through the end of this block
        alpha = hmm.filter((X_all[first : end + 1] - mu) / sd)
        probs[r + 1 : end + 1] = alpha[r + 1 - first :]
        if i == 0:
            probs[r] = alpha[r - first]
        prev = hmm
        fits.append((state.index[r], hmm))
    LOG.info("regime HMM: %d walk-forward fits, %d states", len(fits), n_states)
    cols = [f"regime_{k}" for k in range(n_states)]
    return pd.DataFrame(probs, index=state.index, columns=cols), fits


def latest_regime_model(fits):
    return fits[-1][1] if fits else None
