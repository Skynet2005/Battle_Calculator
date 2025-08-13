import React from "react";
import { View, Text, TextInput } from "react-native";
import { styles } from "../styles";

export type WarAcademyBonuses = {
  infantry_attack_pct: number;
  infantry_defense_pct: number;
  infantry_lethality_pct: number;
  infantry_health_pct: number;
  lancer_attack_pct: number;
  lancer_defense_pct: number;
  lancer_lethality_pct: number;
  lancer_health_pct: number;
  marksman_attack_pct: number;
  marksman_defense_pct: number;
  marksman_lethality_pct: number;
  marksman_health_pct: number;
};

type Props = {
  side: "atk" | "def";
  disabled?: boolean;
  value?: WarAcademyBonuses;
  onChange?: (v: WarAcademyBonuses) => void;
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

const empty: WarAcademyBonuses = {
  infantry_attack_pct: 0,
  infantry_defense_pct: 0,
  infantry_lethality_pct: 0,
  infantry_health_pct: 0,
  lancer_attack_pct: 0,
  lancer_defense_pct: 0,
  lancer_lethality_pct: 0,
  lancer_health_pct: 0,
  marksman_attack_pct: 0,
  marksman_defense_pct: 0,
  marksman_lethality_pct: 0,
  marksman_health_pct: 0,
};

export const WarAcademySection: React.FC<Props> = ({ side, disabled, value, onChange }) => {
  const sideLabelStyle = side === "atk" ? styles.attackerLabel : styles.defenderLabel;
  const val = value || empty;
  const setVal = (k: keyof WarAcademyBonuses, v: number) => onChange && onChange({ ...val, [k]: v });

  const renderClass = (cls: "Infantry" | "Lancer" | "Marksman") => {
    const key = cls.toLowerCase();
    return (
      <View key={`wa-${cls}`} style={[styles.card, { marginBottom: 8 }]}>
        <Text style={[styles.label, sideLabelStyle]}>{cls}</Text>
        <View style={styles.row}>
          <PctField label="Attack %" value={(val as any)[`${key}_attack_pct`]} onChange={(v)=> setVal(`${key}_attack_pct` as any, v)} disabled={disabled} />
          <PctField label="Defense %" value={(val as any)[`${key}_defense_pct`]} onChange={(v)=> setVal(`${key}_defense_pct` as any, v)} disabled={disabled} />
        </View>
        <View style={styles.row}>
          <PctField label="Lethality %" value={(val as any)[`${key}_lethality_pct`]} onChange={(v)=> setVal(`${key}_lethality_pct` as any, v)} disabled={disabled} />
          <PctField label="Health %" value={(val as any)[`${key}_health_pct`]} onChange={(v)=> setVal(`${key}_health_pct` as any, v)} disabled={disabled} />
        </View>
      </View>
    );
  };

  return (
    <View style={styles.panel}>
      <Text style={[styles.subHeader, sideLabelStyle]}>War Academy Bonuses</Text>
      {renderClass("Infantry")}
      {renderClass("Lancer")}
      {renderClass("Marksman")}
    </View>
  );
};


