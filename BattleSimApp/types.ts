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
   export interface PassiveEffects {
     attacker: string[];  // e.g. ["Golden Guard +18% DEF", …]
     defender: string[];
   }

   /** final cumulative % bonuses after passives applied */
   export interface Bonuses {
     attacker: Record<string, number>; // { attack: 0.22, defense: 0.12, … }
     defender: Record<string, number>;
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

     /* server-side proc counter map  "SkillName-side" → count */
     proc_stats?: Record<string, number>;

     /* NEW: bullet list of expedition-skill impacts */
     passive_effects?: PassiveEffects;

     /* NEW: merged % bonuses after buffs/debuffs */
     bonuses?: Bonuses;

     /* when sims > 1 the server includes the first run here */
     sample_battle?: SimResult;
   }
