"""
Data-model definitions for the expedition battle engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, Any


# ─────────────────────────────────────────────────────────────────────────────
# Troop definitions
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class TroopDefinition:
    """
    Immutable base stats for one troop tier (e.g. “Infantry FC-9”).
    """
    name: str
    power: float
    attack: float
    defense: float
    lethality: float
    health: float
    stat_bonuses: Dict[str, float] = field(
        default_factory=lambda: {
            "attack": 0.0,
            "defense": 0.0,
            "lethality": 0.0,
            "health": 0.0,
        }
    )


# ─────────────────────────────────────────────────────────────────────────────
# Skill & Exclusive-Weapon
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class Skill:
    """
    Generic skill container (heroes or exclusive weapons).

    multiplier   – % of ATK/DEF/etc. expressed as 0-1 float
    proc_chance  – 0 → passive; otherwise chance per attack/round
    extra        – any additional numeric fields (crit, shield %, etc.)
    resolver     – optional callback(state, side, troop_group, hero, skill_lvl)
    """
    name: str
    multiplier: float
    proc_chance: float = 0.0
    description: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)
    resolver: Optional[Callable] = None


@dataclass
class ExclusiveWeapon:
    """
    Stats/perks at a *specific* EW level.
    """
    name: str
    level: int
    power: int
    attack: int
    defense: int
    health: int
    perks: Dict[str, float] = field(default_factory=dict)
    skills: Dict[str, Skill] = field(default_factory=dict)   # expedition only
