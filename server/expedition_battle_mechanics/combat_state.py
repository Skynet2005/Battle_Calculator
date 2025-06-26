"""
CombatState – resolves expedition battles round-by-round.

This version contains:

•  Lazy import of ON_ATTACK to avoid circular-import crashes.
•  Per-turn dispatcher (ON_TURN) for timed skills such as Hendrik's
   "Armor of Barnacles" and "Dragon's Heir".
•  Full passive-skill aggregation via PASSIVE_SKILLS
   (implements Gatot: Golden Guard, Royal Legion, Indestructible City;
    Hendrik: Worm's Ravage, Abyssal Blessing).
•  Helper methods get_side_groups / get_enemy_groups.
•  Temporary defense bonus fields (temp_def_bonus / temp_def_bonus_turns)
   on TroopGroup with automatic expiry each round.
"""

from __future__ import annotations

import random
from collections import defaultdict
from typing import Dict, Tuple, DefaultDict

from expedition_battle_mechanics.formation import RallyFormation
from expedition_battle_mechanics.bonus import BonusSource
from expedition_battle_mechanics.troop import TroopGroup
from expedition_battle_mechanics.hero import Hero

# passive buffs / debuffs (always on)
from expedition_battle_mechanics.skill_handlers.passive import PASSIVE_SKILLS

