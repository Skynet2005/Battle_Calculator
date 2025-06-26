"""
Combat round resolver — now tracks skill proc counts.
Cleaned up: no .class_name attribute required.
NO SECTION ABBREVIATED.
"""

import random
from collections import defaultdict
from typing import Dict, Optional, Tuple

from expedition_battle_mechanics.bonus import BonusSource
from expedition_battle_mechanics.formation import RallyFormation
from expedition_battle_mechanics.troop import TroopGroup


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def troop_class(group: TroopGroup) -> str:
    """Return 'Infantry' | 'Lancer' | 'Marksman' from the troop's name."""
    name = group.definition.name
    if "Infantry" in name:
        return "Infantry"
    if "Lancer" in name:
        return "Lancer"
    return "Marksman"


# ─────────────────────────────────────────────────────────────────────────────
class BattleReportInput:
    def __init__(
        self,
        attacker_formation: RallyFormation,
        defender_formation: RallyFormation,
        attacker_bonus: BonusSource,
        defender_bonus: BonusSource,
        skill_trigger_counts: Optional[Dict[str, int]] = None,
    ):
        self.attacker_formation = attacker_formation
        self.defender_formation = defender_formation
        self.attacker_bonus = attacker_bonus
        self.defender_bonus = defender_bonus
        self.skill_trigger_counts = skill_trigger_counts or {}


