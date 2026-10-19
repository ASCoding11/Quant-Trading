"""Daily OHLCV download from Yahoo Finance (via ``yfinance``) with a local cache.

Prices are split- and dividend-adjusted (``auto_adjust=True``) so that
close-to-close returns are total returns. Because adjustments change the whole
history whenever a dividend is paid, the cache is refreshed by re-downloading
rather than appending.
"""
from __future__ import annotations

import time
from pathlib import Path

import pandas as pd

from ..utils import LOG, load_frame, save_frame
from .market import FIELDS, MarketData

_YF_FIELDS = {"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}


def to_yahoo(ticker: str) -> str:
    """Yahoo uses '-' for share classes: BRK.B -> BRK-B."""
    return ticker.strip().upper().replace(".", "-").replace("/", "-")


def to_alpaca(ticker: str) -> str:
    """Alpaca uses '.' for share classes: BRK-B -> BRK.B."""
    return ticker.strip().upper().replace("-", ".")


def _download_batch(tickers: list[str], start: str, end: str | None) -> dict[str, pd.DataFrame]:
    import yfinance as yf

    raw = yf.download(
        tickers, start=start, end=end, auto_adjust=True, actions=False,
        group_by="column", threads=True, progress=False,
    )
    out: dict[str, pd.DataFrame] = {}
    if raw is None or raw.empty:
        return out
    if not isinstance(raw.columns, pd.MultiIndex):  # single ticker
        raw.columns = pd.MultiIndex.from_product([raw.columns, tickers])
    for f, yf_name in _YF_FIELDS.items():
        if yf_name in raw.columns.get_level_values(0):
            df = raw[yf_name].copy()
            df.index = pd.to_datetime(df.index).tz_localize(None).normalize()
            out[f] = df
    return out


def download_prices(
    tickers: list[str],
    start: str = "2000-01-01",
    end: str | None = None,
    batch_size: int = 100,
    retries: int = 2,
) -> MarketData:
    """Download OHLCV for many tickers in batches. Tickers that fail are dropped."""
    tickers = list(dict.fromkeys(to_yahoo(t) for t in tickers))
    frames: dict[str, list[pd.DataFrame]] = {f: [] for f in FIELDS}
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i : i + batch_size]
        for attempt in range(retries + 1):
            try:
                got = _download_batch(batch, start, end)
                break
            except Exception as exc:  # network hiccups, rate limits
                LOG.warning("batch %d failed (%s); retry %d", i // batch_size, exc, attempt + 1)
                time.sleep(5 * (attempt + 1))
                got = {}
        for f in FIELDS:
            if f in got:
                frames[f].append(got[f])
        LOG.info("downloaded %d / %d tickers", min(i + batch_size, len(tickers)), len(tickers))

    if not frames["close"]:
        raise RuntimeError("No price data downloaded - check your internet connection.")
    panels = {f: pd.concat(frames[f], axis=1).sort_index() for f in FIELDS}
    close = panels["close"]
    close = close.loc[:, ~close.columns.duplicated()]
    keep = close.columns[close.notna().sum() > 0]
    panels = {f: panels[f].loc[:, ~panels[f].columns.duplicated()].reindex(columns=keep) for f in FIELDS}
    # drop dates where (almost) nothing traded: holidays that sneak in
    active = panels["close"].notna().mean(axis=1) > 0.05
    panels = {f: df.loc[active] for f, df in panels.items()}
    return MarketData(**panels)


def cache_paths(cache_dir: str | Path) -> dict[str, Path]:
    cache_dir = Path(cache_dir)
    return {f: cache_dir / "prices" / f for f in FIELDS}


def save_market(md: MarketData, cache_dir: str | Path) -> None:
    for f, p in cache_paths(cache_dir).items():
        save_frame(getattr(md, f).astype("float32"), p)


def load_market(cache_dir: str | Path) -> MarketData | None:
    panels = {}
    for f, p in cache_paths(cache_dir).items():
        df = load_frame(p)
        if df is None:
            return None
        panels[f] = df
    return MarketData(**panels)


def last_completed_session(now: pd.Timestamp | None = None) -> pd.Timestamp:
    """Most recent weekday whose US session has closed (ignores holidays)."""
    now = now or pd.Timestamp.now(tz="America/New_York")
    day = now.normalize().tz_localize(None)
    if now.hour < 17:  # data for today is not final before ~5pm ET
        day -= pd.Timedelta(days=1)
    while day.weekday() >= 5:
        day -= pd.Timedelta(days=1)
    return day


def get_market_data(
    tickers: list[str], start: str, end: str | None, cache_dir: str | Path,
    batch_size: int = 100, force: bool = False,
) -> MarketData:
    """Load from cache when it is fresh and covers the tickers, else download."""
    cached = None if force else load_market(cache_dir)
    want = {to_yahoo(t) for t in tickers}
    if cached is not None:
        have = set(cached.tickers)
        target_end = pd.Timestamp(end) - pd.Timedelta(days=1) if end else last_completed_session()
        # allow for a holiday: fresh if within 4 calendar days of the target
        fresh = cached.dates[-1] >= target_end - pd.Timedelta(days=4)
        covered = len(want - have) <= max(5, 0.01 * len(want))
        starts_ok = cached.dates[0] <= pd.Timestamp(start) + pd.Timedelta(days=10)
        if fresh and covered and starts_ok:
            LOG.info("using cached prices (%d tickers, through %s)", len(have), cached.dates[-1].date())
            return cached.subset(tickers=[t for t in cached.tickers if t in want])
    md = download_prices(sorted(want), start=start, end=end, batch_size=batch_size)
    save_market(md, cache_dir)
    return md
