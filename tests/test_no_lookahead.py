"""The most important test in the repository.

A trading system leaks the future if any value it computes for day D changes
when data *after* D is deleted. These tests compute every signal, the regime
probabilities and the final model forecasts twice - once on the full history
and once on history truncated at D - and require identical values at D.
"""
import numpy as np
import pytest

from qtrade.features.context import FeatureContext
from qtrade.pipeline import build_research
from qtrade.signals import REGISTRY, compute_signals

CUT = 900  # the "today" whose values must not depend on the future


@pytest.fixture(scope="module")
def two_contexts(market, cfg):
    md, _ = market
    full = FeatureContext(md, cfg)
    trunc = FeatureContext(md.subset(end=md.dates[CUT]), cfg)
    return full, trunc


@pytest.mark.parametrize("name", sorted(REGISTRY))
def test_signal_has_no_lookahead(two_contexts, name):
    full, trunc = two_contexts
    a = compute_signals(full, [name])[name].iloc[CUT].to_numpy(dtype=float)
    b = compute_signals(trunc, [name])[name].iloc[CUT].to_numpy(dtype=float)
    assert np.isfinite(a).sum() > 10, f"{name} produced no values"
    np.testing.assert_allclose(a, b, rtol=1e-4, atol=1e-5, equal_nan=True,
                               err_msg=f"signal {name} uses future data")


def test_regimes_and_forecasts_have_no_lookahead(market, cfg):
    md, _ = market
    full = build_research(md, cfg)
    trunc = build_research(md.subset(end=md.dates[CUT]), cfg)
    np.testing.assert_allclose(full.regimes.iloc[CUT].to_numpy(), trunc.regimes.iloc[CUT].to_numpy(),
                               atol=1e-8, err_msg="regime probabilities use future data")
    for model in full.wf.predictions:
        a = full.prediction(model)[CUT]
        b = trunc.prediction(model)[CUT]
        assert np.isfinite(a).sum() > 10
        np.testing.assert_allclose(a, b, rtol=1e-4, atol=1e-5, equal_nan=True,
                                   err_msg=f"model {model} forecast uses future data")


def test_target_is_strictly_future(market, cfg):
    """The training label at row t must start at the *next* day's open."""
    from qtrade.pipeline import forward_returns

    md, _ = market
    f = forward_returns(md, 1)
    t, tk = 500, md.tickers[0]
    expected = md.open[tk].iloc[t + 2] / md.open[tk].iloc[t + 1] - 1
    assert abs(f[tk].iloc[t] - expected) < 1e-12
