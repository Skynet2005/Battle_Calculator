import React from "react";
import { Text, View, TextInput, TouchableOpacity } from "react-native";
import { ChiefGearSlot, ChiefCharmOption, ChiefGearSelectionMap, ChiefCharmLevelsMap, ChiefSkinBonuses } from "../types";
import { Picker } from "@react-native-picker/picker";
import axios from "axios";
import { ClassRow } from "./ClassRow";
import { Hero, Class, ClassSel } from "../types";
import { styles } from "../styles";
import { ChiefSkinSection } from "./ChiefSkinSection";

interface Props {
  side: "atk" | "def";
  heroes: Hero[];
  troops: string[];

  heroSel: ClassSel;
  troopSel: ClassSel;
  slotSel: { [cls in Class]: string };
  ratioSel: { [cls in Class]: string };
  ewLevelSel: { [cls in Class]: string };

  /* setters for the four objects above */
  setHeroSel: React.Dispatch<React.SetStateAction<ClassSel>>;
  setTroopSel: React.Dispatch<React.SetStateAction<ClassSel>>;
  setSlotSel: React.Dispatch<
    React.SetStateAction<{ [cls in Class]: string }>
  >;
  setRatioSel: React.Dispatch<
    React.SetStateAction<{ [cls in Class]: string }>
  >;
  setEwLevelSel: React.Dispatch<
    React.SetStateAction<{ [cls in Class]: string }>
  >;
  disabled?: boolean;
  capacity: string;
  setCapacity: (v: string) => void;
  // optional: gear/charm selection lift to parent for persistence
  gearSelection?: ChiefGearSelectionMap;
  onGearSelectionChange?: (v: ChiefGearSelectionMap) => void;
  charmLevels?: ChiefCharmLevelsMap;
  onCharmLevelsChange?: (v: ChiefCharmLevelsMap) => void;
  // Chief Skin bonuses
  chiefSkinBonuses?: ChiefSkinBonuses;
  onChiefSkinBonusesChange?: (bonuses: ChiefSkinBonuses) => void;
}

