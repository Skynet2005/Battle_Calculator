import React from "react";
import axios from "axios";
import { Text, View, TouchableOpacity } from "react-native";
import { styles } from "../styles";
import type { ChiefCharmOption, ChiefCharmLevelsMap, ChiefGearSlot } from "../types";
import { Picker, PickerItem } from "./WebCompatiblePicker";

type Props = {
  side: "atk" | "def";
  hideHeader?: boolean;
  disabled?: boolean;
  value?: ChiefCharmLevelsMap;
  onChange?: (v: ChiefCharmLevelsMap) => void;
};

const gearSlots: ChiefGearSlot[] = ["Cap", "Coat", "Ring", "Watch", "Pants", "Weapon"];

export const ChiefCharmsSection: React.FC<Props> = ({ side, hideHeader, disabled, value, onChange }) => {
  const [opts, setOpts] = React.useState<ChiefCharmOption[]>([]);
  const [levelsBySlot, setLevelsBySlot] = React.useState<Record<string, [number, number, number]>>(value as any || {});
  const [totals, setTotals] = React.useState<null | {
    leth: number; hp: number; pow: number;
    infantry_lethality_pct: number; infantry_health_pct: number;
    lancer_lethality_pct: number; lancer_health_pct: number;
    marksman_lethality_pct: number; marksman_health_pct: number;
  }>(null);

  React.useEffect(() => {
    axios.get("http://localhost:8000/api/gear/chief/charms/options")
      .then((r) => setOpts(r.data))
      .catch(() => {});
  }, []);

  // deep compare helper for charm levels
  const charmLevelsEqual = React.useCallback((a?: Record<string, [number, number, number]>, b?: Record<string, [number, number, number]>) => {
    if (!a && !b) return true;
    if (!a || !b) return false;
    for (const slot of gearSlots) {
      const av = a[slot];
      const bv = b[slot];
      if (!av && !bv) continue;
      if (!av || !bv) return false;
      for (let i = 0; i < 3; i++) if ((av[i] ?? 0) !== (bv[i] ?? 0)) return false;
    }
    return true;
  }, []);

  // Sync external value (only when content actually differs)
  React.useEffect(() => {
    if (!value) return;
    if (!charmLevelsEqual(levelsBySlot, value as any)) {
      setLevelsBySlot(value as any);
    }
  }, [value, levelsBySlot, charmLevelsEqual]);

  // If parent did not provide a controlled value, emit defaults upward once ready
  React.useEffect(() => {
    if (value) return; // controlled by parent
    if (opts.length > 0 && Object.keys(levelsBySlot).length > 0) {
      const hasDefaults = gearSlots.every(slot => levelsBySlot[slot] && levelsBySlot[slot].every(v => v > 0));
      if (hasDefaults && onChange) {
        onChange(levelsBySlot as any);
      }
    }
  }, [opts, levelsBySlot, onChange, value]);

  // ensure default [0,0,0] arrays for each slot
  React.useEffect(() => {
    setLevelsBySlot((prev) => {
      const next = { ...prev } as Record<string, [number, number, number]>;
      gearSlots.forEach((s) => {
        if (!next[s]) next[s] = [0, 0, 0];
      });
      // Removed onChange call to prevent setState during render
      return next;
    });
  }, []);

  // Default charm levels to highest available level if empty
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
      // Removed onChange call to prevent setState during render
      return changed ? next : prev;
    });
  }, [opts]);

  const recalc = React.useCallback(() => {
    const payload: Record<string, number[]> = {};
    let allFilled = true;
    gearSlots.forEach((s) => {
      const arr = levelsBySlot[s] || [0, 0, 0];
      payload[s] = arr;
      if (arr.some((v) => v <= 0)) allFilled = false;
    });
    if (!allFilled) {
      setTotals(null);
      return;
    }
    axios.post("http://localhost:8000/api/gear/chief/charms/calc", { levels_by_slot: payload })
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
        const ev = { kind: 'chief-charms-totals', side, totals: d };
        try { (global as any).onChiefGearCharms?.(ev); } catch {}
        try { (global as any).dispatchEvent?.(new CustomEvent('chief-gear-charms', { detail: ev })); } catch {}
      })
      .catch(() => setTotals(null));
  }, [levelsBySlot, side]);

  React.useEffect(() => { 
    if (opts.length > 0 && Object.keys(levelsBySlot).length > 0) {
      recalc(); 
    }
  }, [opts, levelsBySlot.Cap?.[0], levelsBySlot.Cap?.[1], levelsBySlot.Cap?.[2],
      levelsBySlot.Coat?.[0], levelsBySlot.Coat?.[1], levelsBySlot.Coat?.[2],
      levelsBySlot.Ring?.[0], levelsBySlot.Ring?.[1], levelsBySlot.Ring?.[2],
      levelsBySlot.Watch?.[0], levelsBySlot.Watch?.[1], levelsBySlot.Watch?.[2],
      levelsBySlot.Pants?.[0], levelsBySlot.Pants?.[1], levelsBySlot.Pants?.[2],
      levelsBySlot.Weapon?.[0], levelsBySlot.Weapon?.[1], levelsBySlot.Weapon?.[2]
  ]); // depend on individual indices to avoid new array references triggering

  const sideLabelStyle = side === "atk" ? styles.attackerLabel : styles.defenderLabel;
  const sidePickerStyle = side === "atk" ? styles.attackerPicker : styles.defenderPicker;

  const levels = opts.map((o) => o.level);

  return (
    <View style={styles.panel}>
      {!hideHeader && <Text style={[styles.subHeader, sideLabelStyle]}>Chief Charms</Text>}

      {gearSlots.map((slot) => (
        <View key={slot} style={styles.row}>
          <Text style={styles.label}>{slot} — 3 Charms</Text>
          <View style={styles.inlineRow}>
            {[0, 1, 2].map((idx) => (
              <View key={`${slot}-${idx}`} style={{ flex: 1 }}>
                <Text style={styles.helperText}>Charm {idx + 1}</Text>
                <Picker
                  enabled={!disabled}
                  selectedValue={(levelsBySlot[slot] || [0, 0, 0])[idx]}
                  onValueChange={(v) => {
                    const next = { ...(levelsBySlot || {}) } as Record<string, [number, number, number]>;
                    const arr = next[slot] || [0, 0, 0];
                    arr[idx] = v;
                    next[slot] = arr as [number, number, number];
                    setLevelsBySlot(next);
                    onChange?.(next as any);
                  }}
                  style={[styles.picker, sidePickerStyle]}
                >
                  {levels.map((lvl) => (
                    <PickerItem key={`${slot}-lvl-${lvl}`} label={`Level ${lvl}`} value={lvl} />
                  ))}
                </Picker>
              </View>
            ))}
          </View>
        </View>
      ))}

      {totals && (
        <View style={styles.totalBar}>
          <Text style={styles.totalText}>Lethality: {totals.leth.toFixed(2)}%</Text>
          <Text style={styles.totalText}>Health: {totals.hp.toFixed(2)}%</Text>
          <Text style={styles.totalText}>Power: {Math.round(totals.pow).toLocaleString()}</Text>
        </View>
      )}
    </View>
  );
};
