import pathlib
import sys
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "server"))

from expedition_battle_mechanics.bonus import BonusSource
from expedition_battle_mechanics.combat_state import BattleReportInput
from expedition_battle_mechanics.definitions import Skill, ExclusiveWeapon
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


def _base_heroes():
    return [
        Hero("I", "Infantry", "SSR", 1, {}, {"exploration": [], "expedition": []}),
        Hero("L", "Lancer", "SSR", 1, {}, {"exploration": [], "expedition": []}),
        Hero("M", "Marksman", "SSR", 1, {}, {"exploration": [], "expedition": []}),
    ]


def test_support_only_first_skill():
    heroes = _base_heroes()
    ratios = {"Infantry": 1.0, "Lancer": 0.0, "Marksman": 0.0}

    sk1 = Skill(name="Abyssal Blessing", multiplier=0.10)
    sk2 = Skill(name="Ironclad", multiplier=0.20)
    support = Hero(
        "Support",
        "Marksman",
        "SSR",
        1,
        {},
        {"exploration": [], "expedition": [sk1, sk2]},
    )

    atk_form = RallyFormation(heroes, ratios, 100, _basic_troop_defs(), support_heroes=[support])
    def_form = RallyFormation(heroes, ratios, 100, _basic_troop_defs())

    atk_bs = BonusSource(atk_form.all_heroes())
    def_bs = BonusSource(def_form.all_heroes())

    rpt = BattleReportInput(atk_form, def_form, atk_bs, def_bs)
    res = simulate_battle(rpt, max_rounds=1)

    assert (
        res["bonuses"]["attacker"].get("All", {}).get("attack", 0.0)
        == pytest.approx(0.10)
    )
    assert res["bonuses"]["attacker"]["Infantry"].get("defense", 0.0) == 0


def test_only_top_four_joiners():
    heroes = _base_heroes()
    ratios = {"Infantry": 1.0, "Lancer": 0.0, "Marksman": 0.0}

    skill = Skill(name="Treasure Hunter", multiplier=0.05)
    supports = [
        Hero(f"S{i}", "Marksman", "SSR", 1, {}, {"exploration": [], "expedition": [skill]})
        for i in range(5)
    ]

    atk_form = RallyFormation(heroes, ratios, 100, _basic_troop_defs(), support_heroes=supports)
    def_form = RallyFormation(heroes, ratios, 100, _basic_troop_defs())

    atk_bs = BonusSource(atk_form.all_heroes())
    def_bs = BonusSource(def_form.all_heroes())
    rpt = BattleReportInput(atk_form, def_form, atk_bs, def_bs)
    res = simulate_battle(rpt, max_rounds=1)

    assert (
        res["bonuses"]["attacker"].get("All", {}).get("attack", 0.0)
        == pytest.approx(0.20)
    )


def test_support_exclusive_weapon_ignored():
    heroes = _base_heroes()
    ratios = {"Infantry": 1.0, "Lancer": 0.0, "Marksman": 0.0}

    ew = ExclusiveWeapon(name="EW", level=1, power=0, attack=0, defense=0, health=0, perks={"attack": 0.15})
    support = Hero(
        "SupportEW",
        "Marksman",
        "SSR",
        1,
        {},
        {"exploration": [], "expedition": []},
        exclusive_weapon=ew,
    )

    atk_form = RallyFormation(heroes, ratios, 100, _basic_troop_defs(), support_heroes=[support])
    bs = BonusSource(atk_form.all_heroes())
    assert "attack" not in bs.base_bonuses
