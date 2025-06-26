"""
CombatState
===========

•  Resolves an expedition battle round-by-round.
•  Aggregates *passive expedition skills* from every hero (both sides)
   into attacker_bonus / defender_bonus **and** records a readable log
   that the front-end can display.
•  Tracks on-attack and on-turn procs for existing skill handlers.
•  Provides helper accessors and proc counter.
"""

from __future__ import annotations

import random
from collections import defaultdict
from typing import Dict, Tuple, DefaultDict, Callable

from expedition_battle_mechanics.formation import RallyFormation
from expedition_battle_mechanics.bonus import BonusSource
from expedition_battle_mechanics.troop import TroopGroup
from expedition_battle_mechanics.hero import Hero

# passive always-on expedition skill handlers
from expedition_battle_mechanics.skill_handlers.passive import PASSIVE_SKILLS

# ─────────────────────────────────────────────────────────────────────────────
#   Input wrapper
# ─────────────────────────────────────────────────────────────────────────────
class BattleReportInput:
    """
    Packs both formations plus their static BonusSource so we can deepcopy
    once per simulation.
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
#   CombatState core
# ─────────────────────────────────────────────────────────────────────────────
class CombatState:
    """
    Holds all mutable fight state; `step_round()` runs exactly one turn.
    """

    # --------------------------------------------------------------------- #
    def __init__(self, rpt: BattleReportInput) -> None:
        # ----- groups -----------------------------------------------------
        self.attacker_groups: Dict[str, TroopGroup] = (
            rpt.attacker_formation.troop_groups
        )
        self.defender_groups: Dict[str, TroopGroup] = (
            rpt.defender_formation.troop_groups
        )

        # ----- heroes -----------------------------------------------------
        self.attacker_heroes: Dict[str, Hero] = rpt.attacker_formation.heroes
        self.defender_heroes: Dict[str, Hero] = rpt.defender_formation.heroes

        for h in self.attacker_heroes.values():
            h.side = "atk"
        for h in self.defender_heroes.values():
            h.side = "def"

        # ----- static bonuses (city / pet / weapon perks) -----------------
        self.attacker_bonus: Dict[str, float] = rpt.attacker_bonus.total_bonuses
        self.defender_bonus: Dict[str, float] = rpt.defender_bonus.total_bonuses

        # ----- passive expedition skill log -------------------------------
        self.passive_effects: DefaultDict[str, list[str]] = defaultdict(list)

        # merge passive expedition buffs
        self._apply_passives()

        # ----- bookkeeping ------------------------------------------------
        self.turn: int = 0
        self.skill_procs: DefaultDict[str, int] = defaultdict(int)
        self.pending_extra_damage: float = 0.0

    # ─────────────────────────────────────────────────────────────────────
    #   Passive skill aggregation
    # ─────────────────────────────────────────────────────────────────────
    def _apply_passives(self) -> None:
        """
        Executes every handler in PASSIVE_SKILLS exactly once, merges its
        stat changes into the correct bonus dict and appends a readable line
        to self.passive_effects for UI.
        """

        def make_adder(
            own: Dict[str, float],
            enemy: Dict[str, float],
            label: str,
        ) -> Callable[[str, float], None]:
            """
            Closure that passive handlers call to register a buff/debuff.
            """

            def _add(key: str, pct: float) -> None:
                # enemy-stat-down
                if key.startswith("enemy-"):
                    stat = key.replace("enemy-", "").replace("-down", "")
                    enemy[stat] = enemy.get(stat, 0.0) - pct
                    self.passive_effects[label].append(
                        f"{stat} {pct*100:+.1f}%  (enemy)"
                    )
                    return

                # class-specific keys are flattened
                stat = key.split("-")[-1] if "-" in key else key
                own[stat] = own.get(stat, 0.0) + pct
                self.passive_effects[label].append(f"{stat} {pct*100:+.1f}%")

            return _add

        heroes = list(self.attacker_heroes.values()) + list(
            self.defender_heroes.values()
        )
        for hero in heroes:
            adder = make_adder(
                self.attacker_bonus if hero.side == "atk" else self.defender_bonus,
                self.defender_bonus if hero.side == "atk" else self.attacker_bonus,
                hero.side,
            )
            for sk in hero.skills["expedition"]:
                handler = PASSIVE_SKILLS.get(sk.name)
                if handler:
                    lvl = hero.selected_skill_levels.get(sk.name, 5)
                    handler(hero, lvl, adder)

    # ─────────────────────────────────────────────────────────────────────
    #   Helper utilities
    # ─────────────────────────────────────────────────────────────────────
    def _proc(self, name: str, side: str) -> None:
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
    #   Round lifecycle
    # ─────────────────────────────────────────────────────────────────────
    def is_over(self) -> bool:
        atk_alive = any(g.count > 0 for g in self.attacker_groups.values())
        def_alive = any(g.count > 0 for g in self.defender_groups.values())
        return not (atk_alive and def_alive)

    # ------------------------------------------------------------------ #
    def step_round(self) -> None:
        """
        sequence:
          1) attacker damages defender (including ON_ATTACK skills)
          2) defender damages attacker
          3) per-turn skills (ON_TURN)
          4) expire temporary buffs
        """

        # -------- import handlers lazily (avoid circular) ----------------
        from expedition_battle_mechanics.skill_handlers.on_attack import ON_ATTACK
        from expedition_battle_mechanics.skill_handlers.on_turn import ON_TURN

        # -------- phase A: attacker fires -------------------------------
        atk_map = self._compute_side_damage(
            self.attacker_groups, self.defender_groups, self.attacker_bonus, "atk"
        )
        self._apply_damage(self.defender_groups, atk_map)

        # -------- phase B: defender fires -------------------------------
        def_map = self._compute_side_damage(
            self.defender_groups, self.attacker_groups, self.defender_bonus, "def"
        )
        self._apply_damage(self.attacker_groups, def_map)

        # -------- phase C: timed skills ---------------------------------
        for hero in list(self.attacker_heroes.values()) + list(
            self.defender_heroes.values()
        ):
            for sk in hero.skills["expedition"]:
                handler = ON_TURN.get(sk.name)
                if handler:
                    lvl = hero.selected_skill_levels.get(sk.name, 5)
                    handler(self, hero, lvl)

        # -------- phase D: temporary defense buffs expire --------------
        for g in list(self.attacker_groups.values()) + list(
            self.defender_groups.values()
        ):
            if g.temp_def_bonus_turns > 0:
                g.temp_def_bonus_turns -= 1
                if g.temp_def_bonus_turns == 0:
                    g.temp_def_bonus = 0.0

        self.turn += 1

    # ─────────────────────────────────────────────────────────────────────
    #   Damage helpers
    # ─────────────────────────────────────────────────────────────────────
    def _compute_side_damage(
        self,
        attackers: Dict[str, TroopGroup],
        defenders: Dict[str, TroopGroup],
        bonus: Dict[str, float],
        side: str,
    ) -> Dict[str, float]:
        """
        Returns damage map {defender_class: raw_dmg} and also triggers all
        ON_ATTACK handlers.
        """

        from expedition_battle_mechanics.skill_handlers.on_attack import ON_ATTACK

        dmg: DefaultDict[str, float] = defaultdict(float)
        total_enemy = sum(d.count for d in defenders.values() if d.count > 0)
        if total_enemy == 0:
            return dmg

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

                # distribute queued extra damage proportionally
                share = deff.count / total_enemy
                extra = self.pending_extra_damage * share

                dmg[dcls] += base + extra

        self.pending_extra_damage = 0.0
        return dmg

    # ------------------------------------------------------------------ #
    def _troop_skill_mods(
        self, atk: TroopGroup, deff: TroopGroup
    ) -> Tuple[float, float, float]:
        """
        Returns (atk_multiplier, def_multiplier, damage_multiplier) for the
        troop-skill rock/paper/scissor and crystal procs.
        """

        atk_mul = def_mul = 1.0
        dmg_mul = 1.0

        # Infantry ↔ Lancer intrinsic bonus
        if atk.class_name == "Infantry" and deff.class_name == "Lancer":
            atk_mul *= 1.10
            def_mul *= 1.10

        # Infantry defense crystals
        if deff.class_name == "Infantry":
            def_mul *= 1.06  # Body of Light static
            if random.random() < 0.375:
                dmg_mul = 0.0  # Crystal Shield full absorb
                self._proc("Crystal Shield", deff.class_name.lower())
                if random.random() < 0.15:
                    self._proc("Body of Light", deff.class_name.lower())

        # Lancer attack crystals
        if atk.class_name == "Lancer":
            if deff.class_name == "Marksman":
                atk_mul *= 1.10  # Charge intrinsic
            if random.random() < 0.15:
                atk_mul *= 2.0  # Crystal Lance
                self._proc("Crystal Lance", atk.class_name.lower())
        if deff.class_name == "Lancer" and random.random() < 0.10:
            dmg_mul *= 0.5  # Incandescent Field
            self._proc("Incandescent Field", deff.class_name.lower())

        # Marksman attack crystals
        if atk.class_name == "Marksman":
            if deff.class_name == "Infantry":
                atk_mul *= 1.10  # Ranged Strike
            if random.random() < 0.10:
                atk_mul *= 2.0  # Volley
                self._proc("Volley", atk.class_name.lower())
            if random.random() < 0.30:
                atk_mul *= 1.50 * 1.25  # Gunpowder + Flame Charge
                self._proc("Crystal Gunpowder", atk.class_name.lower())

        return atk_mul, def_mul, dmg_mul

    # ------------------------------------------------------------------ #
    def _apply_damage(self, groups: Dict[str, TroopGroup], dmg: Dict[str, float]):
        """
        Translate raw damage into troop losses after shield absorbs.
        """
        for cls, raw in dmg.items():
            g = groups[cls]
            if g.count <= 0 or raw <= 0.0:
                continue

            # absorb with shield
            if g.shield > 0.0:
                absorbed = min(g.shield, raw)
                raw -= absorbed
                g.shield -= absorbed

            # convert remaining raw to troop losses
            losses = max(int(raw / g.definition.health), 1)
            g.count = max(g.count - losses, 0)
