import React from "react";
import axios from "axios";
import { Picker } from "@react-native-picker/picker";
import { Text, View, TouchableOpacity } from "react-native";
import { styles } from "../../styles";

type GearProps = { side: "atk" | "def"; hideHeader?: boolean; disabled?: boolean };

const gearSlots: Array<"Cap" | "Coat" | "Ring" | "Watch" | "Pants" | "Weapon"> = [
  "Cap",
  "Coat",
  "Ring",
  "Watch",
  "Pants",
  "Weapon",
];

export const ChiefGearSection: React.FC<GearProps> = ({ side, hideHeader, disabled }) => {
  // Created Logic for review: fetch options once
  const [options, setOptions] = React.useState<Record<string, { tier: string; stars: number; attackPct: number; defensePct: number; power: number }[]>>({} as any);
  const [sel, setSel] = React.useState<Record<string, { tier: string; stars: number }>>({});
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

  const tiersFor = (slot: string) => (options[slot] || []).map((o) => o.tier).filter((v, i, a) => a.indexOf(v) === i);
  const starsFor = (slot: string, tier: string) => (options[slot] || []).filter((o) => o.tier === tier).map((o) => o.stars);

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
      })
      .catch(() => setTotals(null));
  }, [sel, side]);

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

  const adjustStar = React.useCallback((slot: string, delta: number) => {
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
                    enabled={!disabled}
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
                    enabled={!disabled}
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


