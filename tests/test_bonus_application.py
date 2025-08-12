import random

import pathlib
import sys

import pytest

# Add server directory to path so tests can import battle mechanics
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "server"))

from expedition_battle_mechanics.bonus import BonusSource
from expedition_battle_mechanics.combat_state import BattleReportInput, CombatState
from expedition_battle_mechanics.definitions import ExclusiveWeapon
from expedition_battle_mechanics.formation import RallyFormation
from expedition_battle_mechanics.hero import Hero
# Use weighted variant in tests to maintain expected behavior while default engine uses strict-doc mode
from expedition_battle_mechanics.simulation import simulate_battle_weighted as simulate_battle


def _make_side(
    attack_bonus: float = 0.0,
    defense_bonus: float = 0.0,
    health_bonus: float = 0.0,
    lethality_bonus: float = 0.0,
    base_lethality: int = 0,
):
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
            "Lethality": base_lethality,
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
            "Lethality": base_lethality,
            "Health": 10,
            "StatBonuses": {"Attack": 0.0, "Defense": 0.0, "Lethality": 0.0, "Health": 0.0},
        },
        "Marksman (FC1)": {
            "Power": 100,
            "Attack": 30,
            "Defense": 10,
            "Lethality": base_lethality,
            "Health": 10,
            "StatBonuses": {"Attack": 0.0, "Defense": 0.0, "Lethality": 0.0, "Health": 0.0},
        },
    }

    form = RallyFormation(heroes, ratios, 100, td)
    bs = BonusSource(
        heroes,
        city_buffs={
            "attack": attack_bonus,
            "defense": defense_bonus,
            "health": health_bonus,
            "lethality": lethality_bonus,
        },
    )
    return form, bs


def _run(att_bonus=0.0, def_bonus=0.0, def_health=0.0):
    atk_form, atk_bs = _make_side(attack_bonus=att_bonus)
    def_form, def_bs = _make_side(defense_bonus=def_bonus, health_bonus=def_health)
    rpt = BattleReportInput(atk_form, def_form, atk_bs, def_bs)
    random.seed(0)
    res = simulate_battle(rpt, max_rounds=1)
    return res["defender"]["survivors"]["Infantry"]


def _run_leth(leth_bonus=0.0):
    atk_form, atk_bs = _make_side(lethality_bonus=leth_bonus, base_lethality=10)
    def_form, def_bs = _make_side()
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


def test_lethality_bonus_increases_damage():
    base = _run_leth()
    lethal = _run_leth(leth_bonus=1.0)  # +100% lethality
    assert lethal < base


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


def test_special_bonus_hits_harder_than_regular():
    base_surv = _run(att_bonus=0.15)

    atk_form, _ = _make_side()
    def_form, def_bs = _make_side()
    special_bs = BonusSource(atk_form.all_heroes(), territory_buffs={"attack": 0.15})
    rpt = BattleReportInput(atk_form, def_form, special_bs, def_bs)
    random.seed(0)
    res = simulate_battle(rpt, max_rounds=1)
    special_surv = res["defender"]["survivors"]["Infantry"]

    assert special_surv < base_surv


def test_special_bonus_formula_matches_wiki():
    atk_form, _ = _make_side()
    def_form, def_bs = _make_side()
    special_bs = BonusSource(atk_form.all_heroes(), territory_buffs={"attack": 0.15})
    rpt = BattleReportInput(atk_form, def_form, special_bs, def_bs)
    state = CombatState(rpt)

    random.seed(0)
    dmg, _by_cls, _extra = state._compute_side_damage(
        state.attacker_groups,
        state.defender_groups,
        state.attacker_bonus,
        state.attacker_special,
        "atk",
    )
    atk = state.attacker_groups["Infantry"]
    deff = state.defender_groups["Infantry"]
    ratio = atk.definition.power / (atk.definition.power + deff.definition.power)
    eff_atk = atk.definition.attack
    eff_atk = eff_atk * (1 + 0.15) + atk.definition.attack * 0.15
    atk_mul, def_mul, dmg_mul = state._troop_skill_mods(atk, deff)
    eff_atk *= atk_mul
    eff_leth = atk.definition.lethality
    eff_leth = eff_leth * (1 + 0.15) + atk.definition.lethality * 0.15
    eff_leth *= atk_mul
    eff_def = deff.definition.defense * def_mul
    expected = (
        max(eff_atk * ratio - eff_def, eff_atk * ratio * 0.01) + eff_leth * ratio
    ) * atk.count * dmg_mul
    assert dmg["Infantry"] == pytest.approx(expected)

