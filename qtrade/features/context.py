"""Derived panels shared by many signals, computed once and cached."""
from __future__ import annotations

from functools import cached_property

import numpy as np
import pandas as pd

from ..config import Config
from ..data.market import MarketData
from ..utils import rolling_beta, safe_div
from .factors import FactorModel, fit_factor_model


class FeatureContext:
    """Everything a signal might need, built lazily from one ``MarketData``.

    All panels are aligned to ``md.close`` (dates x tickers) and every row uses
    only information available at that day's close.
    """

    def __init__(self, md: MarketData, cfg: Config | None = None):
        self.md = md
        self.cfg = cfg or Config()

    # -- raw returns -----------------------------------------------------
    @cached_property
    def ret(self) -> pd.DataFrame:
        """Close-to-close total return."""
        return self.md.close.pct_change(fill_method=None)

    @cached_property
    def log_ret(self) -> pd.DataFrame:
        return np.log1p(self.ret)

    @cached_property
    def overnight(self) -> pd.DataFrame:
        """Previous close -> today's open."""
        return safe_div(self.md.open, self.md.close.shift(1)) - 1

    @cached_property
    def intraday(self) -> pd.DataFrame:
        """Today's open -> today's close."""
        return safe_div(self.md.close, self.md.open) - 1

    @cached_property
    def dollar_volume(self) -> pd.DataFrame:
        return self.md.close * self.md.volume

    @cached_property
    def adv(self) -> pd.DataFrame:
        """21-day median dollar volume."""
        return self.dollar_volume.rolling(21, min_periods=10).median()

    @cached_property
    def vol_21(self) -> pd.DataFrame:
        return self.ret.rolling(21, min_periods=15).std()

    @cached_property
    def vol_63(self) -> pd.DataFrame:
        return self.ret.rolling(63, min_periods=40).std()

    @cached_property
    def spread(self) -> pd.DataFrame:
        """Corwin-Schultz (2012) bid-ask spread estimated from daily highs and lows,
        averaged over 21 days. Used as a signal and by the transaction-cost model."""
        h, l = self.md.high, self.md.low
        hl = np.log(safe_div(h, l)) ** 2
        beta = hl + hl.shift(1)
        h2 = pd.DataFrame(np.fmax(h.values, h.shift(1).values), index=h.index, columns=h.columns)
        l2 = pd.DataFrame(np.fmin(l.values, l.shift(1).values), index=l.index, columns=l.columns)
        gamma = np.log(safe_div(h2, l2)) ** 2
        k = 3 - 2 * np.sqrt(2)
        alpha = (np.sqrt(2 * beta) - np.sqrt(beta)) / k - np.sqrt(gamma / k)
        s = 2 * (np.exp(alpha) - 1) / (1 + np.exp(alpha))
        return s.clip(lower=0).rolling(21, min_periods=10).mean()

    # -- market ----------------------------------------------------------
    @cached_property
    def market_ret(self) -> pd.Series:
        """Equal-weighted average return of the universe."""
        return self.ret.clip(-0.5, 0.5).mean(axis=1)

    @cached_property
    def beta_252(self) -> pd.DataFrame:
        return rolling_beta(self.ret, self.market_ret, 252)

    # -- tradability -----------------------------------------------------
    @cached_property
    def tradable(self) -> pd.DataFrame:
        """True where the stock can be traded tomorrow based on today's data."""
        u = self.cfg.universe
        history = self.md.close.notna().rolling(252, min_periods=1).sum() >= 240
        price_ok = self.md.close >= u.min_price
        liquid = self.adv >= u.min_dollar_volume
        return history & price_ok & liquid & self.md.close.notna()

    # -- statistical factor model ---------------------------------------
    @cached_property
    def factor_model(self) -> FactorModel:
        f = self.cfg.factors
        return fit_factor_model(
            self.ret.where(self.md.close.notna()).clip(-0.5, 0.5),
            n_factors=f.n_factors, window=f.window, refit_every=f.refit_every,
            n_clusters=f.n_clusters, seed=self.cfg.model.seed,
        )

    @cached_property
    def resid(self) -> pd.DataFrame:
        return self.factor_model.residuals

    @cached_property
    def clusters(self) -> pd.DataFrame:
        return self.factor_model.cluster_panel(self.ret.index, self.ret.columns)

    # -- market-wide state features (input to the regime HMM) -----------
    @cached_property
    def market_state(self) -> pd.DataFrame:
        r = self.ret.clip(-0.5, 0.5)
        mkt = self.market_ret
        rv = mkt.rolling(10, min_periods=5).std() * np.sqrt(252)
        disp = r.std(axis=1)
        # share of variance explained by the market (a correlation gauge)
        mkt_var = mkt.rolling(21, min_periods=10).var()
        avg_var = (r.pow(2).mean(axis=1)).rolling(21, min_periods=10).mean()
        corr_share = (mkt_var / avg_var).clip(0, 1)
        out = pd.DataFrame({
            "mkt_ret_5d": mkt.rolling(5, min_periods=3).sum(),
            "log_rvol": np.log(rv.clip(lower=1e-4)),
            "log_dispersion": np.log(disp.clip(lower=1e-5)),
            "corr_share": corr_share,
        })
        return out
