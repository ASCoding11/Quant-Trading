"""Intraday strategy: no look-ahead, flat every night, and sane accounting."""
import copy

import numpy as np
import pytest

from qtrade.config import Config
from qtrade.intraday.features import day_features, history
from qtrade.intraday.strategy import ic_for_sizing, prepare, run_backtest, target_weights
from qtrade.intraday.synthetic import make_intraday


@pytest.fixture(scope="module")
def setup():
    bars = make_intraday(n_stocks=50, n_days=90, seed=2)
    cfg = Config()
    icfg = cfg.intraday
    icfg.train_months, icfg.min_train_months = 2, 1
    hist, pred, log, final, daily_ic = prepare(bars, icfg)
    return bars, icfg, hist, pred, daily_ic


def test_features_never_see_later_bars(setup):
    bars, icfg, hist, _, _ = setup
    d, b = 40, 30
    args = [bars.open[d], bars.close[d], bars.volume[d], bars.vwap[d], hist.prev_close[d], hist.sigma[d],
            hist.vol_base[d]]
    full = day_features(*args)
    cut = [a.copy() for a in args]
    for a in cut[:4]:
        a[b + 1:] = np.nan if a.dtype.kind == "f" else 0
    cut[2][b + 1:] = 0.0
    np.testing.assert_allclose(day_features(*cut)[: b + 1], full[: b + 1], atol=1e-5)


def test_history_uses_only_earlier_days(setup):
    bars, icfg, hist, _, _ = setup
    d = 50
    later = bars.subset_days(slice(0, d + 1))
    later.close = later.close.copy()
    later.close[d] *= 1.5                    # change today's prices: today's baselines must not move
    h2 = history(later, icfg.vol_days)
    np.testing.assert_allclose(h2.sigma[d], hist.sigma[d], rtol=1e-5)
    np.testing.assert_allclose(h2.vol_base[d], hist.vol_base[d], rtol=1e-5)


def test_planted_reversal_is_found_and_flat_forecast_is_flat(setup):
    bars, icfg, hist, pred, daily_ic = setup
    assert np.nanmean(daily_ic) > 0.05
    ic = ic_for_sizing(daily_ic)
    zero = np.where(np.isfinite(pred), 0.0, np.nan)
    flat = run_backtest(bars, hist, zero, icfg, ic)
    assert np.abs(flat["ret"]).max() < 1e-12 and flat["turnover"].max() == 0
    bt = run_backtest(bars, hist, pred, icfg, ic, frictionless=True)
    assert bt["ret"].mean() > 0


def test_trading_less_often_trades_less(setup):
    bars, icfg, hist, pred, daily_ic = setup
    ic = ic_for_sizing(daily_ic)
    slow = copy.deepcopy(icfg)
    slow.rebalance_every = 6
    fast_t = run_backtest(bars, hist, pred, icfg, ic)["turnover"].mean()
    slow_t = run_backtest(bars, hist, pred, slow, ic)["turnover"].mean()
    assert slow_t < fast_t


def test_target_is_dollar_neutral_and_capped():
    icfg = Config().intraday
    rng = np.random.default_rng(0)
    n = 200
    w = target_weights(rng.standard_normal(n), rng.uniform(0.001, 0.003, n), np.full(n, 5e8), np.zeros(n),
                       icfg, ic=0.05)
    icfg0 = copy.deepcopy(icfg)
    icfg0.cost_aversion = 0.0
    w0 = target_weights(rng.standard_normal(n), rng.uniform(0.001, 0.003, n), np.full(n, 5e8), np.zeros(n),
                        icfg0, ic=0.05)
    assert abs(w0.sum()) < 1e-9 and abs(np.abs(w0).sum() - icfg.gross) < 1e-9
    assert (w0 != 0).sum() == 2 * icfg.n_side
    assert np.abs(w).sum() <= icfg.gross + 1e-9


def _frames(bars, days):
    import pandas as pd

    out = {}
    for i, t in enumerate(bars.tickers):
        parts = []
        for d in days:
            idx = (bars.days[d] + pd.to_timedelta(9 * 60 + 30 + 5 * np.arange(bars.n_bars), unit="min"))
            parts.append(pd.DataFrame({"open": bars.open[d, :, i], "close": bars.close[d, :, i],
                                       "volume": bars.volume[d, :, i], "vwap": bars.vwap[d, :, i]},
                                      index=idx.tz_localize("America/New_York")))
        out[t] = pd.concat(parts)
    return out


def test_live_forecast_matches_backtest(setup):
    """The live trader rebuilds features from raw bars; it must match the backtest."""
    from qtrade.intraday.live import LiveState, decide
    from qtrade.intraday.strategy import Session

    bars, icfg, hist, _, _ = setup
    d = 60
    coef = np.random.default_rng(1).standard_normal(len(__import__("qtrade.intraday.features",
                                                                   fromlist=["FEATURES"]).FEATURES))
    state = LiveState.__new__(LiveState)
    state.tickers = bars.tickers
    state.hist_frames = _frames(bars, range(d - 30, d))
    state.adv = hist.adv[d]
    live_pred, _, live_sigma = decide(state, _frames(bars, [d]), coef, icfg, bars.days[d])
    X = Session(bars, hist, d).features()
    bt_pred = np.einsum("bnf,f->bn", np.nan_to_num(X), coef)
    bt_pred[~np.isfinite(X[..., 0])] = np.nan
    np.testing.assert_allclose(live_sigma, hist.sigma[d], rtol=1e-4)
    np.testing.assert_allclose(live_pred, bt_pred, rtol=1e-3, atol=1e-3)
