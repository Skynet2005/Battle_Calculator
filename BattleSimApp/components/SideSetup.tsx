import React from "react";
import { Text, View, TouchableOpacity, useWindowDimensions } from "react-native";
import { Picker, PickerItem } from "./WebCompatiblePicker";
import axios from "axios";

import { styles } from "../styles";
import { CollapsibleSection } from "./CollapsibleSection";
import {
  Hero, Class, ClassSel,
  ChiefGearSlot, ChiefGearSelectionMap, ChiefCharmLevelsMap,
  ChiefSkinBonuses, DaybreakBonuses,
  HeroGearSelectionByClass, HeroGearPieceSelection, HeroGearClassSelection,
  ResearchSelection, ResearchBuffs
} from "../types";

import { ClassRow } from "./ClassRow";
import { ResearchSection } from "./ResearchSection";
import { ChiefGearSection } from "./ChiefGearSection";
import { ChiefCharmsSection } from "./ChiefCharmsSection";
import { ChiefSkinSection } from "./ChiefSkinSection";
import { HeroGearSection } from "./HeroGearSection";
import { DaybreakSection } from "./DaybreakSection";

interface Props {
  side: "atk" | "def";
  heroes: Hero[];
  troops: string[];
  
  // Created Logic for review: filtered data by class for better organization
  heroesByClass: { [cls in Class]: Hero[] };
  troopsByClass: { [cls in Class]: string[] };

  heroSel: ClassSel;
  troopSel: ClassSel;
  slotSel: { [cls in Class]: string };
  ratioSel: { [cls in Class]: string };
  ewLevelSel: { [cls in Class]: string };

  /* setters */
  setHeroSel: React.Dispatch<React.SetStateAction<ClassSel>>;
  setTroopSel: React.Dispatch<React.SetStateAction<ClassSel>>;
  setSlotSel: React.Dispatch<React.SetStateAction<{ [cls in Class]: string }>>;
  setRatioSel: React.Dispatch<React.SetStateAction<{ [cls in Class]: string }>>;
  setEwLevelSel: React.Dispatch<React.SetStateAction<{ [cls in Class]: string }>>;

  disabled?: boolean;
  capacity: string;
  setCapacity: (v: string) => void;

  // Attack type to determine if joiners should be shown
  attackType?: "solo" | "rally";

  // Optional persistence
  gearSelection?: ChiefGearSelectionMap;
  onGearSelectionChange?: (v: ChiefGearSelectionMap) => void;
  charmLevels?: ChiefCharmLevelsMap;
  onCharmLevelsChange?: (v: ChiefCharmLevelsMap) => void;

  // Chief Skin bonuses
  chiefSkinBonuses?: ChiefSkinBonuses;
  onChiefSkinBonusesChange?: (bonuses: ChiefSkinBonuses) => void;

  // Daybreak Island bonuses
  daybreakBonuses?: DaybreakBonuses;
  onDaybreakChange?: (b: DaybreakBonuses) => void;

  // Legendary/Mythic Hero Gear
  heroGearSelection?: HeroGearSelectionByClass;
  onHeroGearSelectionChange?: (v: HeroGearSelectionByClass) => void;

  // Support Heroes (Joiners) for Rally
  supportHeroes?: string[];
  onSupportHeroesChange?: (v: string[]) => void;

  // Research
  researchSelection?: ResearchSelection | null;
  onResearchSelectionChange?: (rows: ResearchSelection) => void;
  onResearchBuffsChange?: (buffs: ResearchBuffs) => void;
  // Created Logic for review: choose which subset to render
  variant?: "formation" | "city";
}

