import React from "react";
import { View, Text, TextInput } from "react-native";
import { styles } from "../styles";
import type { PetBaseStats } from "./PetSection";

export type BasePetEntry = {
  name: string;
  base: PetBaseStats;
};

type Props = {
  side: "atk" | "def";
  disabled?: boolean;
  pets: BasePetEntry[];
  onChange: (pets: BasePetEntry[]) => void;
};

const PctField: React.FC<{ label: string; value: number; onChange: (n: number) => void; disabled?: boolean }> = ({ label, value, onChange, disabled }) => {
  const [text, setText] = React.useState<string>(String(value ?? 0));
  React.useEffect(() => { setText(String(value ?? 0)); }, [value]);
  const onText = (t: string) => {
    const cleaned = t.replace(/[^0-9.\-]/g, "");
    if (!/^\-?\d*\.?\d*$/.test(cleaned)) { setText(cleaned); return; }
    setText(cleaned);
    if (cleaned !== "" && cleaned !== "-" && !cleaned.endsWith(".")) {
      const num = parseFloat(cleaned);
      if (isFinite(num)) onChange(Math.max(-9999, Math.min(9999, num)));
    }
  };
  return (
    <View style={{ flex: 1, minWidth: 140, marginRight: 8 }}>
      <Text style={styles.helperText}>{label}</Text>
      <TextInput
        style={styles.input}
        editable={!disabled}
        keyboardType="decimal-pad"
        value={text}
        onChangeText={onText}
        placeholder="0"
        placeholderTextColor="#7B8794"
      />
    </View>
  );
};

const emptyBase = (): PetBaseStats => ({
  troops_attack_pct: 0,
  troops_defense_pct: 0,
  infantry_lethality_pct: 0,
  infantry_health_pct: 0,
  lancer_lethality_pct: 0,
  lancer_health_pct: 0,
  marksman_lethality_pct: 0,
  marksman_health_pct: 0,
});

export const BasePetSection: React.FC<Props> = ({ side, disabled, pets, onChange }) => {
  const sideLabelStyle = side === "atk" ? styles.attackerLabel : styles.defenderLabel;

  const setEntry = (idx: number, next: Partial<BasePetEntry>) => {
    const list = [...pets];
    const curr = list[idx] || { name: "", base: emptyBase() };
    list[idx] = { ...curr, ...next, base: { ...curr.base, ...(next.base || {}) } } as BasePetEntry;
    onChange(list);
  };

  return (
    <View style={styles.panel}>
      <Text style={[styles.subHeader, sideLabelStyle]}>Base Stat Pet Bonuses</Text>
      {pets.map((entry, i) => (
        <View key={`${side}-basepet-${entry.name}`} style={[styles.card, { marginBottom: 8 }]}> 
          <Text style={[styles.label, sideLabelStyle]}>{entry.name}</Text>
          <View style={styles.row}>
            <PctField label="Troops Attack %" value={entry.base.troops_attack_pct} onChange={(v) => setEntry(i, { base: { ...entry.base, troops_attack_pct: v } })} disabled={disabled} />
            <PctField label="Troops Defense %" value={entry.base.troops_defense_pct} onChange={(v) => setEntry(i, { base: { ...entry.base, troops_defense_pct: v } })} disabled={disabled} />
          </View>
          <View style={styles.row}>
            <PctField label="Infantry Lethality %" value={entry.base.infantry_lethality_pct} onChange={(v) => setEntry(i, { base: { ...entry.base, infantry_lethality_pct: v } })} disabled={disabled} />
            <PctField label="Infantry Health %" value={entry.base.infantry_health_pct} onChange={(v) => setEntry(i, { base: { ...entry.base, infantry_health_pct: v } })} disabled={disabled} />
          </View>
          <View style={styles.row}>
            <PctField label="Lancer Lethality %" value={entry.base.lancer_lethality_pct} onChange={(v) => setEntry(i, { base: { ...entry.base, lancer_lethality_pct: v } })} disabled={disabled} />
            <PctField label="Lancer Health %" value={entry.base.lancer_health_pct} onChange={(v) => setEntry(i, { base: { ...entry.base, lancer_health_pct: v } })} disabled={disabled} />
          </View>
          <View style={styles.row}>
            <PctField label="Marksman Lethality %" value={entry.base.marksman_lethality_pct} onChange={(v) => setEntry(i, { base: { ...entry.base, marksman_lethality_pct: v } })} disabled={disabled} />
            <PctField label="Marksman Health %" value={entry.base.marksman_health_pct} onChange={(v) => setEntry(i, { base: { ...entry.base, marksman_health_pct: v } })} disabled={disabled} />
          </View>
        </View>
      ))}
    </View>
  );
};


