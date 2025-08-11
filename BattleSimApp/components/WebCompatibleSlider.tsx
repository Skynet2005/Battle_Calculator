import React from "react";
import { Platform } from "react-native";

type Props = {
  value: number;
  minimumValue?: number;
  maximumValue?: number;
  step?: number;
  onValueChange: (value: number) => void;
  style?: any;
  accessibilityLabel?: string;
};

const WebCompatibleSlider: React.FC<Props> = ({
  value,
  minimumValue = 0,
  maximumValue = 1,
  step = 0.01,
  onValueChange,
  style,
  accessibilityLabel,
}) => {
  if (Platform.OS === "web") {
    const percent = ((value - minimumValue) / (maximumValue - minimumValue)) * 100;
    return (
      <input
        type="range"
        aria-label={accessibilityLabel || "Slider"}
        title={accessibilityLabel || "Slider"}
        value={value}
        min={minimumValue}
        max={maximumValue}
        step={step}
        onChange={(e) => onValueChange(parseFloat((e.target as HTMLInputElement).value))}
        style={{ width: "100%", ...(style || {}) }}
      />
    );
  }

  const Slider = require("@react-native-community/slider").default;
  return (
    <Slider
      value={value}
      minimumValue={minimumValue}
      maximumValue={maximumValue}
      step={step}
      onValueChange={onValueChange}
      style={style}
    />
  );
};

export default WebCompatibleSlider;


