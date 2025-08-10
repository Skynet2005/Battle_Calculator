import React from "react";
import { Picker } from "@react-native-picker/picker";
import { Text, View } from "react-native";
import { Hero } from "../types";
import { styles } from "../styles";
import { SimplePicker } from "../utils/pickers";

interface Props {
  side: "atk" | "def";
  idx: number;
  heroes: Hero[];
  selected: string;
  onChange: (name: string) => void;
  disabled?: boolean;
}

export const JoinerRow: React.FC<Props> = ({ side, idx, heroes, selected, onChange, disabled }) => {
  const heroItems = React.useMemo(() => {
    const list = [...heroes].sort((a, b) =>
      a.generation === b.generation ? a.name.localeCompare(b.name) : a.generation - b.generation
    );
    let lastGen: number | null = null;
    return list.flatMap((h) => {
      const arr: React.ReactElement[] = [];
      if (h.generation !== lastGen) {
        arr.push(
          <Picker.Item
            key={`hdr-${side}-joiner-${idx}-${h.generation}`}
            label={`-- Gen ${h.generation} --`}
            value=""
            enabled={false}
            color="#FFFFFF"
          />
        );
        lastGen = h.generation;
      }
      arr.push(
        <Picker.Item
          key={`${side}-joiner-${idx}-${h.name}`}
          label={h.name}
          value={h.name}
          color="#FFFFFF"
        />
      );
      return arr;
    });
  }, [heroes, idx, side]);

  const col = side === "atk" ? styles.attackerLabel : styles.defenderLabel;
  const pickStyle = side === "atk" ? styles.attackerPicker : styles.defenderPicker;

  const pickerItems = React.useMemo(() => {
    const items: { label: string; value: string; color?: string; enabled?: boolean }[] = [
      { label: "None", value: "", color: "#FFFFFF" },
    ];
    let lastGen: number | null = null;
    const list = [...heroes].sort((a, b) =>
      a.generation === b.generation ? a.name.localeCompare(b.name) : a.generation - b.generation
    );
    list.forEach((h) => {
      if (h.generation !== lastGen) {
        items.push({ label: `-- Gen ${h.generation} --`, value: `__gen-${h.generation}`, color: "#FFFFFF", enabled: false });
        lastGen = h.generation;
      }
      items.push({ label: h.name, value: h.name, color: "#FFFFFF" });
    });
    return items;
  }, [heroes]);

  return (
    <View style={styles.row}>
      <Text style={[styles.label, col]}>
        Joiner {idx + 1} Hero {side === "atk" ? "(Attacker)" : "(Defender)"}
      </Text>
      <SimplePicker
        items={pickerItems}
        selectedValue={selected}
        onChange={(v) => onChange(v)}
        style={[styles.picker, pickStyle]}
        dropdownIconColor="#FFFFFF"
        enabled={!disabled}
      />
    </View>
  );
};

