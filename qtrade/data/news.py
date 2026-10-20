"""News headlines from Alpaca's news API (Benzinga feed, back to 2015).

One parquet file per calendar month holds every article that tags at least one
stock in the universe: id, timestamps, headline, summary, source, url and the
tagged symbols. Months already stored are skipped on later runs, except the
two most recent, which are re-fetched to pick up late articles. Article text is
not downloaded (headlines and summaries are what sentiment signals use, and it
keeps the store small).

Point-in-time use: an article is only known from its ``created_at`` time, so
any signal built from it must use ``created_at`` <= decision time.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import pandas as pd

from ..utils import LOG
from .intraday import AlpacaBars
from .loader import to_alpaca, to_yahoo

NEWS_URL = "https://data.alpaca.markets/v1beta1/news"
FIELDS = ["id", "created_at", "updated_at", "headline", "summary", "author", "source", "url", "symbols"]


def fetch_window(client: AlpacaBars, symbols: list[str], start: str, end: str,
                 batch: int = 100) -> list[dict]:
    """Every article between start and end tagging any of ``symbols``."""
    seen: dict[int, dict] = {}
    for i in range(0, len(symbols), batch):
        params = {"symbols": ",".join(to_alpaca(s) for s in symbols[i : i + batch]),
                  "start": start, "end": end, "limit": 50, "sort": "asc", "include_content": "false"}
        while True:
            data = client._get(params, url=NEWS_URL)
            for a in data.get("news") or []:
                seen[a["id"]] = a
            token = data.get("next_page_token")
            if not token:
                break
            params["page_token"] = token
    return list(seen.values())


def articles_to_frame(items: list[dict]) -> pd.DataFrame:
    if not items:
        return pd.DataFrame(columns=FIELDS)
    df = pd.DataFrame(items)
    for c in FIELDS:
        if c not in df:
            df[c] = None
    df = df[FIELDS].copy()
    df["symbols"] = df["symbols"].apply(lambda s: ",".join(to_yahoo(x) for x in (s or [])))
    for c in ("created_at", "updated_at"):
        df[c] = pd.to_datetime(df[c], utc=True)
    df["summary"] = df["summary"].fillna("").astype(str)
    return df.drop_duplicates("id").sort_values("created_at").reset_index(drop=True)


def month_path(store_dir: str | Path, month: pd.Period) -> Path:
    return Path(store_dir) / f"news_{month.strftime('%Y-%m')}.parquet"


def download_news(symbols: list[str], store_dir: str | Path, start: str = "2015-01-01",
                  client: AlpacaBars | None = None, time_budget_min: float | None = None) -> pd.DataFrame:
    """Fetch month by month; returns a manifest of articles per month."""
    client = client or AlpacaBars()
    store_dir = Path(store_dir)
    store_dir.mkdir(parents=True, exist_ok=True)
    now = pd.Timestamp.now(tz="UTC") - pd.Timedelta(minutes=30)
    months = pd.period_range(pd.Timestamp(start), now.tz_localize(None), freq="M")
    refresh = set(months[-2:])
    t0 = time.time()
    complete = True
    for k, m in enumerate(months):
        path = month_path(store_dir, m)
        if path.exists() and m not in refresh:
            continue
        if time_budget_min and (time.time() - t0) / 60 > time_budget_min:
            LOG.warning("time budget reached at %s; re-run to resume", m)
            complete = False
            break
        lo = m.start_time.tz_localize("UTC")
        hi = min(m.end_time.tz_localize("UTC"), now)
        try:
            df = articles_to_frame(fetch_window(client, symbols, lo.isoformat(), hi.isoformat()))
        except RuntimeError as exc:
            LOG.warning("%s: %s", m, exc)
            complete = False
            continue
        df.to_parquet(path)
        LOG.info("[%d/%d] %s: %d articles (%d API calls so far)", k + 1, len(months), m, len(df), client.calls)
    man = news_manifest(store_dir)
    man.attrs["complete"] = complete
    return man


def news_manifest(store_dir: str | Path) -> pd.DataFrame:
    rows = []
    for p in sorted(Path(store_dir).glob("news_*.parquet")):
        df = pd.read_parquet(p, columns=["id", "symbols"])
        rows.append({"month": p.stem[5:], "articles": len(df),
                     "tagged_symbols": len({s for x in df["symbols"] for s in x.split(",") if s})})
    return pd.DataFrame(rows, columns=["month", "articles", "tagged_symbols"])


def write_news_manifest(m: pd.DataFrame, store_dir: str | Path, extra: dict | None = None) -> Path:
    summary = {
        "dataset": "news", "months": len(m), "total_articles": int(m["articles"].sum()) if len(m) else 0,
        "first_month": m["month"].min() if len(m) else None, "last_month": m["month"].max() if len(m) else None,
        "complete": bool(m.attrs.get("complete", True)),
        "updated": pd.Timestamp.now(tz="UTC").isoformat(),
    } | (extra or {})
    path = Path(store_dir) / "manifest.json"
    path.write_text(json.dumps(summary, indent=2))
    m.to_csv(Path(store_dir) / "manifest.csv", index=False)
    return path


def load_news(store_dir: str | Path, start: str | None = None, end: str | None = None) -> pd.DataFrame:
    """All stored articles (optionally between two dates), one row per article."""
    files = sorted(Path(store_dir).glob("news_*.parquet"))
    if start:
        files = [f for f in files if f.stem[5:] >= str(pd.Period(start, "M"))]
    if end:
        files = [f for f in files if f.stem[5:] <= str(pd.Period(end, "M"))]
    if not files:
        return pd.DataFrame(columns=FIELDS)
    df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
    return df.drop_duplicates("id").sort_values("created_at").reset_index(drop=True)


def article_counts(news: pd.DataFrame, freq: str = "D") -> pd.DataFrame:
    """Articles per (period, ticker) - a first, simple attention signal."""
    x = news[["created_at", "symbols"]].assign(ticker=news["symbols"].str.split(",")).explode("ticker")
    x = x[x["ticker"].astype(bool)]
    x["period"] = x["created_at"].dt.tz_convert("America/New_York").dt.tz_localize(None).dt.to_period(freq)
    return x.groupby(["period", "ticker"]).size().unstack(fill_value=0)
