"""
Immutable hero profile with helper methods.
NO SECTION ABBREVIATED.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from expedition_battle_mechanics.definitions import Skill, ExclusiveWeapon


@dataclass(slots=True)
class Hero:
    # ───── static identity ────────────────────────────────────────────────
    name: str
    char_class: str                  # "Infantry" | "Lancer" | "Marksman"
    rarity: str
    generation: int
    base_stats: Dict[str, float]

    # ───── skills & weapon ────────────────────────────────────────────────
    skills: Dict[str, List[Skill]]              # {"exploration":[…], "expedition":[…]}
    exclusive_weapon: Optional[ExclusiveWeapon] = None

    # ───── selections (set by loader) ─────────────────────────────────────
    selected_skill_levels: Dict[str, int] = field(default_factory=dict)
    selected_ew_level: Optional[int] = None

    # ───── runtime metadata (populated by CombatState / Formation)─────────
    side: str = ""                               # "atk" or "def" (set later)

    # ───── helpers ────────────────────────────────────────────────────────
    def get_stat(self, key: str, default: float = 0.0) -> float:
        return self.base_stats.get(key, default)

    def skills_pct(self, name: str, lvl: int) -> float:
        for branch in ("exploration", "expedition"):
            for sk in self.skills.get(branch, []):
                if sk.name == name:
                    lp = sk.extra.get("level_percentage", {})
                    val = lp.get(lvl, sk.multiplier)
                    return val if isinstance(val, (int, float)) else 0.0
        return 0.0

    def has_skill(self, name: str) -> bool:
        return any(sk.name == name for lst in self.skills.values() for sk in lst)
