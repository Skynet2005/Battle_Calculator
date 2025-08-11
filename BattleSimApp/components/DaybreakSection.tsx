import React from "react";
import { View, Text, TextInput, TouchableOpacity, Platform } from "react-native";
import { styles } from "../styles";
import type { DaybreakBonuses } from "../types";

type Props = {
  side: "atk" | "def";
  disabled?: boolean;
  value?: DaybreakBonuses;
  onChange?: (bonuses: DaybreakBonuses) => void;
};

const defaultBonuses: DaybreakBonuses = {
  infantry_attack_pct: 0,
  infantry_defense_pct: 0,
  lancer_attack_pct: 0,
  lancer_defense_pct: 0,
  marksman_attack_pct: 0,
  marksman_defense_pct: 0,
  troops_attack_pct: 0,
  troops_defense_pct: 0,
  troops_lethality_pct: 0,
  troops_health_pct: 0,
};

export const DaybreakSection: React.FC<Props> = ({ side, disabled, value, onChange }) => {
  const [bonuses, setBonuses] = React.useState<DaybreakBonuses>(value || defaultBonuses);

  // Keep raw input strings so decimals like "12." are preserved while typing
  const toInputMap = (b: DaybreakBonuses) => ({
    infantry_attack_pct: String(b.infantry_attack_pct ?? 0),
    infantry_defense_pct: String(b.infantry_defense_pct ?? 0),
    lancer_attack_pct: String(b.lancer_attack_pct ?? 0),
    lancer_defense_pct: String(b.lancer_defense_pct ?? 0),
    marksman_attack_pct: String(b.marksman_attack_pct ?? 0),
    marksman_defense_pct: String(b.marksman_defense_pct ?? 0),
    troops_attack_pct: String(b.troops_attack_pct ?? 0),
    troops_defense_pct: String(b.troops_defense_pct ?? 0),
    troops_lethality_pct: String(b.troops_lethality_pct ?? 0),
    troops_health_pct: String(b.troops_health_pct ?? 0),
  });

  const [inputs, setInputs] = React.useState<Record<keyof DaybreakBonuses, string>>(toInputMap(value || defaultBonuses));

  // Sync external value
  React.useEffect(() => {
    if (value) {
      setBonuses(value);
      setInputs(toInputMap(value));
    }
  }, [value]);

  const resetAll = () => {
    const reset = { ...defaultBonuses };
    setBonuses(reset);
    setInputs(toInputMap(reset));
    onChange?.(reset);
  };

  const commitIfParsable = (key: keyof DaybreakBonuses) => {
    const text = inputs[key];
    const parsed = parseFloat((text || '').replace(',', '.'));
    if (Number.isFinite(parsed)) {
      const next = { ...bonuses, [key]: parsed } as DaybreakBonuses;
      setBonuses(next);
      onChange?.(next);
    }
  };

  const updateBonus = (key: keyof DaybreakBonuses, value: string) => {
    // Normalize decimal separator and keep raw string for display
    const normalized = value.replace(',', '.');
    setInputs(prev => ({ ...prev, [key]: normalized }));
    // If mid-entry (empty or trailing decimal), don't push to parent to avoid wiping the dot
    if (normalized === '' || normalized === '-' || normalized.endsWith('.')) {
      return;
    }
    const parsed = parseFloat(normalized);
    if (!Number.isFinite(parsed)) {
      return;
    }
    const next = { ...bonuses, [key]: parsed } as DaybreakBonuses;
    setBonuses(next);
    onChange?.(next);
  };

  const sideLabelStyle = side === "atk" ? styles.attackerLabel : styles.defenderLabel;
  const sideInputStyle = side === "atk" ? styles.attackerPicker : styles.defenderPicker;

  // Ensure decimals are allowed across platforms (web/mobile)
  const keyboardTypeValue = Platform.OS === 'web' ? 'default' : 'decimal-pad';
  const webInputModeProps = Platform.OS === 'web' ? ({ inputMode: 'decimal' } as any) : undefined;

  const handleKeyPress = (e: any, field: keyof DaybreakBonuses) => {
    if (Platform.OS !== 'web') return;
    const key = e?.nativeEvent?.key;
    if (key === '.' || key === ',') {
      e?.preventDefault?.();
      const next = (inputs[field] || '') + key;
      updateBonus(field, next);
    }
  };

  return (
    <View style={styles.panel}>
      <Text style={[styles.subHeader, sideLabelStyle]}>Daybreak Island Bonuses</Text>
      
      <View style={styles.row}>
        <Text style={styles.label}>Infantry Attack (%)</Text>
        <TextInput
          style={[styles.input, sideInputStyle]}
          editable={!disabled}
          keyboardType={keyboardTypeValue as any}
          {...webInputModeProps}
          value={inputs.infantry_attack_pct}
          onChangeText={(v) => updateBonus("infantry_attack_pct", v)}
          onKeyPress={(e) => handleKeyPress(e, 'infantry_attack_pct')}
          onBlur={() => commitIfParsable("infantry_attack_pct")}
          placeholder="0"
          placeholderTextColor="#7B8794"
        />
      </View>

      <View style={styles.row}>
        <Text style={styles.label}>Infantry Defense (%)</Text>
        <TextInput
          style={[styles.input, sideInputStyle]}
          editable={!disabled}
          keyboardType={keyboardTypeValue as any}
          {...webInputModeProps}
          value={inputs.infantry_defense_pct}
          onChangeText={(v) => updateBonus("infantry_defense_pct", v)}
          onKeyPress={(e) => handleKeyPress(e, 'infantry_defense_pct')}
          onBlur={() => commitIfParsable("infantry_defense_pct")}
          placeholder="0"
          placeholderTextColor="#7B8794"
        />
      </View>

      <View style={styles.row}>
        <Text style={styles.label}>Lancer Attack (%)</Text>
        <TextInput
          style={[styles.input, sideInputStyle]}
          editable={!disabled}
          keyboardType={keyboardTypeValue as any}
          {...webInputModeProps}
          value={inputs.lancer_attack_pct}
          onChangeText={(v) => updateBonus("lancer_attack_pct", v)}
          onKeyPress={(e) => handleKeyPress(e, 'lancer_attack_pct')}
          onBlur={() => commitIfParsable("lancer_attack_pct")}
          placeholder="0"
          placeholderTextColor="#7B8794"
        />
      </View>

      <View style={styles.row}>
        <Text style={styles.label}>Lancer Defense (%)</Text>
        <TextInput
          style={[styles.input, sideInputStyle]}
          editable={!disabled}
          keyboardType={keyboardTypeValue as any}
          {...webInputModeProps}
          value={inputs.lancer_defense_pct}
          onChangeText={(v) => updateBonus("lancer_defense_pct", v)}
          onKeyPress={(e) => handleKeyPress(e, 'lancer_defense_pct')}
          onBlur={() => commitIfParsable("lancer_defense_pct")}
          placeholder="0"
          placeholderTextColor="#7B8794"
        />
      </View>

      <View style={styles.row}>
        <Text style={styles.label}>Marksman Attack (%)</Text>
        <TextInput
          style={[styles.input, sideInputStyle]}
          editable={!disabled}
          keyboardType={keyboardTypeValue as any}
          {...webInputModeProps}
          value={inputs.marksman_attack_pct}
          onChangeText={(v) => updateBonus("marksman_attack_pct", v)}
          onKeyPress={(e) => handleKeyPress(e, 'marksman_attack_pct')}
          onBlur={() => commitIfParsable("marksman_attack_pct")}
          placeholder="0"
          placeholderTextColor="#7B8794"
        />
      </View>

      <View style={styles.row}>
        <Text style={styles.label}>Marksman Defense (%)</Text>
        <TextInput
          style={[styles.input, sideInputStyle]}
          editable={!disabled}
          keyboardType={keyboardTypeValue as any}
          {...webInputModeProps}
          value={inputs.marksman_defense_pct}
          onChangeText={(v) => updateBonus("marksman_defense_pct", v)}
          onKeyPress={(e) => handleKeyPress(e, 'marksman_defense_pct')}
          onBlur={() => commitIfParsable("marksman_defense_pct")}
          placeholder="0"
          placeholderTextColor="#7B8794"
        />
      </View>

      <View style={styles.row}>
        <Text style={styles.label}>Troops Attack (%)</Text>
        <TextInput
          style={[styles.input, sideInputStyle]}
          editable={!disabled}
          keyboardType={keyboardTypeValue as any}
          {...webInputModeProps}
          value={inputs.troops_attack_pct}
          onChangeText={(v) => updateBonus("troops_attack_pct", v)}
          onKeyPress={(e) => handleKeyPress(e, 'troops_attack_pct')}
          onBlur={() => commitIfParsable("troops_attack_pct")}
          placeholder="0"
          placeholderTextColor="#7B8794"
        />
      </View>

      <View style={styles.row}>
        <Text style={styles.label}>Troops Defense (%)</Text>
        <TextInput
          style={[styles.input, sideInputStyle]}
          editable={!disabled}
          keyboardType={keyboardTypeValue as any}
          {...webInputModeProps}
          value={inputs.troops_defense_pct}
          onChangeText={(v) => updateBonus("troops_defense_pct", v)}
          onKeyPress={(e) => handleKeyPress(e, 'troops_defense_pct')}
          onBlur={() => commitIfParsable("troops_defense_pct")}
          placeholder="0"
          placeholderTextColor="#7B8794"
        />
      </View>

      <View style={styles.row}>
        <Text style={styles.label}>Troops Lethality (%)</Text>
        <TextInput
          style={[styles.input, sideInputStyle]}
          editable={!disabled}
          keyboardType={keyboardTypeValue as any}
          {...webInputModeProps}
          value={inputs.troops_lethality_pct}
          onChangeText={(v) => updateBonus("troops_lethality_pct", v)}
          onKeyPress={(e) => handleKeyPress(e, 'troops_lethality_pct')}
          onBlur={() => commitIfParsable("troops_lethality_pct")}
          placeholder="0"
          placeholderTextColor="#7B8794"
        />
      </View>

      <View style={styles.row}>
        <Text style={styles.label}>Troops Health (%)</Text>
        <TextInput
          style={[styles.input, sideInputStyle]}
          editable={!disabled}
          keyboardType={keyboardTypeValue as any}
          {...webInputModeProps}
          value={inputs.troops_health_pct}
          onChangeText={(v) => updateBonus("troops_health_pct", v)}
          onKeyPress={(e) => handleKeyPress(e, 'troops_health_pct')}
          onBlur={() => commitIfParsable("troops_health_pct")}
          placeholder="0"
          placeholderTextColor="#7B8794"
        />
      </View>

      <View style={[styles.inlineRow, { marginTop: 8 }]}>
        <TouchableOpacity onPress={resetAll} style={styles.miniButton} disabled={!!disabled}>
          <Text style={styles.miniButtonText}>Reset All</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};
