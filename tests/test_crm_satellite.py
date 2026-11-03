"""CRM satellite study: the signal never uses satellite days inside the publication lag."""
import numpy as np
import pandas as pd

from qtrade.data import satellite as S
from qtrade.research import crm_satellite as C


def _daily(days, frp):
    return pd.DataFrame({"date": days, "site": "X", "commodity": "copper", "fire_pixels": (frp > 0).astype(int),
                         "frp_mw": frp, "clear_pixels": 100})


def test_signal_ignores_days_inside_the_lag():
    days = pd.date_range("2020-01-01", "2022-12-31", freq="D")
    frp = np.full(len(days), 50.0)
    act = C.activity(_daily(days, frp))
    fridays = pd.date_range("2021-06-04", "2022-12-30", freq="W-FRI")
    base = C.signals(act, fridays)["level (28d FRP vs its trailing year)"]["copper"]
    # a huge spike in the last LAG_DAYS before a Friday must not move that Friday's signal
    f = fridays[-1]
    frp2 = frp.copy()
    frp2[(days > f - pd.Timedelta(days=C.LAG_DAYS)) & (days <= f)] = 1e6
    spiked = C.signals(C.activity(_daily(days, frp2)), fridays)["level (28d FRP vs its trailing year)"]["copper"]
    assert np.isclose(spiked.loc[f], base.loc[f])
    # ... but it shows up once the lag has passed
    ext = pd.date_range("2020-01-01", f + pd.Timedelta(days=21), freq="D")
    frp3 = np.full(len(ext), 50.0)
    frp3[(ext > f - pd.Timedelta(days=C.LAG_DAYS)) & (ext <= f)] = 1e6
    later = pd.date_range("2021-06-04", f + pd.Timedelta(days=21), freq="W-FRI")
    after = C.signals(C.activity(_daily(ext, frp3)), later)["level (28d FRP vs its trailing year)"]["copper"]
    assert after.loc[later[-1]] > base.loc[f] + 1


def test_evaluate_finds_a_planted_relationship():
    fridays = pd.date_range("2012-01-06", "2026-06-26", freq="W-FRI")
    rng = np.random.default_rng(0)
    sig = pd.DataFrame({"copper": rng.normal(size=len(fridays))}, index=fridays)
    ret = pd.DataFrame({"HG=F": -0.01 * np.sign(sig["copper"]) + rng.normal(0, 0.01, len(fridays))}, index=fridays)
    t = C.evaluate(sig, ret).iloc[0]
    assert t["direction"] == "fade activity" and t["sharpe_test"] > 3 and t["corr_test"] < 0


def test_daily_by_site_takes_the_stronger_overpass():
    raw = pd.DataFrame({"date": [pd.Timestamp("2024-01-01")] * 2, "site": "X", "commodity": "nickel",
                        "satellite": ["Terra", "Aqua"], "fire_pixels": [2, 5], "frp_mw": [30.0, 80.0], "clear_pixels": [90, 60]})
    d = S.daily_by_site(raw).iloc[0]
    assert d["fire_pixels"] == 5 and d["frp_mw"] == 80.0
