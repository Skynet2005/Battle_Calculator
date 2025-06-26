"""
Handlers executed whenever a troop *attacks*.

CRITICAL CHANGE:
– No longer imports CombatState directly (breaks circular import).
Type hints use `typing.Any` so static checkers remain quiet.
"""

from __future__ import annotations

import random
from typing import Dict, Callable, Any

from expedition_battle_mechanics.hero import Hero
from expedition_battle_mechanics.troop import TroopGroup

# State is typed as Any to avoid circular reference
Handler = Callable[[Any, str, TroopGroup, Hero, int], None]

# ─────────────────────────────────────────────────────────────────────────────
def kings_bestowal(state: Any,
                   side: str,
                   tg: TroopGroup,
                   hero: Hero,
                   lvl: int) -> None:
    pct = hero.skills_pct("King's Bestowal", lvl)
    tg.shield = getattr(tg, "shield", 0.0) + hero.get_stat("attack") * pct
    state._proc("King's Bestowal", side)


def torrential_impact(state: Any,
                      side: str,
                      tg: TroopGroup,
                      hero: Hero,
                      lvl: int) -> None:
    if random.random() >= 0.20:
        return
    pct = hero.skills_pct("Torrential Impact", lvl)
    extra = hero.get_stat("attack") * pct * tg.count
    state.pending_extra_damage += extra
    state._proc("Torrential Impact", side)


# central registry -----------------------------------------------------------
ON_ATTACK: Dict[str, Handler] = {
    "King's Bestowal": kings_bestowal,
    "Torrential Impact": torrential_impact,
    # add more attack-skills here …
}
