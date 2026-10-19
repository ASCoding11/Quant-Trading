"""Signal registry: decorate a function and it becomes part of the library."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pandas as pd

from ..features.context import FeatureContext

SignalFn = Callable[[FeatureContext], pd.DataFrame]


@dataclass(frozen=True)
class SignalSpec:
    name: str
    family: str
    fn: SignalFn
    description: str


REGISTRY: dict[str, SignalSpec] = {}


def signal(family: str, description: str):
    """Register ``fn`` under its own name. Positive values = expected to outperform."""

    def wrap(fn: SignalFn) -> SignalFn:
        REGISTRY[fn.__name__] = SignalSpec(fn.__name__, family, fn, description)
        return fn

    return wrap


def list_signals() -> pd.DataFrame:
    return pd.DataFrame(
        [{"signal": s.name, "family": s.family, "description": s.description} for s in REGISTRY.values()]
    )
