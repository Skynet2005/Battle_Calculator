"""
Executed once per *full* round, after both sides have attacked.
Keeps a per-hero turn counter in CombatState.turn_tracker.
NO SECTION ABBREVIATED.
"""

from typing import Dict, Callable, Any
from expedition_battle_mechanics.hero import Hero
from expedition_battle_mechanics.troop import TroopGroup

Handler = Callable[[Any, Hero, int], None]   # state, hero, lvl

# --------------------------------------------------------------------------- #
def armor_of_barnacles(state, hero: Hero, lvl: int):
    if state.turn % 4 != 0:      # triggers every 4th turn starting turn 0
        return
    pct = hero.skills_pct("Armor of Barnacles", lvl)
    for tg in state.get_side_groups(hero):   # helper we’ll add below
        tg.temp_def_bonus = pct             # lasts 2 turns
    state._proc("Armor of Barnacles", hero.side)

def dragons_heir(state, hero: Hero, lvl: int):
    if state.turn % 3 != 0:
        return
    pct = hero.skills_pct("Dragon's Heir", lvl)
    dmg = hero.get_stat("attack") * pct
    # evenly split across all enemy groups
    for tg in state.get_enemy_groups(hero):
        state.pending_extra_damage += dmg * tg.count
    state._proc("Dragon's Heir", hero.side)

ON_TURN: Dict[str, Handler] = {
    "Armor of Barnacles": armor_of_barnacles,
    "Dragon's Heir": dragons_heir,
}
