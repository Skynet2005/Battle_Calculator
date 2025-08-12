import pathlib, sys
from unittest.mock import patch

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "server"))

import hero_data.hero_loader as hl
from expedition_battle_mechanics.loader import hero_from_dict
from expedition_battle_mechanics.troop import TroopGroup
from expedition_battle_mechanics.definitions import TroopDefinition
from expedition_battle_mechanics.on_attack import venom_infusion
from expedition_battle_mechanics.on_turn import (
    chemical_terror,
    toxic_release,
)


class DummyState:
    def __init__(self, turn=0):
        self.turn = turn
        self.extra = 0.0
        self.temp_calls = []

    def add_extra_damage(self, side, amount):
        self.extra += amount

    def add_temp_bonus(self, side, key, pct, turns):
        self.temp_calls.append((side, key, pct, turns))

    def _proc(self, *args, **kwargs):
        pass


def _lancer_group(count=10):
    td = TroopDefinition(
        name="Lancer (FC1)",
        power=100,
        attack=30,
        defense=10,
        lethality=0,
        health=10,
        stat_bonuses={},
    )
    return TroopGroup(td, count)


def test_venom_infusion_extra_and_debuff():
    gord = hero_from_dict(hl.HEROES["Gordon"])
    gord.side = "atk"
    tg = _lancer_group(10)
    state = DummyState()
    with patch("random.random", return_value=0.0):
        venom_infusion(state, "atk", tg, gord, 5)
    expected_extra = gord.get_stat("attack") * 1.0 * tg.count
    assert state.extra == pytest.approx(expected_extra)
    assert ("def", "attack", -0.20, 1) in state.temp_calls


def test_chemical_terror_and_toxic_release_bonuses():
    gord = hero_from_dict(hl.HEROES["Gordon"])
    gord.side = "atk"
    state = DummyState(turn=0)
    chemical_terror(state, gord, 5)
    assert ("atk", "Lancer-attack", 1.5, 1) in state.temp_calls
    assert ("def", "attack", -0.30, 1) in state.temp_calls

    state = DummyState(turn=0)
    toxic_release(state, gord, 5)
    assert ("def", "Infantry-defense", -0.30, 2) in state.temp_calls
    assert ("def", "Marksman-attack", -0.30, 2) in state.temp_calls
