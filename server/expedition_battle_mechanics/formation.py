# expedition_battle_mechanics/formation.py

import re
from typing import List, Dict, Iterable

from .troop import TroopGroup
from .definitions import TroopDefinition
from .hero import Hero

class RallyFormation:
    """Represents a solo march or rally leader formation.

    ``heroes``           – exactly one hero for each troop class
    ``support_heroes``   – optional list of rally joiner heroes whose
                          expedition skills / exclusive weapons should be
                          considered even though they do **not** command a
                          troop group.
    """

    def __init__(
        self,
        heroes: List[Hero],
        troop_ratios: Dict[str, float],
        total_capacity: int,
        troop_definitions: Dict[str, dict],
        support_heroes: Iterable[Hero] | None = None,
        pets: dict | None = None,
    ):
        # Validate heroes: must have one of each type for the main formation
        self.heroes = {h.char_class: h for h in heroes}
        for t in ["Infantry", "Lancer", "Marksman"]:
            if t not in self.heroes:
                raise ValueError(f"Missing hero for {t}")

        # rally joiners (may be empty)
        self.support_heroes: List[Hero] = list(support_heroes or [])

        # Game rule: only the top four joiners contribute their first
        # expedition skill and none of their exclusive‑weapon perks.  We sort
        # joiners by the level of that first skill (highest first), truncate
        # to four, then strip extra skills and equipment.

        def _skill_level(hero: Hero) -> int:
            if hero.skills.get("expedition"):
                sk = hero.skills["expedition"][0]
                return hero.selected_skill_levels.get(sk.name, 5)
            return 0

        # sort & truncate
        self.support_heroes.sort(key=_skill_level, reverse=True)
        self.support_heroes = self.support_heroes[:4]

        # keep only the first expedition skill and remove exclusive weapons
        for h in self.support_heroes:
            if h.skills.get("expedition"):
                h.skills["expedition"] = h.skills["expedition"][:1]
            else:
                h.skills["expedition"] = []
            h.exclusive_weapon = None

        self.troop_ratios = troop_ratios  # e.g., {"Infantry": 0.5, "Lancer": 0.3, "Marksman": 0.2}
        self.total_capacity = total_capacity
        self.troop_definitions = troop_definitions
        self.troop_groups = self._create_troop_groups()
        # store pets meta
        self.pets = pets or []

    # ------------------------------------------------------------------ #
    def all_heroes(self) -> List[Hero]:
        """Return primary + support heroes for bonus/skill aggregation."""
        return list(self.heroes.values()) + self.support_heroes

    def _create_troop_groups(self) -> Dict[str, TroopGroup]:
        """
        Creates TroopGroup instances based on ratios and total capacity.
        """
        groups: Dict[str, TroopGroup] = {}
        for t in ["Infantry", "Lancer", "Marksman"]:
            ratio = self.troop_ratios.get(t, 0.0)
            count = int(self.total_capacity * ratio)
            troop_def = self._get_highest_fc_troop(t)
            groups[t] = TroopGroup(troop_def, count)
        return groups

    def _get_highest_fc_troop(self, troop_type: str) -> TroopDefinition:
        """
        Finds the highest Formation Class (FC) troop for the given type.
        """
        # Include any definition key that contains the troop_type
        candidates = [
            name for name in self.troop_definitions
            if troop_type in name
        ]

        if not candidates:
            raise ValueError(f"No troop definitions found for type '{troop_type}'")

        def fc_num(name: str) -> int:
            m = re.search(r"FC(\d+)", name)
            return int(m.group(1)) if m else 0

        best = max(candidates, key=fc_num)
        tdict = self.troop_definitions[best]  # This is a dict with keys Power, Attack, etc.

        return TroopDefinition(
            name=best,
            power=tdict["Power"],
            attack=tdict["Attack"],
            defense=tdict["Defense"],
            lethality=tdict["Lethality"],
            health=tdict["Health"],
            stat_bonuses=tdict["StatBonuses"]
        )

# Alias for backward compatibility
Formation = RallyFormation
