# """
# Combat round resolver — full RNG implementation of troop skills.
# NO SECTION ABBREVIATED.
# """

# import random
# from collections import defaultdict
# from typing import Dict, Optional

# from expedition_battle_mechanics.bonus import BonusSource
# from expedition_battle_mechanics.formation import RallyFormation
# from expedition_battle_mechanics.troop import TroopGroup


# class BattleReportInput:  # unchanged
#     def __init__(
#         self,
#         attacker_formation: RallyFormation,
#         defender_formation: RallyFormation,
#         attacker_bonus: BonusSource,
#         defender_bonus: BonusSource,
#         skill_trigger_counts: Optional[Dict[str, int]] = None,
#     ):
#         self.attacker_formation = attacker_formation
#         self.defender_formation = defender_formation
#         self.attacker_bonus = attacker_bonus
#         self.defender_bonus = defender_bonus
#         self.skill_trigger_counts = skill_trigger_counts or {}


# class CombatState:
#     """Mutable state advanced one round at a time."""

#     def __init__(self, report: BattleReportInput):
#         # direct references — the higher-level simulate_battle() deep-copies first
#         self.attacker_groups = report.attacker_formation.troop_groups
#         self.defender_groups = report.defender_formation.troop_groups
#         self.attacker_heroes = report.attacker_formation.heroes
#         self.defender_heroes = report.defender_formation.heroes
#         self.attacker_bonus = report.attacker_bonus.total_bonuses
#         self.defender_bonus = report.defender_bonus.total_bonuses
#         self.skill_triggers = report.skill_trigger_counts
#         self.turn = 0

#     # ─────────────────────────────────────────────────────────────────────────
#     # Battle loop
#     # ─────────────────────────────────────────────────────────────────────────
#     def is_over(self) -> bool:
#         atk_alive = any(g.count > 0 for g in self.attacker_groups.values())
#         def_alive = any(g.count > 0 for g in self.defender_groups.values())
#         return not (atk_alive and def_alive)

#     def step_round(self) -> None:
#         atk_buffs = self._get_total_bonuses(self.attacker_bonus)
#         def_buffs = self._get_total_bonuses(self.defender_bonus)

#         # compute damage maps in both directions
#         dmg_to_def = self._compute_side_damage(
#             self.attacker_groups,
#             self.defender_groups,
#             atk_buffs,
#             self.attacker_heroes,
#         )
#         dmg_to_atk = self._compute_side_damage(
#             self.defender_groups,
#             self.attacker_groups,
#             def_buffs,
#             self.defender_heroes,
#         )

#         self._apply_damage(self.defender_groups, dmg_to_def)
#         self._apply_damage(self.attacker_groups, dmg_to_atk)

#         self.turn += 1

#     # ─────────────────────────────────────────────────────────────────────────
#     # Buffs (only global health/attack/defense from research etc.)
#     # ─────────────────────────────────────────────────────────────────────────
#     @staticmethod
#     def _get_total_bonuses(bonus_source: dict) -> Dict[str, float]:
#         # bonus_source is already a flat dict {attack, defense, health}
#         return bonus_source

#     # ─────────────────────────────────────────────────────────────────────────
#     # Damage calculation
#     # ─────────────────────────────────────────────────────────────────────────
#     def _compute_side_damage(
#         self,
#         attackers: Dict[str, TroopGroup],
#         defenders: Dict[str, TroopGroup],
#         side_bonuses: Dict[str, float],
#         side_heroes,
#     ):
#         """
#         Each attacker class distributes damage across **all** defender classes.
#         Lancer Ambusher: 20 % chance to replicate the hit onto Marksman.
#         """
#         damage_map = defaultdict(float)
#         total_enemy = sum(g.count for g in defenders.values() if g.count > 0)
#         if total_enemy == 0:
#             return damage_map

#         for atk_cls, atk_group in attackers.items():
#             if atk_group.count <= 0:
#                 continue

#             hero = side_heroes[atk_cls]
#             skill_damage_total = self._compute_skill_damage(atk_group, hero)

#             for def_cls, def_group in defenders.items():
#                 if def_group.count <= 0:
#                     continue

#                 atk_mult, def_mult, dmg_mult = self._troop_skill_modifiers(
#                     atk_group, def_group
#                 )

#                 dmg = self._base_damage(
#                     atk_group,
#                     def_group,
#                     side_bonuses,
#                     atk_mult,
#                     def_mult,
#                     dmg_mult,
#                 )

#                 # share skill damage proportional to defender troop count
#                 share = def_group.count / total_enemy
#                 dmg += skill_damage_total * share

#                 # Ambusher extra hit on Marksman
#                 if (
#                     atk_cls == "Lancer"
#                     and def_cls == "Infantry"
#                     and defenders["Marksman"].count > 0
#                     and random.random() < 0.20
#                 ):
#                     damage_map["Marksman"] += dmg  # replicate same dmg to Marksman

#                 damage_map[def_cls] += dmg

#         return damage_map

