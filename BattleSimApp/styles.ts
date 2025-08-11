import { StyleSheet, Platform } from "react-native";

/**
 * styles.ts
 * ----------
 * Modern, responsive design system for React Native + RN Web.
 * - Mobile-first with fluid spacing and max-width containers
 * - Consistent buttons, inputs, rows, and panels
 * - Attacker/Defender themed accents
 * - Light/Dark theme support with setTheme()
 */

type Theme = "dark" | "light";

let currentTheme: Theme = "dark";

const palette = (isDark: boolean) => ({
  // Surfaces
  background: isDark ? "#0F172A" : "#F8FAFC",
  surface: isDark ? "#111827" : "#FFFFFF",
  surfaceAlt: isDark ? "#1F2937" : "#F1F5F9",
  surfaceMuted: isDark ? "#374151" : "#E5E7EB",
  overlay: isDark ? "rgba(0,0,0,0.5)" : "rgba(0,0,0,0.25)",

  // Text
  text: isDark ? "#F8FAFC" : "#0F172A",
  textSecondary: isDark ? "#CBD5E1" : "#334155",
  textMuted: isDark ? "#94A3B8" : "#64748B",

  // Borders
  border: isDark ? "#334155" : "#E2E8F0",
  borderStrong: isDark ? "#475569" : "#CBD5E1",

  // Brand
  primary: "#6366F1",
  primaryHover: "#4F46E5",

  // Status
  success: isDark ? "#22C55E" : "#16A34A",
  warning: isDark ? "#F59E0B" : "#D97706",
  danger: isDark ? "#EF4444" : "#DC2626",

  // Side accents
  attacker: isDark ? "#3B82F6" : "#2563EB",
  defender: isDark ? "#EF4444" : "#DC2626",
  attackerBg: isDark ? "#111827" : "#EFF6FF",
  defenderBg: isDark ? "#111827" : "#FEF2F2",
});

