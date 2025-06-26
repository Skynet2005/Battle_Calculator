/* ──────────────────────────────────────────────────────────────
   Type Declarations
   ────────────────────────────────────────────────────────────── */

export type Class = "Infantry" | "Lancer" | "Marksman";

export type ClassSel = {
  Infantry: string;
  Lancer: string;
  Marksman: string;
};

export interface Hero {
  name: string;
  charClass: string;          // "infantry" | "lancer" | "marksman"
  generation: number;
}

export type TroopBreakdown = { [cls in Class]?: number };

export interface SideDetails {
  heroes: {
    [cls in Class]: {
      name: string;
      class: string;
      generation: number;
      skills: string[];
      troop_level: string;
      troop_power: number;
      count_start: number;
      count_end: number;
    };
  };
  total_power: number;
  kills: TroopBreakdown;
  survivors: TroopBreakdown;
}

export interface SimResult {
  winner?: string;
  rounds?: number;

  attacker_win_rate?: number;
  defender_win_rate?: number;
  avg_attacker_survivors?: number;
  avg_defender_survivors?: number;

  proc_stats?: { [skill: string]: number };

  sample_battle?: {
    winner: string;
    rounds: number;
    attacker: SideDetails;
    defender: SideDetails;
    proc_stats?: { [skill: string]: number };
  };

  attacker?: SideDetails;
  defender?: SideDetails;
}
