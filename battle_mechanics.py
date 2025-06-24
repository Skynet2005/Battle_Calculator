# battle_mechanics.py
# TODO: Add all the Troop Type Skills as well.. Each has it's unique skills that trigger. The mechnaics of Troop Skills can be added here after the Troop Definitions are imported.

import random
from typing import Dict, List, Optional, Any

class TroopDefinition:
    """
    Defines the base stats for a troop type (e.g., Infantry FC1, Marksman FC5, etc.).
    """
    def __init__(self,
                 name: str,
                 power: float,
                 attack: float,
                 defense: float,
                 lethality: float,
                 health: float,
                 stat_bonuses: Optional[Dict[str, float]] = None):
        self.name = name
        self.power = power
        self.attack = attack
        self.defense = defense
        self.lethality = lethality
        self.health = health
        self.stat_bonuses = stat_bonuses or {
            "attack": 0.0,
            "defense": 0.0,
            "lethality": 0.0,
            "health": 0.0
        }

class Skill:
    """
    Represents a single skill with a damage multiplier and an optional proc chance.
    """
    def __init__(self,
                 name: str,
                 multiplier: float,
                 proc_chance: Optional[float] = None):
        self.name = name
        self.multiplier = multiplier
        self.proc_chance = proc_chance or 0.0

class ExclusiveWeapon:
    """
    Represents a hero's exclusive weapon and its stat bonuses and skills.
    """
    def __init__(self,
                 level: int,
                 power: float,
                 attack: float,
                 defense: float,
                 health: float,
                 stat_bonuses: Dict[str, float],
                 skills: Dict[str, Skill]):
        self.level = level
        self.power = power
        self.attack = attack
        self.defense = defense
        self.health = health
        self.stat_bonuses = stat_bonuses
        self.skills = skills

class Hero:
    """
    Represents a hero with base stats, skills (both exploration and expedition), and an optional exclusive weapon.
    """
    def __init__(self,
                 name: str,
                 char_class: str,
                 rarity: str,
                 generation: int,
                 base_stats: Dict[str, float],
                 skills: Dict[str, List[Skill]],
                 exclusive_weapon: Optional[ExclusiveWeapon] = None):
        self.name = name
        self.char_class = char_class
        self.rarity = rarity
        self.generation = generation
        self.base_stats = base_stats
        self.skills = skills  # {"exploration": [...], "expedition": [...]}
        self.exclusive_weapon = exclusive_weapon

class BonusSource:
    """
    Aggregates all stat bonuses (hero base, weapon, city, territory, etc.) into a single lookup.
    """
    def __init__(self,
                 hero: Hero,
                 city_buffs: Optional[Dict[str, float]] = None,
                 territory_buffs: Optional[Dict[str, float]] = None,
                 pet_buffs: Optional[Dict[str, float]] = None):
        self.hero = hero
        self.city_buffs = city_buffs or {}
        self.territory_buffs = territory_buffs or {}
        self.pet_buffs = pet_buffs or {}
        self.total_bonuses = self._aggregate_bonuses()

    def _aggregate_bonuses(self) -> Dict[str, float]:
        tb = {"attack": 0.0, "defense": 0.0, "lethality": 0.0, "health": 0.0}
        if self.hero.exclusive_weapon:
            for k, v in self.hero.exclusive_weapon.stat_bonuses.items():
                tb[k] = tb.get(k, 0.0) + v
        for k, v in self.city_buffs.items():
            tb[k] = tb.get(k, 0.0) + v
        for k, v in self.territory_buffs.items():
            tb[k] = tb.get(k, 0.0) + v
        for k, v in self.pet_buffs.items():
            tb[k] = tb.get(k, 0.0) + v
        return tb

class TroopGroup:
    """
    A group of troops of a single type, with current count.
    """
    def __init__(self, definition: TroopDefinition, count: int):
        self.definition = definition
        self.count = count

class BattleReportInput:
    """
    Container for all manually-input battle data.
    """
    def __init__(self,
                 attacker_troops: List[TroopGroup],
                 defender_troops: List[TroopGroup],
                 attacker_bonus: BonusSource,
                 defender_bonus: BonusSource,
                 skill_trigger_counts: Optional[Dict[str, int]] = None):
        self.attacker_troops = attacker_troops
        self.defender_troops = defender_troops
        self.attacker_bonus = attacker_bonus
        self.defender_bonus = defender_bonus
        self.skill_trigger_counts = skill_trigger_counts or {}

