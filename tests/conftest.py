import warnings

import pytest

from qtrade.config import Config
from qtrade.data import make_market

warnings.filterwarnings("ignore", category=RuntimeWarning)


def small_config() -> Config:
    cfg = Config()
    cfg.universe.min_dollar_volume = 0
    cfg.factors.n_factors = 5
    cfg.factors.window = 126
    cfg.factors.n_clusters = 6
    cfg.regime.min_history = 300
    cfg.regime.refit_every = 200
    cfg.regime.n_init = 2
    cfg.model.min_train = 300
    cfg.model.train_window = 400
    cfg.model.retrain_every = 100
    cfg.model.models = ["ridge", "regime_ridge", "ic_weighted"]
    cfg.model.ensemble = ["ridge", "regime_ridge", "ic_weighted"]
    return cfg


@pytest.fixture(scope="session")
def market():
    md, regimes = make_market(n_stocks=60, n_days=1100, seed=11)
    return md, regimes


@pytest.fixture(scope="session")
def cfg():
    return small_config()
