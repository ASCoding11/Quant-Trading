"""The shadow HFT simulation: orders execute after the latency at the book prevailing then."""
import numpy as np
import pandas as pd

from qtrade.intraday import hft_shadow as S

T0 = pd.Timestamp("2026-10-22 15:00:00", tz="UTC")


def at(s, ms=0):
    return T0 + pd.Timedelta(seconds=s) + pd.Timedelta(milliseconds=ms)


def test_taker_fills_at_the_quote_after_the_latency():
    h = S.ShadowHFT(["AAA"], latency_ms=5, jitter_ms=0)
    h.on_quote("AAA", at(0), 100.00, 900, 100.02, 100)        # lopsided book: decide to buy at t=0
    h.on_quote("AAA", at(0, 3), 100.01, 900, 100.03, 100)     # 3 ms later the ask moved up ...
    h.on_quote("AAA", at(0, 9), 100.02, 900, 100.05, 100)     # ... the order arrived at 5 ms: pays 100.03
    h.on_quote("AAA", at(30, 2), 100.10, 500, 100.12, 500)    # exit decided at 30.005, quote at 30.002 stands
    h.on_quote("AAA", at(30, 20), 100.20, 500, 100.22, 500)
    h.step(at(31))
    t = h.take_closed()
    tk = t[t.strategy == "imbalance_taker"].iloc[0]
    assert tk.entry_price == 100.03 and tk.exit_price == 100.10
    assert np.isclose(tk.latency_ms, 5.0)
    assert np.isclose(tk.pnl_bp, (100.10 / 100.03 - 1) * 1e4)


def test_maker_orders_go_live_after_the_latency():
    h = S.ShadowHFT(["AAA"], latency_ms=5, jitter_ms=0)
    h.on_quote("AAA", at(0), 50.00, 300, 50.02, 300)           # balanced book: no taker
    h.step(at(1))                                              # maker orders decided at 1.000, live at 1.005
    h.on_trade("AAA", at(1, 2), 50.00, 100)                    # before ours arrived: no fill
    h.on_trade("AAA", at(1, 8), 50.00, 100)                    # after: our bid fills at 50.00
    h.on_quote("AAA", at(31, 10), 50.01, 300, 50.03, 300)     # exit sent at 31.008, arrives 31.013
    h.step(at(32))
    t = h.take_closed()
    mm = t[t.strategy == "market_maker"]
    assert len(mm) == 1 and mm.iloc[0].side == "buy" and mm.iloc[0].entry_price == 50.00
    assert mm.iloc[0].exit_price == 50.01
    assert (t.strategy == "maker_with_signal").sum() == 0
    assert set(S.summary(t)["strategy"]) == {"market_maker"}


def test_jitter_is_a_few_milliseconds():
    h = S.ShadowHFT(["AAA"], seed=3)
    d = [h._delay().total_seconds() * 1e3 for _ in range(200)]
    assert min(d) >= S.LATENCY_MS and max(d) <= S.LATENCY_MS + S.JITTER_MS


def test_sheet_rows_and_summary():
    t = pd.DataFrame([{"strategy": "market_maker", "symbol": "AAA", "side": "buy", "decision_time": at(0),
                       "entry_time": at(0, 5), "entry_price": 50.0, "exit_time": at(30, 6), "exit_price": 50.01,
                       "pnl_bp": 2.0, "pnl_mid_bp": 3.0, "spread_bp": 4.0, "imbalance": 0.1, "latency_ms": 5.5}])
    rows = S.SheetWriter._rows(t)
    assert rows[0][3].endswith(".005") and rows[0][-1] == 5.5
    s = S._summary_rows(t)
    assert s[0][0] == "Strategy" and s[1][:2] == ["market_maker", 1]