#     # --------------------------------------------------------------------- #
#     # Base damage before skills share
#     # --------------------------------------------------------------------- #
#     def _base_damage(
#         self,
#         atk_group: TroopGroup,
#         def_group: TroopGroup,
#         bonuses: Dict[str, float],
#         atk_mult: float,
#         def_mult: float,
#         dmg_mult: float,
#     ) -> float:
#         if def_group.count <= 0:
#             return 0.0

#         eff_atk = atk_group.definition.attack * (1 + bonuses.get("attack", 0.0))
#         eff_def = def_group.definition.defense * (1 + bonuses.get("defense", 0.0))

#         eff_atk *= atk_mult
#         eff_def *= def_mult

#         # very small floor damage so battles cannot stall
#         ratio = atk_group.definition.power / (
#             atk_group.definition.power + def_group.definition.power
#         )
#         per_troop = max(eff_atk * ratio - eff_def, eff_atk * ratio * 0.01)

#         return per_troop * atk_group.count * dmg_mult

#     # --------------------------------------------------------------------- #
#     # Skill-damage (heroes — not troop skills)
#     # --------------------------------------------------------------------- #
#     def _compute_skill_damage(self, atk_group, hero) -> float:
#         total = 0.0
#         for sk in hero.skills.get("expedition", []):
#             # deterministic trigger counts (if supplied) otherwise RNG
#             triggers = self.skill_triggers.get(sk.name)
#             atk_stat = hero.base_stats.get(
#                 f"{hero.char_class}-attack", hero.base_stats.get("attack", 0)
#             )
#             dmg_each = sk.multiplier * atk_stat
#             if triggers is not None:
#                 total += dmg_each * triggers
#             else:
#                 total += dmg_each * atk_group.count * sk.proc_chance
#         return total

#     # --------------------------------------------------------------------- #
#     # Troop skill modifiers — **full RNG fidelity**
#     # --------------------------------------------------------------------- #
#     @staticmethod
#     def _troop_skill_modifiers(atk: TroopGroup, deff: TroopGroup):
#         """Return per-exchange multipliers (attack, defense, damage-taken)."""
#         atk_mult, def_mult, dmg_mult = 1.0, 1.0, 1.0

#         a_name = atk.definition.name
#         d_name = deff.definition.name

#         a_cls = "Infantry" if "Infantry" in a_name else "Lancer" if "Lancer" in a_name else "Marksman"
#         d_cls = "Infantry" if "Infantry" in d_name else "Lancer" if "Lancer" in d_name else "Marksman"

#         # ─── Class counters (always-on) ────────────────────────────────────
#         if a_cls == "Infantry" and d_cls == "Lancer":
#             atk_mult *= 1.10  # Master Brawler
#         if a_cls == "Lancer" and d_cls == "Marksman":
#             atk_mult *= 1.10  # Charge
#         if a_cls == "Marksman" and d_cls == "Infantry":
#             atk_mult *= 1.10  # Ranged Strike

#         # Bands of Steel – defender Infantry vs Lancer gets +10 % DEF
#         if d_cls == "Infantry" and a_cls == "Lancer":
#             def_mult *= 1.10

#         # Flame Charge flat +4 % ATK for all Marksman attacks
#         if a_cls == "Marksman":
#             atk_mult *= 1.04

#         # ─── Proc-based effects ───────────────────────────────────────────
#         # Crystal Lance – 15 % chance Lancer double-dmg
#         if a_cls == "Lancer" and random.random() < 0.15:
#             atk_mult *= 2.0

#         # Volley – 10 % chance Marksman strike twice
#         if a_cls == "Marksman" and random.random() < 0.10:
#             atk_mult *= 2.0

#         # Crystal Gunpowder – 30 % chance +50 % dmg
#         gunpowder_proc = False
#         if a_cls == "Marksman" and random.random() < 0.30:
#             atk_mult *= 1.50
#             gunpowder_proc = True

#         # Flame Charge extra 25 % only when Gunpowder procs
#         if a_cls == "Marksman" and gunpowder_proc:
#             atk_mult *= 1.25

#         # Crystal Shield – 37.5 % chance Infantry negate ALL dmg
#         shield_proc = False
#         if d_cls == "Infantry" and random.random() < 0.375:
#             dmg_mult = 0.0
#             shield_proc = True

#         # Body of Light – +6 % DEF always, +15 % extra reduction if shield proc
#         if d_cls == "Infantry":
#             def_mult *= 1.06
#             if shield_proc and random.random() < 0.15:
#                 dmg_mult *= 0.85  # additional 15 % reduction

#         # Incandescent Field – Lancer 10 % chance to take half dmg
#         if d_cls == "Lancer" and random.random() < 0.10:
#             dmg_mult *= 0.5

#         return atk_mult, def_mult, dmg_mult

#     # --------------------------------------------------------------------- #
#     # Apply damage map to groups
#     # --------------------------------------------------------------------- #
#     @staticmethod
#     def _apply_damage(groups: Dict[str, TroopGroup], damage_map: Dict[str, float]):
#         for cls, dmg in damage_map.items():
#             group = groups[cls]
#             if group.count <= 0 or dmg <= 0:
#                 continue
#             hp = group.definition.health
#             losses = max(int(dmg / hp), 1)
#             group.count = max(group.count - losses, 0)
