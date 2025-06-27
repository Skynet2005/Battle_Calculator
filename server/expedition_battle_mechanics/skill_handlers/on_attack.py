"""
ON_ATTACK skill handlers – updated to use `state.add_extra_damage`.
FULL FILE, nothing abbreviated.
"""

from __future__ import annotations
import random
from typing import Dict, Callable, Any

from expedition_battle_mechanics.hero import Hero
from expedition_battle_mechanics.troop import TroopGroup

Handler = Callable[[Any, str, TroopGroup, Hero, int], None]  # state, side, tg, hero, lvl

# ─────────────────────────────────────────────────────────────────────────────
def kings_bestowal(state: Any, side: str, tg: TroopGroup, hero: Hero, lvl: int) -> None:
    pct = hero.skills_pct("King's Bestowal", lvl)
    tg.shield = getattr(tg, "shield", 0.0) + hero.get_stat("attack") * pct
    state._proc("King's Bestowal", side, tg.class_name)

# ─────────────────────────────────────────────────────────────────────────────
def torrential_impact(state: Any, side: str, tg: TroopGroup, hero: Hero, lvl: int) -> None:
    if tg.class_name != "Lancer":
        return
    if random.random() >= 0.20:
        return
    pct = hero.skills_pct("Torrential Impact", lvl)
    extra = hero.get_stat("attack") * pct * tg.count
    state.add_extra_damage(side, extra)
    state._proc("Torrential Impact", side, tg.class_name)

# ─────────────────────────────────────────────────────────────────────────────
def bounty_temptation(state: Any, side: str, tg: TroopGroup, hero: Hero, lvl: int) -> None:
    if tg.class_name != "Lancer":
        return
    if random.random() >= 0.50:
        return
    pct = hero.skills_pct("Bounty Temptation", lvl)
    extra = hero.get_stat("attack") * pct * tg.count
    state.add_extra_damage(side, extra)
    state._proc("Bounty Temptation", side, tg.class_name)

# --------------------------------------------------------------------------- #
ON_ATTACK: Dict[str, Handler] = {
    "King's Bestowal":  kings_bestowal,
    "Torrential Impact": torrential_impact,
    "Bounty Temptation": bounty_temptation,
}
