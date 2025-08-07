import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "server"))

import hero_data.hero_loader as hl
import pytest
from expedition_battle_mechanics.loader import hero_from_dict


def test_complex_level_percentage_skills_load():
    """Heroes with nested level_percentage mappings should still load."""

    for name in ["Hector", "Ahmose", "Wayne"]:
        hero = hero_from_dict(hl.HEROES[name])
        assert len(hero.skills["expedition"]) >= 3
        for sk in hero.skills["expedition"]:
            lvl = hero.selected_skill_levels.get(sk.name, 5)
            assert isinstance(hero.skills_pct(sk.name, lvl), float)


def test_all_expedition_skills_have_level_percentage():
    for hero_name, data in hl.HEROES.items():
        for sk in data.get("skills", {}).get("expedition", {}).values():
            assert "level_percentage" in sk, f"{hero_name} {sk['skill-name']}"
        ew = data.get("exclusive-weapon") or {}
        for lvl in ew.get("levels", []):
            exp = lvl.get("skills", {}).get("expedition")
            if exp:
                assert "level_percentage" in exp, f"{hero_name} {exp['skill-name']}"


def test_missing_skill_percentages_present():
    philly = hero_from_dict(hl.HEROES["Philly"])
    assert philly.skills_pct("Vigor Tactics", 5) == pytest.approx(0.15)

    edith = hero_from_dict(hl.HEROES["Edith"])
    assert edith.skills_pct("Strategic Balance", 5) == pytest.approx(0.20)

    bradley = hero_from_dict(hl.HEROES["Bradley"])
    assert bradley.skills_pct("Power Shot", 5) == pytest.approx(0.30)
    assert bradley.skills_pct("Siege Insight", 1) == pytest.approx(0.15)

    gordon = hero_from_dict(hl.HEROES["Gordon"])
    assert gordon.skills_pct("Toxic Release", 5) == pytest.approx(0.30)
    assert gordon.skills_pct("Bio Assault", 1) == pytest.approx(0.15)

    wu = hero_from_dict(hl.HEROES["Wu Ming"])
    assert wu.skills_pct("Shadow's Evasion", 5) == pytest.approx(0.25)
