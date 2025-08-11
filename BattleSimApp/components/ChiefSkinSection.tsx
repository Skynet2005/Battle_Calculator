import React from "react";
import { Text, View, TextInput, TouchableOpacity } from "react-native";
import { ChiefSkinBonuses } from "../types";
import { styles } from "../styles";

type Side = "atk" | "def";

interface Props {
  side: Side;
  value?: ChiefSkinBonuses;
  onChange?: (bonuses: ChiefSkinBonuses) => void;
  disabled?: boolean;
}

export const ChiefSkinSection: React.FC<Props> = ({ side, value, onChange, disabled }) => {
  const [bonuses, setBonuses] = React.useState<ChiefSkinBonuses>({
    troops_lethality_pct: 0,
    troops_health_pct: 0,
    troops_defense_pct: 0,
    troops_attack_pct: 0,
  });
  
  // Separate display values to allow decimal input
  const [displayValues, setDisplayValues] = React.useState<Record<keyof ChiefSkinBonuses, string>>({
    troops_lethality_pct: "0",
    troops_health_pct: "0",
    troops_defense_pct: "0",
    troops_attack_pct: "0",
  });

  // Sync with external value
  React.useEffect(() => {
    if (value) {
      setBonuses(value);
      setDisplayValues({
        troops_lethality_pct: String(value.troops_lethality_pct),
        troops_health_pct: String(value.troops_health_pct),
        troops_defense_pct: String(value.troops_defense_pct),
        troops_attack_pct: String(value.troops_attack_pct),
      });
    }
  }, [value]);

  const updateBonus = (key: keyof ChiefSkinBonuses, v: string) => {
    setDisplayValues(prev => ({ ...prev, [key]: v }));
    if (v === "" || v === ".") return;
    const parsed = parseFloat(v);
    if (!isNaN(parsed)) {
      const numValue = Math.max(0, Math.min(150, parsed));
      if (bonuses[key] !== numValue) {
        const next = { ...bonuses, [key]: numValue };
        setBonuses(next);
        onChange?.(next);
      }
    }
  };

  const resetBonuses = () => {
    const next = { troops_lethality_pct: 0, troops_health_pct: 0, troops_defense_pct: 0, troops_attack_pct: 0 };
    setBonuses(next);
    setDisplayValues({ troops_lethality_pct: "0", troops_health_pct: "0", troops_defense_pct: "0", troops_attack_pct: "0" });
    onChange?.(next);
  };

  const maxBonuses = () => {
    const next = { troops_lethality_pct: 150, troops_health_pct: 150, troops_defense_pct: 150, troops_attack_pct: 150 };
    setBonuses(next);
    setDisplayValues({ troops_lethality_pct: "150", troops_health_pct: "150", troops_defense_pct: "150", troops_attack_pct: "150" });
    onChange?.(next);
  };

  const sideColor = side === "atk" ? styles.attackerLabel : styles.defenderLabel;
  const sidePicker = side === "atk" ? styles.attackerPicker : styles.defenderPicker;

  const Item = (label: string, key: keyof ChiefSkinBonuses) => (
    <View style={{ flex: 1 }}>
      <Text style={[styles.label, sideColor]}>{label}</Text>
      <TextInput
        style={[styles.input, sidePicker]}
        value={displayValues[key]}
        onChangeText={(v) => updateBonus(key, v)}
        keyboardType="numeric"
        placeholder="0"
        placeholderTextColor="#7B8794"
        editable={!disabled}
      />
      <Text style={styles.helperText}>%</Text>
    </View>
  );

  return (
    <View style={styles.panel}>
      <View style={[styles.row, styles.inlineRow]}>
        {Item("Troops Attack", "troops_attack_pct")}
        {Item("Troops Defense", "troops_defense_pct")}
      </View>
      <View style={[styles.row, styles.inlineRow]}>
        {Item("Troops Lethality", "troops_lethality_pct")}
        {Item("Troops Health", "troops_health_pct")}
      </View>

      <View style={[styles.inlineRow, { marginTop: 8 }]}>
        <TouchableOpacity onPress={resetBonuses} style={styles.miniButton}>
          <Text style={styles.miniButtonText}>Reset</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={maxBonuses} style={styles.miniButton}>
          <Text style={styles.miniButtonText}>Max</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};
