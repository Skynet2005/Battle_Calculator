"""
simulation.py
=============

•  simulate_battle  – runs one fight and *returns*:
     - winner, rounds
     - attacker / defender breakdown
     - proc_stats          (on-attack / on-turn skill procs)
     - passive_effects     (bullet-ready log of stat changes)
     - bonuses             (final cumulative % per side)

•  monte_carlo_battle – repeats simulate_battle N times and aggregates
   win rate & survivors; includes the first run as “sample_battle”.
"""

import logging
from copy import deepcopy
from typing import Any, Dict
from collections import defaultdict

from expedition_battle_mechanics.combat_state import (
    CombatState,
    BattleReportInput,
)

# ─────────────────────────────────────────────────────────────────────────────
# logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(h)
logger.setLevel(logging.INFO)


# ─────────────────────────────────────────────────────────────────────────────
def _hero_info(
    heroes: Dict[str, Any],
    groups_after: Dict[str, Any],
    start: Dict[str, int],
) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for cls, hero in heroes.items():
        grp = groups_after[cls]
        out[cls] = {
            "name": hero.name,
            "class": hero.char_class,
            "generation": hero.generation,
            "skills": [s.name for s in hero.skills.get("expedition", [])],
            "troop_level": grp.definition.name,
            "troop_power": grp.definition.power,
            "count_start": start[cls],
            "count_end": grp.count,
        }
    return out


# ─────────────────────────────────────────────────────────────────────────────
def simulate_battle(
    report: BattleReportInput, max_rounds: int = 10_000
) -> Dict[str, Any]:
    rpt = deepcopy(report)
    state = CombatState(rpt)

    atk_start = {t: g.count for t, g in state.attacker_groups.items()}
    def_start = {t: g.count for t, g in state.defender_groups.items()}

    while not state.is_over() and state.turn < max_rounds:
        state.step_round()

    atk_end = {t: g.count for t, g in state.attacker_groups.items()}
    def_end = {t: g.count for t, g in state.defender_groups.items()}

    atk_kills = {t: def_start[t] - def_end[t] for t in atk_start}
    def_kills = {t: atk_start[t] - atk_end[t] for t in def_start}

    winner = "attacker" if sum(atk_end.values()) > sum(def_end.values()) else "defender"

    return {
        "winner": winner,
        "rounds": state.turn,
        "attacker": {
            "heroes": _hero_info(state.attacker_heroes, state.attacker_groups, atk_start),
            "total_power": sum(
                grp.definition.power * atk_start[cls]
                for cls, grp in state.attacker_groups.items()
            ),
            "kills": atk_kills,
            "survivors": atk_end,
        },
        "defender": {
            "heroes": _hero_info(state.defender_heroes, state.defender_groups, def_start),
            "total_power": sum(
                grp.definition.power * def_start[cls]
                for cls, grp in state.defender_groups.items()
            ),
            "kills": def_kills,
            "survivors": def_end,
        },
        "proc_stats": dict(state.skill_procs),
        "passive_effects": {
            "attacker": state.passive_effects["atk"],
            "defender": state.passive_effects["def"],
        },
        "bonuses": {
            "attacker": state.attacker_bonus,
            "defender": state.defender_bonus,
        },
    }


# ─────────────────────────────────────────────────────────────────────────────
def monte_carlo_battle(
    report: BattleReportInput, n_sims: int = 1_000
) -> Dict[str, Any]:
    wins = {"attacker": 0, "defender": 0}
    atk_surv = def_surv = 0
    proc_sum: Dict[str, int] = defaultdict(int)
    sample = None

    for i in range(n_sims):
        res = simulate_battle(report, max_rounds=10_000)
        if i == 0:
            sample = res
        wins[res["winner"]] += 1
        atk_surv += sum(res["attacker"]["survivors"].values())
        def_surv += sum(res["defender"]["survivors"].values())
        for k, v in res["proc_stats"].items():
            proc_sum[k] += v

    return {
        "attacker_win_rate": wins["attacker"] / n_sims,
        "defender_win_rate": wins["defender"] / n_sims,
        "avg_attacker_survivors": atk_surv / n_sims,
        "avg_defender_survivors": def_surv / n_sims,
        "proc_stats": dict(proc_sum),
        "sample_battle": sample,
    }
