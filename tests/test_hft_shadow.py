"""The shadow HFT state machine: taker entries and exits, maker fills only when a trade prints through."""
import numpy as np
import pandas as pd

from qtrade.intraday import hft_shadow as S

T0 = pd.Timestamp("2026-10-22 15:00:00", tz="UTC")


def at(s):
    return T0 + pd.Timedelta(seconds=s)


def test_imbalance_taker_crosses_in_and_out():
    h = S.ShadowHFT(["AAA"])
    h.on_quote("AAA", at(0), 100.00, 900, 100.02, 100)        # far more bid than offered: buy at the ask
    h.step(at(0))
    h.on_quote("AAA", at(29), 100.10, 500, 100.12, 500)
    h.step(at(29))
    assert h.take_closed().empty                               # not yet 30 s
    h.step(at(30))
    t = h.take_closed()
    taker = t[t.strategy == "imbalance_taker"].iloc[0]
    assert taker.side == "buy" and taker.entry_price == 100.02 and taker.exit_price == 100.10
    assert np.isclose(taker.pnl_bp, (100.10 / 100.02 - 1) * 1e4 - S.FEE_BP)


def test_maker_fills_instantly_at_its_price():
    h = S.ShadowHFT(["AAA"])
    h.on_quote("AAA", at(0), 50.00, 300, 50.02, 300)           # balanced: no taker, maker on both sides
    h.step(at(0))
    h.on_trade("AAA", at(2), 50.01, 100)                       # above the bid: no fill
    h.on_trade("AAA", at(3), 50.00, 100)                       # at the bid: instant fill at 50.00
    h.on_trade("AAA", at(12), 50.05, 100)                      # after the ask order expired: no fill
    h.on_quote("AAA", at(33), 50.01, 300, 50.03, 300)
    h.step(at(33))
    t = h.take_closed()
    mm = t[t.strategy == "market_maker"]
    assert len(mm) == 1 and mm.iloc[0].side == "buy" and mm.iloc[0].entry_price == 50.00
    assert mm.iloc[0].exit_price == 50.01                      # sells at the bid 30 s after the fill
    assert (t.strategy == "maker_with_signal").sum() == 0      # imbalance 0: the signal quotes neither side
    s = S.summary(t)
    assert set(s["strategy"]) == {"market_maker"}
