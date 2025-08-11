import React from 'react';
import { Platform } from 'react-native';

// Web-compatible picker for React 19 compatibility
const WebPicker: React.FC<{
  selectedValue: any;
  onValueChange: (value: any) => void;
  enabled?: boolean;
  style?: any;
  children: React.ReactNode;
  accessibilityLabel?: string;
}> = ({
  selectedValue,
  onValueChange,
  enabled = true,
  style,
  children,
  accessibilityLabel,
}) => {
  if (Platform.OS === 'web') {
    // Ensure we always have a non-empty label for accessibility
    const label = accessibilityLabel?.trim() || 'Picker selection';

    return (
      <select
        value={selectedValue}
        onChange={(e) => onValueChange(e.target.value)}
        disabled={!enabled}
        aria-label={label}
        title={label}
        name="web-picker"
        style={{
          padding: '8px',
          borderRadius: '4px',
          border: '1px solid #ccc',
          backgroundColor: enabled ? 'white' : '#f5f5f5',
          fontSize: '14px',
          minWidth: '100px',
          outline: 'none',
          cursor: enabled ? 'pointer' : 'not-allowed',
        }}
      >
        {children}
      </select>
    );
  }

  // Use the original Picker for native platforms
  const { Picker } = require('@react-native-picker/picker');
  return (
    <Picker
      selectedValue={selectedValue}
      onValueChange={onValueChange}
      enabled={enabled}
      style={style}
    >
      {children}
    </Picker>
  );
};

// Web-compatible Picker.Item for React 19 compatibility
const WebPickerItem: React.FC<{
  label: string;
  value: any;
  color?: string;
  enabled?: boolean;
}> = ({ label, value, color, enabled }) => {
  if (Platform.OS === 'web') {
    return (
      <option value={value} disabled={enabled === false}>
        {label}
      </option>
    );
  }

  // Use the original Picker.Item for native platforms
  const { Picker } = require('@react-native-picker/picker');
  return <Picker.Item label={label} value={value} color={color} enabled={enabled} />;
};

// Export both components
export { WebPicker as Picker, WebPickerItem as PickerItem };
export default WebPicker;
