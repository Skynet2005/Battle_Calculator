"""
TroopGroup – runtime wrapper around TroopDefinition.
NO SECTION ABBREVIATED.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from expedition_battle_mechanics.definitions import TroopDefinition


@dataclass
class TroopGroup:
    # ───── immutable reference ────────────────────────────────────────────
    definition: TroopDefinition
    count: int

    # ───── derived, auto-filled in __post_init__ ───────────────────────────
    class_name: str = field(init=False)          # Infantry / Lancer / Marksman

    # ───── runtime mutables (hero & troop skills) ─────────────────────────
    shield: float = 0.0                          # running shield HP
    reflect_pct: float = 0.0                     # % of dmg reflected

    temp_def_bonus: float = 0.0                  # +DEF% lasting N turns
    temp_def_bonus_turns: int = 0                # countdown

    # ───── helpers ────────────────────────────────────────────────────────
    def __post_init__(self):
        lower = self.definition.name.lower()
        if "infantry" in lower:
            self.class_name = "Infantry"
        elif "lancer" in lower:
            self.class_name = "Lancer"
        else:
            self.class_name = "Marksman"

    def is_alive(self) -> bool:
        return self.count > 0

    def take_losses(self, n: int) -> None:
        self.count = max(self.count - n, 0)
