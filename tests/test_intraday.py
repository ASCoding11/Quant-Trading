"""Intraday downloader against a fake Alpaca API (no network)."""
import numpy as np
import pandas as pd
import pytest

import qtrade.data.intraday as intr


class FakeResponse:
    def __init__(self, status, payload=None, text=""):
        self.status_code, self._payload, self.text = status, payload, text

    def json(self):
        return self._payload


class FakeAlpaca:
    """Serves 5-minute bars (including pre/after-market) with small pages."""

    def __init__(self, days, symbols, page=50, fail_first=0):
        self.headers = {}
        self.page = page
        self.fail_left = fail_first
        self.requests = []
        rows = []
        for d in days:
            # 04:00-20:00 New York time, like Alpaca's extended-hours SIP bars
            times = pd.date_range(f"{d} 04:00", f"{d} 19:55", freq="5min", tz="America/New_York")
            for s in symbols:
                for i, t in enumerate(times):
                    px = 100 + i * 0.01
                    rows.append((s, t.tz_convert("UTC"), {"t": t.tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ"),
                                                          "o": px, "h": px + 0.1, "l": px - 0.1, "c": px,
                                                          "v": 1000, "n": 10, "vw": px}))
        rows.sort(key=lambda r: (r[0], r[1]))
        self.rows = rows

    def get(self, url, params=None, timeout=None):
        self.requests.append(dict(params))
        if self.fail_left:
            self.fail_left -= 1
            return FakeResponse(429)
        syms = params["symbols"].split(",")
        lo, hi = pd.Timestamp(params["start"]), pd.Timestamp(params["end"])
        sel = [r for r in self.rows if r[0] in syms and lo <= r[1] <= hi]
        off = int(params.get("page_token") or 0)
        chunk = sel[off : off + self.page]
        bars = {}
        for s, _, b in chunk:
            bars.setdefault(s, []).append(b)
        nxt = str(off + self.page) if off + self.page < len(sel) else None
        return FakeResponse(200, {"bars": bars, "next_page_token": nxt})


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(intr.time, "sleep", lambda s: None)


def _client(fake):
    return intr.AlpacaBars("k", "s", session=fake)


def test_paging_and_regular_hours_filter(tmp_path):
    fake = FakeAlpaca(["2024-03-04", "2024-03-05"], ["AAPL", "BRK.B"], page=37)
    m = intr.download(["AAPL", "BRK-B"], tmp_path, "5Min", "2024-03-01", _client(fake))
    assert set(m["ticker"]) == {"AAPL", "BRK-B"}             # share class mapped both ways
    assert (m["rows"] == 2 * 78).all()                        # 78 five-minute bars per regular session
    df = intr.load_symbol(tmp_path, "AAPL")
    assert df.index[0].strftime("%H:%M") == "09:30" and df.index[-1].strftime("%H:%M") == "15:55"
    assert fake.requests[0]["adjustment"] == "all" and len(fake.requests) > 2


def test_retry_on_rate_limit(tmp_path):
    fake = FakeAlpaca(["2024-03-04"], ["MSFT"], fail_first=2)
    m = intr.download(["MSFT"], tmp_path, "5Min", "2024-03-01", _client(fake))
    assert m["rows"].iloc[0] == 78


def test_resume_appends_only_new_bars(tmp_path):
    fake = FakeAlpaca(["2024-03-04", "2024-03-05", "2024-03-06"], ["XOM"])
    client = _client(fake)
    intr.update_symbol(client, tmp_path, "XOM", "5Min", "2024-03-01", "2024-03-05T00:00:00Z")
    assert len(intr.load_symbol(tmp_path, "XOM")) == 78
    added, total = intr.update_symbol(client, tmp_path, "XOM", "5Min", "2024-03-01", "2024-03-07T00:00:00Z")
    assert added == 2 * 78 and total == 3 * 78
    assert pd.Timestamp(fake.requests[-1]["start"]) > pd.Timestamp("2024-03-04T20:00:00Z")
    added, total = intr.update_symbol(client, tmp_path, "XOM", "5Min", "2024-03-01", "2024-03-07T00:00:00Z")
    assert added == 0 and total == 3 * 78
    panel = intr.load_panel(tmp_path)
    assert panel["close"].shape == (3 * 78, 1) and np.isfinite(panel["close"].to_numpy()).all()


def test_rate_limiter_blocks_when_window_full(monkeypatch):
    clock = {"t": 1000.0}
    slept = []
    monkeypatch.setattr(intr.time, "monotonic", lambda: clock["t"])
    monkeypatch.setattr(intr.time, "sleep", lambda s: (slept.append(s), clock.__setitem__("t", clock["t"] + s)))
    lim = intr.RateLimiter(per_minute=3)
    for _ in range(4):
        lim.wait()
    assert len(slept) == 1 and 59 < slept[0] <= 61
