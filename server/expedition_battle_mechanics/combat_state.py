"""
combat_state.py
===============

•  Resolves an expedition battle round-by-round.
•  Always-on expedition buffs aggregated on construction.
•  ON_TURN skills executed **before** any volleys.
•  Damage maps for both sides are computed first, then casualties are
   applied simultaneously.
•  Side-specific buckets hold hero “flat damage” additions.
"""

from __future__ import annotations

import random
from collections import defaultdict
from typing import Dict, Tuple, DefaultDict, Callable, Optional

from expedition_battle_mechanics.formation import RallyFormation
from expedition_battle_mechanics.bonus import BonusSource
from expedition_battle_mechanics.troop import TroopGroup
from expedition_battle_mechanics.hero import Hero

# passive expedition buffs
from expedition_battle_mechanics.skill_handlers.passive import PASSIVE_SKILLS


# ─────────────────────────────────────────────────────────────────────────────
class BattleReportInput:
    def __init__(
        self,
        attacker_formation: RallyFormation,
        defender_formation: RallyFormation,
        attacker_bonus: BonusSource,
        defender_bonus: BonusSource,
    ):
        self.attacker_formation = attacker_formation
        self.defender_formation = defender_formation
        self.attacker_bonus = attacker_bonus
        self.defender_bonus = defender_bonus


