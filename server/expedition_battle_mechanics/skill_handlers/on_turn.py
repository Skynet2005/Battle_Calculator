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

# ─────────────────────────────────────────────────────────────────────────────
ON_TURN: Dict[str, Handler] = {
    "Armor of Barnacles": armor_of_barnacles,
    "Dragon's Heir":      dragons_heir,
}