export const SideSetup: React.FC<Props> = (p) => {
  const sum = (Object.values(p.ratioSel) as string[])
    .map((v) => parseFloat(v || "0"))
    .reduce((a, b) => a + (isNaN(b) ? 0 : b), 0);
  const isOk = Math.abs(sum - 1) < 0.001;

  const classes: Class[] = ["Infantry", "Lancer", "Marksman"];
  const [counts, setCounts] = React.useState<{ [cls in Class]: string }>({ Infantry: "", Lancer: "", Marksman: "" });
  const [countsTouched, setCountsTouched] = React.useState(false);
  const capacityInt = parseInt(p.capacity, 10) || 0;

  React.useEffect(() => {
    if (countsTouched) return;
    const next: { [cls in Class]: string } = { Infantry: "", Lancer: "", Marksman: "" };
    (classes).forEach((cls) => {
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

  const sumCounts = classes.map((c) => parseInt(counts[c] || "0", 10) || 0).reduce((a, b) => a + b, 0);

  const normalize = () => {
    // Created Logic for review: normalize ratios to sum to 1
    const vals = (Object.values(p.ratioSel) as string[]).map((v) => Math.max(0, parseFloat(v || "0")));
    const total = vals.reduce((a, b) => a + (isNaN(b) ? 0 : b), 0);
    const safeTotal = total > 0 ? total : 1;
    const classes: Class[] = ["Infantry", "Lancer", "Marksman"];
    const next = { ...p.ratioSel } as { [cls in Class]: string };
    classes.forEach((cls, i) => {
      next[cls] = String(Math.round((vals[i] / safeTotal) * 1000) / 1000);
    });
    p.setRatioSel(next);
  };

  // Collapsible state for Chief Gear & Charms section
  const [gearCollapsed, setGearCollapsed] = React.useState(false);

  return (
    <>
      {/* Chief Gear & Charms (collapsible, side-by-side) */}
      <View style={{ marginBottom: 8 }}>
        <View style={styles.sectionHeaderRow}>
          <Text style={styles.subHeader}>Chief Gear & Charms</Text>
          <TouchableOpacity style={styles.sectionToggleBtn} onPress={() => setGearCollapsed((c) => !c)}>
            <Text style={styles.sectionToggleText}>{gearCollapsed ? "Expand" : "Collapse"}</Text>
          </TouchableOpacity>
        </View>
        {!gearCollapsed && (
          <View style={[styles.row, { flexDirection: 'row' }]}>
            <View style={{ flex: 1, minWidth: 0, marginRight: 6 }}>
              <ChiefGearSection
                side={p.side}
                hideHeader
                disabled={p.disabled}
                value={p.gearSelection}
                onChange={p.onGearSelectionChange}
              />
            </View>
            <View style={{ flex: 1, minWidth: 0, marginLeft: 6 }}>
              <ChiefCharmsSection
                side={p.side}
                hideHeader
                disabled={p.disabled}
                value={p.charmLevels as any}
                onChange={p.onCharmLevelsChange as any}
              />
            </View>
          </View>
        )}
      </View>

      {/* Chief Skin Bonuses */}
      <View style={{ marginBottom: 8 }}>
        <ChiefSkinSection
          side={p.side}
          value={p.chiefSkinBonuses}
          onChange={p.onChiefSkinBonusesChange}
          disabled={p.disabled}
        />
      </View>

      {(["Infantry", "Lancer", "Marksman"] as const).map((cls) => {
        const others = (["Infantry", "Lancer", "Marksman"] as const)
          .filter((c) => c !== cls)
          .map((c) => Math.max(0, parseFloat(p.ratioSel[c] || "0")))
          .reduce((a, b) => a + (isNaN(b) ? 0 : b), 0);
        const remainingPct = Math.max(0, Math.round((1 - others) * 100));
        const currentPct = Math.max(0, Math.round(parseFloat(p.ratioSel[cls] || "0") * 100));
        const maxPercent = Math.max(currentPct, remainingPct);
        return (
        <ClassRow
          key={`${p.side}-${cls}`}
          cls={cls}
          side={p.side}
          heroes={p.heroes}
          troops={p.troops}
          heroSel={p.heroSel[cls]}
          troopSel={p.troopSel[cls]}
          slot={p.slotSel[cls]}
          ewLevel={p.ewLevelSel[cls] || "10"}
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
          setEwLevel={(v) =>
            p.setEwLevelSel((prev) => ({ ...prev, [cls]: v }))
          }
          setRatio={(v) =>
            p.setRatioSel((prev) => {
              // Created Logic for review: clamp per-side ratios so total <= 1 (<=100%)
              const classes: Class[] = ["Infantry", "Lancer", "Marksman"];
              const requested = Math.max(0, Math.min(1, parseFloat(v || "0")));
              const otherSum = classes
                .filter((c) => c !== cls)
                .map((c) => Math.max(0, parseFloat(prev[c] || "0")))
                .reduce((a, b) => a + (isNaN(b) ? 0 : b), 0);
              const maxAllowed = Math.max(0, 1 - otherSum);
              const finalVal = Math.min(requested, maxAllowed);
              const out = String(Math.round(finalVal * 1000) / 1000);
              return { ...prev, [cls]: out } as { [k in Class]: string };
            })
          }
          disabled={p.disabled}
          maxPercent={maxPercent}
          countValue={counts[cls]}
          onCountChange={(t) => onCountChange(cls, t)}
          onLoadCountFromRatio={() => {
            const r = Math.max(0, parseFloat(p.ratioSel[cls] || "0"));
            const c = String(Math.round(capacityInt * r));
            setCounts((prev) => ({ ...prev, [cls]: c }));
          }}
        />
        );
      })}
      <View style={styles.helperActionsRow}>
        <Text style={styles.linkTextSecondary} onPress={() => {
          const classes: Class[] = ["Infantry", "Lancer", "Marksman"];
          const val = String(Math.round((1/3) * 1000) / 1000);
          p.setRatioSel(Object.fromEntries(classes.map(c => [c, val])) as { [k in Class]: string });
        }}>Even Split</Text>
        <Text style={styles.linkText} onPress={() => {
          p.setRatioSel({ Infantry: "1", Lancer: "0", Marksman: "0" });
        }}>100% Infantry</Text>
        <Text style={styles.linkText} onPress={() => {
          p.setRatioSel({ Infantry: "0", Lancer: "1", Marksman: "0" });
        }}>100% Lancer</Text>
        <Text style={styles.linkText} onPress={() => {
          p.setRatioSel({ Infantry: "0", Lancer: "0", Marksman: "1" });
        }}>100% Marksman</Text>
        {!isOk && (
          <Text style={styles.linkTextDanger} onPress={normalize}>Normalize</Text>
        )}
      </View>
      <View style={styles.helperActionsRow}>
        <Text style={styles.linkTextSecondary} onPress={() => {
          // Load counts from current ratios and capacity
          setCountsTouched(false);
        }}>Reload all counts from ratios</Text>
        <Text style={styles.linkText} onPress={() => {
          // Adjust capacity to match sum of manual counts
          p.setCapacity(String(sumCounts));
        }}>Set Capacity = Sum of counts</Text>
      </View>
      <Text style={[styles.helperText, (sumCounts === capacityInt) ? styles.helperTextOk : styles.helperTextWarn]}>
        Sum of counts: {sumCounts} / Capacity: {capacityInt}
      </Text>
      <Text
        style={[
          styles.helperText,
          isOk ? styles.helperTextOk : styles.helperTextWarn,
        ]}
      >
        {p.side === "atk" ? "Attacker" : "Defender"} ratios sum: {sum.toFixed(3)}
      </Text>
      <View style={styles.progressBar}>
        <View style={[styles.progressFill, { width: `${Math.min(100, Math.max(0, sum * 100))}%`, backgroundColor: isOk ? '#10B981' : '#F59E0B' }]} />
      </View>
    </>
  );
};

/* ────────────────────────────────────────────────────────────── */
/* Chief Gear UI                                                 */
/* ────────────────────────────────────────────────────────────── */

type GearProps = { side: "atk" | "def"; hideHeader?: boolean; disabled?: boolean; value?: ChiefGearSelectionMap; onChange?: (v: ChiefGearSelectionMap) => void };

const gearSlots: ChiefGearSlot[] = ["Cap", "Coat", "Ring", "Watch", "Pants", "Weapon"];

const ChiefGearSection: React.FC<GearProps> = ({ side, hideHeader, value, onChange }) => {
  // Created Logic for review: fetch options once
  const [options, setOptions] = React.useState<Record<string, { tier: string; stars: number; attackPct: number; defensePct: number; power: number }[]>>({} as any);
  const [sel, setSel] = React.useState<Record<string, { tier: string; stars: number }>>(value || {});
  const [totals, setTotals] = React.useState<null | {
    atk: number; def: number; pow: number; atkBonus: number; defBonus: number;
    infantry_attack_pct: number; infantry_defense_pct: number;
    lancer_attack_pct: number; lancer_defense_pct: number;
    marksman_attack_pct: number; marksman_defense_pct: number;
  }>(null);
  const atkSetActive = !!(totals && totals.atkBonus > 0);
  const defSetActive = !!(totals && totals.defBonus > 0);

  React.useEffect(() => {
    axios
      .get("http://localhost:8000/api/gear/chief/options")
      .then((r) => setOptions(r.data))
      .catch(() => {});
  }, []);

  // Default selections to the last available items if empty
  React.useEffect(() => {
    setSel((prev) => {
      const next = { ...prev } as Record<string, { tier: string; stars: number }>;
      let changed = false;
      gearSlots.forEach((slot) => {
        const tiers = (options[slot] || []).map((o) => o.tier).filter((v, i, a) => a.indexOf(v) === i);
        if (tiers.length === 0) return;
        if (!next[slot] || !next[slot].tier) {
          const lastTier = tiers[tiers.length - 1];
          const stars = (options[slot] || []).filter((o) => o.tier === lastTier).map((o) => o.stars);
          const lastStar = stars.length ? stars[stars.length - 1] : 0;
          next[slot] = { tier: lastTier, stars: lastStar };
          changed = true;
        } else if (next[slot] && (next[slot].stars === undefined || next[slot].stars === 0)) {
          const stars = (options[slot] || []).filter((o) => o.tier === next[slot].tier).map((o) => o.stars);
          if (stars.length) {
            next[slot] = { tier: next[slot].tier, stars: stars[stars.length - 1] };
            changed = true;
          }
        }
      });
      return changed ? next : prev;
    });
  }, [options]);

  // sync from external value
  React.useEffect(() => {
    if (value) setSel(value);
  }, [value]);

  const tiersFor = (slot: ChiefGearSlot) => (options[slot] || []).map((o) => o.tier).filter((v, i, a) => a.indexOf(v) === i);
  const starsFor = (slot: ChiefGearSlot, tier: string) => (options[slot] || []).filter((o) => o.tier === tier).map((o) => o.stars);

  const recalc = React.useCallback(() => {
    const items = gearSlots
      .filter((s) => sel[s] && sel[s].tier)
      .map((s) => ({ item: s, tier: sel[s].tier, stars: sel[s].stars ?? 0 }));
    if (items.length !== gearSlots.length) {
      setTotals(null);
      return;
    }
    axios
      .post("http://localhost:8000/api/gear/chief/calc", { items })
      .then((r) => {
        const d = r.data;
        setTotals({
          atk: d.total_attack_pct,
          def: d.total_defense_pct,
          pow: d.total_power,
          atkBonus: d.set_bonus_attack_pct,
          defBonus: d.set_bonus_defense_pct,
          infantry_attack_pct: d.infantry_attack_pct,
          infantry_defense_pct: d.infantry_defense_pct,
          lancer_attack_pct: d.lancer_attack_pct,
          lancer_defense_pct: d.lancer_defense_pct,
          marksman_attack_pct: d.marksman_attack_pct,
          marksman_defense_pct: d.marksman_defense_pct,
        });
        // emit to parent
        const payload = { kind: 'chief-gear-totals', side, totals: d };
        try {
          (global as any).onChiefGearCharms?.(payload);
        } catch {}
        try {
          (global as any).dispatchEvent?.(new CustomEvent('chief-gear-charms', { detail: payload }));
        } catch {}
        onChange && onChange(sel as ChiefGearSelectionMap);
      })
      .catch(() => setTotals(null));
  }, [sel]);

  React.useEffect(() => { recalc(); }, [recalc]);

  const maxAll = React.useCallback(() => {
    setSel((prev) => {
      const next: Record<string, { tier: string; stars: number }> = { ...prev };
      gearSlots.forEach((slot) => {
        const tiers = (options[slot] || []).map((o) => o.tier).filter((v, i, a) => a.indexOf(v) === i);
        if (tiers.length === 0) return;
        const lastTier = tiers[tiers.length - 1];
        const stars = (options[slot] || []).filter((o) => o.tier === lastTier).map((o) => o.stars);
        const lastStar = stars.length ? stars[stars.length - 1] : 0;
        next[slot] = { tier: lastTier, stars: lastStar };
      });
      return next;
    });
  }, [options]);

  const clearAll = React.useCallback(() => {
    setSel({});
    setTotals(null);
  }, []);

  const adjustStar = React.useCallback((slot: ChiefGearSlot, delta: number) => {
    setSel((prev) => {
      const currTier = prev[slot]?.tier || "";
      if (!currTier) return prev;
      const starList = (options[slot] || []).filter((o) => o.tier === currTier).map((o) => o.stars);
      if (starList.length === 0) return prev;
      const curr = prev[slot]?.stars ?? starList[starList.length - 1];
      const idx = Math.max(0, Math.min(starList.length - 1, starList.indexOf(curr) + delta));
      return { ...prev, [slot]: { tier: currTier, stars: starList[idx] } };
    });
  }, [options]);

  return (
    <View style={{ marginBottom: 8 }}>
      {!hideHeader && (
        <Text style={[styles.subHeader]}>{side === "atk" ? "Attacker" : "Defender"} Chief Gear</Text>
      )}
      <View style={styles.helperActionsRow}>
        <Text style={styles.linkTextSecondary} onPress={maxAll}>Max All</Text>
        <Text style={styles.linkText} onPress={clearAll}>Clear</Text>
      </View>
      <View style={[styles.row, { flexDirection: 'row', flexWrap: 'wrap' }]}> 
        {gearSlots.map((slot) => {
          const tierSel = sel[slot]?.tier || "";
          const starSel = sel[slot]?.stars ?? 0;
          const tiers = tiersFor(slot);
          const stars = tierSel ? starsFor(slot, tierSel) : [];
          return (
            <View key={`${side}-${slot}`} style={{ flexBasis: '50%', paddingHorizontal: 6, marginBottom: 8, minWidth: 265 }}>
              <Text style={[styles.label]}>{slot}</Text>
              <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                <View style={[styles.pickerContainer, { flex: 2 }]}> 
                  <Picker
                    selectedValue={tierSel}
                    onValueChange={(v) => setSel((s) => {
                      const tier = String(v);
                      const stars = (options[slot] || []).filter((o) => o.tier === tier).map((o) => o.stars);
                      const lastStar = stars.length ? stars[stars.length - 1] : 0;
                      return { ...s, [slot]: { tier, stars: lastStar } };
                    })}
                    enabled={true}
                  >
                    {tiers.length === 0 ? (
                      <Picker.Item label="Loading…" value="" />
                    ) : (
                      [<Picker.Item key="_sel" label="Select Tier" value="" />,
                       ...tiers.map((t) => (
                         <Picker.Item key={t} label={t} value={t} />
                       ))]
                    )}
                  </Picker>
                </View>
                <View style={[styles.pickerContainer, { flex: 1 }]}> 
                  <Picker
                    selectedValue={String(starSel)}
                    onValueChange={(v) => setSel((s) => ({ ...s, [slot]: { tier: tierSel, stars: parseInt(String(v), 10) || 0 } }))}
                    enabled={true}
                  >
                    {tierSel === "" ? (
                      <Picker.Item label="Select Tier first" value={"0"} />
                    ) : (
                      [<Picker.Item key="_star" label="★" value={"0"} />,
                       ...stars.map((st) => (
                         <Picker.Item key={`${tierSel}-${st}`} label={`★${st}`} value={String(st)} />
                       ))]
                    )}
                  </Picker>
                </View>
              </View>
              <View style={{ flexDirection: 'row', alignItems: 'flex-end', marginTop: 6, justifyContent: 'flex-end' }}>
                <TouchableOpacity style={styles.miniButton} onPress={() => adjustStar(slot, -1)}>
                  <Text style={styles.miniButtonText}>-</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.miniButton} onPress={() => adjustStar(slot, 1)}>
                  <Text style={styles.miniButtonText}>+</Text>
                </TouchableOpacity>
              </View>
            </View>
          );
        })}
      </View>
      {totals && (
        <View style={styles.tableContainer}>
          <View style={styles.tableHeaderRow}>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Class</Text>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Attack %</Text>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Defense %</Text>
          </View>
          {[{ c: 'Infantry', a: totals.infantry_attack_pct, d: totals.infantry_defense_pct },
            { c: 'Lancer', a: totals.lancer_attack_pct, d: totals.lancer_defense_pct },
            { c: 'Marksman', a: totals.marksman_attack_pct, d: totals.marksman_defense_pct }].map((row) => (
            <View key={`gear-row-${row.c}`} style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 1 }]}>{row.c}</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>{row.a.toFixed(2)}%</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>{row.d.toFixed(2)}%</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>{totals.pow}</Text>
            </View>
          ))}
          <View style={styles.tableRow}>
            <Text style={[styles.tableCell, { flex: 4 }]}>Set bonuses — +{totals.defBonus.toFixed(2)}% Defense; +{totals.atkBonus.toFixed(2)}% Attack</Text>
          </View>
        </View>
      )}
    </View>
  );
};

