"""Consumer earnings study: release timing, outcomes and point-in-time features."""
import numpy as np
import pandas as pd

from qtrade.data.consumer import _earnings_rows, is_consumer
from qtrade.data import make_market
from qtrade.research import consumer_earnings as C

NY = "America/New_York"


def test_sec_parsing_and_consumer_codes():
    block = {"form": ["8-K", "10-Q", "8-K"], "items": ["2.02,9.01", "", "5.02"],
             "acceptanceDateTime": ["2020-05-05T16:05:00.000Z", "2020-05-06T10:00:00.000Z", "2020-06-01T12:00:00.000Z"],
             "filingDate": ["2020-05-05", "2020-05-06", "2020-06-01"]}
    rows = _earnings_rows("ABC", block)
    assert len(rows) == 1 and rows[0]["items"] == "2.02,9.01"
    assert is_consumer(5812) and is_consumer("5311") and not is_consumer(3674) and not is_consumer(None)


def _setup():
    md, _ = make_market(n_stocks=20, n_days=1500, seed=2, start="2015-01-02")
    t = md.tickers[3]
    d = md.dates[700]
    events = pd.DataFrame({"ticker": [t, t, t],
                           "accepted": [pd.Timestamp(d.date()).tz_localize(NY) + pd.Timedelta(hours=16, minutes=5),
                                        pd.Timestamp(md.dates[760].date()).tz_localize(NY) + pd.Timedelta(hours=7),
                                        pd.Timestamp(md.dates[800].date()).tz_localize(NY) + pd.Timedelta(hours=12)],
                           "session": ["after_close", "before_open", "during"]})
    profiles = pd.DataFrame({"ticker": [t], "consumer": [True]})
    return md, events, profiles


def test_entry_is_the_last_close_before_the_release():
    md, events, profiles = _setup()
    ev = C.build_events(md, events, profiles)
    assert len(ev) == 2                                    # the mid-session release is left out
    assert ev.loc[0, "entry"] == 700 and ev.loc[0, "exit"] == 701        # after the close: MOC that day
    assert ev.loc[1, "entry"] == 759 and ev.loc[1, "exit"] == 760        # before the open: MOC the day before
    out = C.outcomes(md, ev)
    j = ev.loc[0, "col"]
    raw = md.open.iat[701, j] / md.close.iat[700, j] - 1
    assert abs(out.loc[0, "ann_ret"] - raw) < 0.05        # market-relative version of close -> next open


def test_page_views_of_the_entry_day_are_not_used():
    md, events, profiles = _setup()
    ev = C.outcomes(md, C.build_events(md, events, profiles))
    t = ev.loc[0, "ticker"]
    idx = pd.date_range("2015-01-01", md.dates[-1], freq="D")
    views = pd.DataFrame({t: np.full(len(idx), 100.0)}, index=idx)
    base = C.features(md, ev, views, None)
    views.loc[views.index >= md.dates[700], t] = 1e6        # a spike from the entry day on
    after = C.features(md, ev, views, None)
    assert np.isclose(base.loc[0, "wiki_attention"], after.loc[0, "wiki_attention"])
