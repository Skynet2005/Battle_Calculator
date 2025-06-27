"""
Passive expedition skills that are always “on”.
"""

from typing import Dict, Callable
from expedition_battle_mechanics.hero import Hero

AddFn = Callable[[str, float], None]

# ─────────────────────────────────────────────────────────────────────────────
# Gatot
def golden_guard(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Golden Guard", lvl)
    add("Infantry-defense", pct)


def royal_legion(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Royal Legion", lvl)
    add("enemy-attack-down", pct)


def indestructible_city(hero: Hero, lvl: int, add: AddFn) -> None:
    if hero.side == "def":
        pct = hero.skills_pct("Indestructible City", lvl)
        add("defense", pct)

# ─────────────────────────────────────────────────────────────────────────────
# Hendrik
def worms_ravage(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Worm's Ravage", lvl)
    add("enemy-defense-down", pct)


def abyssal_blessing(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Abyssal Blessing", lvl)
    add("attack", pct)

# ─────────────────────────────────────────────────────────────────────────────
# Sonya
def treasure_hunter(hero: Hero, lvl: int, add: AddFn) -> None:
    """
    Treasure Hunter – flat damage boost for the entire side.
    Modeled as +ATK%.
    """
    pct = hero.skills_pct("Treasure Hunter", lvl)
    add("attack", pct)


def bio_assault(hero: Hero, lvl: int, add: AddFn) -> None:
    """
    Bio Assault – Mangrove Frog EW passive.
    Applies only while Sonya is DEFENDING.
    Grants +Lethality% to the defender’s whole army.
    """
    if hero.side == "def":
        pct = hero.skills_pct("Bio Assault", lvl)
        add("lethality", pct)

# ─────────────────────────────────────────────────────────────────────────────
PASSIVE_SKILLS: Dict[str, Callable[[Hero, int, AddFn], None]] = {
    # Gatot
    "Golden Guard":         golden_guard,
    "Royal Legion":         royal_legion,
    "Indestructible City":  indestructible_city,
    # Hendrik
    "Worm's Ravage":        worms_ravage,
    "Abyssal Blessing":     abyssal_blessing,
    # Sonya
    "Treasure Hunter":      treasure_hunter,
    "Bio Assault":          bio_assault,
}
