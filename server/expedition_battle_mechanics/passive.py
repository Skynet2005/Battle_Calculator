"""
Passive expedition skills that are always “on”.
"""

from typing import Dict, Callable
from .hero import Hero

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
# Jessie (Epic) – rally meta joiner
# Created Logic for review: Model Jessie's expedition passives as flat % bonuses.
def stand_of_arms(hero: Hero, lvl: int, add: AddFn) -> None:
    """Jessie increases damage dealt → approximate as +attack% (flat)."""
    pct = hero.skills_pct("Stand of Arms", lvl)
    add("attack", pct)


def bulwarks(hero: Hero, lvl: int, add: AddFn) -> None:
    """Jessie reduces damage taken → approximate as +defense% (flat)."""
    pct = hero.skills_pct("Bulwarks", lvl)
    add("defense", pct)


# ─────────────────────────────────────────────────────────────────────────────
# Gwen – expedition passives
# Created Logic for review:
# - Eagle Vision: increases target's damage taken → enemy-defense-down
# - Air Dominance: after every 5 attacks grant extra damage → model as flat damage% for all troops
# - Blastmaster: every 4 attacks add extra damage → model as flat damage% for Marksmen
def eagle_vision(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Eagle Vision", lvl)
    add("enemy-defense-down", pct)


def air_dominance(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Air Dominance", lvl)
    # Apply as generic damage% so it boosts all classes' output
    add("damage", pct)


def blastmaster(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Blastmaster", lvl)
    add("Marksman-damage", pct)


# Gwen EW expedition: "Marauder" – Rally Troops Lethality up
def marauder(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Marauder", lvl)
    add("lethality", pct)


# ─────────────────────────────────────────────────────────────────────────────
# Renee – expedition passives moved to ON_TURN timing (see on_turn.py)
def nightmare_trace(hero: Hero, lvl: int, add: AddFn) -> None:
    return  # timing-based; handled in on_turn


def dreamcatcher(hero: Hero, lvl: int, add: AddFn) -> None:
    return  # timing-based; handled in on_turn


def dreamslice(hero: Hero, lvl: int, add: AddFn) -> None:
    return  # timing-based; handled in on_turn


# Renee EW expedition: "Wistful Enhancement" – Rally Troops' Lethality up
def wistful_enhancement(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Wistful Enhancement", lvl)
    add("lethality", pct)


# ─────────────────────────────────────────────────────────────────────────────
# Patrick (Epic) – defensive joiner
# Created Logic for review: Model Patrick's expedition passives as flat % bonuses.
def super_nutrients(hero: Hero, lvl: int, add: AddFn) -> None:
    """Patrick increases Health for all troops."""
    pct = hero.skills_pct("Super Nutrients", lvl)
    add("health", pct)


def caloric_booster(hero: Hero, lvl: int, add: AddFn) -> None:
    """Patrick increases Attack for all troops."""
    pct = hero.skills_pct("Caloric Booster", lvl)
    add("attack", pct)


# ─────────────────────────────────────────────────────────────────────────────
# Reina – expedition passives
# Created Logic for review:
# - Assassin's Instinct: normal attack damage up → model as generic damage%
# - Swift Jive: chance to dodge normals → approximate as enemy-attack-down at 50% weight of listed chance
# - Shadow Blade: 25% chance extra lancer attack for [120–200]% → expected value as Lancer-damage = 0.25 * multiplier
def assassins_instinct(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Assassin's Instinct", lvl)
    add("damage", pct)


def swift_jive(hero: Hero, lvl: int, add: AddFn) -> None:
    chance = hero.skills_pct("Swift Jive", lvl)
    add("enemy-attack-down", chance * 0.5)  # Created Logic for review


def shadow_blade(hero: Hero, lvl: int, add: AddFn) -> None:
    mult = hero.skills_pct("Shadow Blade", lvl)
    expected = 0.25 * mult  # 25% proc chance
    add("Lancer-damage", expected)


# Reina EW expedition: "Fiery Invasion" – Rally Troop Lethality up
def fiery_invasion(hero: Hero, lvl: int, add: AddFn) -> None:
    pct = hero.skills_pct("Fiery Invasion", lvl)
    add("lethality", pct)


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
    # Jessie
    "Stand of Arms":        stand_of_arms,
    "Bulwarks":             bulwarks,
    # Patrick
    "Super Nutrients":      super_nutrients,
    "Caloric Booster":      caloric_booster,
    # Bradley
    "Power Shot":           power_shot,
    "Siege Insight":        siege_insight,
    # Gwen
    "Eagle Vision":         eagle_vision,
    "Air Dominance":        air_dominance,
    "Blastmaster":          blastmaster,
    # Gwen EW
    "Marauder":             marauder,
    # Renee
    "Nightmare Trace":      nightmare_trace,
    "Dreamcatcher":         dreamcatcher,
    "Dreamslice":           dreamslice,
    # Renee EW
    "Wistful Enhancement":  wistful_enhancement,
    # Reina
    "Assassin's Instinct":  assassins_instinct,
    "Swift Jive":           swift_jive,
    "Shadow Blade":         shadow_blade,
    # Reina EW
    "Fiery Invasion":       fiery_invasion,
}

# ─────────────────────────────────────────────────────────────────────────────
# Strategy mapping for passive skills
# ─────────────────────────────────────────────────────────────────────────────
from .stacking import AdditiveStrategy, MaxStrategy

# Skills that use MaxStrategy (non-stacking)
MAX_STRATEGY_SKILLS = {
    "Royal Legion",      # enemy attack down - doesn't stack
    "Worm's Ravage",     # enemy defense down - doesn't stack
    "Power Shot",        # enemy defense down - doesn't stack
    "Abyssal Blessing",  # attack up - use highest value across heroes
    # For damage-taken debuffs and damage multipliers, keep additive unless balance requires max
}

def get_passive_strategy(skill_name: str):
    """Return the stacking strategy for a given passive skill."""
    if skill_name in MAX_STRATEGY_SKILLS:
        return MaxStrategy()
    return AdditiveStrategy()
