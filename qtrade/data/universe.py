"""Universe: the top N US companies by market cap with >= 15 years of history.

How it works
------------
1. Get a *candidate list* ranked by market capitalisation. The default source
   is the iShares Russell 3000 ETF (IWV) holdings file, which lists ~2,600 US
   stocks with their market value, so ranking by ETF dollar holdings is ranking
   by float-adjusted market cap.
2. Walk down that list in batches, download price history, and keep a company
   only if its first trading day is at least ``min_history_years`` ago.
3. Stop once ``size`` companies have passed.

Important bias warning
----------------------
Choosing today's large, long-lived companies and testing them over the past
15+ years introduces *survivorship* and *look-ahead* bias: the backtest never
holds a company that went bankrupt or shrank out of the top 1000. Backtest
returns will be flattered by this. The README explains how to read results.
"""
from __future__ import annotations

import io
import urllib.request
from pathlib import Path

import pandas as pd

from ..utils import LOG
from .loader import download_prices, to_yahoo

ISHARES_URLS = {
    "ishares_r3000": (
        "https://www.ishares.com/us/products/239714/ishares-russell-3000-etf/"
        "1467271812596.ajax?fileType=csv&fileName=IWV_holdings&dataType=fund"
    ),
    "ishares_r1000": (
        "https://www.ishares.com/us/products/239707/ishares-russell-1000-etf/"
        "1467271812596.ajax?fileType=csv&fileName=IWB_holdings&dataType=fund"
    ),
}
WIKI_INDEXES = {
    "S&P 500": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
    "S&P 400": "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies",
    "S&P 600": "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies",
}
_UA = {"User-Agent": "Mozilla/5.0 (qtrade research; +https://github.com/ASCoding11/quant-trading)"}


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_ishares_holdings(text: str) -> pd.DataFrame:
    """Parse an iShares holdings CSV (it has a few lines of preamble)."""
    lines = text.splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("Ticker"))
    df = pd.read_csv(io.StringIO("\n".join(lines[start:])), thousands=",")
    df = df[df.get("Asset Class", "Equity").astype(str).str.strip() == "Equity"]
    df = df.rename(columns={"Ticker": "ticker", "Name": "name", "Sector": "sector",
                            "Market Value": "market_value"})
    df["ticker"] = df["ticker"].astype(str).str.strip()
    df = df[df["ticker"].str.fullmatch(r"[A-Z][A-Z0-9.\-]{0,6}")]
    df["market_value"] = pd.to_numeric(df["market_value"], errors="coerce")
    df = df.dropna(subset=["market_value"]).sort_values("market_value", ascending=False)
    return df[["ticker", "name", "sector", "market_value"]].drop_duplicates("ticker").reset_index(drop=True)


def candidates_from_ishares(source: str) -> pd.DataFrame:
    return parse_ishares_holdings(_fetch(ISHARES_URLS[source]))


def candidates_from_wikipedia() -> pd.DataFrame:
    """Fallback: S&P 1500 constituents (no market cap -> ranked later by $ volume)."""
    rows = []
    for name, url in WIKI_INDEXES.items():
        tables = pd.read_html(io.StringIO(_fetch(url)))
        tbl = next(t for t in tables if any(str(c).lower() in ("symbol", "ticker symbol", "ticker") for c in t.columns))
        col = next(c for c in tbl.columns if str(c).lower() in ("symbol", "ticker symbol", "ticker"))
        sec = next((c for c in tbl.columns if "sector" in str(c).lower()), None)
        for _, r in tbl.iterrows():
            rows.append({"ticker": str(r[col]).strip(), "name": "", "index": name,
                         "sector": r[sec] if sec is not None else "", "market_value": float("nan")})
    return pd.DataFrame(rows).drop_duplicates("ticker").reset_index(drop=True)


def share_class_variants(ticker: str) -> list[str]:
    """iShares writes BRK.B as 'BRKB'; try 'BRK-B' when the plain symbol fails."""
    t = to_yahoo(ticker)
    out = [t]
    if "-" not in t and len(t) >= 4 and t[-1] in "ABCK":
        out.append(f"{t[:-1]}-{t[-1]}")
    return out


