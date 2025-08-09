/* ──────────────────────────────────────────────────────────────
   Type Declarations
   ────────────────────────────────────────────────────────────── */

   export type Class = "Infantry" | "Lancer" | "Marksman";

   export type ClassSel = {
     Infantry: string;
     Lancer: string;
     Marksman: string;
   };

   /** hero list item fetched from /api/heroes */
   export interface Hero {
     name: string;
     charClass: string;          // "infantry" | "lancer" | "marksman"
     generation: number;
   }

   /** kills / survivors keyed by troop class */
   export type TroopBreakdown = { [cls in Class]?: number };

   /** hero details embedded in a finished battle */
   export interface HeroInfo {
     name: string;
     class: string;
     generation: number;
     skills: string[];
     exclusive_weapon?: { name: string; level: number } | null;
     skill_pcts?: Record<string, number>;
     troop_level: string;
     troop_power: number;
     count_start: number;
     count_end: number;
     count_lost: number;
     loss_pct: number;
     kills: number;
     kill_pct: number;
   }

   export interface SideSummary {
     start: number;
     end: number;
     losses: number;
     loss_pct: number;
     kills: number;
     kill_pct: number;
   }

   /** one side (attacker / defender) in the final report */
   export interface SideDetails {
     heroes: { [cls in Class]: HeroInfo };
     total_power: number;
     kills: TroopBreakdown;
     survivors: TroopBreakdown;
     summary: SideSummary;
   }

   /** bullet-ready passive-skill log (added by backend) */
   export interface PassiveEffectBuckets {
     Infantry: string[];
     Lancer: string[];
     Marksman: string[];
     All: string[];
   }

   export interface PassiveEffects {
     attacker: PassiveEffectBuckets;
     defender: PassiveEffectBuckets;
   }

   interface BonusBuckets {
     Infantry: Record<string, number>;
     Lancer: Record<string, number>;
     Marksman: Record<string, number>;
     All: Record<string, number>;
   }

   /** final cumulative % bonuses after passives applied */
   export interface Bonuses {
     attacker: BonusBuckets;
     defender: BonusBuckets;
     attacker_special?: Record<string, number>;
     defender_special?: Record<string, number>;
   }

   interface ProcBuckets {
     attacker: Record<string, Record<string, number>>;
     defender: Record<string, Record<string, number>>;
   }

   interface PowerStats {
     attacker: { start: number; end: number; lost: number; dealt: number };
     defender: { start: number; end: number; lost: number; dealt: number };
     difference: { start: number; end: number };
   }

   /** root object returned by /api/simulate */
   export interface SimResult {
     /* always present in every call */
     winner: string;
     rounds: number;

     /* Monte-Carlo stats (present if sims > 1) */
     attacker_win_rate?: number;
     defender_win_rate?: number;
     avg_attacker_survivors?: number;
     avg_defender_survivors?: number;

     /* single run or sample battle detail */
     attacker?: SideDetails;
     defender?: SideDetails;

     /* server-side proc counter buckets */
     proc_stats?: ProcBuckets;

     /* NEW: bullet list of expedition-skill impacts */
     passive_effects?: PassiveEffects;

     /* NEW: merged % bonuses after buffs/debuffs */
     bonuses?: Bonuses;

     /* power/damage breakdown */
     power?: PowerStats;

     /* when sims > 1 the server includes the first run here */
     sample_battle?: SimResult;
   }

   // Chief gear types
   export type ChiefGearSlot = "Cap" | "Coat" | "Ring" | "Watch" | "Pants" | "Weapon";

   export interface ChiefGearOption {
     tier: string;
     stars: number;
     attackPct: number;
     defensePct: number;
     power: number;
   }

   export type ChiefGearOptionsBySlot = { [slot in ChiefGearSlot]: ChiefGearOption[] };

   export interface ChiefGearSelectionItem {
     item: ChiefGearSlot;
     tier: string;
     stars: number;
   }

   export interface ChiefGearTotals {
     total_attack_pct: number;
     total_defense_pct: number;
     total_power: number;
     set_bonus_attack_pct: number;
     set_bonus_defense_pct: number;
     breakdown: Record<string, { attackPct: number; defensePct: number; power: number }>;
  // Created Logic for review: class-specific base totals (percent, without set bonuses)
  infantry_attack_pct: number;
  infantry_defense_pct: number;
  lancer_attack_pct: number;
  lancer_defense_pct: number;
  marksman_attack_pct: number;
  marksman_defense_pct: number;
  infantry_power: number;
  lancer_power: number;
  marksman_power: number;
   }

   // Chief Charms types
   export interface ChiefCharmOption {
     level: number;
     lethalityPct: number;
     healthPct: number;
     power: number;
   }

   export interface ChiefCharmsTotals {
     total_lethality_pct: number;
     total_health_pct: number;
     total_power: number;
     breakdown: Record<string, { lethalityPct: number; healthPct: number; power: number }>;
  // Created Logic for review: class-specific totals
  infantry_lethality_pct: number;
  infantry_health_pct: number;
  lancer_lethality_pct: number;
  lancer_health_pct: number;
  marksman_lethality_pct: number;
  marksman_health_pct: number;
  infantry_power: number;
  lancer_power: number;
  marksman_power: number;
   }