"""News and fundamentals downloaders against fake APIs (no network)."""
import pandas as pd
import pytest

import qtrade.data.fundamentals as fund
import qtrade.data.intraday as intr
import qtrade.data.news as news


class Resp:
    def __init__(self, status, payload=None):
        self.status_code, self._p, self.text = status, payload, ""

    def json(self):
        return self._p


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(intr.time, "sleep", lambda s: None)
    monkeypatch.setattr(fund.time, "sleep", lambda s: None)


class FakeNews:
    def __init__(self):
        self.headers = {}
        self.starts = []
        self.items = []
        for i, day in enumerate(pd.date_range("2024-01-03", "2024-03-20", freq="5D")):
            self.items.append({"id": i, "created_at": f"{day.date()}T14:00:00Z", "updated_at": f"{day.date()}T14:00:00Z",
                               "headline": f"News {i}", "summary": "", "author": "a", "source": "benzinga",
                               "url": "u", "symbols": ["AAPL", "BRK.B"] if i % 2 else ["MSFT"]})

    def get(self, url, params=None, timeout=None):
        assert url == news.NEWS_URL and params["limit"] <= 50
        self.starts.append(params["start"])
        syms = set(params["symbols"].split(","))
        lo, hi = pd.Timestamp(params["start"]), pd.Timestamp(params["end"])
        sel = [a for a in self.items if syms & set(a["symbols"]) and lo <= pd.Timestamp(a["created_at"]) <= hi]
        off = int(params.get("page_token") or 0)
        page = sel[off : off + 2]
        return Resp(200, {"news": page, "next_page_token": str(off + 2) if off + 2 < len(sel) else None})


def test_news_months_paging_dedupe_and_resume(tmp_path, monkeypatch):
    fake = FakeNews()
    client = intr.AlpacaBars("k", "s", session=fake)
    monkeypatch.setattr(news.pd.Timestamp, "now", classmethod(lambda cls, tz=None: pd.Timestamp("2024-03-31", tz="UTC")))
    m = news.download_news(["AAPL", "MSFT", "BRK-B"], tmp_path, "2024-01-01", client)
    assert list(m["month"]) == ["2024-01", "2024-02", "2024-03"]
    assert m["articles"].sum() == len(fake.items)                   # every article exactly once
    df = news.load_news(tmp_path)
    assert "BRK-B" in ",".join(df["symbols"])                       # share class mapped back
    counts = news.article_counts(df)
    assert counts.to_numpy().sum() == sum(len(a["symbols"]) for a in fake.items)
    fake.starts.clear()
    news.download_news(["AAPL", "MSFT", "BRK-B"], tmp_path, "2024-01-01", client)
    months = {s[:7] for s in fake.starts}
    assert months == {"2024-02", "2024-03"}                          # only the last two months re-fetched


class FakeSec:
    def __init__(self):
        self.headers = {}

    def get(self, url, timeout=None):
        if url == fund.TICKERS_URL:
            return Resp(200, {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple"},
                              "1": {"cik_str": 789019, "ticker": "MSFT", "title": "Microsoft"}})
        if "CIK0000789019" in url:   # SEC sometimes sends numbers as text
            e = [{"end": "2023-09-30", "val": "5", "fy": "2023", "fp": "FY", "form": "10-K", "filed": "2023-10-30",
                  "accn": "b1"}]
            return Resp(200, {"cik": "789019", "facts": {"us-gaap": {"Assets": {"units": {"USD": e}}}}})
        if "CIK0000320193" in url:
            q = [{"start": "2023-07-02", "end": "2023-09-30", "val": 100, "fy": 2023, "fp": "FY", "form": "10-K",
                  "filed": "2023-11-03", "accn": "a1"},
                 {"start": "2023-10-01", "end": "2023-12-30", "val": 120, "fy": 2024, "fp": "Q1", "form": "10-Q",
                  "filed": "2024-02-02", "accn": "a2"},
                 {"start": "2022-10-01", "end": "2023-09-30", "val": 400, "fy": 2023, "fp": "FY", "form": "10-K",
                  "filed": "2023-11-03", "accn": "a1"}]
            return Resp(200, {"cik": 320193, "facts": {"us-gaap": {"NetIncomeLoss": {"units": {"USD": q}}},
                                                       "dei": {}}})
        return Resp(404)


def test_fundamentals_point_in_time(tmp_path):
    client = fund.SecClient(session=FakeSec())
    man = fund.download_fundamentals(["AAPL", "MSFT", "ZZZZ"], tmp_path, client)
    assert man.set_index("ticker").loc["AAPL", "facts"] == 3 and man.set_index("ticker").loc["ZZZZ", "facts"] == 0
    facts = fund.load_fundamentals(tmp_path)
    dates = pd.to_datetime(["2023-11-01", "2023-11-03", "2024-01-15", "2024-02-02"])
    q = fund.point_in_time(facts, "NetIncomeLoss", dates, ["AAPL"])["AAPL"]
    assert pd.isna(q.iloc[0])                 # not filed yet: no look-ahead
    assert q.iloc[1] == 100 and q.iloc[2] == 100 and q.iloc[3] == 120
    a = fund.point_in_time(facts, "NetIncomeLoss", dates, ["AAPL"], annual=True)["AAPL"]
    assert a.iloc[1] == 400


def test_sec_403_explains_user_agent():
    class Deny:
        headers = {}

        def get(self, url, timeout=None):
            return Resp(403)

    with pytest.raises(SystemExit, match="SEC_USER_AGENT"):
        fund.SecClient(session=Deny()).get_json(fund.TICKERS_URL)