export const SideSetup: React.FC<Props> = (p) => {
  const { width } = useWindowDimensions();
  const isVerySmall = width < 480;

  // Calculate counts from ratios and capacity
  const classes: Class[] = ["Infantry", "Lancer", "Marksman"];
  const [counts, setCounts] = React.useState<{ [cls in Class]: string }>({ Infantry: "", Lancer: "", Marksman: "" });
  const [countsTouched, setCountsTouched] = React.useState(false);
  const capacityInt = parseInt(p.capacity, 10) || 0;

  React.useEffect(() => {
    if (countsTouched) return;
    const next: { [cls in Class]: string } = { Infantry: "", Lancer: "", Marksman: "" };
    classes.forEach((cls) => {
      const r = Math.max(0, parseFloat(p.ratioSel[cls] || "0"));
      next[cls] = String(Math.round(capacityInt * r));
    });
    setCounts(next);
  }, [p.ratioSel.Infantry, p.ratioSel.Lancer, p.ratioSel.Marksman, capacityInt, countsTouched]);

  const onCountChange = (cls: Class, txt: string) => {
    const cleaned = txt.replace(/[^0-9]/g, "");
    setCounts((prev) => ({ ...prev, [cls]: cleaned }));
    setCountsTouched(true);
    const nums = classes.map((c) => parseInt(c === cls ? cleaned : (counts[c] || "0"), 10) || 0);
    const total = nums.reduce((a, b) => a + b, 0);
    if (total > 0) {
      const nextRatios: { [k in Class]: string } = { Infantry: "0", Lancer: "0", Marksman: "0" };
      classes.forEach((c, i) => {
        nextRatios[c] = String(Math.round((nums[i] / total) * 1000) / 1000);
      });
      p.setRatioSel(nextRatios);
    }
  };

  const showFormation = (p.variant ?? "formation") === "formation";
  const showCity = (p.variant ?? "formation") === "city";

  return (
    <View>
      {showFormation && (
        (["Infantry","Lancer","Marksman"] as Class[]).map((cls) => {
          const heroSel = p.heroSel[cls];
          const troopSel = p.troopSel[cls];
          const slot = p.slotSel[cls];
          const ew = p.ewLevelSel[cls];
          const ratio = p.ratioSel[cls];

          const defaultPiece = { type: cls, enhancement: 0, stars: 0, level: 0, essence_level: 0, mastery_forged: true, mastery_level: 0, stacking: "additive" as const };
          const gearSel = {
            goggles: defaultPiece,
            boot: defaultPiece,
            glove: defaultPiece,
            belt: defaultPiece,
          } as any;

          const onHeroChange = (c: Class, name: string) => p.setHeroSel({ ...p.heroSel, [c]: name });
          const onTroopChange = (c: Class, troop: string) => p.setTroopSel({ ...p.troopSel, [c]: troop });
          const onSlotChange = (c: Class, v: string) => p.setSlotSel({ ...p.slotSel, [c]: v });
          const onEwChange = (c: Class, v: string) => p.setEwLevelSel({ ...p.ewLevelSel, [c]: v });
          const onRatioChange = (c: Class, v: string) => p.setRatioSel({ ...p.ratioSel, [c]: v });

          return (
            <CollapsibleSection key={`${p.side}-${cls}`} title={`${cls} Setup`} defaultOpen={false}>
              <View>
                <ClassRow
                  cls={cls}
                  side={p.side}
                  heroes={p.heroesByClass[cls]}
                  troops={p.troopsByClass[cls]}
                  heroSel={heroSel}
                  troopSel={troopSel}
                  slot={slot}
                  ewLevel={ew}
                  ratio={ratio}
                  onHeroChange={onHeroChange}
                  onTroopChange={onTroopChange}
                  onSlotChange={onSlotChange}
                  onEwLevelChange={onEwChange}
                  onRatioChange={onRatioChange}
                  count={counts[cls]}
                  onCountChange={onCountChange}
                  gearSel={gearSel}
                  onGearChange={() => {}}
                  charmsSel={{}}
                  onCharmsChange={() => {}}
                  skinSel=""
                  onSkinChange={() => {}}
                />
              </View>
            </CollapsibleSection>
          );
        })
      )}

      {showFormation && p.attackType === "rally" && p.supportHeroes && p.onSupportHeroesChange && (
        <CollapsibleSection title="Support Heroes (Joiners)">
          <View style={isVerySmall ? styles.mobileRow : styles.row}>
            {p.supportHeroes!.map((hero, idx) => (
              <View key={`${p.side}-joiner-${idx}`} style={{ flex: 1, minWidth: 0, marginRight: idx < p.supportHeroes!.length - 1 ? 8 : 0 }}>
                <Text style={styles.helperText}>Joiner {idx + 1}</Text>
                <Picker
                  selectedValue={hero}
                  onValueChange={(value) => {
                    const newSupport = [...p.supportHeroes!];
                    newSupport[idx] = value;
                    p.onSupportHeroesChange!(newSupport);
                  }}
                  style={[styles.picker, p.side === "atk" ? styles.attackerPicker : styles.defenderPicker]}
                  enabled={!p.disabled}
                >
                  <PickerItem label="None" value="" />
                  {p.heroes.map((h) => (
                    <PickerItem key={h.name} label={h.name} value={h.name} />
                  ))}
                </Picker>
              </View>
            ))}
          </View>
        </CollapsibleSection>
      )}

      {showCity && (
        <>
          {/* City Buffs Section (Gear & Charms) */}
          <CollapsibleSection
            title={`Chief Gear & Charms`}
            defaultOpen={false}
          >
            <View style={[isVerySmall ? styles.mobileRow : styles.row, { flexDirection: isVerySmall ? 'column' : 'row' }]}> 
              <View style={{ flex: 1, minWidth: 0, marginRight: isVerySmall ? 0 : 6, marginBottom: isVerySmall ? 8 : 0 }}>
                <ChiefGearSection
                  side={p.side}
                  hideHeader
                  disabled={p.disabled}
                  value={p.gearSelection}
                  onChange={p.onGearSelectionChange}
                />
              </View>
              <View style={{ flex: 1, minWidth: 0, marginLeft: isVerySmall ? 0 : 6 }}>
                <ChiefCharmsSection
                  side={p.side}
                  hideHeader
                  disabled={p.disabled}
                  value={p.charmLevels as any}
                  onChange={p.onCharmLevelsChange as any}
                />
              </View>
            </View>
          </CollapsibleSection>

          {/* Chief Skin Bonuses */}
          <CollapsibleSection title="Chief Skin Bonuses" defaultOpen={false}>
            <View style={isVerySmall ? styles.mobileRow : styles.row}>
              <ChiefSkinSection
                side={p.side}
                disabled={p.disabled}
                value={p.chiefSkinBonuses}
                onChange={p.onChiefSkinBonusesChange}
              />
            </View>
          </CollapsibleSection>

          {/* Legendary/Mythic Hero Gear */}
          <CollapsibleSection title="Legendary/Mythic Hero Gear" defaultOpen={false}>
            <View style={isVerySmall ? styles.mobileRow : styles.row}>
              <HeroGearSection
                side={p.side}
                disabled={p.disabled}
                value={p.heroGearSelection as any}
                onChange={p.onHeroGearSelectionChange as any}
              />
            </View>
          </CollapsibleSection>

          {/* Daybreak Island Bonuses */}
          <CollapsibleSection title="Daybreak Island Bonuses" defaultOpen={false}>
            <View style={isVerySmall ? styles.mobileRow : styles.row}>
              <DaybreakSection
                side={p.side}
                disabled={p.disabled}
                value={p.daybreakBonuses}
                onChange={p.onDaybreakChange}
              />
            </View>
          </CollapsibleSection>

          {/* Research */}
          <CollapsibleSection title="Battle Research" defaultOpen={false}>
            <View style={isVerySmall ? styles.mobileRow : styles.row}>
              <ResearchSection
                side={p.side}
                onChange={(b) => p.onResearchBuffsChange && p.onResearchBuffsChange(b)}
                onSelectionChange={(rows)=> p.onResearchSelectionChange && p.onResearchSelectionChange(rows)}
                value={p.researchSelection || undefined}
              />
            </View>
          </CollapsibleSection>
        </>
      )}

      {/* Removed separate Troop Ratios & Counts section (moved into ClassRow) */}
    </View>
  );
};
