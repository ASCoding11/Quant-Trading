"""The live auction trader builds exactly the book the backtest holds for the same day."""
import numpy as np
import pandas as pd

from qtrade.config import Config
from qtrade.intraday import slice_sim as S
from qtrade.intraday.auction_live import build_book
from qtrade.intraday.synthetic import make_intraday

NY = "America/New_York"


def _frames(bars, d):
    """Today's 5-minute bars and the daily bars (official open / close) as Alpaca would return them."""
    Q0, _, _, qc = S.day_prices(bars)
    five, daily = {}, {}
    for i, t in enumerate(bars.tickers):
        idx = (bars.days[d] + pd.to_timedelta(9 * 60 + 30 + 5 * np.arange(bars.n_bars), unit="min")).tz_localize(NY)
        five[t] = pd.DataFrame({"open": bars.open[d, :, i], "close": bars.close[d, :, i]}, index=idx)
        didx = pd.DatetimeIndex(bars.days[d - 25:d + 1]).tz_localize(NY)
        daily[t] = pd.DataFrame({"open": Q0[d - 25:d + 1, i], "close": qc[d - 25:d + 1, i]}, index=didx)
    return five, daily


def test_live_book_matches_backtest():
    bars = make_intraday(n_stocks=50, n_days=60, seed=8)
    d = 45
    signs = {"last30_fade": 1.0, "overnight_persistence": -1.0}
    acfg = Config().auction
    five, daily = _frames(bars, d)
    book = build_book(five, daily, bars.tickers, signs, acfg, bars.days[d])
    sig = S.signals(bars)
    _, _, _, qc = S.day_prices(bars)
    ok = np.isfinite(qc[d]) & (qc[d] > 0)
    ref = np.zeros(len(bars.tickers))
    for s in acfg.strategies:
        ref += S._weights(signs[s] * sig[s][d], ok & np.isfinite(sig[s][d]), acfg.frac) * acfg.gross / 2
    live = np.array([book["weights"][t] for t in bars.tickers])
    assert np.allclose(live, ref)
    assert np.abs(live).sum() <= acfg.gross + 1e-9               # at most the target gross (strategies can net)
    assert abs(live.sum()) < 1e-9                                 # dollar-neutral


def test_unshortable_names_are_not_shorted():
    bars = make_intraday(n_stocks=50, n_days=60, seed=8)
    five, daily = _frames(bars, 45)
    book = build_book(five, daily, bars.tickers, {}, Config().auction, bars.days[45], shortable=set())
    assert all(w >= 0 for w in book["weights"].values())
