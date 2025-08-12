import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "server"))

import hero_data.hero_loader as hl
from expedition_battle_mechanics.loader import hero_from_dict
from expedition_battle_mechanics import passive as ps


def test_edith_passives():
    edith = hero_from_dict(hl.HEROES["Edith"])

    out = {}
    ps.strategic_balance(edith, 5, lambda k, v: out.setdefault(k, v))
    ps.ironclad(edith, 5, lambda k, v: out.setdefault(k, v))
    ps.steel_sentinel(edith, 5, lambda k, v: out.setdefault(k, v))

    edith.side = "def"
    ps.fortworks(edith, 5, lambda k, v: out.setdefault(k, v))

    assert out["Marksman-defense"] == pytest.approx(0.20)
    assert out["Lancer-attack"] == pytest.approx(0.20)
    assert out["Infantry-defense"] == pytest.approx(0.20)
    assert out["Infantry-health"] == pytest.approx(0.25)
    assert out["health"] == pytest.approx(0.15)


def test_power_shot_and_siege_insight():
    brad = hero_from_dict(hl.HEROES["Bradley"])

    out = {}
    ps.power_shot(brad, 5, lambda k, v: out.setdefault(k, v))
    brad.side = "def"
    ps.siege_insight(brad, 5, lambda k, v: out.setdefault(k, v))

    assert out["enemy-lancer_defense-down"] == pytest.approx(0.30)
    assert out["enemy-infantry_defense-down"] == pytest.approx(0.25)
    assert out["attack"] == pytest.approx(0.15)


def test_bio_assault_def_only():
    gord = hero_from_dict(hl.HEROES["Gordon"])

    # attacking rallies should not gain the lethality bonus
    out = {}
    gord.side = "atk"
    ps.bio_assault(gord, 5, lambda k, v: out.setdefault(k, v))
    assert out == {}

    # defenders receive the increase
    out = {}
    gord.side = "def"
    ps.bio_assault(gord, 5, lambda k, v: out.setdefault(k, v))
    assert out["lethality"] == pytest.approx(0.15)
