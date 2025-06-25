# battle_mechanics/loader.py

from typing import Dict, Any, Optional
from expedition_battle_mechanics.definitions import Skill, ExclusiveWeapon
from expedition_battle_mechanics.hero import Hero

# This points to the raw hero data:
from hero_data.hero_loader import HEROES

def hero_from_dict(
    hero_data: Any,
    skill_levels: Optional[Dict[str, int]] = None,
    ew_level: Optional[int] = None
) -> Hero:
    """
    Converts a hero dict (or list of dicts) to a Hero object,
    including both base and exclusive‐weapon skills.
    """
    if isinstance(hero_data, list):
        hero_dict = hero_data[0]
    else:
        hero_dict = hero_data

    name       = hero_dict.get('hero-name')
    char_class = hero_dict.get('hero-class', '').capitalize()
    rarity     = hero_dict.get('rarity')
    generation = hero_dict.get('generation')
    base_stats = hero_dict.get('base-stats', {})

    # Build skill lists
    skills = {"exploration": [], "expedition": []}
    for sk_type in ("exploration", "expedition"):
        for sk in (hero_dict.get('skills', {}) or {}).get(sk_type, {}).values():
            lvl = max(sk.get('level_percentage', {}).keys(), default=None)
            multiplier = sk.get('level_percentage', {}).get(lvl, 0.0)
            proc = sk.get('proc_chance', 0.0)
            skills[sk_type].append(Skill(sk['skill-name'], multiplier, proc))

    # Parse exclusive weapon
    ew = hero_dict.get('exclusive-weapon')
    ew_obj = None
    ew_skills: Dict[str, Skill] = {}
    if ew and 'levels' in ew:
            levels = ew['levels']
            # choose the requested EW level (or highest)
            idx = (ew_level - 1) if ew_level and 1 <= ew_level <= len(levels) else len(levels) - 1
            data = levels[idx]

            # build stat bonuses dict
            stat_bonuses = {
                k.replace('infantry-', '').replace('marksman-', '').replace('lancer-', ''): v
                for k,v in data.items()
                if k.endswith('-health') or k.endswith('-lethality')
            }

            # pull out any exploration/expedition skills on the weapon
            for sk_type in ("exploration", "expedition"):
                sk_info = data.get('skills', {}).get(sk_type)
                if sk_info:
                    mp = sk_info.get('level_percentage', 0.0)
                    ew_skills[sk_type] = Skill(sk_info['skill-name'], mp, sk_info.get('proc_chance', 0.0))

            ew_obj = ExclusiveWeapon(
                level      = data.get('level'),
                power      = data.get('power', 0),
                attack     = data.get('attack', 0),
                defense    = data.get('defense', 0),
                health     = data.get('health', 0),
                stat_bonuses = stat_bonuses,
                skills     = ew_skills
            )

            # ————— Merge EW skills into the hero’s lists —————
            for sk_type, sk in ew_skills.items():
                skills.setdefault(sk_type, []).append(sk)

    return Hero(
        name=name,
        char_class=char_class,
        rarity=rarity,
        generation=generation,
        base_stats=base_stats,
        skills=skills,
        exclusive_weapon=ew_obj,
        selected_skill_levels=skill_levels,
        selected_ew_level=ew_level
    )
