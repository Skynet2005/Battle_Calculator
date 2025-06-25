# battle_mechanics/combat_state.py

import random
from collections import defaultdict
from typing import Dict, Any, Optional

from expedition_battle_mechanics.formation import RallyFormation
from expedition_battle_mechanics.bonus import BonusSource
from expedition_battle_mechanics.troop import TroopGroup
from hero_data.hero_loader import HEROES

class BattleReportInput:
    """
    Container for all manually-input battle data, now supporting 3-hero rallies, troop ratios, and capacity.
    """
    def __init__(
        self,
        attacker_formation: RallyFormation,
        defender_formation: RallyFormation,
        attacker_bonus: BonusSource,
        defender_bonus: BonusSource,
        skill_trigger_counts: Optional[Dict[str, int]] = None
    ):
        self.attacker_formation = attacker_formation
        self.defender_formation = defender_formation
        self.attacker_bonus = attacker_bonus
        self.defender_bonus = defender_bonus
        self.skill_trigger_counts = skill_trigger_counts or {}

class CombatState:
    """
    Represents an ongoing combat, resolving rounds until one side is wiped out.
    """
    def __init__(self, report: BattleReportInput):
        self.attacker_groups = report.attacker_formation.troop_groups
        self.defender_groups = report.defender_formation.troop_groups
        self.attacker_heroes = report.attacker_formation.heroes
        self.defender_heroes = report.defender_formation.heroes
        self.attacker_bonus = report.attacker_bonus.total_bonuses
        self.defender_bonus = report.defender_bonus.total_bonuses
        self.skill_triggers = report.skill_trigger_counts
        self.turn = 0
        self.attacker_effects = self._aggregate_hero_effects(self.attacker_heroes)
        self.defender_effects = self._aggregate_hero_effects(self.defender_heroes)

    def _aggregate_hero_effects(self, heroes):
        effects = {"Infantry": {}, "Lancer": {}, "Marksman": {}, "all": {}, "enemy": {}}
        for hero in heroes.values():
            hero_dict = HEROES.get(hero.name)
            if isinstance(hero_dict, list):
                hero_dict = hero_dict[0]
            exp_skills = (hero_dict.get('skills', {}) or {}).get('expedition', {}) if hero_dict else {}
            for sk in hero.skills.get("expedition", []):
                # ... full effect-parsing logic (identical to your original)
                pass  # copy-paste the entire logic block here
        return effects

    def is_over(self) -> bool:
        atk_alive = any(g.count > 0 for g in self.attacker_groups.values())
        def_alive = any(g.count > 0 for g in self.defender_groups.values())
        return not (atk_alive and def_alive)

    def step_round(self):
        atk_buffs = self._get_total_buffs(self.attacker_effects, self.defender_effects)
        def_buffs = self._get_total_buffs(self.defender_effects, self.attacker_effects)
        atk_damage = self._compute_side_damage(
            self.attacker_groups, self.defender_groups,
            self.attacker_bonus, self.attacker_heroes,
            atk_buffs, def_buffs
        )
        def_damage = self._compute_side_damage(
            self.defender_groups, self.attacker_groups,
            self.defender_bonus, self.defender_heroes,
            def_buffs, atk_buffs
        )
        self._apply_damage(self.defender_groups, atk_damage, self.defender_bonus)
        self._apply_damage(self.attacker_groups, def_damage, self.attacker_bonus)
        self.turn += 1

    def _get_total_buffs(self, own_effects, enemy_effects):
        """
        Combine all buffs/debuffs for each troop type for this turn.
        Returns: {troop_type: {stat: value, ...}}
        """
        buffs = {t: {} for t in ["Infantry", "Lancer", "Marksman"]}
        for t in buffs:
            # Start with 'all' buffs
            for stat, val in own_effects["all"].items():
                buffs[t][stat] = buffs[t].get(stat, 0.0) + val
            # Add troop-type specific buffs
            for stat, val in own_effects[t].items():
                buffs[t][stat] = buffs[t].get(stat, 0.0) + val
            # Add enemy debuffs (e.g., damage_taken)
            for stat, val in enemy_effects["enemy"].items():
                buffs[t][stat] = buffs[t].get(stat, 0.0) + val
        return buffs

    def _compute_side_damage(self, attackers, defenders, bonuses, heroes, own_buffs, enemy_buffs):
        """
        Calculates damage dealt by one side to the other.
        Returns a map of troop type to damage amount.
        """
        damage_map = defaultdict(float)
        for t in ["Infantry", "Lancer", "Marksman"]:
            atk = attackers[t]
            defn = defenders[t]
            hero = heroes[t]
            # Skip if either attacker or defender has no troops
            if atk.count <= 0 or defn.count <= 0:
                continue
            # Calculate base damage from troops
            dmg = self._compute_damage(atk, defn, bonuses, hero, own_buffs[t], enemy_buffs[t])
            # Add damage from hero skills
            dmg += self._compute_skill_damage(atk, hero)
            damage_map[t] += dmg
        return damage_map

    def _compute_damage(self, atk_group, def_group, bonuses, hero, atk_buffs, def_buffs):
        """
        Calculates damage from one troop group to another, considering all buffs and bonuses.
        """
        if def_group.count <= 0:
            return 0.0

        # Only apply hero's stat bonuses to their troop type
        eff_atk = atk_group.definition.attack * (1 + bonuses.get("attack", 0.0))
        eff_def = def_group.definition.defense * (1 + bonuses.get("defense", 0.0))

        # Apply troop and hero buffs
        eff_atk *= (1 + atk_buffs.get("attack", 0.0))
        eff_def *= (1 + def_buffs.get("defense", 0.0))

        # Apply health buffs for defender
        eff_hp = def_group.definition.health * (1 + def_buffs.get("health", 0.0))

        # Troop skill modifiers (reuse or refactor as needed)
        mods = self._troop_skill_modifiers(atk_group, def_group)
        eff_atk *= mods["attack_multiplier"]
        eff_def *= mods["defense_multiplier"]

        # Apply damage taken debuff
        damage_taken_mult = 1 + def_buffs.get("damage_taken", 0.0)

        # Calculate power-based ratio for damage calculation
        p_atk = atk_group.definition.power
        p_def = def_group.definition.power
        ratio = p_atk / (p_atk + p_def) if (p_atk + p_def) > 0 else 0.0

        # Calculate base damage per troop
        base_per_troop = max(eff_atk * ratio - eff_def, 0.0)

        # Calculate total expected damage including all multipliers
        total = base_per_troop * atk_group.count * mods["damage_multiplier"] * damage_taken_mult
        return total

    def _compute_skill_damage(self, atk_group, hero):
        """
        Calculates additional damage from hero skills.
        """
        total = 0.0
        for sk in hero.skills.get("expedition", []):
            # Get explicit trigger count or calculate expected value
            triggers = self.skill_triggers.get(sk.name, None)
            # Use hero's class-specific attack stat if available, otherwise use general attack
            atk_stat = hero.base_stats.get(f"{hero.char_class}-attack", hero.base_stats.get("attack", 0))
            dmg_per = sk.multiplier * atk_stat

            if triggers is not None:
                # Use explicit trigger count
                total += dmg_per * triggers
            else:
                # Calculate expected triggers based on proc chance
                expected = atk_group.count * sk.proc_chance
                total += dmg_per * expected
        return total

    def _apply_damage(self, groups, damage_map, bonuses):
        """
        Applies calculated damage to troop groups, reducing their counts.
        """
        for t in ["Infantry", "Lancer", "Marksman"]:
            dmg = damage_map.get(t, 0.0)
            group = groups[t]
            if group.count <= 0:
                continue

            # Calculate effective health per troop with bonuses
            hp_per = group.definition.health * (1 + bonuses.get("health", 0.0))

            # Calculate troop losses
            losses = int(dmg / hp_per)

            # Update troop count, ensuring it doesn't go below zero
            group.count = max(group.count - losses, 0)

    def _troop_skill_modifiers(
        self,
        atk_group: TroopGroup,
        def_group: TroopGroup
    ) -> Dict[str, float]:
        """
        Computes expected multipliers for attack, defense, and damage reduction
        based on troop-type skills (type advantages, procs, crystals, etc.).
        """
        atk_mult = 1.0
        def_mult = 1.0
        dmg_mult = 1.0

        atk_name = atk_group.definition.name
        def_name = def_group.definition.name

        # Infantry vs Lancer
        if atk_name.startswith("Infantry") and def_name.startswith("Lancer"):
            atk_mult *= 1.10   # Master Brawler: +10% attack vs Lancers
            def_mult *= 1.10   # Bands of Steel: +10% defense vs Lancers

        # Crystal Shield & Body of Light for Infantry defense
        if def_name.startswith("Infantry"):
            # Crystal Shield: 37.5% chance to offset damage => expected damage reduction
            dmg_mult *= (1 - 0.375)
            # Body of Light: +6% defense
            def_mult *= 1.06
            # Body of Light: additional 15% damage reduction when shield active (37.5% chance)
            dmg_mult *= (1 - (0.375 * 0.15))

        # Lancer vs Marksman
        if atk_name.startswith("Lancer") and def_name.startswith("Marksman"):
            atk_mult *= 1.10   # Charge: +10% attack vs Marksman
            atk_mult *= 1.20   # Ambusher: expected +20% extra damage
            atk_mult *= 1.15   # Crystal Lance: expected +15% extra damage (double-damage proc)
        # Incandescent Field: Lancer defense
        if def_name.startswith("Lancer"):
            # 10% chance to take half damage => expected 5% reduction
            dmg_mult *= (1 - (0.10 * 0.5))

        # Marksman vs Infantry
        if atk_name.startswith("Marksman") and def_name.startswith("Infantry"):
            atk_mult *= 1.10   # Ranged Strike: +10% attack vs Infantry
            atk_mult *= 1.10   # Volley: expected +10% extra (chance to strike twice)
            atk_mult *= 1.15   # Crystal Gunpowder: expected +15% extra
            atk_mult *= 1.04   # Flame Charge: +4% base attack
            atk_mult *= 1.075  # Flame Charge extra: expected +7.5%

        return {
            "attack_multiplier": atk_mult,
            "defense_multiplier": def_mult,
            "damage_multiplier": dmg_mult
        }
