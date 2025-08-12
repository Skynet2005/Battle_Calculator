import React from "react";
import axios from "axios";
import { View, Text, TextInput, TouchableOpacity } from "react-native";
import { styles } from "../styles";
import type { HeroGearSelectionByClass, HeroGearClassSelection, HeroGearPieceSelection, StackMode } from "../types";

type Props = {
  side: "atk" | "def";
  disabled?: boolean;
  value?: HeroGearSelectionByClass | null;
  onChange?: (v: HeroGearSelectionByClass) => void;
  onlyClass?: "Infantry" | "Lancer" | "Marksman";
};

const defaultPiece = (type: "Infantry" | "Lancer" | "Marksman"): HeroGearPieceSelection => ({
  type,
  level: 200,
  essence_level: 20,
});

const emptySelection: HeroGearSelectionByClass = {
  Infantry: { goggles: defaultPiece("Infantry"), boot: defaultPiece("Infantry"), glove: defaultPiece("Infantry"), belt: defaultPiece("Infantry") },
  Lancer: { goggles: defaultPiece("Lancer"), boot: defaultPiece("Lancer"), glove: defaultPiece("Lancer"), belt: defaultPiece("Lancer") },
  Marksman: { goggles: defaultPiece("Marksman"), boot: defaultPiece("Marksman"), glove: defaultPiece("Marksman"), belt: defaultPiece("Marksman") },
};

export const HeroGearSection: React.FC<Props> = ({ side, disabled, value, onChange, onlyClass }) => {
  const [sel, setSel] = React.useState<HeroGearSelectionByClass>(value || emptySelection);
  const [totals, setTotals] = React.useState<any | null>(null);

  // sync external value
  React.useEffect(() => {
    if (value) setSel(value);
  }, [value]);

  const resetAll = () => {
    setSel(emptySelection);
    onChange?.(emptySelection);
    setTotals(null);
  };

  const recalc = React.useCallback(() => {
    const payload = {
      infantry: sel.Infantry,
      lancer: sel.Lancer,
      marksman: sel.Marksman,
    } as any;
    axios
      .post("http://localhost:8000/api/hero-gear/calc", payload)
      .then((r) => {
        setTotals(r.data);
        const ev = { kind: "hero-gear-totals", side, totals: r.data };
        try { (global as any).onChiefGearCharms?.(ev); } catch {}
        try { (global as any).dispatchEvent?.(new CustomEvent("chief-gear-charms", { detail: ev })); } catch {}
      })
      .catch(() => setTotals(null));
  }, [sel, side]);

  React.useEffect(() => { 
    if (Object.keys(sel).length > 0) {
      recalc(); 
    }
  }, [sel.Infantry, sel.Lancer, sel.Marksman]); // Use specific properties instead of entire object

  const sideLabelStyle = side === "atk" ? styles.attackerLabel : styles.defenderLabel;
  const sidePickerStyle = side === "atk" ? styles.attackerPicker : styles.defenderPicker;

  return (
    <View style={styles.panel}>
      <Text style={[styles.subHeader, sideLabelStyle]}>Hero Gear{onlyClass ? ` — ${onlyClass}` : ""}</Text>

      {(((onlyClass ? [onlyClass] : ["Infantry","Lancer","Marksman"]) as unknown) as ("Infantry"|"Lancer"|"Marksman")[]).map((cls) => (
        <View key={`${side}-gear-${cls}`}>
          <Text style={[styles.label, sideLabelStyle]}>{cls}</Text>
          {(Object.keys(sel[cls]) as (keyof HeroGearClassSelection)[]).map((piece) => (
            <View key={`${side}-${cls}-${piece}`} style={[styles.card]}>
              <Text style={styles.label}>{piece.toUpperCase()}</Text>
              <View style={styles.inlineRow}>
                <View style={{ flex: 1 }}>
                  <Text style={styles.helperText}>Level (0–200)</Text>
                  <TextInput
                    style={[styles.input, sidePickerStyle]}
                    editable={!disabled}
                    keyboardType="number-pad"
                    value={String((sel[cls] as any)[piece].level ?? 0)}
                    onChangeText={(v) => {
                      const lv = Math.max(0, Math.min(200, parseInt(v || "0", 10) || 0));
                      const next = { ...sel } as any;
                      next[cls] = { ...next[cls] };
                      next[cls][piece] = { ...next[cls][piece], level: lv };
                      setSel(next);
                      onChange?.(next);
                    }}
                    placeholder="0"
                    placeholderTextColor="#7B8794"
                  />
                </View>
                <View style={{ flex: 1 }}>
                  <Text style={styles.helperText}>Essence (0–20)</Text>
                  <TextInput
                    style={[styles.input, sidePickerStyle]}
                    editable={!disabled}
                    keyboardType="number-pad"
                    value={String((sel[cls] as any)[piece].essence_level ?? 0)}
                    onChangeText={(v) => {
                      const es = Math.max(0, Math.min(20, parseInt(v || "0", 10) || 0));
                      const next = { ...sel } as any;
                      next[cls] = { ...next[cls] };
                      next[cls][piece] = { ...next[cls][piece], essence_level: es };
                      setSel(next);
                      onChange?.(next);
                    }}
                    placeholder="0"
                    placeholderTextColor="#7B8794"
                  />
                </View>
              </View>
            </View>
          ))}
        </View>
      ))}

      <View style={[styles.inlineRow, { marginTop: 8 }]}>
        <TouchableOpacity onPress={resetAll} style={styles.miniButton} disabled={!!disabled}>
          <Text style={styles.miniButtonText}>Reset All</Text>
        </TouchableOpacity>
      </View>

      {totals && (
        <View style={styles.totalBar}>
          <Text style={styles.totalText}>Inf Leth: {Number(totals.infantry_lethality_pct).toFixed(2)}%</Text>
          <Text style={styles.totalText}>Lan Leth: {Number(totals.lancer_lethality_pct).toFixed(2)}%</Text>
          <Text style={styles.totalText}>MM Leth: {Number(totals.marksman_lethality_pct).toFixed(2)}%</Text>
        </View>
      )}
    </View>
  );
};