# ─────────────────────────────────────────────────────────────────────────────
class CombatState:
    """Mutable fight state; `step_round()` advances exactly one round."""

    def __init__(self, rpt: BattleReportInput) -> None:
        # formations
        self.attacker_groups: Dict[str, TroopGroup] = (
            rpt.attacker_formation.troop_groups
        )
        self.defender_groups: Dict[str, TroopGroup] = (
            rpt.defender_formation.troop_groups
        )

        # heroes
        self.attacker_heroes: Dict[str, Hero] = rpt.attacker_formation.heroes
        self.defender_heroes: Dict[str, Hero] = rpt.defender_formation.heroes
        for h in self.attacker_heroes.values():
            h.side = "atk"
        for h in self.defender_heroes.values():
            h.side = "def"

        # static city / pet / EW perks
        self.attacker_bonus: Dict[str, float] = rpt.attacker_bonus.total_bonuses
        self.defender_bonus: Dict[str, float] = rpt.defender_bonus.total_bonuses

        # readable passive log for UI
        self.passive_effects: DefaultDict[str, list[str]] = defaultdict(list)

        # merge always-on buffs
        self._apply_passives()

        # bookkeeping
        self.turn: int = 0
        self.skill_procs: DefaultDict[str, int] = defaultdict(int)

        # side-specific “flat extra dmg” buckets
        self._extra_damage: Dict[str, float] = {"atk": 0.0, "def": 0.0}

    # ─────────────────────────────────────────────────────────────────────
    #   public helper for handlers
    def add_extra_damage(self, side: str, amount: float) -> None:
        self._extra_damage[side] += amount

    # ─────────────────────────────────────────────────────────────────────
    #   passive-buff aggregation
    # ─────────────────────────────────────────────────────────────────────
    def _apply_passives(self) -> None:
        def make_adder(
            own: Dict[str, float],
            enemy: Dict[str, float],
            label: str,
            skill_name: str,
        ) -> Callable[[str, float], None]:
            def _add(key: str, pct: float) -> None:
                if key.startswith("enemy-"):
                    stat = key.replace("enemy-", "").replace("-down", "")
                    enemy[stat] = enemy.get(stat, 0.0) - pct
                    self.passive_effects[label].append(
                        f"{skill_name}: {stat} {pct*100:+.1f}%  (enemy)"
                    )
                    return
                stat = key.split("-")[-1] if "-" in key else key
                own[stat] = own.get(stat, 0.0) + pct
                self.passive_effects[label].append(
                    f"{skill_name}: {stat} {pct*100:+.1f}%"
                )

            return _add

        heroes = list(self.attacker_heroes.values()) + list(
            self.defender_heroes.values()
        )
        for hero in heroes:
            for sk in hero.skills["expedition"]:
                handler = PASSIVE_SKILLS.get(sk.name)
                if handler:
                    lvl = hero.selected_skill_levels.get(sk.name, 5)
                    handler(
                        hero,
                        lvl,
                        make_adder(
                            self.attacker_bonus if hero.side == "atk" else self.defender_bonus,
                            self.defender_bonus if hero.side == "atk" else self.attacker_bonus,
                            hero.side,
                            sk.name,
                        ),
                    )

    # ─────────────────────────────────────────────────────────────────────
    #   skill-proc bookkeeping
    # ─────────────────────────────────────────────────────────────────────
    def _proc(self, name: str, side: str, troop_class: Optional[str] = None) -> None:
        if troop_class is not None:
            self.skill_procs[f"{name}-{side}-{troop_class}"] += 1
        else:
            self.skill_procs[f"{name}-{side}"] += 1

    def get_side_groups(self, hero: Hero):
        return (
            self.attacker_groups.values()
            if hero.side == "atk"
            else self.defender_groups.values()
        )

    def get_enemy_groups(self, hero: Hero):
        return (
            self.defender_groups.values()
            if hero.side == "atk"
            else self.attacker_groups.values()
        )

    # ─────────────────────────────────────────────────────────────────────
    #   round lifecycle
    # ─────────────────────────────────────────────────────────────────────
    def is_over(self) -> bool:
        atk_alive = any(g.count > 0 for g in self.attacker_groups.values())
        def_alive = any(g.count > 0 for g in self.defender_groups.values())
        return not (atk_alive and def_alive)

    # ------------------------------------------------------------------ #
    def _run_on_turn(self, side: str) -> None:
        from expedition_battle_mechanics.skill_handlers.on_turn import ON_TURN

        heroes = (
            self.attacker_heroes.values() if side == "atk" else self.defender_heroes.values()
        )
        for hero in heroes:
            for sk in hero.skills["expedition"]:
                handler = ON_TURN.get(sk.name)
                if handler:
                    lvl = hero.selected_skill_levels.get(sk.name, 5)
                    handler(self, hero, lvl)

    # ------------------------------------------------------------------ #
    def step_round(self) -> None:
        """
        Hybrid model:
            • ON_TURN skills first (both sides).
            • Attacker fires; if defender collapses ⇒ round ends here.
            • Defender fires; if attacker collapses ⇒ round ends here.
            • Buff-duration bookkeeping.
        """

        # 0) ON_TURN buffs / nukes for BOTH sides
        self._run_on_turn("atk")
        self._run_on_turn("def")

        # 1) attacker → defender
        atk_map = self._compute_side_damage(
            self.attacker_groups, self.defender_groups, self.attacker_bonus, "atk"
        )
        self._apply_damage(self.defender_groups, atk_map)

        # early-exit if defender dead
        if all(g.count == 0 for g in self.defender_groups.values()):
            self.turn += 1
            return

        # 2) defender → attacker
        def_map = self._compute_side_damage(
            self.defender_groups, self.attacker_groups, self.defender_bonus, "def"
        )
        self._apply_damage(self.attacker_groups, def_map)

        # early-exit if attacker dead
        if all(g.count == 0 for g in self.attacker_groups.values()):
            self.turn += 1
            return

        # 3) expire 2-turn defence buffs
        for g in list(self.attacker_groups.values()) + list(
            self.defender_groups.values()
        ):
            if g.temp_def_bonus_turns > 0:
                g.temp_def_bonus_turns -= 1
                if g.temp_def_bonus_turns == 0:
                    g.temp_def_bonus = 0.0

        self.turn += 1

    # ─────────────────────────────────────────────────────────────────────
    #   damage helpers
    # ─────────────────────────────────────────────────────────────────────
    def _compute_side_damage(
        self,
        attackers: Dict[str, TroopGroup],
        defenders: Dict[str, TroopGroup],
        bonus: Dict[str, float],
        side: str,
    ) -> Dict[str, float]:
        """
        Returns {defender_class: raw_damage}.  Invokes ON_ATTACK handlers.
        """

        from expedition_battle_mechanics.skill_handlers.on_attack import ON_ATTACK

        dmg: DefaultDict[str, float] = defaultdict(float)
        total_enemy = sum(d.count for d in defenders.values() if d.count > 0)
        if total_enemy == 0:
            return dmg

        extra_pool = self._extra_damage[side]

        for cls, atk in attackers.items():
            if atk.count <= 0:
                continue

            hero = (
                self.attacker_heroes[cls] if side == "atk" else self.defender_heroes[cls]
            )

            # on-attack skills
            for sk in hero.skills["expedition"]:
                handler = ON_ATTACK.get(sk.name)
                if handler:
                    lvl = hero.selected_skill_levels.get(sk.name, 5)
                    handler(self, side, atk, hero, lvl)

            for dcls, deff in defenders.items():
                if deff.count <= 0:
                    continue

                atk_mul, def_mul, dmg_mul = self._troop_skill_mods(atk, deff)

                eff_atk = atk.definition.attack * (1 + bonus.get("attack", 0.0))
                eff_def = deff.definition.defense * (1 + bonus.get("defense", 0.0))
                eff_def *= 1 + deff.temp_def_bonus

                eff_atk *= atk_mul
                eff_def *= def_mul

                ratio = atk.definition.power / (
                    atk.definition.power + deff.definition.power
                )
                per_troop = max(eff_atk * ratio - eff_def, eff_atk * ratio * 0.01)
                base = per_troop * atk.count * dmg_mul

                share = deff.count / total_enemy
                extra = extra_pool * share

                dmg[dcls] += base + extra

        # bucket consumed
        self._extra_damage[side] = 0.0
        return dmg

    # ------------------------------------------------------------------ #
    def _troop_skill_mods(
        self, atk: TroopGroup, deff: TroopGroup
    ) -> Tuple[float, float, float]:
        atk_mul = def_mul = 1.0
        dmg_mul = 1.0

        if atk.class_name == "Infantry" and deff.class_name == "Lancer":
            atk_mul *= 1.10
            def_mul *= 1.10

        if deff.class_name == "Infantry":
            def_mul *= 1.06
            if random.random() < 0.375:
                dmg_mul = 0.0
                self._proc("Crystal Shield", "def", deff.class_name.lower())
                if random.random() < 0.15:
                    self._proc("Body of Light", "def", deff.class_name.lower())

        if atk.class_name == "Infantry":
            atk_mul *= 1.06
            if random.random() < 0.375:
                atk_mul *= 2.0
                self._proc("Crystal Shield", "atk", atk.class_name.lower())
                if random.random() < 0.15:
                    self._proc("Body of Light", "atk", atk.class_name.lower())

        if atk.class_name == "Lancer":
            if deff.class_name == "Marksman":
                atk_mul *= 1.10
            if random.random() < 0.15:
                atk_mul *= 2.0
                self._proc("Crystal Lance", "atk", atk.class_name.lower())
        if deff.class_name == "Lancer" and random.random() < 0.10:
            dmg_mul *= 0.5
            self._proc("Incandescent Field", "def", deff.class_name.lower())

        if atk.class_name == "Marksman":
            if deff.class_name == "Infantry":
                atk_mul *= 1.10
            if random.random() < 0.10:
                atk_mul *= 2.0
                self._proc("Volley", "atk", atk.class_name.lower())
            if random.random() < 0.30:
                atk_mul *= 1.50 * 1.25
                self._proc("Crystal Gunpowder", "atk", atk.class_name.lower())

        return atk_mul, def_mul, dmg_mul

    # ------------------------------------------------------------------ #
    def _apply_damage(self, groups: Dict[str, TroopGroup], dmg: Dict[str, float]):
        for cls, raw in dmg.items():
            g = groups[cls]
            if g.count <= 0 or raw <= 0.0:
                continue

            if g.shield > 0.0:
                absorbed = min(g.shield, raw)
                raw -= absorbed
                g.shield -= absorbed

            losses = max(int(raw / g.definition.health), 1)
            g.count = max(g.count - losses, 0)
