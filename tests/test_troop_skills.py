import pathlib
import sys
from unittest.mock import patch

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "server"))

from expedition_battle_mechanics.combat_state import BattleReportInput, CombatState
from expedition_battle_mechanics.formation import RallyFormation
from expedition_battle_mechanics.hero import Hero
from expedition_battle_mechanics.bonus import BonusSource


def _make_state():
    heroes = [
        Hero("I", "Infantry", "SSR", 1, {}, {"exploration": [], "expedition": []}),
        Hero("L", "Lancer", "SSR", 1, {}, {"exploration": [], "expedition": []}),
        Hero("M", "Marksman", "SSR", 1, {}, {"exploration": [], "expedition": []}),
    ]
    ratios = {"Infantry": 1.0, "Lancer": 1.0, "Marksman": 1.0}
    td = {
        "Infantry (FC1)": {
            "Power": 100,
            "Attack": 30,
            "Defense": 10,
            "Lethality": 0,
            "Health": 10,
            "StatBonuses": {"Attack": 0.0, "Defense": 0.0, "Lethality": 0.0, "Health": 0.0},
        },
        "Lancer (FC1)": {
            "Power": 100,
            "Attack": 30,
            "Defense": 10,
            "Lethality": 0,
            "Health": 10,
            "StatBonuses": {"Attack": 0.0, "Defense": 0.0, "Lethality": 0.0, "Health": 0.0},
        },
        "Marksman (FC1)": {
            "Power": 100,
            "Attack": 30,
            "Defense": 10,
            "Lethality": 0,
            "Health": 10,
            "StatBonuses": {"Attack": 0.0, "Defense": 0.0, "Lethality": 0.0, "Health": 0.0},
        },
    }
    atk_form = RallyFormation(heroes, ratios, 1, td)
    def_form = RallyFormation(heroes, ratios, 1, td)
    atk_bs = BonusSource(heroes)
    def_bs = BonusSource(heroes)
    rpt = BattleReportInput(atk_form, def_form, atk_bs, def_bs)
    return CombatState(rpt)


def test_infantry_vs_lancer_only_attack_bonus():
    state = _make_state()
    inf = state.attacker_groups["Infantry"]
    lan = state.defender_groups["Lancer"]
    with patch("random.random", return_value=1.0):
        atk_mul, def_mul, dmg_mul = state._troop_skill_mods(inf, lan)
    assert atk_mul == pytest.approx(1.10)
    assert def_mul == pytest.approx(1.0)
    assert dmg_mul == pytest.approx(1.0)


def test_infantry_defense_against_lancer():
    state = _make_state()
    lan = state.attacker_groups["Lancer"]
    inf = state.defender_groups["Infantry"]
    with patch("random.random", return_value=1.0):
        atk_mul, def_mul, dmg_mul = state._troop_skill_mods(lan, inf)
    assert atk_mul == pytest.approx(1.0)
    assert def_mul == pytest.approx(1.06 * 1.10)
    assert dmg_mul == pytest.approx(1.0)


def test_marksman_base_attack_bonus():
    state = _make_state()
    mar = state.attacker_groups["Marksman"]
    lan = state.defender_groups["Lancer"]
    with patch("random.random", return_value=1.0):
        atk_mul, def_mul, dmg_mul = state._troop_skill_mods(mar, lan)
    assert atk_mul == pytest.approx(1.04)
    assert def_mul == pytest.approx(1.0)
    assert dmg_mul == pytest.approx(1.0)
