"""Configuration: every tunable number in one place.

Defaults live in the dataclasses below; ``config/default.yaml`` mirrors them
and any YAML file passed with ``--config`` overrides only the keys it sets.
"""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class UniverseConfig:
    size: int = 1000                 # number of companies to trade
    min_history_years: float = 15.0  # must have traded at least this long
    candidate_source: str = "ishares_r3000"  # ishares_r3000 | wikipedia | file
    universe_file: str | None = None # CSV with a 'ticker' column (source=file)
    min_price: float = 5.0           # skip penny stocks on a given day
    min_dollar_volume: float = 5e6   # 21-day median $ volume needed to trade


@dataclass
class DataConfig:
    start: str = "2000-01-01"
    end: str | None = None           # None = today
    cache_dir: str = "data"
    batch_size: int = 100            # tickers per yfinance request


@dataclass
class FactorConfig:
    n_factors: int = 15              # PCA eigenportfolios (Avellaneda-Lee)
    window: int = 252                # days of returns used for each PCA
    refit_every: int = 21            # re-estimate loadings monthly
    n_clusters: int = 20             # k-means peer groups on PCA loadings


@dataclass
class RegimeConfig:
    n_states: int = 3                # hidden market regimes
    refit_every: int = 252           # re-run Baum-Welch once a year
    min_history: int = 756           # 3 years before the first fit
    n_init: int = 5                  # random restarts for EM
    max_iter: int = 200


@dataclass
class ModelConfig:
    horizon: int = 5                 # predict open(t+1) -> open(t+1+h), in days
    train_window: int = 1260         # 5 years rolling training window
    min_train: int = 756             # 3 years before first prediction
    retrain_every: int = 63          # quarterly walk-forward refits
    models: list[str] = field(default_factory=lambda: [
        "ridge", "elastic_net", "regime_ridge", "kernel_ridge", "gbm", "ic_weighted",
    ])
    ensemble: list[str] = field(default_factory=lambda: [
        "ridge", "regime_ridge", "kernel_ridge", "gbm", "ic_weighted",
    ])
    trade_model: str = "ensemble"    # which prediction the portfolio trades
    gbm_max_rows: int = 400_000      # subsample for gradient boosting
    rff_features: int = 256          # random Fourier features (kernel ridge)
    seed: int = 7
    signals: list[str] | None = None # None = every registered signal


@dataclass
class PortfolioConfig:
    target_vol: float = 0.10         # annualized volatility target
    max_gross: float = 2.0           # sum |w| cap: 2.0 = 100% long + 100% short (Reg T limit)
    max_weight: float = 0.02         # per-name cap as a fraction of equity
    kelly_fraction: float = 0.5      # half-Kelly cap on leverage
    ic_prior: float = 0.01           # prior daily IC for Bayesian shrinkage
    ic_prior_days: int = 252         # weight of that prior, in days
    ic_lookback: int = 252           # trailing window for realized IC
    weighting: str = "kelly"         # kelly (alpha / variance) | rank (proportional to score)
    factor_neutral: bool = True      # hedge PCA factors as well as net dollars
    cost_aversion: float = 1.0       # scales costs in the no-trade band (>1 trades less)
    trade_rate: float = 1.0          # extra partial adjustment toward target (1 = off)
    no_trade_band: float = 0.0002    # ignore trades smaller than 2 bp of equity
    drawdown_limit: float = 0.15     # cut risk after a 15% drawdown
    drawdown_scale: float = 0.5      # ...to half size until recovery


@dataclass
class CostConfig:
    aum: float = 10_000_000          # account size used for market impact
    commission_bps: float = 0.0      # Alpaca charges no commission
    slippage_bps: float = 1.0        # fill vs. official open price
    # half-spread by liquidity tier: (min 21-day median $ volume, half-spread bps)
    spread_tiers: list = field(default_factory=lambda: [
        [500e6, 1.5], [100e6, 3.0], [20e6, 6.0], [0.0, 12.0],
    ])
    impact_coef: float = 0.5         # square-root impact: c * sigma * sqrt(Q/ADV)
    borrow_bps_annual: float = 50.0  # stock-loan fee on short notional


@dataclass
class LiveConfig:
    dry_run: bool = True             # print orders instead of sending them
    order_type: str = "auto"         # auto | opg (market-on-open) | market
    min_order_value: float = 50.0    # skip orders smaller than this ($)
    capital_fraction: float = 1.0    # fraction of paper equity to deploy
    log_dir: str = "logs"


@dataclass
class Config:
    universe: UniverseConfig = field(default_factory=UniverseConfig)
    data: DataConfig = field(default_factory=DataConfig)
    factors: FactorConfig = field(default_factory=FactorConfig)
    regime: RegimeConfig = field(default_factory=RegimeConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    portfolio: PortfolioConfig = field(default_factory=PortfolioConfig)
    costs: CostConfig = field(default_factory=CostConfig)
    live: LiveConfig = field(default_factory=LiveConfig)
    report_dir: str = "reports"
    diagnostics: bool = True         # also backtest portfolio-construction variants

    # -- helpers ---------------------------------------------------------
    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def load(cls, path: str | Path | None = None, overrides: dict | None = None) -> "Config":
        cfg = cls()
        if path:
            with open(path) as fh:
                _merge(cfg, yaml.safe_load(fh) or {})
        if overrides:
            _merge(cfg, overrides)
        return cfg


def _merge(obj, updates: dict) -> None:
    for key, value in updates.items():
        if not hasattr(obj, key):
            raise KeyError(f"Unknown config key: {key}")
        current = getattr(obj, key)
        if dataclasses.is_dataclass(current) and isinstance(value, dict):
            _merge(current, value)
        else:
            setattr(obj, key, value)
