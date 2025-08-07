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
    Bio Assault – increases Rally troops' Lethality.

    The in‑game skill only activates while defending.  Earlier revisions
    of the simulator applied it for both sides which inflated attacking
    Gordon/Sonya rallies.  Restrict the bonus to defenders to mirror the
    intended behaviour.
    """
    if hero.side == "def":
        pct = hero.skills_pct("Bio Assault", lvl)
        add("lethality", pct)


# ─────────────────────────────────────────────────────────────────────────────
# Edith
def strategic_balance(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Strategic Balance", lvl)
    add("Marksman-defense", pct)
    add("Lancer-attack", pct)


def ironclad(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Ironclad", lvl)
    add("Infantry-defense", pct)


def steel_sentinel(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Steel Sentinel", lvl)
    for cls in ("Infantry", "Lancer", "Marksman"):
        add(f"{cls}-health", pct)


def fortworks(hero: Hero, lvl: int, add: AddFn) -> None:
    if hero.side == "def":
        pct = hero.skills_pct("Fortworks", lvl)
        add("health", pct)


# ─────────────────────────────────────────────────────────────────────────────
# Bradley
def power_shot(hero: Hero, lvl: int, add: AddFn) -> None:
    sk = next(s for s in hero.skills["expedition"] if s.name == "Power Shot")
    l_map = sk.extra.get("lancer_damage_percentage", {})
    i_map = sk.extra.get("infantry_damage_percentage", {})
    l_pct = l_map.get(str(lvl), hero.skills_pct("Power Shot", lvl))
    i_pct = i_map.get(str(lvl), 0.0)
    add("enemy-lancer_defense-down", l_pct)
    add("enemy-infantry_defense-down", i_pct)


def siege_insight(hero: Hero, lvl: int, add: AddFn) -> None:
    if hero.side == "def":
        pct = hero.skills_pct("Siege Insight", lvl)
        add("attack", pct)

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
    # Edith
    "Strategic Balance":    strategic_balance,
    "Ironclad":             ironclad,
    "Steel Sentinel":       steel_sentinel,
    "Fortworks":            fortworks,
    # Bradley
    "Power Shot":           power_shot,
    "Siege Insight":        siege_insight,
}
