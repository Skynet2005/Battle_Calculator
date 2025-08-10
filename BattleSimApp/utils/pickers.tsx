import React from "react";
import { Picker } from "@react-native-picker/picker";

type PickerItem = { label: string; value: string | number; color?: string; enabled?: boolean };

interface SimplePickerProps {
  items: PickerItem[];
  selectedValue: string | number;
  onChange: (v: any) => void;
  style?: any;
  dropdownIconColor?: string;
  enabled?: boolean;
}

export const SimplePicker: React.FC<SimplePickerProps> = ({ items, selectedValue, onChange, style, dropdownIconColor = "#FFFFFF", enabled = true }) => {
  return (
    <Picker selectedValue={selectedValue} onValueChange={onChange} style={style} dropdownIconColor={dropdownIconColor} enabled={enabled}>
      {items.map((it, i) => (
        <Picker.Item key={`${String(it.value)}-${i}`} label={it.label} value={it.value} color={it.color ?? "#FFFFFF"} enabled={it.enabled ?? true} />
      ))}
    </Picker>
  );
};


