"""
Data-model definitions for the expedition battle engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, Any, List


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


# ─────────────────────────────────────────────────────────────────────────────
# Battle Report Structures
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class PowerDelta:
    """Power tracking for start/end/difference."""
    attacker: Dict[str, int] = field(default_factory=lambda: {"start": 0, "end": 0})
    defender: Dict[str, int] = field(default_factory=lambda: {"start": 0, "end": 0})
    difference: Dict[str, int] = field(default_factory=lambda: {"start": 0, "end": 0})


@dataclass
class SideSummary:
    """Summary statistics for one side."""
    start: int = 0
    end: int = 0
    losses: int = 0
    loss_pct: float = 0.0
    kills: int = 0
    kill_pct: float = 0.0


@dataclass
class Report:
    """Complete battle report structure."""
    attacker_formation: Any = None  # Formation
    defender_formation: Any = None  # Formation
    attacker: Dict[str, Any] = field(default_factory=dict)
    defender: Dict[str, Any] = field(default_factory=dict)
    power: PowerDelta = field(default_factory=PowerDelta)
    passive_effects: Dict[str, Dict[str, List[str]]] = field(default_factory=dict)
    bonuses: Dict[str, Dict[str, float]] = field(default_factory=dict)
    proc_stats: Dict[str, Dict[str, Dict[str, int]]] = field(default_factory=dict)
    timeline: List[Dict[str, Any]] = field(default_factory=list)
    rounds: int = 0
    winner: str = ""


@dataclass
class BattleReportInput:
    """Input structure for battle simulation."""
    attacker_formation: Any = None  # Formation
    defender_formation: Any = None  # Formation
    attacker_bonuses: Dict[str, float] = field(default_factory=dict)
    defender_bonuses: Dict[str, float] = field(default_factory=dict)
