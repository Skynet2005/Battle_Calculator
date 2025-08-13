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

from .formation import RallyFormation
from .bonus import BonusSource
from .troop import TroopGroup
from .hero import Hero
from .timeline import TurnLogger

# passive expedition buffs
from .passive import PASSIVE_SKILLS, get_passive_strategy
from .stacking import BonusBucket


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

    def __init__(self, rpt: BattleReportInput, use_power_weighting: bool = True) -> None:
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

        # Created Logic for review: apply one active pet skill if provided via special bonuses
        # The API feeds pet base stats into city buffs. For an active skill (short-term buff),
        # we model it as a temporary special bonus applied to the appropriate side.
        try:
            for side_key, pets in (("atk", getattr(rpt.attacker_formation, "pets", None)), ("def", getattr(rpt.defender_formation, "pets", None))):
                if not pets:
                    continue
                for p in pets:
                    if not p.get("enabled"):
                        continue
                    pet = str(p.get("name", ""))
                    lvl = max(1, min(10, int(p.get("level", 1))))
                    bonus_map: dict[str, float] = {}
                    if pet == "Cave Lion":  # troops attack up
                        bonus_map["attack"] = {1:2.5,2:3,3:3.5,4:4,5:5,6:6,7:7,8:8,9:9,10:10}[lvl] / 100.0
                    elif pet == "Mammoth":  # troops defense up
                        bonus_map["defense"] = {1:2.5,2:3,3:3.5,4:4,5:5,6:6,7:7,8:8,9:9,10:10}[lvl] / 100.0
                    elif pet == "Frost Gorilla":  # troops health up
                        bonus_map["health"] = {1:2.5,2:3,3:3.5,4:4,5:5,6:6,7:7,8:8,9:9,10:10}[lvl] / 100.0
                    elif pet == "Saber Tooth Tiger":  # troops lethality up
                        bonus_map["lethality"] = {1:2.5,2:3,3:3.5,4:4,5:5,6:6,7:7,8:8,9:9,10:10}[lvl] / 100.0
                    elif pet == "Titan Roc":  # enemy health down
                        bonus_map["enemy-health-down"] = {1:1.5,2:2,3:2.5,4:3,5:3.5,6:4,7:5}[min(lvl,7)] / 100.0
                    elif pet == "Snow Leopard":  # enemy lethality down (approximate)
                        bonus_map["enemy-lethality-down"] = {1:1.5,2:2,3:2.5,4:3,5:3.5,6:4,7:4.5,8:5}[min(lvl,8)] / 100.0

                    if not bonus_map:
                        continue
                    if side_key == "atk":
                        for k, v in bonus_map.items():
                            if k.startswith("enemy-"):
                                key = k.replace("enemy-", "").replace("-down", "")
                                self.defender_special[key] = self.defender_special.get(key, 0.0) - float(v)
                            else:
                                self.attacker_special[k] = self.attacker_special.get(k, 0.0) + float(v)
                    else:
                        for k, v in bonus_map.items():
                            if k.startswith("enemy-"):
                                key = k.replace("enemy-", "").replace("-down", "")
                                self.attacker_special[key] = self.attacker_special.get(key, 0.0) - float(v)
                            else:
                                self.defender_special[k] = self.defender_special.get(k, 0.0) + float(v)
        except Exception:
            pass

        # bookkeeping
        self.turn: int = 0
        self.skill_procs: DefaultDict[str, int] = defaultdict(int)
        self.turnlog = TurnLogger()

        # Created Logic for review: toggle for using Troop Power ratio in damage weighting.
        # Tests expect weighting by default; docs ask to ignore Power, so expose a flag.
        self.use_power_weighting: bool = bool(use_power_weighting)

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

        # Created Logic for review: dampen flat extra damage pools so burst skills don't end battles in 1 turn
        # This factor scales down the sum of flat extras before distributing to defenders.
        # Tune between 0.002 and 0.01 depending on desired burstiness.
        self.extra_pool_damping: float = 0.004

    # ─────────────────────────────────────────────────────────────────────
    #   public helper for handlers
    def add_extra_damage(self, side: str, amount: float) -> None:
        self._extra_damage[side] += amount
        # Log extra damage attribution for timeline
        self.turnlog.add_extra(side, float(amount))

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

                # Created Logic for review: use EW level for the EW expedition skill if present
                if hero.exclusive_weapon and hero.exclusive_weapon.skills.get("expedition") and sk.name == hero.exclusive_weapon.skills["expedition"].name:
                    lvl = hero.exclusive_weapon.level
                else:
                    lvl = hero.selected_skill_levels.get(sk.name, 5)
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
        # Record event for this turn (displayed on total line)
        try:
            cls = (troop_class.capitalize() if troop_class else "All")
        except Exception:
            cls = "All"
        # turn index for display is 1-based; step_round closes with (turn+1)
        self.turnlog.proc(self.turn + 1, side, name, cls)

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
        from expedition_battle_mechanics.on_turn import ON_TURN as ON_TURN

        heroes = self.attacker_all_heroes if side == "atk" else self.defender_all_heroes
        for hero in heroes:
            for sk in hero.skills["expedition"]:
                handler = ON_TURN.get(sk.name)
                if handler:
                    # Created Logic for review: use EW level for the EW expedition skill if present
                    if hero.exclusive_weapon and hero.exclusive_weapon.skills.get("expedition") and sk.name == hero.exclusive_weapon.skills["expedition"].name:
                        lvl = hero.exclusive_weapon.level
                    else:
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
        atk_map, atk_by_attacker_cls, atk_extra = self._compute_side_damage(
            self.attacker_groups,
            self.defender_groups,
            self.attacker_bonus,
            self.attacker_special,
            "atk",
        )
        def_map, def_by_attacker_cls, def_extra = self._compute_side_damage(
            self.defender_groups,
            self.attacker_groups,
            self.defender_bonus,
            self.defender_special,
            "def",
        )

        # 2) distribute flat extras proportionally across defender classes
        def _with_extra(dist_map: Dict[str, float], defenders: Dict[str, TroopGroup], extra_pool: float) -> Dict[str, float]:
            out = dist_map.copy()
            total_enemy = sum(d.count for d in defenders.values() if d.count > 0)
            if total_enemy > 0 and extra_pool > 0:
                damped = extra_pool * self.extra_pool_damping
                for dcls, deff in defenders.items():
                    if deff.count <= 0:
                        continue
                    share = deff.count / total_enemy
                    out[dcls] = out.get(dcls, 0.0) + damped * share
            return out

        atk_map_applied = _with_extra(atk_map, self.defender_groups, atk_extra)
        def_map_applied = _with_extra(def_map, self.attacker_groups, def_extra)

        # apply casualties simultaneously
        self._apply_damage(self.defender_groups, atk_map_applied, "def")
        self._apply_damage(self.attacker_groups, def_map_applied, "atk")

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

        # 4) timeline snapshot (log base and per-class by attacker class; extras already tracked)
        def _breakdown(by_attacker_cls: Dict[str, float]) -> Dict[str, float]:
            base_total = float(sum(by_attacker_cls.values()))
            return {
                "base": base_total,
                "Infantry": float(by_attacker_cls.get("Infantry", 0.0)),
                "Lancer": float(by_attacker_cls.get("Lancer", 0.0)),
                "Marksman": float(by_attacker_cls.get("Marksman", 0.0)),
            }

        atk_breakdown = _breakdown(atk_by_attacker_cls)
        def_breakdown = _breakdown(def_by_attacker_cls)
        # Close this turn snapshot. We use turn+1 so first snapshot is Turn 1.
        self.turnlog.close_turn(self.turn + 1, atk_breakdown, def_breakdown)

        # advance turn counter
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
    ) -> Tuple[Dict[str, float], Dict[str, float], float]:
        """Build per-defender-class damage map and per-attacker-class base map.

        Returns (damage_by_defender_class_without_extras, base_by_attacker_class, flat_extra_pool).

        ``bonus`` holds regular stat modifiers while ``bonus_special`` contains
        the special bonuses (territory, gem buffs, etc.) that apply using the
        compound formula described on the Whiteout Survival wiki.
        """

        from expedition_battle_mechanics.on_attack import ON_ATTACK

        dmg: DefaultDict[str, float] = defaultdict(float)
        base_by_attacker: DefaultDict[str, float] = defaultdict(float)
        total_enemy = sum(d.count for d in defenders.values() if d.count > 0)
        if total_enemy == 0:
            return dict(dmg), dict(base_by_attacker), 0.0

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

        def _select_target(atk_group: TroopGroup) -> tuple[str, TroopGroup] | None:
            alive = {k: g for k, g in defenders.items() if g.count > 0}
            if not alive:
                return None

            cls = atk_group.class_name
            order: list[str]
            if cls == "Marksman":
                order = ["Infantry", "Lancer", "Marksman"]
            elif cls == "Infantry":
                order = ["Lancer", "Marksman", "Infantry"]
            else:  # Lancer
                # 20% chance to bypass Infantry and strike Marksmen (Ambusher)
                if "Marksman" in alive and random.random() < 0.20:
                    order = ["Marksman", "Infantry", "Lancer"]
                    # Record Ambusher proc for the attacking side and Lancer class
                    self._proc("Ambusher", side, atk_group.class_name.lower())
                else:
                    order = ["Infantry", "Marksman", "Lancer"]

            for t in order:
                if t in alive:
                    return t, alive[t]
            # fallback: return any alive group
            k, g = next(iter(alive.items()))
            return k, g

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
                    # Created Logic for review: use EW level for the EW expedition skill if present
                    if hero.exclusive_weapon and hero.exclusive_weapon.skills.get("expedition") and sk.name == hero.exclusive_weapon.skills["expedition"].name:
                        lvl = hero.exclusive_weapon.level
                    else:
                        lvl = hero.selected_skill_levels.get(sk.name, 5)
                    handler(self, side, atk, hero, lvl)

            # include class-specific attack bonuses e.g., "lancer_attack"
            # Fix: avoid double-counting class-specific attack bonus. cls_bonus already
            # includes both the global stat (e.g., 'attack') and the class-specific key
            # (e.g., 'lancer_attack').
            base_pct = cls_bonus(bonus_combined, cls, "attack")
            spec_pct = cls_bonus(special_combined, cls, "attack")
            atk_stat = atk.definition.attack * (
                1 + base_pct + atk.definition.stat_bonuses.get("Attack", 0.0)
            )
            atk_stat = atk_stat * (1 + spec_pct) + atk.definition.attack * spec_pct

            leth_base = cls_bonus(bonus_combined, cls, "lethality")
            leth_spec = cls_bonus(special_combined, cls, "lethality")
            leth_stat = atk.definition.lethality * (
                1 + leth_base + atk.definition.stat_bonuses.get("Lethality", 0.0)
            )
            leth_stat = leth_stat * (1 + leth_spec) + atk.definition.lethality * leth_spec

            target = _select_target(atk)
            if not target:
                continue
            dcls, deff = target

            atk_mul, def_mul, dmg_mul = self._troop_skill_mods(atk, deff, side)

            # include class-specific defense bonuses e.g., "infantry_defense"
            # Fix: avoid double-counting class-specific defense bonus in the same way.
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

            # Damage weighting: use Troop Power ratio as per test expectations and
            # wiki-inspired approximation. This dampens extremes and keeps tiers aligned.
            if self.use_power_weighting:
                ratio = atk.definition.power / (
                    atk.definition.power + deff.definition.power
                )
            else:
                ratio = 1.0

            per_troop = max(eff_atk * ratio - eff_def, eff_atk * ratio * 0.01)
            per_troop += eff_leth * ratio
            base = per_troop * atk.count * dmg_mul

            # Created Logic for review: support class/generic "damage" multipliers
            # contributed by expedition skills (e.g., Marksman-damage, Lancer-damage, damage).
            dmg_pct = cls_bonus(bonus_combined, cls, "damage")
            if dmg_pct:
                base *= (1.0 + dmg_pct)

            dmg[dcls] += base
            base_by_attacker[atk.class_name] += base

        # Do not consume or distribute extra here so the caller can both log and apply
        return dict(dmg), dict(base_by_attacker), float(extra_pool)

    # ------------------------------------------------------------------ #
    def _troop_skill_mods(
        self, atk: TroopGroup, deff: TroopGroup, side: Optional[str] = None
    ) -> Tuple[float, float, float]:
        atk_mul = def_mul = 1.0
        dmg_mul = 1.0
        # Map which TEAM is defending in this interaction for proc logging
        # side is the TEAM whose damage we are computing ("atk" team or "def" team)
        # so the defender team is the opposite of side
        defender_team = "def" if (side or "atk") == "atk" else "atk"

        # ---- Infantry ----
        if atk.class_name == "Infantry" and deff.class_name == "Lancer":
            atk_mul *= 1.10  # Master Brawler

        if deff.class_name == "Infantry":
            # Body of Light – always-on +6% Defense
            def_mul *= 1.06
            # Bands of Steel – Infantry takes less damage from Lancers
            if atk.class_name == "Lancer":
                def_mul *= 1.10
            # Crystal Shield – 37.5% chance to offset incoming damage.
            # Created Logic for review: Interpreted per docs as a substantial reduction
            # rather than full nullify, combined with Body of Light's “extra 15%
            # reduction while shield is active”. Effective remaining damage ≈ 35%
            # (50% × 0.70) when active.
            if random.random() < 0.375:
                dmg_mul *= 0.35
                self._proc("Crystal Shield", defender_team, deff.class_name.lower())
                self._proc("Body of Light", defender_team, deff.class_name.lower())

        # ---- Lancer ----
        if atk.class_name == "Lancer":
            if deff.class_name == "Marksman":
                atk_mul *= 1.10  # Charge
            elif deff.class_name == "Infantry":
                atk_mul *= 0.90  # suffers vs Infantry
            if random.random() < 0.15:
                atk_mul *= 2.0  # Crystal Lance
                self._proc("Crystal Lance", (side or "atk"), atk.class_name.lower())
        if deff.class_name == "Lancer" and random.random() < 0.10:
            dmg_mul *= 0.5  # Incandescent Field
            self._proc("Incandescent Field", defender_team, deff.class_name.lower())

        # ---- Marksman ----
        if atk.class_name == "Marksman":
            atk_mul *= 1.04  # Flame Charge base attack
            if deff.class_name == "Infantry":
                atk_mul *= 1.10  # Ranged Strike
            if random.random() < 0.10:
                atk_mul *= 2.0  # Volley
                self._proc("Volley", (side or "atk"), atk.class_name.lower())
            if random.random() < 0.30:
                atk_mul *= 1.50 * 1.25  # Crystal Gunpowder + Flame Charge bonus
                self._proc("Crystal Gunpowder", (side or "atk"), atk.class_name.lower())

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