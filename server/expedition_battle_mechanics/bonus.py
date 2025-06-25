# battle_mechanics/bonus.py

from typing import Dict, Optional
from expedition_battle_mechanics.hero import Hero

class BonusSource:
    """
    Aggregates all stat bonuses (hero base, weapon, city, territory, etc.)
    into a single lookup.
    """
    def __init__(
        self,
        hero: Hero,
        city_buffs: Optional[Dict[str, float]] = None,
        territory_buffs: Optional[Dict[str, float]] = None,
        pet_buffs: Optional[Dict[str, float]] = None
    ):
        self.hero = hero
        self.city_buffs = city_buffs or {}
        self.territory_buffs = territory_buffs or {}
        self.pet_buffs = pet_buffs or {}
        self.total_bonuses = self._aggregate_bonuses()

    def _aggregate_bonuses(self) -> Dict[str, float]:
        """
        Combines all bonus sources into a single dictionary of stat bonuses.
        """
        tb = {"attack": 0.0, "defense": 0.0, "lethality": 0.0, "health": 0.0}
        # Exclusive weapon
        if self.hero.exclusive_weapon:
            for k, v in self.hero.exclusive_weapon.stat_bonuses.items():
                tb[k] = tb.get(k, 0.0) + v
        # City buffs
        for k, v in self.city_buffs.items():
            tb[k] = tb.get(k, 0.0) + v
        # Territory buffs
        for k, v in self.territory_buffs.items():
            tb[k] = tb.get(k, 0.0) + v
        # Pet buffs
        for k, v in self.pet_buffs.items():
            tb[k] = tb.get(k, 0.0) + v
        return tb
