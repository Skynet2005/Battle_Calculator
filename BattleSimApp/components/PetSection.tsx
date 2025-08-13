import React from "react";
import { View, Text, TextInput, Switch } from "react-native";
import { styles } from "../styles";
import { Picker, PickerItem } from "./WebCompatiblePicker";

type Class = "Infantry" | "Lancer" | "Marksman";

export type PetBaseStats = {
  troops_attack_pct: number;
  troops_defense_pct: number;
  infantry_lethality_pct: number;
  infantry_health_pct: number;
  lancer_lethality_pct: number;
  lancer_health_pct: number;
  marksman_lethality_pct: number;
  marksman_health_pct: number;
};

export type PetName = "Cave Lion" | "Mammoth" | "Frost Gorilla" | "Saber Tooth Tiger" | "Titan Roc" | "Snow Leopard";

export type PetEntry = {
  name: PetName;
  base: PetBaseStats;
  level: number; // 1-10
  enabled: boolean;
};

type Props = {
  side: "atk" | "def";
  disabled?: boolean;
  pets: PetEntry[];
  onChange: (pets: PetEntry[]) => void;
};

const PctField: React.FC<{ label: string; value: number; onChange: (n: number) => void; disabled?: boolean }> = ({ label, value, onChange, disabled }) => {
  const [text, setText] = React.useState<string>(String(value ?? 0));
  React.useEffect(() => {
    // Sync when external value changes
    setText(String(value ?? 0));
  }, [value]);

  const onText = (t: string) => {
    // Allow intermediate states like "", "-", "1." while typing
    const cleaned = t.replace(/[^0-9.\-]/g, "");
    if (!/^\-?\d*\.?\d*$/.test(cleaned)) {
      setText(cleaned);
      return;
    }
    setText(cleaned);
    // Commit only when it parses to a finite number and not an intermediate state
    if (cleaned !== "" && cleaned !== "-" && !cleaned.endsWith(".")) {
      const num = parseFloat(cleaned);
      if (isFinite(num)) {
        const clamped = Math.max(-9999, Math.min(9999, num));
        onChange(clamped);
      }
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

const PETS: PetName[] = ["Titan Roc", "Snow Leopard", "Cave Lion", "Saber Tooth Tiger", "Mammoth", "Frost Gorilla"];

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

export const PetSection: React.FC<Props> = ({ side, disabled, pets, onChange }) => {
  const sideLabelStyle = side === "atk" ? styles.attackerLabel : styles.defenderLabel;
  const sidePickerStyle = side === "atk" ? styles.attackerPicker : styles.defenderPicker;

  return (
    <View style={styles.panel}>
      <Text style={[styles.subHeader, sideLabelStyle]}>Pet Bonuses</Text>

      {PETS.map((petName) => {
        const idx = pets.findIndex((p) => p.name === petName);
        const entry = idx >= 0 ? pets[idx] : { name: petName, base: emptyBase(), level: 1, enabled: false } as PetEntry;
        const setEntry = (next: Partial<PetEntry>) => {
          const list = [...pets];
          const i = idx >= 0 ? idx : list.length;
          if (idx < 0) list.push(entry);
          list[i] = { ...entry, ...next, base: { ...entry.base, ...(next.base || {}) } };
          onChange(list);
        };
        const setBase = (k: keyof PetBaseStats, v: number) => setEntry({ base: { ...entry.base, [k]: v } });
        return (
          <View key={`${side}-pet-${petName}`} style={[styles.card, { marginBottom: 8 }]}>
            <View style={{ flexDirection: "row", alignItems: "center", justifyContent: "space-between" }}>
              <Text style={[styles.label, sideLabelStyle]}>{petName}</Text>
              <View style={{ flexDirection: "row", alignItems: "center" }}>
                <Text style={styles.helperText}>Level</Text>
                <Picker
                  enabled={!disabled}
                  selectedValue={entry.level}
                  onValueChange={(v) => setEntry({ level: Number(v) })}
                  style={[styles.picker, { width: 90 }]}
                >
                  {[1,2,3,4,5,6,7,8,9,10].map((n) => (
                    <PickerItem key={`${petName}-lv-${n}`} label={`${n}`} value={n} />
                  ))}
                </Picker>
                <Text style={[styles.helperText, { marginLeft: 12 }]}>Active</Text>
                <Switch value={!!entry.enabled} onValueChange={(v) => setEntry({ enabled: v })} disabled={disabled} />
              </View>
            </View>
            <View style={styles.row}>
              <PctField label="Troops Attack %" value={entry.base.troops_attack_pct} onChange={(v) => setBase("troops_attack_pct", v)} disabled={disabled} />
              <PctField label="Troops Defense %" value={entry.base.troops_defense_pct} onChange={(v) => setBase("troops_defense_pct", v)} disabled={disabled} />
            </View>
            <View style={styles.row}>
              <PctField label="Infantry Lethality %" value={entry.base.infantry_lethality_pct} onChange={(v) => setBase("infantry_lethality_pct", v)} disabled={disabled} />
              <PctField label="Infantry Health %" value={entry.base.infantry_health_pct} onChange={(v) => setBase("infantry_health_pct", v)} disabled={disabled} />
            </View>
            <View style={styles.row}>
              <PctField label="Lancer Lethality %" value={entry.base.lancer_lethality_pct} onChange={(v) => setBase("lancer_lethality_pct", v)} disabled={disabled} />
              <PctField label="Lancer Health %" value={entry.base.lancer_health_pct} onChange={(v) => setBase("lancer_health_pct", v)} disabled={disabled} />
            </View>
            <View style={styles.row}>
              <PctField label="Marksman Lethality %" value={entry.base.marksman_lethality_pct} onChange={(v) => setBase("marksman_lethality_pct", v)} disabled={disabled} />
              <PctField label="Marksman Health %" value={entry.base.marksman_health_pct} onChange={(v) => setBase("marksman_health_pct", v)} disabled={disabled} />
            </View>
          </View>
        );
      })}
    </View>
  );
};


