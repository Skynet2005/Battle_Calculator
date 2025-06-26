"""
BonusSource – aggregates **permanent** non-skill buffs into one dict.

After this revision, passive expedition skills are handled exclusively
inside CombatState._apply_passives, guaranteeing that every hero on every
side is processed exactly once.
"""

from __future__ import annotations
from typing import Dict, Optional
from expedition_battle_mechanics.hero import Hero


class BonusSource:
    """
    Self.total_bonuses example:
      {
        "attack": 0.12,
        "Infantry-defense": 0.30,
        ...
      }
    """

    # ------------------------------------------------------------------ #
    def __init__(
        self,
        hero: Hero,
        city_buffs: Optional[Dict[str, float]] = None,
        territory_buffs: Optional[Dict[str, float]] = None,
        pet_buffs: Optional[Dict[str, float]] = None,
    ):
        self.hero = hero
        self.city_buffs = city_buffs or {}
        self.territory_buffs = territory_buffs or {}
        self.pet_buffs = pet_buffs or {}

        # one mutable dict we keep updating
        self.total_bonuses: Dict[str, float] = {}
        self._aggregate()

    # ------------------------------------------------------------------ #
    def _add(self, key: str, val: float) -> None:
        """Utility – accumulate percentages from multiple sources."""
        self.total_bonuses[key] = self.total_bonuses.get(key, 0.0) + val

    # ------------------------------------------------------------------ #
    def _aggregate(self) -> None:
        # 1) exclusive-weapon **perks** (flat stat increases)
        ew = self.hero.exclusive_weapon
        if ew:
            for k, v in ew.perks.items():
                # unify key style (“infantry-health” → “infantry_health”)
                self._add(k.replace("-", "_"), v)

        # 2) external permanent buffs
        for src in (self.city_buffs, self.territory_buffs, self.pet_buffs):
            for k, v in src.items():
                self._add(k, v)

        # 3)  ✨ NO expedition skills here anymore ✨
        #     All passive skills are collected once, for every hero,
        #     inside CombatState._apply_passives.
