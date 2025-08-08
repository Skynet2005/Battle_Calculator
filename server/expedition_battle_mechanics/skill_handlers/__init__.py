"""Utilities shared across skill handler modules.

This file currently exposes a small registry describing how passive skills
should stack when multiple heroes provide the same buff.  The intention is to
mirror in‑game rally rules where certain skills (e.g. flat damage boosts) can
stack additively, while others such as chance‑based procs only apply their best
instance.

The registry can be expanded over time as more skills are analysed.  Unlisted
skills default to additive stacking which matches the behaviour for most flat
percentage bonuses discussed in the design brief.
"""

from __future__ import annotations

from expedition_battle_mechanics.stacking import AdditiveStrategy, MaxStrategy, StackingStrategy


# ---------------------------------------------------------------------------
# Passive skill stacking configuration
# ---------------------------------------------------------------------------
# Mapping: skill name -> stacking strategy.  Only a small subset is modelled
# here; additional entries can be added as new heroes or edge cases are
# discovered.  Any skill missing from the mapping will simply stack additively.

PASSIVE_STACKING: dict[str, StackingStrategy] = {
    # Example of a non‑stacking passive: only the highest "Abyssal Blessing"
    # across all participants should apply.  This mirrors guidance that most
    # identical skills do not stack except for a few explicit exceptions like
    # Jessie/Jasser.
    "Abyssal Blessing": MaxStrategy(),

    # Explicitly mark "Treasure Hunter" as additive to document a stacking
    # exception where multiple copies are allowed.  This is useful for tests
    # and serves as a template for future additive overrides.
    "Treasure Hunter": AdditiveStrategy(),
}


def get_passive_strategy(name: str) -> StackingStrategy:
    """Return the stacking strategy for ``name`` (defaults to additive)."""

    return PASSIVE_STACKING.get(name, AdditiveStrategy())

