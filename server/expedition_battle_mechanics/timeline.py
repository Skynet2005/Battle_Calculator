# timeline.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class TurnEvent:
    turn: int
    side: str            # "atk" | "def"
    skill: str
    cls: str = "All"     # "Infantry" | "Lancer" | "Marksman" | "All"
    amount: float = 0.0  # optional: flat extra damage (if any)

@dataclass
class TurnSnapshot:
    turn: int
    attacker: Dict[str, float] = field(default_factory=dict)  # e.g. {"base": 0, "Infantry": 0, "Lancer": 0, "Marksman": 0, "extra": 0}
    defender: Dict[str, float] = field(default_factory=dict)
    events: List[TurnEvent] = field(default_factory=list)

class TurnLogger:
    """
    Minimal per-turn timeline collector.
    Skills call .proc() and .add_extra().
    CombatState calls .close_turn() once per turn with damage breakdowns.
    """
    def __init__(self) -> None:
        self.events: List[TurnEvent] = []
        self.timeline: List[TurnSnapshot] = []
        self._extra_pool = {"atk": 0.0, "def": 0.0}

    def proc(self, turn: int, side: str, skill: str, cls: str = "All", amount: float = 0.0) -> None:
        self.events.append(TurnEvent(turn=turn, side=side, skill=skill, cls=cls, amount=amount))

    def add_extra(self, side: str, amount: float) -> None:
        self._extra_pool[side] += float(amount)

    def close_turn(self, turn: int, atk_breakdown: Dict[str, float], def_breakdown: Dict[str, float]) -> None:
        snap = TurnSnapshot(
            turn=turn,
            attacker={**atk_breakdown, "extra": self._extra_pool["atk"]},
            defender={**def_breakdown, "extra": self._extra_pool["def"]},
            events=[e for e in self.events if e.turn == turn],
        )
        self.timeline.append(snap)
        self._extra_pool = {"atk": 0.0, "def": 0.0}
