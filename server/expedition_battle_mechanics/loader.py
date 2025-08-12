"""
hero_from_dict — translate a raw HEROES entry into a Hero instance.

➤ 2025-06-26 fix:
    _parse_skill now accepts level_percentage as either
       • dict {1: 0.06, 2: 0.12, …}
       • single float 0.75
"""

from __future__ import annotations

from typing import Dict, Any, Optional, List, Union

from .definitions import Skill, ExclusiveWeapon
from .hero import Hero

# raw data registry
try:
    from ..hero_data.hero_loader import HEROES
except ImportError:  # fallback when imported outside package context
    from hero_data.hero_loader import HEROES  # type: ignore


# ─────────────────────────────────────────────────────────────────────────────
# helpers
# ─────────────────────────────────────────────────────────────────────────────
def _normalize_level_pct(val: Union[float, Dict[int, Any]]) -> Dict[int, Any]:
    """Return a level→value mapping for the ``level_percentage`` field.

    ``hero_data`` is not completely uniform – some expedition skills express
    multiple percentages per level (e.g. different values for Infantry and
    Marksmen).  Prior to this fix ``_normalize_level_pct`` attempted to cast
    every value to ``float`` which blew up when encountering those nested
    dictionaries.  The battle engine only requires the mapping structure so we
    preserve complex entries instead of casting them.

    Examples
    --------
    0.75                       → {1: 0.75}
    {1: 0.06, 2: 0.12}         → {1: 0.06, 2: 0.12}
    {1: {"a": 1.0}}            → {1: {"a": 1.0}}
    """
    if isinstance(val, dict):
        out: Dict[int, Any] = {}
        for k, v in val.items():
            if isinstance(v, dict):
                out[int(k)] = {sk: float(sv) for sk, sv in v.items()}
            elif v is None:
                out[int(k)] = 0.0
            else:
                out[int(k)] = float(v)
        return out
    if val is None:
        return {}
    return {1: float(val)}


def _parse_skill(node: dict) -> Skill:
    lp_raw = node.get("level_percentage", {})
    level_pct = _normalize_level_pct(lp_raw)
    max_lvl = max(level_pct) if level_pct else 1
    mult = level_pct.get(max_lvl, 0.0)
    if isinstance(mult, dict):
        mult = 0.0  # complex skills expose details via ``extra`` only

    return Skill(
        name=node["skill-name"],
        multiplier=mult,
        proc_chance=node.get("proc_chance", 0.0) or node.get("chance", 0.0),
        description=node.get("description", ""),
        extra={
            "level_percentage": level_pct,
            **{k: v for k, v in node.items() if k not in {
                "skill-name", "description", "level_percentage",
                "proc_chance", "chance"
            }},
        },
    )


def _build_skill_list(raw: dict,
                      branch: str,
                      overrides: dict | None) -> List[Skill]:
    out: List[Skill] = []
    for node in raw.get("skills", {}).get(branch, {}).values():
        sk = _parse_skill(node)
        if overrides and sk.name in overrides:
            lvl = overrides[sk.name]
            sk.multiplier = sk.extra["level_percentage"].get(lvl, sk.multiplier)
        out.append(sk)
    return out


def _select_ew(raw: dict, ew_level: Optional[int]) -> Optional[ExclusiveWeapon]:
    ew_root = raw.get("exclusive-weapon")
    if not ew_root or "levels" not in ew_root:
        return None

    levels = ew_root["levels"]
    idx = (ew_level - 1) if ew_level and 1 <= ew_level <= len(levels) else len(levels) - 1
    blk = levels[idx]

    perks = {k: v for k, v in blk.items()
             if k.endswith(("-health", "-lethality"))}

    ew_skill = None
    sk_node = blk.get("skills", {}).get("expedition")
    if sk_node:
        ew_skill = _parse_skill(sk_node)

    return ExclusiveWeapon(
        name=ew_root["name"],
        level=blk["level"],
        power=blk.get("power", 0),
        attack=blk.get("attack", 0),
        defense=blk.get("defense", 0),
        health=blk.get("health", 0),
        perks=perks,
        skills={"expedition": ew_skill} if ew_skill else {},
    )


# ─────────────────────────────────────────────────────────────────────────────
# public factory
# ─────────────────────────────────────────────────────────────────────────────
def hero_from_dict(hero_data: dict | list,
                   skill_levels: Optional[Dict[str, int]] = None,
                   ew_level: Optional[int] = None) -> Hero:
    """
    Convert raw HEROES entry into a Hero with resolved skills/EW level.
    """
    raw = hero_data[0] if isinstance(hero_data, list) else hero_data

    name = raw["hero-name"]
    char_class = raw["hero-class"].capitalize()
    rarity = raw.get("rarity", "SSR")
    generation = raw.get("generation", 0)
    base_stats = raw.get("base-stats", {})

    skill_levels = skill_levels or {}

    exploration = _build_skill_list(raw, "exploration", skill_levels)
    expedition  = _build_skill_list(raw, "expedition",  skill_levels)

    ew = _select_ew(raw, ew_level)
    if ew and ew.skills.get("expedition"):
        expedition.append(ew.skills["expedition"])

    return Hero(
        name=name,
        char_class=char_class,
        rarity=rarity,
        generation=generation,
        base_stats=base_stats,
        skills={"exploration": exploration, "expedition": expedition},
        exclusive_weapon=ew,
        selected_skill_levels=skill_levels,
        selected_ew_level=ew_level,
    )
