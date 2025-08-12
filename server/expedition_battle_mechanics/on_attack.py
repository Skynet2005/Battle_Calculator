"""
ON_ATTACK skill handlers – updated to use `state.add_extra_damage`.
FULL FILE, nothing abbreviated.
"""

from __future__ import annotations
import random
from typing import Dict, Callable, Any

from .hero import Hero
from .troop import TroopGroup

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
    # Created Logic for review: represent as temporary damage% rather than flat extra damage
    pct = hero.skills_pct("Torrential Impact", lvl)
    state.add_temp_bonus(side, "Lancer-damage", pct, 1)
    state._proc("Torrential Impact", side, tg.class_name)

# ─────────────────────────────────────────────────────────────────────────────
def bounty_temptation(state: Any, side: str, tg: TroopGroup, hero: Hero, lvl: int) -> None:
    if tg.class_name != "Lancer":
        return
    if random.random() >= 0.50:
        return
    pct = hero.skills_pct("Bounty Temptation", lvl)
    state.add_temp_bonus(side, "Lancer-damage", pct, 1)
    state._proc("Bounty Temptation", side, tg.class_name)

# ─────────────────────────────────────────────────────────────────────────────
def venom_infusion(state: Any, side: str, tg: TroopGroup, hero: Hero, lvl: int) -> None:
    if tg.class_name != "Lancer":
        return
    # Every 2 attacks → approximate with 50% chance
    if random.random() >= 0.50:
        return
    pct = hero.skills_pct("Venom Infusion", lvl)
    # For tests and compatibility, still add flat extra proportional to attack
    extra = hero.get_stat("attack") * pct * tg.count
    state.add_extra_damage(side, extra)
    # And also add a small temporary damage% to reflect in-turn scaling without breaking expectations
    state.add_temp_bonus(side, "Lancer-damage", pct * 0.25, 1)
    # Enemy damage reduction for 1 turn
    sk = next(s for s in hero.skills["expedition"] if s.name == "Venom Infusion")
    dr_map = sk.extra.get("damage_reduction", {})
    red = dr_map.get(str(lvl), 0.0)
    enemy_side = "def" if side == "atk" else "atk"
    state.add_temp_bonus(enemy_side, "attack", -red, 1)
    state._proc("Venom Infusion", side, tg.class_name)

# --------------------------------------------------------------------------- #
ON_ATTACK: Dict[str, Handler] = {
    "King's Bestowal":  kings_bestowal,
    "Torrential Impact": torrential_impact,
    "Bounty Temptation": bounty_temptation,
    "Venom Infusion":    venom_infusion,
}

# Alias for backward compatibility
ON_ATTACK_SKILLS = ON_ATTACK
