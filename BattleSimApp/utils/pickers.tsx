import React from "react";
import { Picker, PickerItem } from "../components/WebCompatiblePicker";
import { Text, View } from "react-native";
import { styles } from "../styles";

type PickerItem = { label: string; value: string | number; color?: string; enabled?: boolean };

interface SimplePickerProps {
  items: PickerItem[];
  selectedValue: string | number;
  onChange: (v: any) => void;
  style?: any;
  dropdownIconColor?: string;
  enabled?: boolean;
}

export const SimplePicker: React.FC<SimplePickerProps> = ({ items, selectedValue, onChange, style, enabled = true }) => {
  return (
    <Picker 
      selectedValue={selectedValue} 
      onValueChange={onChange} 
      style={style} 
      enabled={enabled}
      accessibilityLabel="Simple picker selection"
    >
      {items.map((it, i) => (
        <PickerItem key={`${String(it.value)}-${i}`} label={it.label} value={it.value} />
      ))}
    </Picker>
  );
};