class CombatState:
    """
    Mutable state advanced one round at a time.
    Tracks per-battle skill procs in `self.skill_procs`.
    """

    def __init__(self, report: BattleReportInput):
        self.attacker_groups = report.attacker_formation.troop_groups  # {"Infantry": TroopGroup, ...}
        self.defender_groups = report.defender_formation.troop_groups
        self.attacker_heroes = report.attacker_formation.heroes        # {"Infantry": Hero, ...}
        self.defender_heroes = report.defender_formation.heroes
        self.attacker_bonus = report.attacker_bonus.total_bonuses
        self.defender_bonus = report.defender_bonus.total_bonuses
        self.turn = 0

        # {"Crystal Shield-def": n, "Volley-atk": n, ...}
        self.skill_procs: Dict[str, int] = defaultdict(int)

    # ─────────────────────────────────────────────────────────────────────────
    # Proc-count helper
    # ─────────────────────────────────────────────────────────────────────────
    def _proc(self, name: str, side: str) -> None:
        """Increment `name` for 'atk' or 'def' side."""
        self.skill_procs[f"{name}-{side}"] += 1

    # ─────────────────────────────────────────────────────────────────────────
    # Battle loop
    # ─────────────────────────────────────────────────────────────────────────
    def is_over(self) -> bool:
        atk_alive = any(g.count > 0 for g in self.attacker_groups.values())
        def_alive = any(g.count > 0 for g in self.defender_groups.values())
        return not (atk_alive and def_alive)

    def step_round(self) -> None:
        dmg_to_def = self._compute_side_damage(
            self.attacker_groups,
            self.defender_groups,
            self.attacker_bonus,
            side="atk",
        )
        dmg_to_atk = self._compute_side_damage(
            self.defender_groups,
            self.attacker_groups,
            self.defender_bonus,
            side="def",
        )

        self._apply_damage(self.defender_groups, dmg_to_def)
        self._apply_damage(self.attacker_groups, dmg_to_atk)
        self.turn += 1

    # ─────────────────────────────────────────────────────────────────────────
    # Damage computation
    # ─────────────────────────────────────────────────────────────────────────
    def _compute_side_damage(
        self,
        attackers: Dict[str, TroopGroup],
        defenders: Dict[str, TroopGroup],
        side_bonuses: Dict[str, float],
        side: str,  # "atk" | "def"  (for proc-key suffix)
    ) -> Dict[str, float]:
        damage_map: Dict[str, float] = defaultdict(float)
        total_enemy = sum(g.count for g in defenders.values() if g.count > 0)
        if total_enemy == 0:
            return damage_map

        for atk_cls, atk_group in attackers.items():
            if atk_group.count <= 0:
                continue

            # hero skill damage (un-tracked for procs)
            skill_total = self._compute_skill_damage(atk_cls, atk_group, side)

            for def_cls, def_group in defenders.items():
                if def_group.count <= 0:
                    continue

                atk_mult, def_mult, dmg_mult = self._troop_skill_modifiers(
                    atk_group,
                    def_group,
                    side,
                )

                base = self._base_damage(
                    atk_group,
                    def_group,
                    side_bonuses,
                    atk_mult,
                    def_mult,
                    dmg_mult,
                )

                # share hero-skill damage proportionally
                share = def_group.count / total_enemy
                base += skill_total * share

                # 20 % Ambusher spill-over
                if (
                    atk_cls == "Lancer"
                    and def_cls == "Infantry"
                    and defenders["Marksman"].count > 0
                    and random.random() < 0.20
                ):
                    self._proc("Ambusher", side)
                    damage_map["Marksman"] += base * 0.20  # only the extra 20 %

                damage_map[def_cls] += base

        return damage_map

    # ------------------------------------------------------------------ #
    def _base_damage(
        self,
        atk_group: TroopGroup,
        def_group: TroopGroup,
        bonuses: Dict[str, float],
        atk_mult: float,
        def_mult: float,
        dmg_mult: float,
    ) -> float:
        eff_atk = atk_group.definition.attack * (1 + bonuses.get("attack", 0.0))
        eff_def = def_group.definition.defense * (1 + bonuses.get("defense", 0.0))
        eff_atk *= atk_mult
        eff_def *= def_mult

        ratio = atk_group.definition.power / (
            atk_group.definition.power + def_group.definition.power
        )
        per_troop = max(eff_atk * ratio - eff_def, eff_atk * ratio * 0.01)
        return per_troop * atk_group.count * dmg_mult

    # ------------------------------------------------------------------ #
    def _compute_skill_damage(
        self,
        atk_cls: str,
        atk_group: TroopGroup,
        side: str,
    ) -> float:
        """
        Hero expedition skills (not troop skills). No proc counting here.
        """
        hero = (
            self.attacker_heroes if side == "atk" else self.defender_heroes
        )[atk_cls]
        total = 0.0
        for sk in hero.skills.get("expedition", []):
            atk_stat = hero.base_stats.get(
                f"{hero.char_class}-attack", hero.base_stats.get("attack", 0)
            )
            total += sk.multiplier * atk_stat * atk_group.count * sk.proc_chance
        return total

    # ------------------------------------------------------------------ #
    def _troop_skill_modifiers(
        self,
        atk: TroopGroup,
        deff: TroopGroup,
        side: str,
    ) -> Tuple[float, float, float]:
        """
        Returns (atk_mult, def_mult, dmg_mult) and records troop-skill procs.
        """
        atk_mult = def_mult = 1.0
        dmg_mult = 1.0

        a_cls = troop_class(atk)
        d_cls = troop_class(deff)

        # Always-on counters
        if a_cls == "Infantry" and d_cls == "Lancer":
            atk_mult *= 1.10  # Master Brawler
        if a_cls == "Lancer" and d_cls == "Marksman":
            atk_mult *= 1.10  # Charge
        if a_cls == "Marksman" and d_cls == "Infantry":
            atk_mult *= 1.10  # Ranged Strike

        # Permanent buffs
        if d_cls == "Infantry" and a_cls == "Lancer":
            def_mult *= 1.10  # Bands of Steel
        if a_cls == "Marksman":
            atk_mult *= 1.04  # Flame Charge flat +4 %

        # Proc-based ------------------------------------------------------
        if a_cls == "Lancer" and random.random() < 0.15:  # Crystal Lance
            atk_mult *= 2.0
            self._proc("Crystal Lance", side)

        if a_cls == "Marksman" and random.random() < 0.10:  # Volley
            atk_mult *= 2.0
            self._proc("Volley", side)

        gunpowder = False
        if a_cls == "Marksman" and random.random() < 0.30:  # Crystal Gunpowder
            atk_mult *= 1.50
            gunpowder = True
            self._proc("Crystal Gunpowder", side)
        if a_cls == "Marksman" and gunpowder:
            atk_mult *= 1.25  # Flame Charge bonus 25 %

        shield = False
        if d_cls == "Infantry" and random.random() < 0.375:  # Crystal Shield
            dmg_mult = 0.0
            shield = True
            self._proc("Crystal Shield", "def" if side == "atk" else "atk")

        if d_cls == "Infantry":
            def_mult *= 1.06  # Body of Light passive
            if shield and random.random() < 0.15:
                dmg_mult *= 0.85
                self._proc("Body of Light", "def" if side == "atk" else "atk")

        if d_cls == "Lancer" and random.random() < 0.10:  # Incandescent Field
            dmg_mult *= 0.5
            self._proc("Incandescent Field", "def" if side == "atk" else "atk")

        return atk_mult, def_mult, dmg_mult

    # ------------------------------------------------------------------ #
    @staticmethod
    def _apply_damage(groups: Dict[str, TroopGroup], dmg: Dict[str, float]) -> None:
        for cls, amount in dmg.items():
            g = groups[cls]
            if g.count <= 0 or amount <= 0:
                continue
            losses = max(int(amount / g.definition.health), 1)
            g.count = max(g.count - losses, 0)
