"""
Passive expedition skills that are always “on”.
Each handler receives
    hero : Hero                – owning hero
    lvl  : int                 – skill level (1-5, we default to 5)
    add  : Callable[key, pct]  – collect a stat bonus or debuff

The collector understands four kinds of keys:
    "attack" | "defense" | "health" | "lethality"
        → buff applied to the hero’s entire side
    "Infantry-defense" (etc.)
        → buff applied only to that troop class of the hero’s side
    "enemy-attack-down" | "enemy-defense-down"
        → debuff applied to the *opposing* side
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
    """EW passive – Defender troops DEF ↑"""
    if hero.side == "def":                       # only if Gatot is defending
        pct = hero.skills_pct("Indestructible City", lvl)
        add("defense", pct)


# Hendrik (already in engine but kept here for clarity)
def worms_ravage(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Worm's Ravage", lvl)
    add("enemy-defense-down", pct)


def abyssal_blessing(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Abyssal Blessing", lvl)
    add("attack", pct)


# registry -------------------------------------------------------------------
PASSIVE_SKILLS: Dict[str, Callable[[Hero, int, AddFn], None]] = {
    "Golden Guard":          golden_guard,
    "Royal Legion":          royal_legion,
    "Indestructible City":   indestructible_city,
    "Worm's Ravage":         worms_ravage,
    "Abyssal Blessing":      abyssal_blessing,
}
