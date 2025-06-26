import React from "react";
import { ClassRow } from "./ClassRow";
import { Hero, Class, ClassSel } from "../types";

interface Props {
  side: "atk" | "def";
  heroes: Hero[];
  troops: string[];

  heroSel: ClassSel;
  troopSel: ClassSel;
  slotSel: { [cls in Class]: string };
  ratioSel: { [cls in Class]: string };

  /* setters for the four objects above */
  setHeroSel: React.Dispatch<React.SetStateAction<ClassSel>>;
  setTroopSel: React.Dispatch<React.SetStateAction<ClassSel>>;
  setSlotSel: React.Dispatch<
    React.SetStateAction<{ [cls in Class]: string }>
  >;
  setRatioSel: React.Dispatch<
    React.SetStateAction<{ [cls in Class]: string }>
  >;
}

export const SideSetup: React.FC<Props> = (p) => {
  return (
    <>
      {(["Infantry", "Lancer", "Marksman"] as const).map((cls) => (
        <ClassRow
          key={`${p.side}-${cls}`}
          cls={cls}
          side={p.side}
          heroes={p.heroes}
          troops={p.troops}
          heroSel={p.heroSel[cls]}
          troopSel={p.troopSel[cls]}
          slot={p.slotSel[cls]}
          ratio={p.ratioSel[cls]}
          setHero={(v) =>
            p.setHeroSel((s) => ({ ...s, [cls]: v }))
          }
          setTroop={(v) =>
            p.setTroopSel((s) => ({ ...s, [cls]: v }))
          }
          setSlot={(v) =>
            p.setSlotSel((s) => ({ ...s, [cls]: v }))
          }
          setRatio={(v) =>
            p.setRatioSel((s) => ({ ...s, [cls]: v }))
          }
        />
      ))}
    </>
  );
};
