import sys
import pathlib
import pytest
from fastapi.testclient import TestClient

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "server"))

import server.main as main


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


def _hero(name, char_class, skill=None):
    return {
        "hero-name": name,
        "hero-class": char_class,
        "rarity": "SSR",
        "generation": 1,
        "base-stats": {},
        "skills": {
            "exploration": {},
            "expedition": {"1": skill} if skill else {},
        },
        "exclusive-weapon": None,
    }


def test_support_hero_via_api(monkeypatch):
    # Patch raw heroes and troop definitions
    main.RAW_HEROES = {
        "I": _hero("I", "Infantry"),
        "L": _hero("L", "Lancer"),
        "M": _hero("M", "Marksman"),
        "Support": _hero(
            "Support",
            "Marksman",
            {"skill-name": "Abyssal Blessing", "level_percentage": 0.10},
        ),
    }
    monkeypatch.setattr(main, "TROOP_DEFINITIONS", _basic_troop_defs())

    client = TestClient(main.app)
    payload = {
        "attackerHeroes": ["I", "L", "M"],
        "defenderHeroes": ["I", "L", "M"],
        "attackerSupportHeroes": ["Support"],
        "defenderSupportHeroes": [],
        "attackerRatios": {"Infantry": 1.0, "Lancer": 0.0, "Marksman": 0.0},
        "defenderRatios": {"Infantry": 1.0, "Lancer": 0.0, "Marksman": 0.0},
        "attackerCapacity": 100,
        "defenderCapacity": 100,
        "sims": 1,
        "attackerTroops": {
            "Infantry": "Infantry (FC1)",
            "Lancer": "Lancer (FC1)",
            "Marksman": "Marksman (FC1)",
        },
        "defenderTroops": {
            "Infantry": "Infantry (FC1)",
            "Lancer": "Lancer (FC1)",
            "Marksman": "Marksman (FC1)",
        },
    }

    res = client.post("/api/simulate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["bonuses"]["attacker"]["attack"] == pytest.approx(0.10)
