import React from "react";
import axios from "axios";
import { Picker } from "@react-native-picker/picker";
import { Text, View } from "react-native";
import { styles } from "../../styles";
import type { ChiefCharmOption } from "../../types";

type GearProps = { side: "atk" | "def"; hideHeader?: boolean; disabled?: boolean };

const gearSlots: Array<"Cap" | "Coat" | "Ring" | "Watch" | "Pants" | "Weapon"> = [
  "Cap",
  "Coat",
  "Ring",
  "Watch",
  "Pants",
  "Weapon",
];

export const ChiefCharmsSection: React.FC<GearProps> = ({ side, hideHeader, disabled }) => {
  // Created Logic for review: 3 charms per slot; user selects levels; totals recompute
  const [opts, setOpts] = React.useState<ChiefCharmOption[]>([]);
  const [levelsBySlot, setLevelsBySlot] = React.useState<Record<string, [number, number, number]>>({});
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

  // Default charm levels to the last (highest) available level when empty
  React.useEffect(() => {
    setLevelsBySlot((prev) => {
      const next = { ...prev } as Record<string, [number, number, number]>;
      let changed = false;
      const last = opts.length ? opts[opts.length - 1].level : 0;
      gearSlots.forEach((s) => {
        const arr = next[s] || [0, 0, 0];
        for (let i = 0; i < 3; i++) {
          if (!arr[i] || arr[i] <= 0) {
            arr[i] = last;
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
      })
      .catch(() => setTotals(null));
  }, [levelsBySlot, side]);

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
                enabled={!disabled}
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


