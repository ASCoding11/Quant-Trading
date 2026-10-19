"""Container for the OHLCV panels everything else is computed from."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

FIELDS = ("open", "high", "low", "close", "volume")


@dataclass
class MarketData:
    open: pd.DataFrame
    high: pd.DataFrame
    low: pd.DataFrame
    close: pd.DataFrame
    volume: pd.DataFrame

    def __post_init__(self) -> None:
        idx = self.close.index
        cols = self.close.columns
        for f in FIELDS:
            df = getattr(self, f).reindex(index=idx, columns=cols).astype("float64")
            setattr(self, f, df)
        # a bar is valid only when open and close both exist and are positive
        bad = ~((self.close > 0) & (self.open > 0))
        for f in ("open", "high", "low", "close"):
            setattr(self, f, getattr(self, f).mask(bad))
        # repair impossible highs/lows that occasionally appear in vendor data
        o, c = self.open.values, self.close.values
        self.high = pd.DataFrame(np.fmax(np.fmax(self.high.values, o), c), index=idx, columns=cols)
        self.low = pd.DataFrame(np.fmin(np.fmin(self.low.values, o), c), index=idx, columns=cols)

    # -- convenience -----------------------------------------------------
    @property
    def dates(self) -> pd.DatetimeIndex:
        return self.close.index

    @property
    def tickers(self) -> list[str]:
        return list(self.close.columns)

    def subset(self, tickers=None, start=None, end=None) -> "MarketData":
        tickers = list(tickers) if tickers is not None else self.tickers
        sl = slice(start, end)
        return MarketData(**{f: getattr(self, f).loc[sl, tickers] for f in FIELDS})

    def first_valid_dates(self) -> pd.Series:
        return self.close.apply(lambda s: s.first_valid_index())
