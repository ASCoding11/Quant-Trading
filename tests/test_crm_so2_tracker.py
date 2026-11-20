"""Sentinel-5P SO2 collector, the SO2 signal's publication lag, and the $0 CRM tracker's bookkeeping."""
import numpy as np
import pandas as pd

from qtrade.data import sentinel5p as S5
from qtrade.data.satellite import Site
from qtrade.intraday import crm_sheet as T
from qtrade.research import crm_satellite as C

SITE = Site("X", "copper", 10.0, 20.0)


def _grid(step_km=5.0, n=81):
    k = (np.arange(n) - n // 2) * step_km / 111.0
    lat, lon = np.meshgrid(SITE.lat + k, SITE.lon + k / np.cos(np.radians(SITE.lat)), indexing="ij")
    return lat, lon


def test_site_stats_plume_minus_ring_and_quality_filter():
    lat, lon = _grid()
    d = S5.distance_km(lat, lon, SITE)
    so2 = np.where(d <= 25, 0.001, 0.0002)            # mol/m2
    qa = np.full(so2.shape, 80, dtype=np.uint8)
    qa[d <= 10] = 20                                   # bad pixels near the plant are ignored
    so2[d <= 10] = 1.0
    st = S5.site_stats(lat, lon, so2, qa, SITE)
    assert st["n_plume"] > 0 and st["n_ring"] > 0
    assert np.isclose(st["so2_enh_du"], (0.001 - 0.0002) * S5.MOL_M2_TO_DU)
    far = Site("far", "copper", 50.0, 20.0)
    assert S5.site_stats(lat, lon, so2, qa, far) is None


def test_fill_values_are_dropped():
    lat, lon = _grid()
    so2 = np.full(lat.shape, 9.96921e36, dtype=np.float32)
    st = S5.site_stats(lat, lon, so2, np.full(lat.shape, 90), SITE)
    assert st["n_plume"] == 0 and np.isnan(st["so2_enh_du"])


def test_best_items_prefers_offline_over_near_real_time():
    it = lambda i, orbit, mode: {"id": i, "properties": {"sat:absolute_orbit": orbit, "s5p:processing_mode": mode}}
    items = [it("a", 1, "NRTI"), it("b", 1, "OFFL"), it("c", 2, "NRTI"), it("d", 2, "NRTI"), it("e", 3, "RPRO"),
             it("f", 3, "OFFL")]
    assert sorted(i["id"] for i in S5.best_items(items)) == ["b", "c", "d", "e"]


def test_daily_by_site_weights_overpasses_by_pixels():
    raw = pd.DataFrame({"date": [pd.Timestamp("2024-01-01")] * 2, "site": "X", "commodity": "copper",
                        "n_plume": [10, 30], "so2_enh_du": [1.0, 3.0]})
    assert np.isclose(S5.daily_by_site(raw)["so2_enh_du"].iloc[0], 2.5)


def _so2_daily(days, v):
    return pd.DataFrame({"date": days, "site": "X", "commodity": "copper", "n_plume": 10, "so2_enh_du": v})


def test_so2_signal_ignores_days_inside_the_lag():
    days = pd.date_range("2019-01-01", "2021-12-31", freq="D")
    v = np.full(len(days), 0.5)
    fridays = pd.date_range("2020-06-05", "2021-12-31", freq="W-FRI")
    f = fridays[-1]
    base = C.so2_signals(C.so2_activity(_so2_daily(days, v)), fridays)[C.LEVEL_S5P]["copper"]
    v2 = v.copy()
    v2[(days > f - pd.Timedelta(days=C.LAG_DAYS_S5P)) & (days <= f)] = 1e6
    spiked = C.so2_signals(C.so2_activity(_so2_daily(days, v2)), fridays)[C.LEVEL_S5P]["copper"]
    assert np.isclose(spiked.loc[f], base.loc[f])


def test_mark_and_legs():
    rules = [{"source": "SO2", "commodity": "copper", "instrument": "HG=F", "direction": -1},
             {"source": "MODIS", "commodity": "copper", "instrument": "HG=F", "direction": 1},
             {"source": "SO2", "commodity": "nickel", "instrument": "PICK", "direction": 1}]
    tgt = T.legs(rules, {("SO2", "copper"): 0.3, ("MODIS", "copper"): -2.0})
    assert [t["position"] for t in tgt] == [-1, -1, 0]
    close = pd.Series({"HG=F": 5.0, "PICK": 40.0})
    pos = T.open_legs(tgt, close, 9_000.0, "2026-11-20")
    assert len(pos) == 2 and np.allclose(pos["Notional $"], 3_000.0)
    marked, pnl = T.mark(pos, pd.Series({"HG=F": 5.5, "PICK": 41.0}))
    assert np.isclose(pnl, 2 * -3_000.0 * 0.1) and np.allclose(marked["Mark price"], 5.5)
    marked2, pnl2 = T.mark(marked, pd.Series({"PICK": 41.0}))      # missing price: no P&L, mark unchanged
    assert pnl2 == 0.0 and np.allclose(marked2["Mark price"], 5.5)


def test_due_rebalance():
    empty = pd.DataFrame(columns=T.POS_HEADER)
    some = pd.DataFrame([["SO2"] + [0] * 10], columns=T.POS_HEADER)
    assert T.due_rebalance(pd.Timestamp("2026-11-18"), empty, "2026-11-13")
    assert T.due_rebalance(pd.Timestamp("2026-11-20"), some, "2026-11-13")          # Friday
    assert not T.due_rebalance(pd.Timestamp("2026-11-18"), some, "2026-11-13")      # Wednesday, 5 days on
    assert T.due_rebalance(pd.Timestamp("2026-11-23"), some, "2026-11-13")          # Friday was a holiday


def _fake_child(conn, it, ss):
    import time as _t
    if it["id"] == "hang":
        _t.sleep(60)
    elif it["id"] == "bad":
        conn.send(("err", "filter returned failure"))
    else:
        conn.send(("ok", [(it["id"], 1)]))
    conn.close()


def test_run_isolated_kills_hung_reads():
    import time as _t

    from qtrade.data import sentinel5p as S5

    jobs = [({"id": i}, []) for i in ("a", "hang", "bad", "b")]
    t = _t.time()
    seen, stats = [], {}
    out = list(S5.run_isolated(jobs, workers=4, timeout_s=2, target=_fake_child,
                               before_fork=lambda it: seen.append(it["id"]), stats=stats))
    assert _t.time() - t < 20
    assert len(out) == 4
    assert sorted(r for rows in out for r in rows) == [("a", 1), ("b", 1)]
    assert seen == ["a", "hang", "bad", "b"] and stats["failed"] == 2


def test_month_with_many_failures_is_not_cached(tmp_path, monkeypatch):
    import pandas as pd

    from qtrade.data import sentinel5p as S5

    def fake_collect(a, b):
        df = pd.DataFrame([[pd.Timestamp(a)] + [None] * (len(S5.COLS) - 1)], columns=S5.COLS)
        df.attrs["failed_share"] = 0.6 if a.startswith("2021-05") else 0.0
        return df

    monkeypatch.setattr(S5, "collect", fake_collect)
    out = S5.collect_cached("2021-05-01", "2021-06-30", tmp_path)
    assert len(out) == 2
    assert not (tmp_path / "s5p_2021-05.parquet").exists()
    assert (tmp_path / "s5p_2021-06.parquet").exists()
