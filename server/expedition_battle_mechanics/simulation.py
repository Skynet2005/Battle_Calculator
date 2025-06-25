# battle_mechanics/simulation.py

import logging
from expedition_battle_mechanics.combat_state import CombatState, BattleReportInput
from typing import Dict, Any

# Configure logging for this module
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


def simulate_battle(
    report: BattleReportInput,
    max_rounds: int = 10000
) -> Dict[str, Any]:
    """
    Run a single expedition battle simulation to completion.
    Caps out at `max_rounds` turns to avoid infinite loops, then logs a warning.
    """
    state = CombatState(report)

    # Track initial troop counts for kill calculations
    atk_initial = {t: g.count for t, g in state.attacker_groups.items()}
    def_initial = {t: g.count for t, g in state.defender_groups.items()}

    # Run the turn loop
    while not state.is_over() and state.turn < max_rounds:
        state.step_round()

    # If we stop because of turn cap, log a warning
    if not state.is_over():
        logger.warning(
            f"simulate_battle: reached max_rounds={max_rounds} before battle ended (turn={state.turn})"
        )

    # Final survivors by type
    atk_survivors = {t: g.count for t, g in state.attacker_groups.items()}
    def_survivors = {t: g.count for t, g in state.defender_groups.items()}

    # Determine winner based on remaining troops
    winner = (
        "attacker"
        if sum(atk_survivors.values()) > sum(def_survivors.values())
        else "defender"
    )

    # Compute kills per troop type
    atk_kills = {
        t: def_initial[t] - def_survivors[t]
        for t in ["Infantry", "Lancer", "Marksman"]
    }
    def_kills = {
        t: atk_initial[t] - atk_survivors[t]
        for t in ["Infantry", "Lancer", "Marksman"]
    }

    # Helper: extract hero & troop info
    def hero_info(heroes, formation):
        return {
            t: {
                "name": h.name,
                "class": h.char_class,
                "generation": h.generation,
                "skills": [sk.name for sk in h.skills.get("expedition", [])],
                "troop_level": formation.troop_groups[t].definition.name,
                "troop_power": formation.troop_groups[t].definition.power,
                "troop_count": formation.troop_groups[t].count,
            }
            for t, h in heroes.items()
        }

    atk_hero_info = hero_info(state.attacker_heroes, report.attacker_formation)
    def_hero_info = hero_info(state.defender_heroes, report.defender_formation)

    # Compute total troop power
    atk_total_power = sum(
        info["troop_power"] * info["troop_count"] for info in atk_hero_info.values()
    )
    def_total_power = sum(
        info["troop_power"] * info["troop_count"] for info in def_hero_info.values()
    )

    return {
        "winner": winner,
        "attacker_survivors": sum(atk_survivors.values()),
        "defender_survivors": sum(def_survivors.values()),
        "rounds": state.turn,
        "attacker": {
            "heroes": atk_hero_info,
            "total_power": atk_total_power,
            "kills": atk_kills,
            "survivors": atk_survivors,
        },
        "defender": {
            "heroes": def_hero_info,
            "total_power": def_total_power,
            "kills": def_kills,
            "survivors": def_survivors,
        },
    }


def monte_carlo_battle(
    report: BattleReportInput,
    n_sims: int = 1000
) -> Dict[str, Any]:
    """
    Run `n_sims` independent simulations, aggregate win rates and average survivors,
    and keep the first detailed sample (with per-type kills & survivors).
    """
    results = {
        "attacker_wins": 0,
        "defender_wins": 0,
        "attacker_survivors": [],
        "defender_survivors": [],
    }
    sample_battle = None

    for i in range(n_sims):
        # Reset any per-sim state
        report.skill_trigger_counts = {}

        # Use the same capped simulate_battle (max_rounds default)
        outcome = simulate_battle(report)

        if i == 0:
            sample_battle = outcome

        if outcome["winner"] == "attacker":
            results["attacker_wins"] += 1
        else:
            results["defender_wins"] += 1

        results["attacker_survivors"].append(outcome["attacker_survivors"])
        results["defender_survivors"].append(outcome["defender_survivors"])

    return {
        "attacker_win_rate": results["attacker_wins"] / n_sims,
        "defender_win_rate": results["defender_wins"] / n_sims,
        "avg_attacker_survivors": sum(results["attacker_survivors"]) / n_sims,
        "avg_defender_survivors": sum(results["defender_survivors"]) / n_sims,
        "sample_battle": sample_battle,
    }
