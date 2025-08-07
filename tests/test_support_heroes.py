import pathlib
import sys
import random
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "server"))

from expedition_battle_mechanics.bonus import BonusSource
from expedition_battle_mechanics.combat_state import BattleReportInput
from expedition_battle_mechanics.definitions import Skill
from expedition_battle_mechanics.formation import RallyFormation
from expedition_battle_mechanics.hero import Hero
from expedition_battle_mechanics.simulation import simulate_battle


def _basic_troop_defs():
    return {
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


def test_support_hero_passive_applied():
    # primary heroes commanding troops
    base_heroes = [
        Hero("I", "Infantry", "SSR", 1, {}, {"exploration": [], "expedition": []}),
        Hero("L", "Lancer", "SSR", 1, {}, {"exploration": [], "expedition": []}),
        Hero("M", "Marksman", "SSR", 1, {}, {"exploration": [], "expedition": []}),
    ]
    ratios = {"Infantry": 1.0, "Lancer": 0.0, "Marksman": 0.0}

    # support hero with passive +10% attack
    support_skill = Skill(name="Abyssal Blessing", multiplier=0.10)
    support = Hero(
        "Support",
        "Marksman",
        "SSR",
        1,
        {},
        {"exploration": [], "expedition": [support_skill]},
    )

    atk_form = RallyFormation(
        base_heroes,
        ratios,
        100,
        _basic_troop_defs(),
        support_heroes=[support],
    )
    def_form = RallyFormation(base_heroes, ratios, 100, _basic_troop_defs())

    atk_bs = BonusSource(atk_form.all_heroes())
    def_bs = BonusSource(def_form.all_heroes())

    rpt = BattleReportInput(atk_form, def_form, atk_bs, def_bs)
    random.seed(0)
    res = simulate_battle(rpt, max_rounds=1)

    assert res["bonuses"]["attacker"]["attack"] == pytest.approx(0.10)
