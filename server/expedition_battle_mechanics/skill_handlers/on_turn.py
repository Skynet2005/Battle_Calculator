"""
ON_TURN skill handlers – now deposit extra damage via state.add_extra_damage
FULL FILE, nothing abbreviated.
"""

from typing import Dict, Callable, Any
from expedition_battle_mechanics.hero import Hero
from expedition_battle_mechanics.troop import TroopGroup

Handler = Callable[[Any, Hero, int], None]      # state, hero, lvl

# ─────────────────────────────────────────────────────────────────────────────
def armor_of_barnacles(state: Any, hero: Hero, lvl: int) -> None:
    if state.turn % 4:
        return
    pct = hero.skills_pct("Armor of Barnacles", lvl)
    for tg in state.get_side_groups(hero):
        tg.temp_def_bonus = pct
        tg.temp_def_bonus_turns = 2
    state._proc("Armor of Barnacles", hero.side)

# --------------------------------------------------------------------------- #
def dragons_heir(state: Any, hero: Hero, lvl: int) -> None:
    if state.turn % 3:
        return
    base = hero.get_stat("attack") * hero.skills_pct("Dragon's Heir", lvl)
    for tg in state.get_enemy_groups(hero):
        extra = base * tg.count
        state.add_extra_damage(hero.side, extra)
    state._proc("Dragon's Heir", hero.side)

# --------------------------------------------------------------------------- #
def chemical_terror(state: Any, hero: Hero, lvl: int) -> None:
    if state.turn % 3:
        return
    pct = hero.skills_pct("Chemical Terror", lvl)
    state.add_temp_bonus(hero.side, "Lancer-attack", pct, 1)
    sk = next(s for s in hero.skills["expedition"] if s.name == "Chemical Terror")
    enemy_red = sk.extra.get("enemy_damage_reduction", {}).get(str(lvl), 0.0)
    enemy_side = "def" if hero.side == "atk" else "atk"
    state.add_temp_bonus(enemy_side, "attack", -enemy_red, 1)
    state._proc("Chemical Terror", hero.side)

# --------------------------------------------------------------------------- #
def toxic_release(state: Any, hero: Hero, lvl: int) -> None:
    if state.turn % 4:
        return
    sk = next(s for s in hero.skills["expedition"] if s.name == "Toxic Release")
    inf_inc = sk.extra.get("damage_taken_increase", {}).get(str(lvl), 0.0)
    marks_red = sk.extra.get("marksmen_damage_reduction", {}).get(str(lvl), 0.0)
    enemy_side = "def" if hero.side == "atk" else "atk"
    state.add_temp_bonus(enemy_side, "Infantry-defense", -inf_inc, 2)
    state.add_temp_bonus(enemy_side, "Marksman-attack", -marks_red, 2)
    state._proc("Toxic Release", hero.side)

# ─────────────────────────────────────────────────────────────────────────────
ON_TURN: Dict[str, Handler] = {
    "Armor of Barnacles": armor_of_barnacles,
    "Dragon's Heir":      dragons_heir,
    "Chemical Terror":    chemical_terror,
    "Toxic Release":      toxic_release,
}
