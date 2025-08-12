"""
simulation.py
=============

•  simulate_battle  – returns a dict ready for the front-end, including
   - winner, rounds
   - attacker / defender breakdown
   - proc_stats          (on-attack / on-turn procs)
   - passive_effects     (bullet-ready stat changes)
   - bonuses             (final cumulative % per side)

•  monte_carlo_battle – repeats simulate_battle N times to get averages.
NO SECTION ABBREVIATED.
"""

import logging
from copy import deepcopy
from typing import Any, Dict, List
from collections import defaultdict

from .combat_state import (
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
    kills: Dict[str, int],
    enemy_start: Dict[str, int],
) -> Dict[str, Any]:
    """
    Build a block for each hero that now ALSO exposes
        "skill_pcts": { skill-name: multiplier(float) }
    so the UI can print “+30 %” next to timed skills.
    """
    out: Dict[str, Any] = {}
    for cls, hero in heroes.items():
        grp = groups_after[cls]

        # grab % at the hero’s chosen level (defaults to 5), but use EW level for EW expedition skill
        skill_pcts = {}
        for sk in hero.skills.get("expedition", []):
            if hero.exclusive_weapon and hero.exclusive_weapon.skills.get("expedition") and sk.name == hero.exclusive_weapon.skills["expedition"].name:
                lvl = hero.exclusive_weapon.level
            else:
                lvl = hero.selected_skill_levels.get(sk.name, 5)
            skill_pcts[sk.name] = hero.skills_pct(sk.name, lvl)

        out[cls] = {
            "name": hero.name,
            "class": hero.char_class,
            "generation": hero.generation,
            "skills": [s.name for s in hero.skills.get("expedition", [])],
            "exclusive_weapon": {
                "name": hero.exclusive_weapon.name,
                "level": hero.exclusive_weapon.level,
            }
            if hero.exclusive_weapon
            else None,
            "skill_pcts": skill_pcts,                 #  ← NEW
            "troop_level": grp.definition.name,
            "troop_power": grp.definition.power,
            "count_start": start[cls],
            "count_end": grp.count,
            "count_lost": start[cls] - grp.count,
            "loss_pct": (start[cls] - grp.count) / start[cls] if start[cls] else 0,
            "kills": kills.get(cls, 0),
            "kill_pct": kills.get(cls, 0) / enemy_start.get(cls, 0)
            if enemy_start.get(cls, 0)
            else 0,
        }
    return out


# ---------------------------------------------------------------------------
def _structure_bonuses(bonus: Dict[str, float]) -> Dict[str, Dict[str, float]]:
    """Group flat bonus mapping into class buckets plus an 'All' bucket."""
    classes = ["Infantry", "Lancer", "Marksman"]
    stats = ["attack", "defense", "lethality", "health"]
    out: Dict[str, Dict[str, float]] = {
        cls: {s: 0.0 for s in stats} for cls in classes
    }
    out["All"] = {s: 0.0 for s in stats}

    for key, val in bonus.items():
        if "_" in key:
            cls, stat = key.split("_", 1)
            out.setdefault(cls.capitalize(), {})
            out[cls.capitalize()][stat] = val
        else:
            out["All"][key] = val

    # Created Logic for review: propagate All-bucket stats to each troop class for clarity in reports
    # This does NOT affect battle calculations; it's only for the returned reporting structure
    for cls in classes:
        for stat in stats:
            out[cls][stat] = out[cls].get(stat, 0.0) + out["All"].get(stat, 0.0)
    return out


def _structure_passives(lines: List[str]) -> Dict[str, List[str]]:
    """Categorise passive effect strings into troop classes or 'All'."""
    out: Dict[str, List[str]] = {
        "Infantry": [],
        "Lancer": [],
        "Marksman": [],
        "All": [],
    }
    for ln in lines:
        try:
            after = ln.split(":", 1)[1].strip()
            target = after.split()[0]
            cls = target.split("-")[0]
            cls_cap = cls.capitalize()
            if cls_cap in out:
                out[cls_cap].append(ln)
            else:
                out["All"].append(ln)
        except Exception:
            out["All"].append(ln)
    return out