class CombatState:
    """
    Represents an ongoing combat, resolving rounds until one side is wiped out.
    """
    def __init__(self, report: BattleReportInput):
        self.attacker_groups = [TroopGroup(g.definition, g.count) for g in report.attacker_troops]
        self.defender_groups = [TroopGroup(g.definition, g.count) for g in report.defender_troops]
        self.attacker_bonus = report.attacker_bonus.total_bonuses
        self.defender_bonus = report.defender_bonus.total_bonuses
        self.hero_attacker = report.attacker_bonus.hero
        self.hero_defender = report.defender_bonus.hero
        self.skill_triggers = report.skill_trigger_counts
        self.turn = 0

    def is_over(self) -> bool:
        atk_alive = any(g.count > 0 for g in self.attacker_groups)
        def_alive = any(g.count > 0 for g in self.defender_groups)
        return not (atk_alive and def_alive)

    def step_round(self):
        atk_damage = self._compute_side_damage(
            self.attacker_groups, self.defender_groups, self.attacker_bonus, self.hero_attacker
        )
        def_damage = self._compute_side_damage(
            self.defender_groups, self.attacker_groups, self.defender_bonus, self.hero_defender
        )
        self._apply_damage(self.defender_groups, atk_damage, self.defender_bonus)
        self._apply_damage(self.attacker_groups, def_damage, self.attacker_bonus)
        self.turn += 1

    def _compute_side_damage(
        self,
        attackers: List[TroopGroup],
        defenders: List[TroopGroup],
        bonuses: Dict[str, float],
        hero: Hero
    ) -> Dict[int, float]:
        damage_map = {i: 0.0 for i in range(len(defenders))}
        for i, atk in enumerate(attackers):
            if atk.count <= 0 or i >= len(defenders):
                continue
            def_group = defenders[i]
            dmg = self._compute_damage(atk, def_group, bonuses)
            dmg += self._compute_skill_damage(atk, hero)
            damage_map[i] += dmg
        return damage_map

    def _compute_damage(
        self,
        atk_group: TroopGroup,
        def_group: TroopGroup,
        bonuses: Dict[str, float]
    ) -> float:
        if def_group.count <= 0:
            return 0.0
        eff_atk = atk_group.definition.attack * (1 + bonuses.get("attack", 0.0))
        eff_def = def_group.definition.defense * (1 + bonuses.get("defense", 0.0))
        p_atk = atk_group.definition.power
        p_def = def_group.definition.power
        ratio = p_atk / (p_atk + p_def) if (p_atk + p_def) > 0 else 0.0
        base_per_troop = max(eff_atk * ratio - eff_def, 0.0)
        total = base_per_troop * atk_group.count
        return total

    def _compute_skill_damage(self, atk_group: TroopGroup, hero: Hero) -> float:
        total = 0.0
        for sk in hero.skills.get("expedition", []):
            triggers = self.skill_triggers.get(sk.name, None)
            atk_stat = hero.base_stats.get(f"{hero.char_class}-attack", hero.base_stats.get("attack", 0))
            dmg_per = sk.multiplier * atk_stat
            if triggers is not None:
                total += dmg_per * triggers
            else:
                expected = atk_group.count * sk.proc_chance
                total += dmg_per * expected
        return total

    def _apply_damage(
        self,
        groups: List[TroopGroup],
        damage_map: Dict[int, float],
        bonuses: Dict[str, float]
    ):
        for idx, dmg in damage_map.items():
            if idx >= len(groups):
                continue
            group = groups[idx]
            if group.count <= 0:
                continue
            hp_per = group.definition.health * (1 + bonuses.get("health", 0.0))
            losses = int(dmg / hp_per)
            group.count = max(group.count - losses, 0)

def simulate_battle(report: BattleReportInput, max_rounds: int = 1000) -> Dict[str, Any]:
    """
    Runs a single deterministic battle simulation and returns outcomes.
    """
    state = CombatState(report)
    while not state.is_over() and state.turn < max_rounds:
        state.step_round()
    atk_survivors = sum(g.count for g in state.attacker_groups)
    def_survivors = sum(g.count for g in state.defender_groups)
    winner = "attacker" if atk_survivors > def_survivors else "defender"
    return {
        "winner": winner,
        "attacker_survivors": atk_survivors,
        "defender_survivors": def_survivors,
        "rounds": state.turn
    }

def monte_carlo_battle(report: BattleReportInput, n_sims: int = 1000) -> Dict[str, Any]:
    """
    Runs multiple Monte Carlo simulations sampling skill procs randomly.
    Returns aggregated statistics on win rates and average survivors.
    """
    results = {
        "attacker_wins": 0,
        "defender_wins": 0,
        "attacker_survivors": [],
        "defender_survivors": []
    }
    for _ in range(n_sims):
        report.skill_trigger_counts = {}
        outcome = simulate_battle(report)
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
        "avg_defender_survivors": sum(results["defender_survivors"]) / n_sims
    }
