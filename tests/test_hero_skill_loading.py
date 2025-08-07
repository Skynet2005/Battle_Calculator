import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "server"))

import hero_data.hero_loader as hl
from expedition_battle_mechanics.loader import hero_from_dict


def test_complex_level_percentage_skills_load():
    # Heroes such as Hector, Ahmose and Wayne have expedition skills whose
    # level_percentage field is a nested mapping (multiple values per level).
    # Ensure these load without error and expose at least three expedition
    # skills once converted into Hero instances.
    for name in ["Hector", "Ahmose", "Wayne"]:
        hero = hero_from_dict(hl.HEROES[name])
        assert len(hero.skills["expedition"]) >= 3
        # skills_pct should always yield a float even for complex skills
        for sk in hero.skills["expedition"]:
            lvl = hero.selected_skill_levels.get(sk.name, 5)
            pct = hero.skills_pct(sk.name, lvl)
            assert isinstance(pct, float)
