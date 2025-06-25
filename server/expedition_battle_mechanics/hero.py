# battle_mechanics/hero.py

from typing import Dict, List, Optional
from expedition_battle_mechanics.definitions import Skill, ExclusiveWeapon

class Hero:
    """
    Represents a hero with base stats, skills (both exploration and expedition),
    and an optional exclusive weapon.
    """
    def __init__(
        self,
        name: str,
        char_class: str,
        rarity: str,
        generation: int,
        base_stats: Dict[str, float],
        skills: Dict[str, List[Skill]],
        exclusive_weapon: Optional[ExclusiveWeapon] = None,
        selected_skill_levels: Optional[Dict[str, int]] = None,
        selected_ew_level: Optional[int] = None
    ):
        self.name = name
        self.char_class = char_class
        self.rarity = rarity
        self.generation = generation
        self.base_stats = base_stats
        self.skills = skills  # {"exploration": [...], "expedition": [...]}
        self.exclusive_weapon = exclusive_weapon
        self.selected_skill_levels = selected_skill_levels or {}
        self.selected_ew_level = selected_ew_level
