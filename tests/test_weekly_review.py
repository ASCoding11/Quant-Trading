"""The weekly review: live stats, the fixed verdict rule, reading the sheet logs."""
import numpy as np
import pandas as pd

from qtrade.intraday import weekly_review as W

RULE = {"min_days": 40, "cut_z": -2.0, "halve_z": -1.0}


def _daily(rets, cap=1000.0):
    r = np.asarray(rets, float)
    return pd.DataFrame({"date": pd.bdate_range("2026-01-01", periods=len(r)).strftime("%Y-%m-%d"),
                         "pnl": r * cap, "ret": r})


def test_stats():
    st = W.stats(_daily([0.01, -0.005, 0.002, -0.01]))
    assert st["days"] == 4 and round(st["pnl"], 2) == -3.0
    assert st["hit"] == 0.5 and round(st["max_dd"], 2) == -13.0


def test_verdict_rule():
    rng = np.random.default_rng(0)
    bad = W.stats(_daily(rng.normal(-0.003, 0.01, 120)))       # Sharpe around -5 over 120 days
    assert W.verdict(bad, 1.2, RULE, True)[0] == "cut"
    early = W.stats(_daily(rng.normal(-0.003, 0.01, 20)))
    assert W.verdict(early, 1.2, RULE, True)[0] == "too early"
    ok = W.stats(_daily(rng.normal(0.0008, 0.01, 120)))         # Sharpe around 1.3
    assert W.verdict(ok, 1.2, RULE, True)[0] == "keep"
    assert W.verdict(ok, 1.2, RULE, False)[0] == "off"
    assert W.verdict(ok, None, RULE, True)[0] == "info"


class FakeSheet:
    def __init__(self, tabs):
        self.tabs = tabs

    def get(self, tab, rng):
        return self.tabs.get(tab, [])


def test_review_reads_the_logs():
    tabs = {
        "Momentum flip": [["2026-11-19", 24.5, "SHORT", 1, 1, 1, 2.27, 0.0709, 3210.1, 1],
                          ["2026-11-20", 28.4, "SHORT", 1, 1, 1, 3.23, 0.1005, 3213.33, 1]],
        "Auction book": [["2026-11-19", -4.35, 23.78, 19.43, 0.6, 3100.0, 1, 1, 1, 9, 3242.09],
                         ["2026-11-20", 17.43, 34.97, 52.4, 1.7, 3152.4, 1, 1, 1, 9, 3242.09]],
        "Foreign book": [["2026-11-20", 2.97, 0.09, 3244.25, "UK", 60, 1, 3242.09],
                         ["2026-11-20", 2.2, 0.07, 3246.45, "HK", 34, 1, 3242.09]],
        "Foreign HFT tracker": [["2026-11-20", "Japan", "m", "9", "10", "a", "b", 1, 4, -3, -0.5],
                                ["2026-11-20", "Korea", "m", "9", "10", "a", "b", 1, 4, -3, -1.5]],
        "CRM tracker": [["2026-11-20", 0, 0, 10000, 9, "yes"], ["2026-11-23", -110.32, -1.1, 9889.68, 9, "no"]],
    }
    book = {"momentum_flip": 3242.09, "auction": 3242.09, "foreign": 3242.09, "auction_overnight_weight": 0.0}
    cfg = {"rule": RULE, "backtest_sharpe": {"momentum_flip": 0.33, "auction_overnight": 1.2, "adr": 2.91,
                                             "foreign": 1.5, "foreign_hft_tracker": None, "crm_tracker": None}}
    rows = {r[1]: r for r in W.review(FakeSheet(tabs), book, cfg, "2026-11-28")}
    assert rows["momentum_flip"][3] == 2 and rows["momentum_flip"][4] == 5.5
    assert rows["auction_overnight"][10] == "off" and rows["auction_overnight"][4] == 13.08
    assert rows["adr"][4] == 58.75 and rows["adr"][10] == "too early"
    assert rows["foreign"][3] == 1 and rows["foreign"][4] == 5.17
    assert rows["foreign_hft_tracker"][4] == -2.0 and rows["foreign_hft_tracker"][10] == "info"
    assert rows["crm_tracker"][3] == 2 and rows["crm_tracker"][2] == "no"
