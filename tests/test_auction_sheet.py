"""Auction sleeve in the sheet: overnight book close -> open, ADR book open -> close, at official prices."""
import numpy as np
import pandas as pd

from qtrade.intraday import auction_sheet as A


def test_settle_day_books_overnight_and_adr_and_opens_tonight():
    prev = pd.DataFrame({"Symbol": ["AAA", "BBB"], "Shares": [10.0, -5.0], "Entry (official close)": [100.0, 50.0],
                         "Position $": [1000.0, -250.0]})
    prev.attrs["date"] = "2026-10-22"
    inputs = {"open": {"AAA": 101.0, "BBB": 49.0, "TM": 200.0}, "close": {"AAA": 102.0, "BBB": 48.0, "TM": 202.0},
              "weights": {"AAA": -0.5, "BBB": 0.5}, "adr_weights": {"TM": 0.25}}
    r = A.settle_day("2026-10-23", inputs, prev, equity=5000.0, deposit=0.0)
    assert np.isclose(r["pnl_overnight"], 10 * 1 + (-5) * (-1))          # +10 long, +5 short
    tm = r["trades"][r["trades"].Book == "ADR"].iloc[0]
    assert np.isclose(tm["Shares"], 0.25 * 5000 / 200) and np.isclose(r["pnl_adr"], 6.25 * 2)
    assert np.isclose(r["equity"], 5000 + 15 + 12.5)
    h = r["holdings"].set_index("Symbol")
    assert np.isclose(h.loc["AAA", "Shares"], round(-0.5 * r["equity"] / 102.0, 4))
    assert h.loc["BBB", "Entry (official close)"] == 48.0


def test_first_day_and_deposit():
    empty = pd.DataFrame(columns=A.HOLD_HEADER)
    inputs = {"open": {"AAA": 10.0}, "close": {"AAA": 10.0}, "weights": {"AAA": 1.0}, "adr_weights": {}}
    r = A.settle_day("2026-10-23", inputs, empty, equity=0.0, deposit=4863.13)
    assert r["pnl_overnight"] == 0 and r["pnl_adr"] == 0 and np.isclose(r["equity"], 4863.13)
    assert np.isclose(r["holdings"]["Position $"].sum(), 4863.13, atol=0.01)
    log = pd.DataFrame([["2026-10-23", 0, 0, 0, 0, 4863.13, 1, 0, 4863.13, 0, 4863.13]], columns=A.LOG_HEADER)
    assert A.capital_so_far(log) == 4863.13


def test_missing_exit_price_closes_flat():
    t = A.round_trips("overnight", {"AAA": 3.0}, {"AAA": 20.0}, {}, "a", "b")
    assert t.iloc[0]["P&L $"] == 0 and t.iloc[0]["Exit price"] == 20.0


def test_adr_book_retries_when_yahoo_has_no_home_bars_yet(monkeypatch):
    import types

    from qtrade.config import Config
    from qtrade.intraday import adr_book, auction_live

    calls = {"n": 0}

    def moves(day, names):
        calls["n"] += 1
        return pd.DataFrame() if calls["n"] < 3 else pd.DataFrame(
            [{"adr": "BABA", "market": "China", "home_ret": 0.02, "fx_ret_prev": 0.0}])

    day = pd.Timestamp("2026-11-03")
    bars = pd.DataFrame({"open": [100.0, 101.0], "close": [100.5, 102.0]},
                        index=pd.DatetimeIndex(["2026-11-02 05:00", "2026-11-03 05:00"], tz="UTC"))
    monkeypatch.setattr(adr_book, "home_moves", moves)
    monkeypatch.setattr(auction_live, "_fetch", lambda *a, **k: {"BABA": bars})
    monkeypatch.setattr(auction_live, "_earnings_reactions", lambda *a, **k: {})
    monkeypatch.setattr(auction_live, "build_book", lambda *a, **k: {"weights": {}, "strategies": []})
    monkeypatch.setattr(auction_live, "_adr_prices", lambda *a, **k: {"BABA": 100.0})
    monkeypatch.setattr(A, "ADR_RETRY_S", 0)
    import qtrade.data.intraday as di
    monkeypatch.setattr(di, "AlpacaBars", lambda **k: types.SimpleNamespace())
    cfg = Config.load("config/auction_paper.yaml")
    out = A.day_inputs(cfg, ["AAPL"], {}, day)
    assert calls["n"] == 3 and out["adr_weights"]           # third try found the home bars
