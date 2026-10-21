"""Intraday bars arranged as (day, bar-of-day, stock) arrays.

Every regular session has the same grid of bars (78 five-minute bars from
09:30 to 16:00), so a 3-D array indexes everything cleanly: ``close[d, b, i]``
is stock i's close in bar b of day d. Missing bars are NaN. Half-day sessions
simply have NaN bars after 13:00.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from ..utils import LOG

FIELDS = ("open", "close", "volume", "vwap")


@dataclass
class DayBars:
    days: pd.DatetimeIndex       # D session dates
    tickers: list[str]           # N
    open: np.ndarray             # D x B x N
    close: np.ndarray
    volume: np.ndarray
    vwap: np.ndarray
    bar_minutes: int = 5

    @property
    def n_bars(self) -> int:
        return self.open.shape[1]

    def bar_time(self, b: int) -> str:
        m = 9 * 60 + 30 + b * self.bar_minutes
        return f"{m // 60:02d}:{m % 60:02d}"

    def subset_days(self, sl: slice) -> "DayBars":
        return DayBars(self.days[sl], self.tickers, self.open[sl], self.close[sl], self.volume[sl],
                       self.vwap[sl], self.bar_minutes)


def bars_per_day(bar_minutes: int) -> int:
    return 390 // bar_minutes


def from_frames(frames: dict[str, pd.DataFrame], bar_minutes: int = 5,
                days: pd.DatetimeIndex | None = None) -> DayBars:
    """Build DayBars from {ticker: DataFrame indexed by New York time} with
    open/close/volume/vwap columns (the format of the intraday store)."""
    B = bars_per_day(bar_minutes)
    tickers = list(frames)
    slots, all_days = {}, set()
    for t, df in frames.items():
        idx = df.index if df.index.tz is not None else df.index.tz_localize("America/New_York")
        idx = idx.tz_convert("America/New_York")
        day = idx.tz_localize(None).normalize()
        slot = ((idx.hour * 60 + idx.minute) - (9 * 60 + 30)) // bar_minutes
        ok = (slot >= 0) & (slot < B)
        slots[t] = (day[ok], np.asarray(slot[ok]), df[ok])
        if days is None:
            all_days.update(day[ok].unique())
    days = days if days is not None else pd.DatetimeIndex(sorted(all_days))
    D, N = len(days), len(tickers)
    arrs = {f: np.full((D, B, N), np.nan, dtype=np.float32) for f in FIELDS}
    for i, t in enumerate(tickers):
        day, slot, df = slots[t]
        di = days.get_indexer(day)
        keep = di >= 0
        for f in FIELDS:
            col = df[f].to_numpy(dtype=np.float32) if f in df else np.full(len(df), np.nan, np.float32)
            arrs[f][di[keep], slot[keep], i] = col[keep]
    bad = ~(arrs["open"] > 0) | ~(arrs["close"] > 0)
    for f in ("open", "close", "vwap"):
        arrs[f][bad] = np.nan
    arrs["volume"][bad] = 0.0
    return DayBars(days, tickers, bar_minutes=bar_minutes, **arrs)


def load_store(store: str | Path, n_symbols: int | None = None, start: str | None = None,
               bar_minutes: int = 5) -> DayBars:
    """Load the ``n_symbols`` most liquid names of an intraday store."""
    store = Path(store)
    sym_file = store / "symbols.csv"
    if sym_file.exists():
        tickers = pd.read_csv(sym_file)["ticker"].tolist()
    else:
        tickers = sorted(p.stem for p in store.glob("*.parquet"))
    if n_symbols:
        tickers = tickers[:n_symbols]
    frames = {}
    for t in tickers:
        p = store / f"{t}.parquet"
        if not p.exists():
            continue
        df = pd.read_parquet(p, columns=[c for c in FIELDS])
        if start:
            df = df[df.index >= pd.Timestamp(start, tz=df.index.tz)]
        if len(df):
            frames[t] = df
    if not frames:
        raise SystemExit(f"No intraday bars found in {store}.")
    bars = from_frames(frames, bar_minutes)
    LOG.info("intraday bars: %d days x %d bars x %d stocks (%s -> %s)", len(bars.days), bars.n_bars,
             len(bars.tickers), bars.days[0].date(), bars.days[-1].date())
    return bars
