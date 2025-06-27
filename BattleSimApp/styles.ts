import { StyleSheet } from "react-native";

/*  One central StyleSheet so every component imports the same colors/fonts  */
export const styles = StyleSheet.create({
  /* layout */
  container: { flex: 1, padding: 16, backgroundColor: "#1F2937" },

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
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 2,
  },

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

  /* config section / buttons */
  configSection: { marginTop: 8, marginBottom: 16 },
  buttonContainer: {
    marginTop: 16,
    marginBottom: 8,
    backgroundColor: "#3B82F6",
    paddingVertical: 12,
    borderRadius: 6,
  },
  buttonText: {
    textAlign: "center",
    color: "#F1F5F9",
    fontSize: 16,
    fontWeight: "bold",
  },

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
});
