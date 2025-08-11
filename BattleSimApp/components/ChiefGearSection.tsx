import React from "react";
import axios from "axios";
import { Text, View, TouchableOpacity } from "react-native";
import { styles } from "../styles";
import type { ChiefGearSelectionMap, ChiefGearSlot } from "../types";
import { Picker, PickerItem } from "./WebCompatiblePicker";

type GearProps = {
  side: "atk" | "def";
  hideHeader?: boolean;
  disabled?: boolean;
  value?: ChiefGearSelectionMap;
  onChange?: (v: ChiefGearSelectionMap) => void;
};

const gearSlots: ChiefGearSlot[] = ["Cap", "Coat", "Ring", "Watch", "Pants", "Weapon"];

export const ChiefGearSection: React.FC<GearProps> = ({ side, hideHeader, disabled, value, onChange }) => {
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
    axios.get("http://localhost:8000/api/gear/chief/options")
      .then((r) => setOptions(r.data))
      .catch(() => {});
  }, []);

  // deep compare helpers
  const gearSelectionsEqual = React.useCallback((a?: Record<string, { tier: string; stars: number }>, b?: Record<string, { tier: string; stars: number }> ) => {
    if (!a && !b) return true;
    if (!a || !b) return false;
    for (const slot of gearSlots) {
      const av = a[slot];
      const bv = b[slot];
      if (!av && !bv) continue;
      if (!av || !bv) return false;
      if (av.tier !== bv.tier || (av.stars ?? 0) !== (bv.stars ?? 0)) return false;
    }
    return true;
  }, []);

  // Sync external value (only when content actually differs)
  React.useEffect(() => {
    if (!value) return;
    if (!gearSelectionsEqual(sel, value)) {
      setSel(value);
    }
  }, [value, sel, gearSelectionsEqual]);

  // If parent did not provide a controlled value, emit defaults upward once ready
  React.useEffect(() => {
    if (value) return; // parent controls state; do not push defaults upward
    if (Object.keys(options).length > 0 && Object.keys(sel).length > 0) {
      const hasDefaults = gearSlots.every(slot => sel[slot] && sel[slot].tier && (sel[slot].stars ?? 0) > 0);
      if (hasDefaults && onChange) {
        onChange(sel as ChiefGearSelectionMap);
      }
    }
  }, [options, sel, onChange, value]);

  // Default selections to the last available items if empty
  React.useEffect(() => {
    setSel((prev) => {
      const next = { ...prev } as Record<string, { tier: string; stars: number }>;
      let changed = false;
      gearSlots.forEach((slot) => {
        const list = options[slot] || [];
        const tiers = list.map((o) => o.tier).filter((v, i, a) => a.indexOf(v) === i);
        if (tiers.length === 0) return;
        if (!next[slot] || !next[slot].tier) {
          const lastTier = tiers[tiers.length - 1];
          const starList = list.filter((o) => o.tier === lastTier).map((o) => o.stars);
          const lastStar = starList.length ? starList[starList.length - 1] : 0;
          next[slot] = { tier: lastTier, stars: lastStar };
          changed = true;
        } else if (next[slot] && (next[slot].stars === undefined || next[slot].stars === 0)) {
          const starList = list.filter((o) => o.tier === next[slot].tier).map((o) => o.stars);
          if (starList.length) {
            next[slot] = { tier: next[slot].tier, stars: starList[starList.length - 1] };
            changed = true;
          }
        }
      });
      // Removed onChange call to prevent setState during render
      return changed ? next : prev;
    });
  }, [options]);

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
        // emit events (do not call onChange here to avoid update loops)
        const payload = { kind: 'chief-gear-totals', side, totals: d };
        try { (global as any).onChiefGearCharms?.(payload); } catch {}
        try { (global as any).dispatchEvent?.(new CustomEvent('chief-gear-charms', { detail: payload })); } catch {}
      })
      .catch(() => setTotals(null));
  }, [sel, side]);

  React.useEffect(() => { 
    if (Object.keys(options).length > 0 && Object.keys(sel).length > 0) {
      recalc(); 
    }
  }, [options, sel.Cap, sel.Coat, sel.Ring, sel.Watch, sel.Pants, sel.Weapon]); // Use specific gear slot properties instead of entire object

  const sideLabelStyle = side === "atk" ? styles.attackerLabel : styles.defenderLabel;
  const sidePickerStyle = side === "atk" ? styles.attackerPicker : styles.defenderPicker;

  return (
    <View style={[styles.panel]}>
      {!hideHeader && (
        <Text style={[styles.subHeader, sideLabelStyle]}>
          Chief Gear
        </Text>
      )}

      {gearSlots.map((slot) => (
        <View key={slot} style={styles.row}>
          <Text style={styles.label}>{slot}</Text>
          <View style={styles.inlineRow}>
            <View style={{ flex: 1 }}>
              <Text style={styles.helperText}>Tier</Text>
              <Picker
                enabled={!disabled}
                selectedValue={sel[slot]?.tier || ""}
                onValueChange={(v) => {
                  const next = { ...(sel || {}) };
                  next[slot] = { tier: v, stars: 0 };
                  setSel(next);
                  onChange?.(next as ChiefGearSelectionMap);
                }}
                style={[styles.picker, sidePickerStyle]}
              >
                {tiersFor(slot).map((t) => (
                  <PickerItem key={t} label={t} value={t} />
                ))}
              </Picker>
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.helperText}>Stars</Text>
              <Picker
                enabled={!disabled}
                selectedValue={sel[slot]?.stars ?? 0}
                onValueChange={(v) => {
                  const next = { ...(sel || {}) };
                  next[slot] = { tier: next[slot]?.tier || "", stars: v };
                  setSel(next);
                  onChange?.(next as ChiefGearSelectionMap);
                }}
                style={[styles.picker, sidePickerStyle]}
              >
                {(sel[slot]?.tier ? starsFor(slot, sel[slot].tier) : []).map((s) => (
                  <PickerItem key={`${slot}-${s}`} label={`${s}`} value={s} />
                ))}
              </Picker>
            </View>
          </View>
        </View>
      ))}

      {/* Totals */}
      {totals && (
        <View style={styles.totalBar}>
          <Text style={styles.totalText}>Attack: {totals.atk.toFixed(2)}%</Text>
          <Text style={styles.totalText}>Defense: {totals.def.toFixed(2)}%</Text>
          <Text style={styles.totalText}>Power: {Math.round(totals.pow).toLocaleString()}</Text>
        </View>
      )}

      {/* Set bonus badges */}
      <View style={[styles.inlineRow, { marginTop: 8 }]}>
        <View style={[styles.pill, atkSetActive ? styles.attackerTint : null]}>
          <Text style={styles.pillText}>Set Bonus: Attack {totals?.atkBonus?.toFixed(2) ?? "0.00"}%</Text>
        </View>
        <View style={[styles.pill, defSetActive ? styles.defenderTint : null]}>
          <Text style={styles.pillText}>Set Bonus: Defense {totals?.defBonus?.toFixed(2) ?? "0.00"}%</Text>
        </View>
      </View>
    </View>
  );
};
