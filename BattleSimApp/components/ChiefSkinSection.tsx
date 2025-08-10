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

  const updateBonus = (key: keyof ChiefSkinBonuses, value: string) => {
    // Update display value immediately for responsive typing
    setDisplayValues(prev => ({ ...prev, [key]: value }));
    
    // Handle empty or just decimal point
    if (value === '' || value === '.') {
      return; // Don't update bonuses yet, just update display
    }
    
    const parsed = parseFloat(value);
    if (!isNaN(parsed)) {
      // Clamp the actual value
      const numValue = Math.max(0, Math.min(150, parsed));
      
      // Only update bonuses if the value actually changed
      if (bonuses[key] !== numValue) {
        const newBonuses = { ...bonuses, [key]: numValue };
        setBonuses(newBonuses);
        if (onChange) {
          onChange(newBonuses);
        }
      }
    }
  };

  const resetBonuses = () => {
    const newBonuses = {
      troops_lethality_pct: 0,
      troops_health_pct: 0,
      troops_defense_pct: 0,
      troops_attack_pct: 0,
    };
    setBonuses(newBonuses);
    setDisplayValues({
      troops_lethality_pct: "0",
      troops_health_pct: "0",
      troops_defense_pct: "0",
      troops_attack_pct: "0",
    });
    if (onChange) {
      onChange(newBonuses);
    }
  };

  const maxBonuses = () => {
    const newBonuses = {
      troops_lethality_pct: 150,
      troops_health_pct: 150,
      troops_defense_pct: 150,
      troops_attack_pct: 150,
    };
    setBonuses(newBonuses);
    setDisplayValues({
      troops_lethality_pct: "150",
      troops_health_pct: "150",
      troops_defense_pct: "150",
      troops_attack_pct: "150",
    });
    if (onChange) {
      onChange(newBonuses);
    }
  };

  const sideColor = side === "atk" ? styles.attackerLabel : styles.defenderLabel;
  const sidePicker = side === "atk" ? styles.attackerPicker : styles.defenderPicker;

  return (
    <View style={styles.panel}>
      <View style={styles.sectionHeaderRow}>
        <Text style={[styles.subHeader, sideColor]}>Chief Skin Bonuses</Text>
        <View style={styles.pill}>
          <Text style={styles.pillText}>Max 150% per stat</Text>
        </View>
      </View>
      
      <View style={[styles.row, styles.inlineRow]}>
        <View style={styles.halfCol}>
          <Text style={[styles.label, sideColor]}>Troops Attack</Text>
          <TextInput
            style={[styles.input, sidePicker]}
            value={displayValues.troops_attack_pct}
            onChangeText={(v) => updateBonus('troops_attack_pct', v)}
            keyboardType="numeric"
            placeholder="0"
            placeholderTextColor="#7B8794"
            editable={!disabled}
          />
          <Text style={[styles.helperText, styles.helperTextOk]}>%</Text>
        </View>
        
        <View style={styles.halfCol}>
          <Text style={[styles.label, sideColor]}>Troops Defense</Text>
          <TextInput
            style={[styles.input, sidePicker]}
            value={displayValues.troops_defense_pct}
            onChangeText={(v) => updateBonus('troops_defense_pct', v)}
            keyboardType="numeric"
            placeholder="0"
            placeholderTextColor="#7B8794"
            editable={!disabled}
          />
          <Text style={[styles.helperText, styles.helperTextOk]}>%</Text>
        </View>
      </View>
      
      <View style={[styles.row, styles.inlineRow]}>
        <View style={styles.halfCol}>
          <Text style={[styles.label, sideColor]}>Troops Lethality</Text>
          <TextInput
            style={[styles.input, sidePicker]}
            value={displayValues.troops_lethality_pct}
            onChangeText={(v) => updateBonus('troops_lethality_pct', v)}
            keyboardType="numeric"
            placeholder="0"
            placeholderTextColor="#7B8794"
            editable={!disabled}
          />
          <Text style={[styles.helperText, styles.helperTextOk]}>%</Text>
        </View>
        
        <View style={styles.halfCol}>
          <Text style={[styles.label, sideColor]}>Troops Health</Text>
          <TextInput
            style={[styles.input, sidePicker]}
            value={displayValues.troops_health_pct}
            onChangeText={(v) => updateBonus('troops_health_pct', v)}
            keyboardType="numeric"
            placeholder="0"
            placeholderTextColor="#7B8794"
            editable={!disabled}
          />
          <Text style={[styles.helperText, styles.helperTextOk]}>%</Text>
        </View>
      </View>

      <View style={styles.progressBar}>
        <View 
          style={[
            styles.progressFill, 
            { 
              width: `${Math.min(100, (Object.values(bonuses).reduce((a, b) => a + b, 0) / 600) * 100)}%` 
            }
          ]} 
        />
      </View>

      <View style={styles.helperActionsRow}>
        <TouchableOpacity onPress={maxBonuses} disabled={disabled}>
          <Text style={styles.linkText}>Max All (150%)</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={resetBonuses} disabled={disabled}>
          <Text style={styles.linkTextDanger}>Reset All</Text>
        </TouchableOpacity>
      </View>

      <Text style={[styles.helperText, styles.helperTextWarn, {textAlign: 'center', marginTop: 12}]}>
        These bonuses apply to all troop types (Infantry, Lancer, Marksman)
      </Text>
    </View>
  );
};
