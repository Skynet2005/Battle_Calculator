"""Stacking strategies for combining battle bonuses.

This module implements the **Strategy** design pattern so that different
stacking rules (additive, multiplicative, highest-value wins, etc.) can be
swapped in without altering calling code.  It keeps the battle engine
extensible as new hero skills or buff types are introduced.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class StackingStrategy(ABC):
    """Combine ``current`` and ``value`` according to a stacking rule."""

    @abstractmethod
    def combine(self, current: float, value: float) -> float:  # pragma: no cover - interface
        """Return the aggregated result for ``current`` and ``value``."""


class AdditiveStrategy(StackingStrategy):
    """Simple addition for stackable percentage bonuses."""

    def combine(self, current: float, value: float) -> float:
        return current + value


class MaxStrategy(StackingStrategy):
    """Keep the highest value encountered (non-stacking)."""

    def combine(self, current: float, value: float) -> float:
        return max(current, value)


class MultiplicativeStrategy(StackingStrategy):
    """Multiply percentages: ``(1+a) * (1+b) - 1``."""

    def combine(self, current: float, value: float) -> float:
        return (1 + current) * (1 + value) - 1


class BonusBucket:
    """Container that aggregates bonuses using a chosen strategy.

    Exposes a lightweight dict-like API which keeps existing simulator code
    largely unchanged while enabling more sophisticated stacking behaviour.
    """

    def __init__(self, strategy: StackingStrategy) -> None:
        self.strategy = strategy
        self._bonuses: Dict[str, float] = {}

    def add(self, key: str, value: float) -> None:
        self._bonuses[key] = self.strategy.combine(self._bonuses.get(key, 0.0), value)

    # Dict-style helpers -------------------------------------------------
    def as_dict(self) -> Dict[str, float]:
        return self._bonuses

    def get(self, key: str, default: float = 0.0) -> float:
        return self._bonuses.get(key, default)

    def items(self):  # pragma: no cover - simple passthrough
        return self._bonuses.items()

    def __getitem__(self, key: str) -> float:  # pragma: no cover
        return self._bonuses[key]

