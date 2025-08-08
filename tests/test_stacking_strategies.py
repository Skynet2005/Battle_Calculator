import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "server"))

import pytest
from expedition_battle_mechanics.stacking import (
    AdditiveStrategy,
    BonusBucket,
    MaxStrategy,
    MultiplicativeStrategy,
)


def test_additive_strategy():
    bucket = BonusBucket(AdditiveStrategy())
    bucket.add("attack", 0.1)
    bucket.add("attack", 0.2)
    assert bucket.as_dict()["attack"] == pytest.approx(0.3)


def test_max_strategy():
    bucket = BonusBucket(MaxStrategy())
    bucket.add("attack", 0.1)
    bucket.add("attack", 0.25)
    assert bucket.as_dict()["attack"] == pytest.approx(0.25)


def test_multiplicative_strategy():
    bucket = BonusBucket(MultiplicativeStrategy())
    bucket.add("dmg", 0.1)
    bucket.add("dmg", 0.2)
    # (1+0.1)*(1+0.2)-1 = 0.32
    assert bucket.as_dict()["dmg"] == pytest.approx(0.32)
