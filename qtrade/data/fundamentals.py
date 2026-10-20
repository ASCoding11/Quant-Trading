"""Company fundamentals from SEC EDGAR's free XBRL "company facts" API.

Every 10-K and 10-Q since about 2009 is tagged in XBRL, and the SEC serves all
of a company's tagged numbers in one JSON file. For each stock in the universe
this module keeps a curated set of line items (revenue, earnings, cash flow,
balance sheet, share count...) as a long table with one row per reported
number:

    ticker, cik, tag, unit, value, start, end, fy, fp, form, filed, accn, frame

``filed`` is the date the filing became public. **Signals must only use rows
with filed <= decision date** - ``point_in_time`` does exactly that - otherwise
the backtest would know earnings before they were announced.

SEC rules for automated access: at most 10 requests per second, and a
User-Agent naming who you are. Set ``SEC_USER_AGENT`` (e.g. "Jane Doe
jane@example.com") if the default is rejected.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import numpy as np
import pandas as pd

from ..utils import LOG
from .loader import to_yahoo

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
DEFAULT_UA = "qtrade-research (github.com/ASCoding11/Quant-Trading)"

# line items kept (us-gaap unless prefixed with dei:)
TAGS = [
    # income statement
    "Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet",
    "CostOfRevenue", "CostOfGoodsAndServicesSold", "GrossProfit", "OperatingIncomeLoss",
    "ResearchAndDevelopmentExpense", "SellingGeneralAndAdministrativeExpense",
    "InterestExpense", "IncomeTaxExpenseBenefit", "NetIncomeLoss",
    "EarningsPerShareBasic", "EarningsPerShareDiluted",
    "WeightedAverageNumberOfDilutedSharesOutstanding",
    # cash flow
    "NetCashProvidedByUsedInOperatingActivities", "PaymentsToAcquirePropertyPlantAndEquipment",
    "PaymentsForRepurchaseOfCommonStock", "PaymentsOfDividends", "PaymentsOfDividendsCommonStock",
    "DepreciationDepletionAndAmortization", "ShareBasedCompensation",
    # balance sheet
    "Assets", "AssetsCurrent", "Liabilities", "LiabilitiesCurrent", "StockholdersEquity",
    "CashAndCashEquivalentsAtCarryingValue", "AccountsReceivableNetCurrent", "InventoryNet",
    "LongTermDebt", "LongTermDebtNoncurrent", "RetainedEarningsAccumulatedDeficit", "Goodwill",
    "CommonStockSharesOutstanding",
    # per-share and share counts from the cover page
    "dei:EntityCommonStockSharesOutstanding", "dei:EntityPublicFloat",
]


class SecClient:
    def __init__(self, user_agent: str | None = None, per_second: float = 8.0, session=None):
        import requests

        self.session = session or requests.Session()
        self.session.headers.update({"User-Agent": user_agent or os.environ.get("SEC_USER_AGENT") or DEFAULT_UA,
                                     "Accept-Encoding": "gzip, deflate"})
        self.min_gap = 1.0 / per_second
        self._last = 0.0
        self.calls = 0

    def get_json(self, url: str):
        for attempt in range(6):
            wait = self.min_gap - (time.monotonic() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()
            r = self.session.get(url, timeout=60)
            self.calls += 1
            if r.status_code == 200:
                return r.json()
            if r.status_code == 404:
                return None
            if r.status_code == 403:
                raise SystemExit(
                    "SEC refused the request (403). SEC requires a User-Agent with a name and email: "
                    "set the SEC_USER_AGENT environment variable (repository variable in GitHub), "
                    "e.g. 'Your Name you@example.com'.")
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(min(60, 2 ** attempt))
                continue
            raise RuntimeError(f"SEC error {r.status_code} for {url}")
        raise RuntimeError(f"SEC: too many retries for {url}")


def ticker_to_cik(client: SecClient) -> dict[str, int]:
    data = client.get_json(TICKERS_URL)
    return {to_yahoo(v["ticker"]): int(v["cik_str"]) for v in data.values()}


def parse_facts(facts: dict, ticker: str, tags: list[str] = TAGS, cik: int | None = None) -> pd.DataFrame:
    rows = []
    cik = int(cik if cik is not None else facts.get("cik") or 0)
    for full in tags:
        tax, tag = full.split(":") if ":" in full else ("us-gaap", full)
        node = facts.get("facts", {}).get(tax, {}).get(tag)
        if not node:
            continue
        for unit, entries in node.get("units", {}).items():
            for e in entries:
                rows.append({"ticker": ticker, "cik": cik, "tag": full, "unit": unit, "value": e.get("val"),
                             "start": e.get("start"), "end": e.get("end"), "fy": e.get("fy"),
                             "fp": e.get("fp"), "form": e.get("form"), "filed": e.get("filed"),
                             "accn": e.get("accn"), "frame": e.get("frame")})
    df = pd.DataFrame(rows)
    if len(df):
        # SEC files are not perfectly consistent (numbers sometimes arrive as
        # text), so fix every column's type before saving to parquet
        for c in ("start", "end", "filed"):
            df[c] = pd.to_datetime(df[c], errors="coerce")
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df["cik"] = df["cik"].astype("int64")
        df["fy"] = pd.to_numeric(df["fy"], errors="coerce").astype("Int64")
        for c in ("ticker", "tag", "unit", "fp", "form", "accn", "frame"):
            df[c] = df[c].astype("string")
    return df


def download_fundamentals(tickers: list[str], store_dir: str | Path,
                          client: SecClient | None = None) -> pd.DataFrame:
    client = client or SecClient()
    store_dir = Path(store_dir)
    store_dir.mkdir(parents=True, exist_ok=True)
    ciks = ticker_to_cik(client)
    frames, rows = [], []
    for k, t in enumerate(tickers):
        cik = ciks.get(to_yahoo(t))
        if cik is None:
            rows.append({"ticker": t, "cik": None, "facts": 0, "first_filed": None, "last_filed": None})
            continue
        facts = client.get_json(FACTS_URL.format(cik=cik))
        df = parse_facts(facts, t, cik=cik) if facts else pd.DataFrame()
        if len(df):
            frames.append(df)
        rows.append({"ticker": t, "cik": cik, "facts": len(df),
                     "first_filed": str(df["filed"].min().date()) if len(df) else None,
                     "last_filed": str(df["filed"].max().date()) if len(df) else None})
        if (k + 1) % 100 == 0:
            LOG.info("fundamentals: %d/%d companies", k + 1, len(tickers))
    allf = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    allf.to_parquet(store_dir / "fundamentals.parquet")
    man = pd.DataFrame(rows)
    (store_dir / "manifest.json").write_text(json.dumps({
        "dataset": "fundamentals", "source": "SEC EDGAR XBRL company facts",
        "companies_requested": len(tickers), "companies_with_data": int((man["facts"] > 0).sum()),
        "total_facts": int(man["facts"].sum()), "tags": len(TAGS),
        "first_filed": min((x for x in man["first_filed"] if isinstance(x, str)), default=None),
        "last_filed": max((x for x in man["last_filed"] if isinstance(x, str)), default=None),
        "complete": True, "api_calls": client.calls,
        "updated": pd.Timestamp.now(tz="UTC").isoformat(),
    }, indent=2))
    man.to_csv(store_dir / "manifest.csv", index=False)
    LOG.info("fundamentals: %d companies, %d facts", (man["facts"] > 0).sum(), man["facts"].sum())
    return man


def load_fundamentals(store_dir: str | Path) -> pd.DataFrame:
    return pd.read_parquet(Path(store_dir) / "fundamentals.parquet")


def point_in_time(facts: pd.DataFrame, tag: str, dates: pd.DatetimeIndex, tickers: list[str],
                  annual: bool = False) -> pd.DataFrame:
    """Latest value of ``tag`` *publicly known* on each date (filed <= date).

    Duration items (revenue, income) use quarterly values (about 90-day
    periods) unless ``annual``; instant items (assets, cash) use the latest
    balance-sheet date. Restatements are handled naturally: a later filing
    replaces the earlier figure only from its own filing date onward.
    """
    f = facts[(facts["tag"] == tag) & facts["filed"].notna() & facts["end"].notna()].copy()
    if f["start"].notna().any():
        days = (f["end"] - f["start"]).dt.days
        f = f[(days > 300) & (days < 400)] if annual else f[(days > 70) & (days < 110) | f["start"].isna()]
    f = f.sort_values(["ticker", "filed", "end"])
    out = pd.DataFrame(np.nan, index=dates, columns=tickers)
    for t, g in f.groupby("ticker"):
        if t not in out.columns:
            continue
        # for each filing date, the value for the most recent period known by then
        g = g.sort_values(["filed", "end"]).groupby("filed").tail(1)
        g = g.assign(max_end=g["end"].cummax())
        g = g[g["end"] >= g["max_end"]]
        s = pd.Series(g["value"].to_numpy(), index=g["filed"].to_numpy())
        s = s[~s.index.duplicated(keep="last")]
        out[t] = s.reindex(dates, method="ffill")
    return out