def build_universe(
    size: int = 1000,
    min_history_years: float = 15.0,
    source: str = "ishares_r3000",
    universe_file: str | None = None,
    start: str = "2000-01-01",
    batch_size: int = 100,
    as_of: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Return a DataFrame of selected tickers (in market-cap order) and metadata."""
    as_of = pd.Timestamp(as_of or pd.Timestamp.today().normalize())
    cutoff = as_of - pd.DateOffset(days=int(round(365.25 * min_history_years)))

    if source == "file":
        cand = pd.read_csv(universe_file)
        cand["ticker"] = cand["ticker"].astype(str)
        if "market_value" not in cand:
            cand["market_value"] = float("nan")
    elif source == "wikipedia":
        cand = candidates_from_wikipedia()
    else:
        try:
            cand = candidates_from_ishares(source)
        except Exception as exc:
            LOG.warning("iShares holdings unavailable (%s); falling back to Wikipedia S&P 1500", exc)
            cand = candidates_from_wikipedia()
            source = "wikipedia"
    LOG.info("%d candidate companies from %s", len(cand), source)

    selected: list[dict] = []
    # check a little more than needed per batch, since some fail the history test
    for i in range(0, len(cand), batch_size):
        chunk = cand.iloc[i : i + batch_size]
        variants = {v: row for _, row in chunk.iterrows() for v in share_class_variants(row["ticker"])}
        # A quick check only needs the first bar, but we pull monthly data so
        # the request is cheap; the full daily download happens later.
        md = _first_dates(list(variants), start=start)
        seen = set()
        for sym, first in md.items():
            row = variants[sym]
            if row["ticker"] in seen or pd.isna(first):
                continue
            seen.add(row["ticker"])
            if first <= cutoff:
                selected.append({"ticker": sym, "name": row.get("name", ""), "sector": row.get("sector", ""),
                                 "market_value": row.get("market_value", float("nan")), "first_date": first})
        LOG.info("checked %d candidates, %d qualify", min(i + batch_size, len(cand)), len(selected))
        if source != "wikipedia" and len(selected) >= size:
            break

    uni = pd.DataFrame(selected)
    if source == "wikipedia" or uni["market_value"].isna().all():
        uni = _rank_by_dollar_volume(uni, start)
    uni = uni.drop_duplicates("ticker").head(size).reset_index(drop=True)
    uni["rank"] = range(1, len(uni) + 1)
    LOG.info("universe: %d companies with >= %.0f years of history", len(uni), min_history_years)
    return uni


def _first_dates(tickers: list[str], start: str) -> dict[str, pd.Timestamp]:
    import yfinance as yf

    raw = yf.download(tickers, start=start, interval="1mo", auto_adjust=True,
                      group_by="column", threads=True, progress=False)
    if raw is None or raw.empty:
        return {}
    close = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]].set_axis(tickers, axis=1)
    return {t: close[t].first_valid_index() for t in close.columns}


def _rank_by_dollar_volume(uni: pd.DataFrame, start: str) -> pd.DataFrame:
    """Proxy market-cap ranking by trailing 63-day median dollar volume."""
    recent = (pd.Timestamp.today() - pd.Timedelta(days=120)).strftime("%Y-%m-%d")
    md = download_prices(uni["ticker"].tolist(), start=recent)
    dv = (md.close * md.volume).tail(63).median()
    uni = uni.assign(dollar_volume=uni["ticker"].map(dv)).sort_values("dollar_volume", ascending=False)
    return uni


def save_universe(uni: pd.DataFrame, cache_dir: str | Path) -> Path:
    path = Path(cache_dir) / "universe.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    uni.to_csv(path, index=False)
    return path


def load_universe(cache_dir: str | Path) -> pd.DataFrame | None:
    path = Path(cache_dir) / "universe.csv"
    return pd.read_csv(path) if path.exists() else None