// Chief Charms
const ChiefCharmsSection: React.FC<GearProps> = ({ side, hideHeader, value, onChange }) => {
  // Created Logic for review: 3 charms per slot; user selects levels; totals recompute
  const [opts, setOpts] = React.useState<ChiefCharmOption[]>([]);
  const [levelsBySlot, setLevelsBySlot] = React.useState<Record<string, [number, number, number]>>(value as any || {});
  const [totals, setTotals] = React.useState<null | {
    leth: number; hp: number; pow: number;
    infantry_lethality_pct: number; infantry_health_pct: number;
    lancer_lethality_pct: number; lancer_health_pct: number;
    marksman_lethality_pct: number; marksman_health_pct: number;
  }>(null);
  const lastLevel = opts.length ? opts[opts.length - 1].level : 0;

  React.useEffect(() => {
    axios
      .get("http://localhost:8000/api/gear/chief/charms/options")
      .then((r) => setOpts(r.data))
      .catch(() => {});
  }, []);

  // ensure default [0,0,0] arrays for each slot
  React.useEffect(() => {
    setLevelsBySlot((prev) => {
      const next = { ...prev } as Record<string, [number, number, number]>;
      gearSlots.forEach((s) => {
        if (!next[s]) next[s] = [0, 0, 0];
      });
      return next;
    });
  }, []);

  // sync from external value
  React.useEffect(() => {
    if (value) setLevelsBySlot(value as any);
  }, [value]);

  // Default charm levels to the last (highest) available level when empty
  React.useEffect(() => {
    setLevelsBySlot((prev) => {
      const next = { ...prev } as Record<string, [number, number, number]>;
      let changed = false;
      const lastLevel = opts.length ? opts[opts.length - 1].level : 0;
      gearSlots.forEach((s) => {
        const arr = next[s] || [0, 0, 0];
        for (let i = 0; i < 3; i++) {
          if (!arr[i] || arr[i] <= 0) {
            arr[i] = lastLevel;
            changed = true;
          }
        }
        next[s] = arr as [number, number, number];
      });
      return changed ? next : prev;
    });
  }, [opts]);

  const recalc = React.useCallback(() => {
    // require all slots filled with exactly 3 selections (>0 levels)
    const payload: Record<string, number[]> = {};
    let allFilled = true;
    gearSlots.forEach((s) => {
      const arr = levelsBySlot[s] || [0, 0, 0];
      payload[s] = arr;
      if (arr.some((v) => v <= 0)) {
        allFilled = false;
      }
    });
    if (!allFilled) {
      setTotals(null);
      return;
    }
    axios
      .post("http://localhost:8000/api/gear/chief/charms/calc", { levels_by_slot: payload })
      .then((r) => {
        const d = r.data as any;
        setTotals({
          leth: d.total_lethality_pct,
          hp: d.total_health_pct,
          pow: d.total_power,
          infantry_lethality_pct: d.infantry_lethality_pct,
          infantry_health_pct: d.infantry_health_pct,
          lancer_lethality_pct: d.lancer_lethality_pct,
          lancer_health_pct: d.lancer_health_pct,
          marksman_lethality_pct: d.marksman_lethality_pct,
          marksman_health_pct: d.marksman_health_pct,
        });
        // emit to parent
        const ev = { kind: 'chief-charms-totals', side, totals: d };
        try {
          (global as any).onChiefGearCharms?.(ev);
        } catch {}
        try {
          (global as any).dispatchEvent?.(new CustomEvent('chief-gear-charms', { detail: ev }));
        } catch {}
        onChange && onChange(levelsBySlot as any);
      })
      .catch(() => setTotals(null));
  }, [levelsBySlot]);

  React.useEffect(() => { recalc(); }, [recalc]);

  const maxAll = React.useCallback(() => {
    setLevelsBySlot((prev) => {
      const next: Record<string, [number, number, number]> = { ...prev };
      gearSlots.forEach((s) => {
        next[s] = [lastLevel, lastLevel, lastLevel];
      });
      return next;
    });
  }, [lastLevel]);

  const clearAll = React.useCallback(() => {
    setLevelsBySlot((prev) => {
      const next: Record<string, [number, number, number]> = { ...prev };
      gearSlots.forEach((s) => {
        next[s] = [0, 0, 0];
      });
      return next;
    });
  }, []);

  return (
    <View style={{ marginBottom: 8 }}>
      {!hideHeader && (
        <Text style={[styles.subHeader]}>{side === "atk" ? "Attacker" : "Defender"} Chief Charms</Text>
      )}
      <View style={styles.helperActionsRow}>
        <Text style={styles.linkTextSecondary} onPress={maxAll}>Max All</Text>
        <Text style={styles.linkText} onPress={clearAll}>Clear</Text>
      </View>
      {gearSlots.map((slot) => (
        <View key={`${side}-charms-${slot}`} style={[styles.row, { alignItems: "center", flexDirection: 'row', flexWrap: 'nowrap' }]}>
          <Text style={[styles.label, { width: 84 }]}>{slot}</Text>
          {[0, 1, 2].map((idx) => (
            <View key={`${slot}-${idx}`} style={[styles.pickerContainer, { flex: 1 }]}> 
              <Picker
                selectedValue={String((levelsBySlot[slot] || [0, 0, 0])[idx])}
                onValueChange={(v) =>
                  setLevelsBySlot((prev) => {
                    const arr = (prev[slot] || [0, 0, 0]).slice() as [number, number, number];
                    arr[idx] = parseInt(String(v), 10) || 0;
                    return { ...prev, [slot]: arr } as Record<string, [number, number, number]>;
                  })
                }
              >
                {opts.length === 0 ? (
                  <Picker.Item label="Loading…" value={"0"} />
                ) : (
                  [<Picker.Item key="_lvl" label="Lvl" value={"0"} />,
                   ...opts.map((o) => (
                     <Picker.Item key={`lvl-${o.level}`} label={`${o.level}`} value={String(o.level)} />
                   ))]
                )}
              </Picker>
            </View>
          ))}
        </View>
      ))}
      {totals && (
        <View style={styles.tableContainer}>
          <View style={styles.tableHeaderRow}>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Class</Text>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Lethality %</Text>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Health %</Text>
          </View>
          {[{ c: 'Infantry', le: totals.infantry_lethality_pct, hp: totals.infantry_health_pct },
            { c: 'Lancer', le: totals.lancer_lethality_pct, hp: totals.lancer_health_pct },
            { c: 'Marksman', le: totals.marksman_lethality_pct, hp: totals.marksman_health_pct }].map((row) => (
            <View key={`charms-row-${row.c}`} style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 1 }]}>{row.c}</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>{(row.le ?? 0).toFixed(2)}%</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>{(row.hp ?? 0).toFixed(2)}%</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>{totals.pow}</Text>
            </View>
          ))}
        </View>
      )}
    </View>
  );
};