# ─────────────────────────────────────────────────────────────────────────────
# Input container returned by API layer
# ─────────────────────────────────────────────────────────────────────────────
class BattleReportInput:
    """
    Packs the two formations plus global bonus sources so they can be handed
    to the simulation engine in one object.
    """

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
# Combat core
# ─────────────────────────────────────────────────────────────────────────────
class CombatState:
    """
    Holds every mutable value of an on-going battle and steps one round at a time
    until either side is extinct.
    """

    def __init__(self, rpt: BattleReportInput) -> None:
        # ---- Troop groups --------------------------------------------------
        self.attacker_groups: Dict[str, TroopGroup] = (
            rpt.attacker_formation.troop_groups
        )
        self.defender_groups: Dict[str, TroopGroup] = (
            rpt.defender_formation.troop_groups
        )

        # ---- Heroes --------------------------------------------------------
        self.attacker_heroes: Dict[str, Hero] = rpt.attacker_formation.heroes
        self.defender_heroes: Dict[str, Hero] = rpt.defender_formation.heroes

        # Label side on every hero so skill handlers can branch quickly
        for h in self.attacker_heroes.values():
            h.side = "atk"
        for h in self.defender_heroes.values():
            h.side = "def"

        # ---- Global stat bonuses (city / territory / weapon + passives) ----
        self.attacker_bonus: Dict[str, float] = rpt.attacker_bonus.total_bonuses
        self.defender_bonus: Dict[str, float] = rpt.defender_bonus.total_bonuses

        # Fold in all always-on expedition passives
        self._apply_passives()

        # ---- round & bookkeeping ------------------------------------------
        self.turn: int = 0
        self.skill_procs: DefaultDict[str, int] = defaultdict(int)

        # extra damage produced by on-attack skills in current phase
        self.pending_extra_damage: float = 0.0

    # ─────────────────────────────────────────────────────────────────────
    #   Passive-skill aggregation
    # ─────────────────────────────────────────────────────────────────────
    def _apply_passives(self) -> None:
        """
        Executes every handler in PASSIVE_SKILLS once at battle start,
        merging buffs into attacker_bonus / defender_bonus dicts.
        """

        def collector(side_bonus: Dict[str, float], enemy_bonus: Dict[str, float]):
            """
            Returns a closure that any passive handler can call to record a
            buff (+) on own side or debuff (–) on enemy side.
            """

            def _add(key: str, pct: float) -> None:
                # enemy-xxx-down  → subtract from enemy's stat
                if key.startswith("enemy-"):
                    stat = key.replace("enemy-", "").replace("-down", "")
                    enemy_bonus[stat] = enemy_bonus.get(stat, 0.0) - pct
                    return

                # Class-specific keys ("Infantry-defense") are folded into
                # the generic stat pool for now; refine later if needed.
                if "-" in key:
                    stat = key.split("-")[1]
                else:
                    stat = key
                side_bonus[stat] = side_bonus.get(stat, 0.0) + pct

            return _add

        # Iterate over every hero, call its passive handlers
        for hero in list(self.attacker_heroes.values()) + list(
            self.defender_heroes.values()
        ):
            add_fn = collector(
                self.attacker_bonus if hero.side == "atk" else self.defender_bonus,
                self.defender_bonus if hero.side == "atk" else self.attacker_bonus,
            )
            for sk in hero.skills["expedition"]:
                handler = PASSIVE_SKILLS.get(sk.name)
                if handler:
                    lvl = hero.selected_skill_levels.get(sk.name, 5)
                    handler(hero, lvl, add_fn)

    # ─────────────────────────────────────────────────────────────────────
    #   Utility helpers
    # ─────────────────────────────────────────────────────────────────────
    def _proc(self, skill_name: str, side: str) -> None:
        """Increment proc counter for rich battle report."""
        self.skill_procs[f"{skill_name}-{side}"] += 1

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
    #   Battle lifecycle
    # ─────────────────────────────────────────────────────────────────────
    def is_over(self) -> bool:
        atk_alive = any(g.count > 0 for g in self.attacker_groups.values())
        def_alive = any(g.count > 0 for g in self.defender_groups.values())
        return not (atk_alive and def_alive)

    def step_round(self) -> None:
        """
        Executes one full round:
            1) attacker phase damage + on-attack procs
            2) defender phase damage + on-attack procs
            3) per-turn skill handlers
            4) countdown & clear temporary buffs
        """

        # -------- phase A: attacker damages defender -----------------------
        atk_dmg = self._compute_side_damage(
            attackers=self.attacker_groups,
            defenders=self.defender_groups,
            bonuses=self.attacker_bonus,
            side="atk",
        )

        # -------- phase B: defender damages attacker -----------------------
        def_dmg = self._compute_side_damage(
            attackers=self.defender_groups,
            defenders=self.attacker_groups,
            bonuses=self.defender_bonus,
            side="def",
        )

        # apply the damage maps
        self._apply_damage(self.defender_groups, atk_dmg)
        self._apply_damage(self.attacker_groups, def_dmg)

        # -------- phase C: timed (per-turn) skills -------------------------
        from expedition_battle_mechanics.skill_handlers.on_turn import ON_TURN

        for hero in list(self.attacker_heroes.values()) + list(
            self.defender_heroes.values()
        ):
            for sk in hero.skills["expedition"]:
                handler = ON_TURN.get(sk.name)
                if handler:
                    lvl = hero.selected_skill_levels.get(sk.name, 5)
                    handler(self, hero, lvl)

        # -------- phase D: tick down temporary buffs -----------------------
        for tg in list(self.attacker_groups.values()) + list(
            self.defender_groups.values()
        ):
            if tg.temp_def_bonus > 0.0:
                tg.temp_def_bonus_turns -= 1
                if tg.temp_def_bonus_turns <= 0:
                    tg.temp_def_bonus = 0.0
                    tg.temp_def_bonus_turns = 0

        # round complete
        self.turn += 1

    # ─────────────────────────────────────────────────────────────────────
    #   Damage calculation helpers
    # ─────────────────────────────────────────────────────────────────────
    def _compute_side_damage(
        self,
        attackers: Dict[str, TroopGroup],
        defenders: Dict[str, TroopGroup],
        bonuses: Dict[str, float],
        side: str,
    ) -> Dict[str, float]:
        """
        Returns a map {defender_class: raw_damage} originated by SIDE during
        this half-round (before shields / losses are applied).
        """

        from expedition_battle_mechanics.skill_handlers.on_attack import ON_ATTACK

        dmg_map: DefaultDict[str, float] = defaultdict(float)
        total_enemy_alive = sum(d.count for d in defenders.values() if d.count > 0)
        if total_enemy_alive == 0:
            return dmg_map

        for cls, atk in attackers.items():
            if atk.count <= 0:
                continue

            # Use the correct hero for the current side
            if side == "atk":
                hero = self.attacker_heroes[cls]
            else:
                hero = self.defender_heroes[cls]

            # ---- on-attack skill handlers (e.g., King's Bestowal) ----------
            for sk in hero.skills["expedition"]:
                handler = ON_ATTACK.get(sk.name)
                if handler:
                    lvl = hero.selected_skill_levels.get(sk.name, 5)
                    handler(self, side, atk, hero, lvl)

            flame_charge_proc_this_attack = False
            gunpowder_proc_this_attack = False
            ambusher_proc_this_attack = False

            for dcls, deff in defenders.items():
                if deff.count <= 0:
                    continue

                atk_mult, def_mult, dmg_mult, ambusher_proc, flame_charge_proc, gunpowder_proc = self._troop_skill_mods(atk, deff)

                eff_atk = atk.definition.attack * (1 + bonuses.get("attack", 0.0))
                eff_def = deff.definition.defense * (1 + bonuses.get("defense", 0.0))
                eff_def *= 1 + deff.temp_def_bonus
                eff_atk *= atk_mult
                eff_def *= def_mult
                ratio = atk.definition.power / (atk.definition.power + deff.definition.power)
                per_troop = max(eff_atk * ratio - eff_def, eff_atk * ratio * 0.01)
                base_dmg = per_troop * atk.count * dmg_mult
                share = deff.count / total_enemy_alive
                extra = self.pending_extra_damage * share
                dmg_map[dcls] += base_dmg + extra

                # Only record Flame Charge ONCE per attack
                if flame_charge_proc and not flame_charge_proc_this_attack:
                    self._proc("Flame Charge", hero.side)
                    print(f"[DEBUG] Flame Charge proc recorded for {hero.side}")
                    flame_charge_proc_this_attack = True
                # Only record Gunpowder ONCE per attack
                if gunpowder_proc and not gunpowder_proc_this_attack:
                    self._proc("Crystal Gunpowder", hero.side)
                    print(f"[DEBUG] Crystal Gunpowder proc recorded for {hero.side}")
                    gunpowder_proc_this_attack = True
                # Only record Ambusher ONCE per attack
                if ambusher_proc and not ambusher_proc_this_attack:
                    ambusher_proc_this_attack = True

            # Ambusher logic: if proc, apply 50% of Lancer's attack to Marksman line
            if ambusher_proc_this_attack and atk.class_name == "Lancer":
                if "Marksman" in defenders and defenders["Marksman"].count > 0:
                    marksman = defenders["Marksman"]
                    marksman_eff_def = marksman.definition.defense * (1 + bonuses.get("defense", 0.0))
                    marksman_eff_def *= 1 + marksman.temp_def_bonus
                    ambush_ratio = atk.definition.power / (atk.definition.power + marksman.definition.power)
                    ambush_per_troop = max(eff_atk * ambush_ratio - marksman_eff_def, eff_atk * ambush_ratio * 0.01)
                    ambush_dmg = 0.5 * ambush_per_troop * atk.count
                    if ambush_dmg > 0:
                        dmg_map["Marksman"] += ambush_dmg
                        self._proc("Ambusher", hero.side)
                        print(f"[DEBUG] Ambusher proc recorded for {hero.side}")

        self.pending_extra_damage = 0.0
        return dmg_map

    # -------------------------------------------------------------------
    def _troop_skill_mods(
        self, atk: TroopGroup, deff: TroopGroup
    ) -> tuple:
        """
        Returns (atk_multiplier, def_multiplier, damage_multiplier, ambusher_proc, flame_charge_proc, gunpowder_proc).
        Implements all troop-skill (FC) interactions & procs.
        """
        atk_mul = def_mul = 1.0
        dmg_mul = 1.0
        ambusher_proc = False
        flame_charge_proc = False
        gunpowder_proc = False
        # Infantry ↔ Lancer
        if atk.class_name == "Infantry" and deff.class_name == "Lancer":
            atk_mul *= 1.10
            def_mul *= 1.10
        # Infantry procs (attacker side)
        if atk.class_name == "Infantry":
            # Body of Light: +6% Defense, -15% damage when Crystal Shield active (for attacker)
            if random.random() < 0.375:
                # Crystal Shield attacker proc (simulate as a damage boost or effect)
                self._proc("Crystal Shield", "atk")
                if random.random() < 0.15:
                    self._proc("Body of Light", "atk")
        # Lancer crystal skills
        if atk.class_name == "Lancer" and random.random() < 0.15:
            atk_mul *= 2.0  # Crystal Lance
            self._proc("Crystal Lance", atk.class_name.lower())
        if deff.class_name == "Lancer" and random.random() < 0.10:
            dmg_mul *= 0.5  # Incandescent Field
            self._proc("Incandescent Field", deff.class_name.lower())
        # Lancer ↔ Marksman intrinsic
        if atk.class_name == "Lancer" and deff.class_name == "Marksman":
            atk_mul *= 1.10
        # Ambusher: 20% chance to strike Marksman behind Infantry
        if atk.class_name == "Lancer" and random.random() < 0.20:
            ambusher_proc = True
        # Marksman skills
        if atk.class_name == "Marksman":
            if deff.class_name == "Infantry":
                atk_mul *= 1.10
            if random.random() < 0.10:
                atk_mul *= 2.0  # Volley
                self._proc("Volley", atk.class_name.lower())
            if random.random() < 0.30:
                atk_mul *= 1.50 * 1.25  # Gunpowder & Flame Charge
                gunpowder_proc = True
            # Flame Charge: always +4% basic attack, +25% if Gunpowder procs
            atk_mul *= 1.04
            flame_charge_proc = True
            if gunpowder_proc:
                atk_mul *= 1.25
        # Infantry defensive crystals (defender side)
        if deff.class_name == "Infantry":
            def_mul *= 1.06  # Body of Light (static)
            if random.random() < 0.375:
                dmg_mul = 0.0  # Crystal Shield absorbs
                self._proc("Crystal Shield", "def")
                if random.random() < 0.15:
                    self._proc("Body of Light", "def")
        return atk_mul, def_mul, dmg_mul, ambusher_proc, flame_charge_proc, gunpowder_proc

    # -------------------------------------------------------------------
    def _apply_damage(self, groups: Dict[str, TroopGroup], dmg_map: Dict[str, float]):
        """
        Converts raw damage into troop losses, accounting for shield absorption.
        """

        for cls, raw in dmg_map.items():
            tg = groups[cls]
            if tg.count <= 0 or raw <= 0.0:
                continue

            # absorb by Gatot's "existing shield" skill if used
            if tg.shield > 0.0:
                absorbed = min(tg.shield, raw)
                raw -= absorbed
                tg.shield -= absorbed

            # convert remaining raw damage into troop casualties
            losses = max(int(raw / tg.definition.health), 1)
            tg.count = max(tg.count - losses, 0)
