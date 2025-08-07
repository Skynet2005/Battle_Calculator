"""
BonusSource – aggregates **permanent** non-skill buffs into one dict.

After this revision, passive expedition skills are handled exclusively
inside CombatState._apply_passives, guaranteeing that every hero on every
side is processed exactly once.
"""

from __future__ import annotations
from typing import Dict, Optional, Iterable
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
        heroes: Iterable[Hero],
        city_buffs: Optional[Dict[str, float]] = None,
        territory_buffs: Optional[Dict[str, float]] = None,
        pet_buffs: Optional[Dict[str, float]] = None,
    ):
        """Create a BonusSource for an entire side.

        ``heroes`` can be any iterable of Hero objects.  This allows rally
        joiners' exclusive‑weapon perks to contribute alongside the primary
        three commanders.  All exclusive‑weapon perks are aggregated across the
        list so every equipped weapon contributes its permanent stat increases.
        """

        self.heroes = list(heroes)
        self.city_buffs = {
            k.lower().replace("-", "_"): v for k, v in (city_buffs or {}).items()
        }
        # Treat territory buffs as "special" bonuses that cannot stack
        self.special_buffs = {
            k.lower().replace("-", "_"): v for k, v in (territory_buffs or {}).items()
        }
        self.pet_buffs = {
            k.lower().replace("-", "_"): v for k, v in (pet_buffs or {}).items()
        }

        # separate containers for regular and special bonuses
        self.base_bonuses: Dict[str, float] = {}
        self.special_bonuses: Dict[str, float] = {}
        # backward compatible alias
        self.total_bonuses = self.base_bonuses

        self._aggregate()

    # ------------------------------------------------------------------ #
    def _add_base(self, key: str, val: float) -> None:
        """Utility – accumulate percentages from multiple sources."""
        self.base_bonuses[key] = self.base_bonuses.get(key, 0.0) + val

    def _add_special(self, key: str, val: float) -> None:
        """Utility – special bonuses take the highest value (no stacking)."""
        self.special_bonuses[key] = max(self.special_bonuses.get(key, 0.0), val)

    # ------------------------------------------------------------------ #
    def _aggregate(self) -> None:
        # 1) exclusive-weapon **perks** (flat stat increases)
        for hero in self.heroes:
            ew = hero.exclusive_weapon
            if ew:
                for k, v in ew.perks.items():
                    # unify key style (“infantry-health” → “infantry_health”)
                    self._add_base(k.replace("-", "_").lower(), v)

        # 2) external permanent buffs
        for src in (self.city_buffs, self.pet_buffs):
            for k, v in src.items():
                self._add_base(k, v)

        for k, v in self.special_buffs.items():
            self._add_special(k, v)

        # 3)  ✨ NO expedition skills here anymore ✨
        #     All passive skills are collected once, for every hero,
        #     inside CombatState._apply_passives.
