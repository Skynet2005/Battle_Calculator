# battle_mechanics/definitions.py

from typing import Dict, Optional

class TroopDefinition:
    """
    Defines the base stats for a troop type (e.g., Infantry FC1, Marksman FC5, etc.).
    """
    def __init__(
        self,
        name: str,
        power: float,
        attack: float,
        defense: float,
        lethality: float,
        health: float,
        stat_bonuses: Optional[Dict[str, float]] = None
    ):
        self.name = name
        self.power = power
        self.attack = attack
        self.defense = defense
        self.lethality = lethality
        self.health = health
        self.stat_bonuses = stat_bonuses or {
            "attack": 0.0,
            "defense": 0.0,
            "lethality": 0.0,
            "health": 0.0
        }

class Skill:
    """
    Represents a single skill with a damage multiplier and an optional proc chance.
    """
    def __init__(
        self,
        name: str,
        multiplier: float,
        proc_chance: Optional[float] = None
    ):
        self.name = name
        self.multiplier = multiplier
        self.proc_chance = proc_chance or 0.0

class ExclusiveWeapon:
    """
    Represents a hero's exclusive weapon and its stat bonuses and skills.
    """
    def __init__(
        self,
        level: int,
        power: float,
        attack: float,
        defense: float,
        health: float,
        stat_bonuses: Dict[str, float],
        skills: Dict[str, Skill]
    ):
        self.level = level
        self.power = power
        self.attack = attack
        self.defense = defense
        self.health = health
        self.stat_bonuses = stat_bonuses
        self.skills = skills