export const createThemedStyles = (isDarkMode: boolean) => {
  const c = palette(isDarkMode);

  const webShadow = (lvl: 1 | 2 | 3 = 2) => (Platform.OS === "web"
    ? {
        boxShadow:
          lvl === 1
            ? `0 1px 2px 0 ${isDarkMode ? "rgba(0,0,0,0.3)" : "rgba(0,0,0,0.08)"}`
            : lvl === 2
            ? `0 8px 20px -6px ${isDarkMode ? "rgba(0,0,0,0.35)" : "rgba(0,0,0,0.12)"}`
            : `0 14px 32px -12px ${isDarkMode ? "rgba(0,0,0,0.4)" : "rgba(0,0,0,0.16)"}`,
      }
    : {});

  return StyleSheet.create({
    // Results container (scroll)
    results: { width: "100%" },
    /* Layout */
    container: { flex: 1, backgroundColor: c.background },
    content: { width: "100%", maxWidth: 1400, alignSelf: "center", paddingHorizontal: 16, paddingVertical: 12 },
    scrollableContent: { 
      flex: 1, 
      marginTop: 80
    },

    /* Panels & Cards */
    panel: {
      backgroundColor: c.surface,
      borderRadius: 16,
      borderWidth: 1,
      borderColor: c.border,
      padding: 20,
      marginBottom: 20,
      ...webShadow(2),
      ...(Platform.OS === "web"
        ? { backdropFilter: "saturate(120%) blur(4px)" as any }
        : {
            shadowColor: "#000",
            shadowOffset: { width: 0, height: 6 },
            shadowOpacity: isDarkMode ? 0.25 : 0.12,
            shadowRadius: 12,
            elevation: 6,
          }),
    },
    mobilePanel: { padding: 14, borderRadius: 12, marginBottom: 14, backgroundColor: c.surface, borderWidth: 1, borderColor: c.border },

    card: {
      backgroundColor: c.surfaceAlt,
      borderRadius: 12,
      borderWidth: 1,
      borderColor: c.border,
      padding: 14,
      marginBottom: 12,
      ...webShadow(1),
    },

    /* Rows / Columns */
    row: {
      backgroundColor: c.surfaceAlt,
      borderRadius: 12,
      borderWidth: 1,
      borderColor: c.border,
      padding: 14,
      marginBottom: 12,
      ...webShadow(1),
    },
    mobileRow: { backgroundColor: c.surfaceAlt, borderRadius: 10, borderWidth: 1, borderColor: c.border, padding: 12, marginBottom: 10 },

    inlineRow: { flexDirection: "row", gap: 12 },
    twoColRow: { flexDirection: "row", gap: 16 },
    twoColStack: { flexDirection: "column", gap: 12 },

    col: { flex: 1, minWidth: 0 },
    halfCol: { flex: 1, minWidth: 0 },

    /* Typography */
    header: {
      fontSize: 28,
      fontWeight: "800",
      textAlign: "center",
      color: c.text,
      marginBottom: 12,
      letterSpacing: -0.3,
    },
    subHeader: {
      fontSize: 18,
      fontWeight: "700",
      color: c.text,
      marginBottom: 8,
    },
    // Results headers
    resultHeader: { fontSize: 16, fontWeight: "800", color: c.text, marginBottom: 8 },

    // Segmented control (compact/detailed)
    segmented: { flexDirection: "row", gap: 8, marginBottom: 12 },
    segmentedBtn: {
      paddingHorizontal: 12,
      paddingVertical: 6,
      borderRadius: 999,
      borderWidth: 1,
      borderColor: c.border,
      backgroundColor: c.surfaceAlt,
    },
    segmentedBtnActive: { backgroundColor: c.primary, borderColor: c.primary },
    segmentedText: { fontSize: 13, fontWeight: "700", color: c.text },
    segmentedTextActive: { color: "#FFFFFF" },

    // Side header text colors
    attackerText: { color: c.attacker, fontWeight: "800" },
    defenderText: { color: c.defender, fontWeight: "800" },

    // Result value helpers
    resultValue: { color: c.text, textAlign: "right" },
    zeroText: { color: c.textMuted },

    // Bars for visualizing values in tables
    barTrack: {
      flex: 1,
      height: 8,
      marginLeft: 8,
      borderRadius: 999,
      backgroundColor: c.surfaceMuted,
      overflow: "hidden",
    },
    barFill: {
      height: 8,
      backgroundColor: c.primary,
      borderRadius: 999,
    },
    mobileSubHeader: { fontSize: 16, fontWeight: "700", color: c.text },

    label: { fontSize: 15, fontWeight: "600", color: c.text, marginBottom: 6 },
    helperText: { fontSize: 13, color: c.textMuted },
    attackerLabel: { color: c.attacker, fontWeight: "800" },
    defenderLabel: { color: c.defender, fontWeight: "800" },

    /* Inputs */
    input: {
      height: 48,
      backgroundColor: c.surface,
      color: c.text,
      borderWidth: 2,
      borderColor: c.border,
      borderRadius: 12,
      paddingHorizontal: 14,
      ...(Platform.OS === "web"
        ? {
            transition: "all 0.15s ease",
          }
        : {}),
    },
    smallInput: { height: 42, borderRadius: 10, paddingHorizontal: 12, borderWidth: 2, borderColor: c.border, color: c.text, backgroundColor: c.surface },
    mobileInput: { height: 44, borderRadius: 10, paddingHorizontal: 12, borderWidth: 2, borderColor: c.border, color: c.text, backgroundColor: c.surface },

    picker: {
      height: 48,
      borderWidth: 2,
      borderColor: c.border,
      borderRadius: 12,
      backgroundColor: c.surface,
      color: c.text,
      marginBottom: 8,
    },
    mobilePicker: {
      height: 44,
      borderWidth: 2,
      borderColor: c.border,
      borderRadius: 10,
      backgroundColor: c.surface,
      color: c.text,
      marginBottom: 8,
    },
    pickerSm: { height: 40, borderRadius: 10, borderWidth: 2, borderColor: c.border, backgroundColor: c.surface, color: c.text },

    attackerPicker: { borderColor: c.attacker },
    defenderPicker: { borderColor: c.defender },

    /* Buttons */
    buttonContainer: {
      height: 48,
      borderRadius: 12,
      backgroundColor: c.primary,
      alignItems: "center",
      justifyContent: "center",
      paddingHorizontal: 16,
      ...webShadow(2),
    },
    buttonText: { fontSize: 16, fontWeight: "700", color: "#FFFFFF" },

    secondaryButtonContainer: {
      height: 48,
      borderRadius: 12,
      backgroundColor: c.surfaceAlt,
      borderWidth: 1,
      borderColor: c.border,
      alignItems: "center",
      justifyContent: "center",
      paddingHorizontal: 16,
    },
    dangerButtonContainer: {
      height: 48,
      borderRadius: 12,
      backgroundColor: c.danger,
      alignItems: "center",
      justifyContent: "center",
      paddingHorizontal: 16,
    },
    disabledButton: { opacity: 0.6 },

    mobileButton: {
      height: 44,
      borderRadius: 10,
      backgroundColor: c.primary,
      alignItems: "center",
      justifyContent: "center",
    },
    mobileButtonText: { fontSize: 15, fontWeight: "700", color: "#FFFFFF" },

    miniButton: {
      minHeight: 36,
      borderRadius: 10,
      paddingHorizontal: 12,
      alignItems: "center",
      justifyContent: "center",
      backgroundColor: c.surfaceAlt,
      borderWidth: 1,
      borderColor: c.border,
    },
    miniButtonText: { fontSize: 14, fontWeight: "700", color: c.text },

    pill: {
      paddingHorizontal: 10,
      paddingVertical: 6,
      borderRadius: 999,
      backgroundColor: c.surfaceAlt,
      borderWidth: 1,
      borderColor: c.border,
      alignSelf: "flex-start",
      marginRight: 8,
    },
    pillText: { fontSize: 12, fontWeight: "700", color: c.textMuted },

    /* Radios */
    radioContainer: { flexDirection: "row", gap: 12, alignItems: "center" },
    radioOption: {
      paddingVertical: 8,
      paddingHorizontal: 10,
      borderRadius: 10,
      borderWidth: 1,
      borderColor: c.border,
      backgroundColor: c.surfaceAlt,
      flexDirection: "row",
      alignItems: "center",
      justifyContent: "space-between",
      gap: 10,
      flex: 1,
    },
    radioLabel: { fontSize: 15, fontWeight: "700", color: c.text },
    radioButton: {
      width: 22, height: 22, borderRadius: 11,
      borderWidth: 2, borderColor: c.border, backgroundColor: c.surface,
      alignItems: "center", justifyContent: "center",
    },
    radioButtonSelected: { borderColor: c.primary, backgroundColor: c.surface },
    radioButtonInner: { width: 12, height: 12, borderRadius: 6, backgroundColor: c.primary },

    /* Section headers */
    sectionHeaderRow: { flexDirection: "row", alignItems: "center", justifyContent: "space-between", marginBottom: 8 },
    sectionToggleBtn: {
      borderRadius: 999,
      paddingHorizontal: 12,
      paddingVertical: 6,
      borderWidth: 1,
      borderColor: c.border,
      backgroundColor: c.surfaceAlt,
    },
    sectionToggleText: { fontSize: 13, fontWeight: "700", color: c.text },

    /* Action rows */
    actionsRow: { flexDirection: "row", gap: 12, marginTop: 12 },

    /* Side tints */
    attackerTint: { backgroundColor: c.attackerBg, borderColor: c.attacker },
    defenderTint: { backgroundColor: c.defenderBg, borderColor: c.defender },

    /* Total bars */
    totalBar: {
      flexDirection: "row",
      alignItems: "center",
      justifyContent: "space-between",
      paddingVertical: 10,
      paddingHorizontal: 12,
      backgroundColor: c.surfaceAlt,
      borderRadius: 10,
      borderWidth: 1,
      borderColor: c.border,
      marginTop: 8,
      gap: 10,
    },
    totalText: { fontSize: 14, fontWeight: "700", color: c.text },

    /* Gear sections */
    mobileGearSection: { gap: 8 },
    tabletGearSection: { gap: 10 },
    desktopGearSection: { gap: 12 },
    
    /* Top Bar */
    topBarContainer: {
      backgroundColor: c.surface,
      borderBottomWidth: 1,
      borderBottomColor: c.border,
      width: "100%",
      height: 80,
      ...(Platform.OS === "web" 
        ? { position: "fixed" as any }
        : { position: "absolute" }),
      top: 0,
      left: 0,
      zIndex: 10,
      elevation: 10,
      ...webShadow(2),
    },
    topBarContent: {
      maxWidth: 1400,
      alignSelf: "center",
      width: "100%",
      flexDirection: "row",
      alignItems: "center",
      justifyContent: "space-between",
      gap: 12,
    },
    topBarTitle: {
      color: c.text,
      fontWeight: "800",
      letterSpacing: -0.3,
    },
    topBarIconWrap: {
      paddingHorizontal: 10,
      paddingVertical: 8,
      borderRadius: 999,
      backgroundColor: c.surfaceAlt,
      borderWidth: 1,
      borderColor: c.border,
      alignItems: "center",
      justifyContent: "center",
      marginRight: 8,
    },
    themeToggleButton: {
      paddingHorizontal: 12,
      paddingVertical: 8,
      borderRadius: 999,
      backgroundColor: c.surfaceAlt,
      borderWidth: 1,
      borderColor: c.border,
      marginRight: 8,
    },
    themeToggleText: { color: c.text, fontWeight: "700", fontSize: 13 },
    topBarRunButton: {
      paddingHorizontal: 14,
      paddingVertical: 10,
      borderRadius: 999,
      backgroundColor: c.primary,
      ...webShadow(1),
      marginRight: 8,
      minWidth: 72,
      alignItems: "center",
    },
    topBarRunText: { color: "#FFFFFF", fontWeight: "800", fontSize: 13 },
    topBarProfileButton: {
      paddingHorizontal: 12,
      paddingVertical: 8,
      borderRadius: 999,
      backgroundColor: c.primary,
      ...webShadow(1),
      marginLeft: 8,
    },
    topBarProfileText: { color: "#FFFFFF", fontWeight: "800", fontSize: 13 },

    /* Simple table styles (Profile presets) */
    tableContainer: {
      borderWidth: 1,
      borderColor: c.border,
      borderRadius: 12,
      overflow: "hidden",
      backgroundColor: c.surface,
    },
    tableHeaderRow: {
      flexDirection: "row",
      backgroundColor: c.surfaceAlt,
      borderBottomWidth: 1,
      borderBottomColor: c.border,
      paddingHorizontal: 12,
      paddingVertical: 10,
    },
    tableHeaderCell: { color: c.text, fontWeight: "800" },
    tableRow: {
      flexDirection: "row",
      borderTopWidth: 1,
      borderTopColor: c.border,
      paddingHorizontal: 12,
      paddingVertical: 10,
      alignItems: "center",
    },
    tableCell: { color: c.text },

    /* Stacked rows for small screens */
    stackRow: {
      borderTopWidth: 1,
      borderTopColor: c.border,
      paddingVertical: 10,
      gap: 4,
    },
    stackLabel: { fontSize: 13, fontWeight: "700", color: c.textSecondary },
    stackValue: { fontSize: 14, color: c.text },
  });
};

export let styles = createThemedStyles(true);

export const setTheme = (theme: Theme) => {
  currentTheme = theme;
  const isDark = theme === "dark";
  styles = createThemedStyles(isDark);
  return styles;
};
