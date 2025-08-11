import React from "react";
import { View, Text, TouchableOpacity, ActivityIndicator, useWindowDimensions } from "react-native";
import { styles } from "../styles";
import Svg, { Circle, Path, G } from "react-native-svg";

interface TopBarProps {
  isAuthed: boolean;
  username?: string;
  onProfilePress: () => void;
  onToggleTheme: () => void;
  isDark: boolean;
  onRun?: () => void;
  isRunning?: boolean;
}

const SunIcon = ({ size = 20, color = "#000" }: { size?: number; color?: string }) => (
  <Svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <Circle cx="12" cy="12" r="4.5" stroke={color} strokeWidth="2" />
    <G stroke={color} strokeWidth="2" strokeLinecap="round">
      <Path d="M12 2.5v3" />
      <Path d="M12 18.5v3" />
      <Path d="M2.5 12h3" />
      <Path d="M18.5 12h3" />
      <Path d="M4.7 4.7l2.1 2.1" />
      <Path d="M17.2 17.2l2.1 2.1" />
      <Path d="M19.3 4.7l-2.1 2.1" />
      <Path d="M6.8 17.2l-2.1 2.1" />
    </G>
  </Svg>
);

const MoonIcon = ({ size = 20, color = "#000" }: { size?: number; color?: string }) => (
  <Svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <Path
      d="M21 12.5a8.5 8.5 0 1 1-9.8-8.4 7 7 0 0 0 9.7 9.7c.1-.4.1-.8.1-1.3z"
      fill={color}
    />
  </Svg>
);

export const TopBar: React.FC<TopBarProps> = ({ isAuthed, username, onProfilePress, onToggleTheme, isDark, onRun, isRunning }) => {
  const { width } = useWindowDimensions();
  const isMobile = width < 768;
  const iconColor = isDark ? "#F8FAFC" : "#0F172A";

  return (
    <View style={[
      styles.topBarContainer,
      { paddingVertical: isMobile ? 10 : 16, paddingHorizontal: isMobile ? 10 : 16 }
    ]}>
      <View style={styles.topBarContent}>
        <Text style={[
          styles.topBarTitle,
          { fontSize: isMobile ? 20 : 24 }
        ]}>Battle Simulator</Text>
        <View style={{ flexDirection: 'row', alignItems: 'center' }}>
          {onRun && (
            <TouchableOpacity
              style={[styles.topBarRunButton, isRunning && styles.disabledButton]}
              onPress={onRun}
              disabled={!!isRunning}
            >
              {isRunning ? (
                <ActivityIndicator size="small" color="#FFFFFF" />
              ) : (
                <Text style={styles.topBarRunText}>Run</Text>
              )}
            </TouchableOpacity>
          )}
          <TouchableOpacity style={styles.themeToggleButton} onPress={onToggleTheme}>
            <View>
              {isDark ? <SunIcon size={18} color={iconColor} /> : <MoonIcon size={18} color={iconColor} />}
            </View>
          </TouchableOpacity>
          <TouchableOpacity style={styles.topBarProfileButton} onPress={onProfilePress}>
            <Text style={styles.topBarProfileText}>
              {isAuthed && username ? `👤 ${username}` : "👤 Profile"}
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};
