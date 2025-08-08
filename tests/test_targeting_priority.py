import pathlib
import sys
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "server"))

from expedition_battle_mechanics.formation import RallyFormation
from expedition_battle_mechanics.hero import Hero
from expedition_battle_mechanics.bonus import BonusSource
from expedition_battle_mechanics.combat_state import BattleReportInput
from expedition_battle_mechanics.simulation import simulate_battle


def _make_forms():
    heroes = [
        Hero("I", "Infantry", "SSR", 1, {}, {"exploration": [], "expedition": []}),
        Hero("L", "Lancer", "SSR", 1, {}, {"exploration": [], "expedition": []}),
        Hero("M", "Marksman", "SSR", 1, {}, {"exploration": [], "expedition": []}),
    ]
    ratios = {"Infantry": 1/3, "Lancer": 1/3, "Marksman": 1/3}
    td = {
        "Infantry (FC1)": {"Power": 100, "Attack": 30, "Defense": 10, "Lethality": 0, "Health": 10,
                           "StatBonuses": {"Attack":0.0,"Defense":0.0,"Lethality":0.0,"Health":0.0}},
        "Lancer (FC1)": {"Power": 100, "Attack": 30, "Defense": 10, "Lethality": 0, "Health": 10,
                           "StatBonuses": {"Attack":0.0,"Defense":0.0,"Lethality":0.0,"Health":0.0}},
        "Marksman (FC1)": {"Power": 100, "Attack": 30, "Defense": 10, "Lethality": 0, "Health": 10,
                           "StatBonuses": {"Attack":0.0,"Defense":0.0,"Lethality":0.0,"Health":0.0}},
    }
    atk_form = RallyFormation(heroes, ratios, 3, td)
    def_form = RallyFormation(heroes, ratios, 3, td)
    atk_bs = BonusSource(heroes)
    def_bs = BonusSource(heroes)
    return atk_form, def_form, atk_bs, def_bs


def test_marksmen_do_not_target_marksmen_first():
    atk_form, def_form, atk_bs, def_bs = _make_forms()
    rpt = BattleReportInput(atk_form, def_form, atk_bs, def_bs)
    with patch("random.random", return_value=1.0):
        res = simulate_battle(rpt, max_rounds=1)
    # defender marksmen should survive first round since no bypass
    assert res["defender"]["survivors"]["Marksman"] == 1
    # infantry and lancers take damage
    assert res["defender"]["survivors"]["Infantry"] < 1 or res["defender"]["survivors"]["Lancer"] < 1
