import { StyleSheet, Platform } from "react-native";

/*  One central StyleSheet so every component imports the same colors/fonts  */
export const styles = StyleSheet.create({
  /* layout */
  container: { flex: 1, padding: 16, backgroundColor: "#1F2937" },
  content: { width: "100%", maxWidth: 1200, alignSelf: "center" },
  relativeContainer: { position: "relative" },
  twoColRow: { flexDirection: "row" },
  twoColStack: { flexDirection: "column" },
  col: { flex: 1, minWidth: 0, paddingHorizontal: 6 },

  /* panels */
  panel: {
    backgroundColor: "#111827",
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: "#374151",
  },

  /* headings */
  header: {
    fontSize: 28,
    textAlign: "center",
    marginBottom: 16,
    color: "#F1F5F9",
    fontWeight: "bold",
  },
  subHeader: {
    color: "#F1F5F9",
    fontSize: 14,
    marginTop: 8,
    marginBottom: 4,
    fontWeight: "600",
  },

  /* generic row/card */
  row: {
    marginBottom: 16,
    backgroundColor: "#374151",
    padding: 12,
    borderRadius: 8,
    ...(Platform.OS === "web"
      ? ({ boxShadow: "0 1px 2px rgba(0,0,0,0.2)" } as any)
      : {
          shadowColor: "#000",
          shadowOffset: { width: 0, height: 1 },
          shadowOpacity: 0.2,
          shadowRadius: 2,
          elevation: 2,
        }),
  },
  centerAlign: { alignItems: "center" },
  inlineRow: { flexDirection: "row", alignItems: "flex-start", justifyContent: "center", gap: 12, flexWrap: "wrap" },
  halfCol: { flex: 1, minWidth: 260 },

  /* labels + colours */
  label: { marginBottom: 8, fontSize: 16, color: "#E5E7EB", fontWeight: "500" },
  attackerLabel: { color: "#93C5FD" },
  defenderLabel: { color: "#FCA5A5" },

  /* pickers / text-inputs */
  picker: {
    height: 48,
    borderWidth: 1,
    borderColor: "#4B5563",
    marginBottom: 12,
    backgroundColor: "#374151",
    borderRadius: 4,
    color: "#FFFFFF",
  },
  attackerPicker: { borderColor: "#1E40AF", backgroundColor: "#1E3A8A" },
  defenderPicker: { borderColor: "#7F1D1D", backgroundColor: "#991B1B" },

  input: {
    height: 48,
    borderWidth: 1,
    borderColor: "#4B5563",
    paddingHorizontal: 12,
    borderRadius: 4,
    backgroundColor: "#374151",
    fontSize: 16,
    color: "#E5E7EB",
  },
  smallInput: { width: 75, textAlign: 'center' },
  pickerContainer: {
    backgroundColor: "#111827",
    borderColor: "#374151",
    borderWidth: 1,
    borderRadius: 6,
    marginVertical: 4,
    marginHorizontal: 6,
  },
  errorInput: {
    borderColor: "#DC2626",
    backgroundColor: "#3B1F1F",
  },
  errorText: { color: "#FCA5A5", fontSize: 12, marginTop: 4 },
  searchInput: {
    height: 40,
    borderWidth: 1,
    borderColor: "#4B5563",
    paddingHorizontal: 8,
    borderRadius: 4,
    backgroundColor: "#374151",
    fontSize: 14,
    color: "#E5E7EB",
    marginBottom: 8,
  },

  /* config section / buttons */
  configSection: { marginTop: 8, marginBottom: 16 },
  buttonContainer: {
    marginTop: 16,
    marginBottom: 8,
    backgroundColor: "#3B82F6",
    paddingVertical: 12,
    borderRadius: 6,
  },
  secondaryButtonContainer: {
    marginTop: 16,
    marginBottom: 8,
    backgroundColor: "#6B7280",
    paddingVertical: 12,
    borderRadius: 6,
  },
  dangerButtonContainer: {
    marginTop: 16,
    marginBottom: 8,
    backgroundColor: "#DC2626",
    paddingVertical: 12,
    borderRadius: 6,
  },
  disabledButton: {
    backgroundColor: "#4B5563",
  },
  buttonText: {
    textAlign: "center",
    color: "#F1F5F9",
    fontSize: 16,
    fontWeight: "bold",
  },
  actionsRow: { flexDirection: "row", gap: 8 },
  helperActionsRow: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginTop: 6 },
  linkText: { color: "#93C5FD", textDecorationLine: "underline", fontWeight: "600" },
  linkTextDanger: { color: "#FCA5A5", textDecorationLine: "underline", fontWeight: "600" },
  linkTextSecondary: { color: "#A7F3D0", textDecorationLine: "underline", fontWeight: "600" },

  /* result block */
  results: {
    backgroundColor: "#111827",
    padding: 16,
    borderRadius: 8,
    marginTop: 16,
    marginBottom: 24,
  },
  resultHeader: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#F1F5F9",
    marginBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#4B5563",
    paddingBottom: 8,
  },
  helperText: { fontSize: 12, marginTop: 4 },
  helperTextOk: { color: "#10B981" },
  helperTextWarn: { color: "#F59E0B" },
  resultRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 8,
    paddingVertical: 4,
    borderBottomWidth: 1,
    borderBottomColor: "#4B5563",
  },
  resultLabel: { fontSize: 16, color: "#9CA3AF", flex: 1 },
  resultValue: {
    fontSize: 16,
    fontWeight: "500",
    color: "#E5E7EB",
    flex: 1,
    textAlign: "right",
  },
  attackerText: { color: "#93C5FD" },
  defenderText: { color: "#FCA5A5" },
  zeroText: { color: "#F87171", fontWeight: "700" },

  /* radio */
  radioContainer: { flexDirection: "row", alignItems: "center", marginTop: 8 },
  radioOption: { flexDirection: "row", alignItems: "center", marginRight: 24 },
  radioLabel: { color: "#E5E7EB", fontSize: 16, marginRight: 8 },
  radioButton: {
    width: 22,
    height: 22,
    borderRadius: 11,
    borderWidth: 2,
    borderColor: "#3B82F6",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#1F2937",
    marginRight: 4,
  },
  radioButtonSelected: { borderColor: "#F59E42", backgroundColor: "#2563EB" },
  radioButtonInner: { width: 10, height: 10, borderRadius: 5, backgroundColor: "#F59E42" },

  /* slot + ratio controls */
  slotPickerContainer: { flexDirection: "row", alignItems: "center", marginBottom: 12 },
  slotLabel: { fontSize: 16, marginRight: 8, fontWeight: "500" },
  slotPicker: { width: 100, height: 40, borderWidth: 1, borderRadius: 4, color: "#FFFFFF" },
  ratioRow: { flexDirection: "row", alignItems: "center", marginBottom: 8 },
  ratioInput: {
    flex: 1,
    height: 40,
    marginLeft: 12,
    paddingHorizontal: 8,
    borderWidth: 1,
    borderColor: "#4B5563",
    borderRadius: 4,
    backgroundColor: "#374151",
    color: "#E5E7EB",
  },
  percentLabel: { marginLeft: 8, color: "#E5E7EB", minWidth: 44, textAlign: "right" },
  miniButtons: { flexDirection: "row", marginLeft: 8 },
  miniButton: {
    paddingVertical: 4,
    paddingHorizontal: 8,
    backgroundColor: "#374151",
    borderRadius: 4,
    marginLeft: 4,
  },
  miniButtonText: { color: "#F1F5F9", fontWeight: "600" },

  // Table styles for ResultsSection
  tableContainer: {
    marginVertical: 8,
    borderWidth: 1,
    borderColor: "#4B5563",
    borderRadius: 6,
    overflow: "hidden",
    backgroundColor: "#23272F",
  },
  tableHeaderRow: {
    flexDirection: "row",
    backgroundColor: "#374151",
    borderBottomWidth: 1,
    borderBottomColor: "#4B5563",
    paddingVertical: 6,
    paddingHorizontal: 4,
  },
  tableHeaderCell: {
    fontWeight: "bold",
    color: "#F1F5F9",
    fontSize: 15,
    textAlign: "center",
  },
  tableRow: {
    flexDirection: "row",
    borderBottomWidth: 1,
    borderBottomColor: "#23272F",
    paddingVertical: 4,
    paddingHorizontal: 4,
    alignItems: "center",
  },
  tableCell: {
    color: "#E5E7EB",
    fontSize: 14,
    textAlign: "center",
    flexWrap: "wrap",
  },
  tableCellLeft: {
    textAlign: "left",
  },

  /* overlay while running */
  overlay: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "rgba(0,0,0,0.05)",
    // RN Web recommendation: prefer style.pointerEvents instead of prop
    pointerEvents: "auto" as unknown as undefined,
  },
  overlayCenter: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    alignItems: "center",
    justifyContent: "center",
  },

  // Results toggles
  sectionHeaderRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 8,
  },
  sectionToggleBtn: {
    paddingVertical: 6,
    paddingHorizontal: 10,
    backgroundColor: "#374151",
    borderRadius: 6,
  },
  sectionToggleText: { color: "#F1F5F9", fontWeight: "600" },

  // Sum progress bar
  progressBar: {
    width: "100%",
    height: 8,
    backgroundColor: "#374151",
    borderRadius: 4,
    overflow: "hidden",
    marginTop: 6,
  },
  progressFill: { height: 8, backgroundColor: "#10B981" },

  // Floating action button
  fab: {
    position: "absolute",
    right: 24,
    bottom: 24,
  },
  fabButton: {
    backgroundColor: "#10B981",
    paddingVertical: 14,
    paddingHorizontal: 18,
    borderRadius: 28,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 3,
    ...(Platform.OS === "web" ? ({ boxShadow: "0 2px 6px rgba(0,0,0,0.3)" } as any) : {}),
  },

  // Segmented control
  segmented: {
    flexDirection: "row",
    backgroundColor: "#1F2937",
    borderRadius: 8,
    overflow: "hidden",
    marginBottom: 12,
    borderWidth: 1,
    borderColor: "#374151",
  },
  segmentedBtn: {
    flex: 1,
    paddingVertical: 10,
    alignItems: "center",
  },
  segmentedBtnActive: {
    backgroundColor: "#374151",
  },
  segmentedText: { color: "#9CA3AF", fontWeight: "600" },
  segmentedTextActive: { color: "#F1F5F9" },

  // Pills
  pillRow: { flexDirection: "row", gap: 8, marginBottom: 8, alignItems: "center" },
  pill: {
    paddingVertical: 4,
    paddingHorizontal: 10,
    borderRadius: 999,
    backgroundColor: "#374151",
  },
  pillText: { color: "#F1F5F9", fontWeight: "600" },

  // Tiny bars
  barTrack: {
    flex: 1,
    height: 8,
    backgroundColor: "#23272F",
    borderRadius: 4,
    marginLeft: 6,
  },
  barFill: {
    height: 8,
    backgroundColor: "#3B82F6",
    borderRadius: 4,
  },
});