def _structure_procs(proc: Dict[str, int]) -> Dict[str, Dict[str, Dict[str, int]]]:
    """Split proc counters into side and class buckets."""
    out: Dict[str, Dict[str, Dict[str, int]]] = {
        "attacker": {},
        "defender": {},
    }
    for key, cnt in proc.items():
        parts = key.split("-")
        if len(parts) == 2:
            skill, side = parts
            cls = "All"
        else:
            skill, side, cls = parts
            cls = cls.capitalize()
        side_key = "attacker" if side == "atk" else "defender"
        skill_map = out[side_key].setdefault(skill, {})
        skill_map[cls] = cnt
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

    atk_total_start = sum(atk_start.values())
    def_total_start = sum(def_start.values())
    atk_total_end = sum(atk_end.values())
    def_total_end = sum(def_end.values())
    atk_losses = atk_total_start - atk_total_end
    def_losses = def_total_start - def_total_end
    atk_total_kills = sum(atk_kills.values())
    def_total_kills = sum(def_kills.values())

    atk_power_start = sum(
        grp.definition.power * atk_start[cls]
        for cls, grp in state.attacker_groups.items()
    )
    def_power_start = sum(
        grp.definition.power * def_start[cls]
        for cls, grp in state.defender_groups.items()
    )
    atk_power_end = sum(
        grp.definition.power * atk_end[cls]
        for cls, grp in state.attacker_groups.items()
    )
    def_power_end = sum(
        grp.definition.power * def_end[cls]
        for cls, grp in state.defender_groups.items()
    )

    # Build timeline for charts
    timeline = [
        {
            "turn": snap.turn,
            "attacker": snap.attacker,
            "defender": snap.defender,
            "events": [
                {"side": e.side, "skill": e.skill, "class": e.cls, "amount": e.amount}
                for e in snap.events
            ],
        }
        for snap in state.turnlog.timeline
    ]

    return {
        "winner": winner,
        "rounds": state.turn,
        "attacker": {
            "heroes": _hero_info(
                state.attacker_heroes,
                state.attacker_groups,
                atk_start,
                atk_kills,
                def_start,
            ),
            "total_power": sum(
                grp.definition.power * atk_start[cls]
                for cls, grp in state.attacker_groups.items()
            ),
            "kills": atk_kills,
            "survivors": atk_end,
            "summary": {
                "start": atk_total_start,
                "end": atk_total_end,
                "losses": atk_losses,
                "loss_pct": atk_losses / atk_total_start if atk_total_start else 0,
                "kills": atk_total_kills,
                "kill_pct": atk_total_kills / def_total_start if def_total_start else 0,
            },
        },
        "defender": {
            "heroes": _hero_info(
                state.defender_heroes,
                state.defender_groups,
                def_start,
                def_kills,
                atk_start,
            ),
            "total_power": sum(
                grp.definition.power * def_start[cls]
                for cls, grp in state.defender_groups.items()
            ),
            "kills": def_kills,
            "survivors": def_end,
            "summary": {
                "start": def_total_start,
                "end": def_total_end,
                "losses": def_losses,
                "loss_pct": def_losses / def_total_start if def_total_start else 0,
                "kills": def_total_kills,
                "kill_pct": def_total_kills / atk_total_start if atk_total_start else 0,
            },
        },
        "proc_stats": _structure_procs(dict(state.skill_procs)),
        "passive_effects": {
            "attacker": _structure_passives(state.passive_effects["atk"]),
            "defender": _structure_passives(state.passive_effects["def"]),
        },
        "bonuses": {
            "attacker": _structure_bonuses(state.attacker_bonus),
            "defender": _structure_bonuses(state.defender_bonus),
            "attacker_special": state.attacker_special,
            "defender_special": state.defender_special,
        },
        "power": {
            "attacker": {
                "start": atk_power_start,
                "end": atk_power_end,
                "lost": atk_power_start - atk_power_end,
                "dealt": def_power_start - def_power_end,
            },
            "defender": {
                "start": def_power_start,
                "end": def_power_end,
                "lost": def_power_start - def_power_end,
                "dealt": atk_power_start - atk_power_end,
            },
            "difference": {
                "start": atk_power_start - def_power_start,
                "end": atk_power_end - def_power_end,
            },
        },
        "timeline": timeline,
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
        for side, skills in res["proc_stats"].items():
            for skill, cls_map in skills.items():
                for cls, cnt in cls_map.items():
                    key = (
                        f"{skill}-{side[:3]}"
                        if cls == "All"
                        else f"{skill}-{side[:3]}-{cls.lower()}"
                    )
                    proc_sum[key] += cnt

    return {
        "attacker_win_rate": wins["attacker"] / n_sims,
        "defender_win_rate": wins["defender"] / n_sims,
        "avg_attacker_survivors": atk_surv / n_sims,
        "avg_defender_survivors": def_surv / n_sims,
        "proc_stats": _structure_procs(dict(proc_sum)),
        "sample_battle": sample,
    }


# Convenience wrappers for weighted mode (keeps old behavior explicit)
def simulate_battle_weighted(report: BattleReportInput, max_rounds: int = 10_000) -> Dict[str, Any]:
    return simulate_battle(report, max_rounds=max_rounds)


def monte_carlo_battle_weighted(report: BattleReportInput, n_sims: int = 1_000) -> Dict[str, Any]:
    return monte_carlo_battle(report, n_sims=n_sims)
