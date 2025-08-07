import random

import pathlib
import sys

import pytest

# Add server directory to path so tests can import battle mechanics
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "server"))

from expedition_battle_mechanics.bonus import BonusSource
from expedition_battle_mechanics.combat_state import BattleReportInput
from expedition_battle_mechanics.definitions import ExclusiveWeapon
from expedition_battle_mechanics.formation import RallyFormation
from expedition_battle_mechanics.hero import Hero
from expedition_battle_mechanics.simulation import simulate_battle


def _make_side(attack_bonus=0.0, defense_bonus=0.0, health_bonus=0.0):
    heroes = [
        Hero("I", "Infantry", "SSR", 1, {}, {"exploration": [], "expedition": []}),
        Hero("L", "Lancer", "SSR", 1, {}, {"exploration": [], "expedition": []}),
        Hero("M", "Marksman", "SSR", 1, {}, {"exploration": [], "expedition": []}),
    ]
    ratios = {"Infantry": 1.0, "Lancer": 0.0, "Marksman": 0.0}

    td = {
        "Infantry (FC1)": {
            "Power": 100,
            "Attack": 30,
            "Defense": 10,
            "Lethality": 0,
            "Health": 10,
            "StatBonuses": {
                "Attack": 0.0,
                "Defense": 0.0,
                "Lethality": 0.0,
                "Health": 0.0,
            },
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

    form = RallyFormation(heroes, ratios, 100, td)
    bs = BonusSource(heroes, city_buffs={
        "attack": attack_bonus,
        "defense": defense_bonus,
        "health": health_bonus,
    })
    return form, bs


def _run(att_bonus=0.0, def_bonus=0.0, def_health=0.0):
    atk_form, atk_bs = _make_side(attack_bonus=att_bonus)
    def_form, def_bs = _make_side(defense_bonus=def_bonus, health_bonus=def_health)
    rpt = BattleReportInput(atk_form, def_form, atk_bs, def_bs)
    random.seed(0)
    res = simulate_battle(rpt, max_rounds=1)
    return res["defender"]["survivors"]["Infantry"]


def test_attack_bonus_increases_damage():
    base = _run()
    buffed = _run(att_bonus=1.0)  # +100% attack
    assert buffed < base


def test_defense_bonus_reduces_damage():
    base = _run()
    tougher = _run(def_bonus=1.0)  # +100% defense
    assert tougher > base


def test_health_bonus_reduces_losses():
    base = _run()
    durable = _run(def_health=1.0)  # +100% health
    assert durable > base


def test_bonus_source_aggregates_exclusive_weapons():
    h1 = Hero(
        "H1",
        "Infantry",
        "SSR",
        1,
        {},
        {"exploration": [], "expedition": []},
        exclusive_weapon=ExclusiveWeapon(
            name="W1", level=1, power=0, attack=0, defense=0, health=0, perks={"attack": 0.1}
        ),
    )
    h2 = Hero(
        "H2",
        "Lancer",
        "SSR",
        1,
        {},
        {"exploration": [], "expedition": []},
        exclusive_weapon=ExclusiveWeapon(
            name="W2", level=1, power=0, attack=0, defense=0, health=0, perks={"attack": 0.2}
        ),
    )
    bs = BonusSource([h1, h2])
    assert bs.total_bonuses["attack"] == pytest.approx(0.3)

