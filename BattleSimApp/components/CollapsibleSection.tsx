import React from "react";
import { View, Text, TouchableOpacity, LayoutAnimation, Platform } from "react-native";
import { styles } from "../styles";
import Svg, { Path } from "react-native-svg";

type Props = {
  title: string;
  defaultOpen?: boolean;
  children: React.ReactNode;
  rightActions?: React.ReactNode;
  style?: any;
};

export const CollapsibleSection: React.FC<Props> = ({ title, defaultOpen = true, children, rightActions, style }) => {
  const [open, setOpen] = React.useState<boolean>(defaultOpen);

  const toggle = () => {
    if (Platform.OS !== "web") {
      LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    }
    setOpen((v) => !v);
  };

  return (
    <View style={[styles.panel, style]}>
      <View style={styles.sectionHeaderRow}>
        <Text style={styles.subHeader}>{title}</Text>
        <View style={{ flexDirection: "row", alignItems: "center", gap: 8 }}>
          {rightActions}
          <TouchableOpacity onPress={toggle} style={styles.sectionToggleBtn} accessibilityRole="button">
            <View style={{ flexDirection: "row", alignItems: "center", gap: 6 }}>
              <Text style={styles.sectionToggleText}>{open ? "Hide" : "Show"}</Text>
              <Svg width={14} height={14} viewBox="0 0 24 24" fill="none">
                <Path
                  d={open ? "M6 15l6-6 6 6" : "M6 9l6 6 6-6"}
                  stroke="#64748B"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </Svg>
            </View>
          </TouchableOpacity>
        </View>
      </View>
      {open && (
        <View>{children}</View>
      )}
    </View>
  );
};


