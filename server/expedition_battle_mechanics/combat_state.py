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
from typing import Dict, Tuple, DefaultDict, Callable, Optional, List

from expedition_battle_mechanics.formation import RallyFormation
from expedition_battle_mechanics.bonus import BonusSource
from expedition_battle_mechanics.troop import TroopGroup
from expedition_battle_mechanics.hero import Hero

# passive expedition buffs
from expedition_battle_mechanics.skill_handlers.passive import PASSIVE_SKILLS
from expedition_battle_mechanics.skill_handlers import get_passive_strategy
from expedition_battle_mechanics.stacking import BonusBucket


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

        # support heroes (rally joiners)
        self.attacker_support: List[Hero] = list(
            rpt.attacker_formation.support_heroes
        )
        self.defender_support: List[Hero] = list(
            rpt.defender_formation.support_heroes
        )

        for h in self.attacker_heroes.values():
            h.side = "atk"
        for h in self.defender_heroes.values():
            h.side = "def"
        for h in self.attacker_support:
            h.side = "atk"
        for h in self.defender_support:
            h.side = "def"

        # convenience lists for iteration
        self.attacker_all_heroes = list(self.attacker_heroes.values()) + self.attacker_support
        self.defender_all_heroes = list(self.defender_heroes.values()) + self.defender_support

        # static city / pet / EW perks (base + special)
        self.attacker_bonus: Dict[str, float] = rpt.attacker_bonus.base_bonuses
        self.attacker_special: Dict[str, float] = rpt.attacker_bonus.special_bonuses
        self.defender_bonus: Dict[str, float] = rpt.defender_bonus.base_bonuses
        self.defender_special: Dict[str, float] = rpt.defender_bonus.special_bonuses

        # readable passive log for UI
        self.passive_effects: DefaultDict[str, list[str]] = defaultdict(list)

        # merge always-on buffs
        self._apply_passives()

        # bookkeeping
        self.turn: int = 0
        self.skill_procs: DefaultDict[str, int] = defaultdict(int)

        # side-specific “flat extra dmg” buckets
        self._extra_damage: Dict[str, float] = {"atk": 0.0, "def": 0.0}

        # temporary round-based stat bonuses (attack/defense etc.)
        self.temp_bonus: Dict[str, DefaultDict[str, float]] = {
            "atk": defaultdict(float),
            "def": defaultdict(float),
        }
        self.temp_bonus_turns: Dict[str, DefaultDict[str, int]] = {
            "atk": defaultdict(int),
            "def": defaultdict(int),
        }

    # ─────────────────────────────────────────────────────────────────────
    #   public helper for handlers
    def add_extra_damage(self, side: str, amount: float) -> None:
        self._extra_damage[side] += amount

    # ─────────────────────────────────────────────────────────────────────
    #   passive-buff aggregation
    # ─────────────────────────────────────────────────────────────────────
    def _apply_passives(self) -> None:
        # Collect all passive effects per (side, skill) so that stacking rules
        # can be applied according to rally mechanics (additive vs. highest).
        effects: Dict[tuple[str, str], BonusBucket] = {}

        heroes = self.attacker_all_heroes + self.defender_all_heroes
        for hero in heroes:
            for sk in hero.skills["expedition"]:
                handler = PASSIVE_SKILLS.get(sk.name)
                if not handler:
                    continue

                lvl = hero.selected_skill_levels.get(sk.name, 5)
                collected: list[tuple[str, float]] = []

                def _collect(key: str, pct: float) -> None:
                    collected.append((key, pct))

                handler(hero, lvl, _collect)

                bucket = effects.setdefault(
                    (hero.side, sk.name), BonusBucket(get_passive_strategy(sk.name))
                )
                for key, pct in collected:
                    bucket.add(key, pct)

        # Apply aggregated effects to bonus dictionaries
        for (side, skill_name), bucket in effects.items():
            own = self.attacker_bonus if side == "atk" else self.defender_bonus
            enemy = self.defender_bonus if side == "atk" else self.attacker_bonus

            for key, pct in bucket.as_dict().items():
                if key.startswith("enemy-"):
                    stat = key.replace("enemy-", "").replace("-down", "")
                    stat_key = stat.replace("-", "_")
                    enemy[stat_key] = enemy.get(stat_key, 0.0) - pct
                    self.passive_effects[side].append(
                        f"{skill_name}: {stat} {pct*100:+.1f}%  (enemy)"
                    )
                    continue

                if "-" in key:
                    cls, stat = key.split("-", 1)
                    stat_key = f"{cls.lower()}_{stat}"
                    display = key
                else:
                    stat_key = key
                    display = key
                own[stat_key] = own.get(stat_key, 0.0) + pct
                self.passive_effects[side].append(
                    f"{skill_name}: {display} {pct*100:+.1f}%"
                )

    # ------------------------------------------------------------------ #
    def add_temp_bonus(self, side: str, key: str, pct: float, turns: int) -> None:
        """Apply a temporary stat modifier for ``turns`` rounds."""
        if "-" in key:
            cls, stat = key.split("-", 1)
            norm = f"{cls.lower()}_{stat}"
        else:
            norm = key
        self.temp_bonus[side][norm] += pct
        self.temp_bonus_turns[side][norm] = max(
            self.temp_bonus_turns[side][norm], turns
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

        heroes = self.attacker_all_heroes if side == "atk" else self.defender_all_heroes
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
            • Both sides calculate damage before any losses are applied.
            • Casualties are applied simultaneously.
            • Buff-duration bookkeeping.
        """

        # 0) ON_TURN buffs / nukes for BOTH sides
        self._run_on_turn("atk")
        self._run_on_turn("def")

        # 1) compute damage maps for both sides BEFORE applying
        atk_map = self._compute_side_damage(
            self.attacker_groups,
            self.defender_groups,
            self.attacker_bonus,
            self.attacker_special,
            "atk",
        )
        def_map = self._compute_side_damage(
            self.defender_groups,
            self.attacker_groups,
            self.defender_bonus,
            self.defender_special,
            "def",
        )

        # 2) apply casualties simultaneously
        self._apply_damage(self.defender_groups, atk_map, "def")
        self._apply_damage(self.attacker_groups, def_map, "atk")

        # 3) expire 2-turn defence buffs
        for g in list(self.attacker_groups.values()) + list(
            self.defender_groups.values()
        ):
            if g.temp_def_bonus_turns > 0:
                g.temp_def_bonus_turns -= 1
                if g.temp_def_bonus_turns == 0:
                    g.temp_def_bonus = 0.0

        # 4) decay temporary bonuses
        for side in ("atk", "def"):
            for k in list(self.temp_bonus_turns[side].keys()):
                self.temp_bonus_turns[side][k] -= 1
                if self.temp_bonus_turns[side][k] <= 0:
                    del self.temp_bonus_turns[side][k]
                    del self.temp_bonus[side][k]

        self.turn += 1

    # ─────────────────────────────────────────────────────────────────────
    #   damage helpers
    # ─────────────────────────────────────────────────────────────────────
    def _compute_side_damage(
        self,
        attackers: Dict[str, TroopGroup],
        defenders: Dict[str, TroopGroup],
        bonus: Dict[str, float],
        bonus_special: Dict[str, float],
        side: str,
    ) -> Dict[str, float]:
        """Returns {defender_class: raw_damage}.  Invokes ON_ATTACK handlers.

        ``bonus`` holds regular stat modifiers while ``bonus_special`` contains
        the special bonuses (territory, gem buffs, etc.) that apply using the
        compound formula described on the Whiteout Survival wiki.
        """

        from expedition_battle_mechanics.skill_handlers.on_attack import ON_ATTACK

        dmg: DefaultDict[str, float] = defaultdict(float)
        total_enemy = sum(d.count for d in defenders.values() if d.count > 0)
        if total_enemy == 0:
            return dmg

        extra_pool = self._extra_damage[side]

        # merge temporary bonuses for both sides
        bonus_combined = bonus.copy()
        for k, v in self.temp_bonus[side].items():
            bonus_combined[k] = bonus_combined.get(k, 0.0) + v
        special_combined = bonus_special.copy()

        enemy_base = self.defender_bonus if side == "atk" else self.attacker_bonus
        enemy_special = (
            self.defender_special if side == "atk" else self.attacker_special
        )
        enemy_bonus_combined = enemy_base.copy()
        enemy_special_combined = enemy_special.copy()
        enemy_side = "def" if side == "atk" else "atk"
        for k, v in self.temp_bonus[enemy_side].items():
            enemy_bonus_combined[k] = enemy_bonus_combined.get(k, 0.0) + v

        def cls_bonus(src: Dict[str, float], cls: str, stat: str) -> float:
            key = f"{cls.lower()}_{stat}"
            return src.get(stat, 0.0) + src.get(key, 0.0)

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

            base_pct = cls_bonus(bonus_combined, cls, "attack")
            spec_pct = cls_bonus(special_combined, cls, "attack")
            atk_stat = atk.definition.attack * (
                1 + base_pct + atk.definition.stat_bonuses.get("Attack", 0.0)
            )
            atk_stat = atk_stat * (1 + spec_pct) + atk.definition.attack * spec_pct

            # lethality stat – bypasses defense and chips health directly
            leth_base = cls_bonus(bonus_combined, cls, "lethality")
            leth_spec = cls_bonus(special_combined, cls, "lethality")
            leth_stat = atk.definition.lethality * (
                1 + leth_base + atk.definition.stat_bonuses.get("Lethality", 0.0)
            )
            leth_stat = leth_stat * (1 + leth_spec) + atk.definition.lethality * leth_spec

            for dcls, deff in defenders.items():
                if deff.count <= 0:
                    continue

                atk_mul, def_mul, dmg_mul = self._troop_skill_mods(atk, deff)

                def_base_pct = cls_bonus(enemy_bonus_combined, dcls, "defense")
                def_spec_pct = cls_bonus(enemy_special_combined, dcls, "defense")
                def_stat = deff.definition.defense * (
                    1 + def_base_pct + deff.definition.stat_bonuses.get("Defense", 0.0)
                )
                def_stat = def_stat * (1 + def_spec_pct) + deff.definition.defense * def_spec_pct
                def_stat *= 1 + deff.temp_def_bonus

                eff_atk = atk_stat * atk_mul
                eff_leth = leth_stat * atk_mul
                eff_def = def_stat * def_mul

                ratio = atk.definition.power / (
                    atk.definition.power + deff.definition.power
                )
                per_troop = max(eff_atk * ratio - eff_def, eff_atk * ratio * 0.01)
                per_troop += eff_leth * ratio
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

        # ---- Infantry ----
        if atk.class_name == "Infantry" and deff.class_name == "Lancer":
            atk_mul *= 1.10  # Master Brawler

        if deff.class_name == "Infantry":
            def_mul *= 1.06  # Body of Light (always-on portion)
            if atk.class_name == "Lancer":
                def_mul *= 1.10  # Bands of Steel
            if random.random() < 0.375:  # Crystal Shield
                dmg_mul = 0.0
                self._proc("Crystal Shield", "def", deff.class_name.lower())
                if random.random() < 0.15:  # Body of Light bonus when shield active
                    dmg_mul *= 0.85
                    self._proc("Body of Light", "def", deff.class_name.lower())

        # ---- Lancer ----
        if atk.class_name == "Lancer":
            if deff.class_name == "Marksman":
                atk_mul *= 1.10  # Charge
            if random.random() < 0.15:
                atk_mul *= 2.0  # Crystal Lance
                self._proc("Crystal Lance", "atk", atk.class_name.lower())
        if deff.class_name == "Lancer" and random.random() < 0.10:
            dmg_mul *= 0.5  # Incandescent Field
            self._proc("Incandescent Field", "def", deff.class_name.lower())

        # ---- Marksman ----
        if atk.class_name == "Marksman":
            atk_mul *= 1.04  # Flame Charge base attack
            if deff.class_name == "Infantry":
                atk_mul *= 1.10  # Ranged Strike
            if random.random() < 0.10:
                atk_mul *= 2.0  # Volley
                self._proc("Volley", "atk", atk.class_name.lower())
            if random.random() < 0.30:
                atk_mul *= 1.50 * 1.25  # Crystal Gunpowder + Flame Charge bonus
                self._proc("Crystal Gunpowder", "atk", atk.class_name.lower())

        return atk_mul, def_mul, dmg_mul

    # ------------------------------------------------------------------ #
    def _apply_damage(self, groups: Dict[str, TroopGroup], dmg: Dict[str, float], side: str):
        """Apply raw damage to a side's troop groups.

        ``side`` is the defending side ("atk" or "def") so we can look up the
        appropriate health bonuses without relying on object identity.
        """

        bonus = (self.attacker_bonus if side == "atk" else self.defender_bonus).copy()
        for k, v in self.temp_bonus[side].items():
            bonus[k] = bonus.get(k, 0.0) + v
        special = self.attacker_special if side == "atk" else self.defender_special

        for cls, raw in dmg.items():
            g = groups[cls]
            if g.count <= 0 or raw <= 0.0:
                continue

            if g.shield > 0.0:
                absorbed = min(g.shield, raw)
                raw -= absorbed
                g.shield -= absorbed

            cls_l = g.class_name.lower()
            base_pct = (
                bonus.get("health", 0.0)
                + bonus.get(f"{cls_l}_health", 0.0)
                + g.definition.stat_bonuses.get("Health", 0.0)
            )
            spec_pct = special.get("health", 0.0) + special.get(f"{cls_l}_health", 0.0)
            hp = g.definition.health * (1 + base_pct)
            hp = hp * (1 + spec_pct) + g.definition.health * spec_pct

            losses = max(int(raw / hp), 1)
            g.count = max(g.count - losses, 0)
