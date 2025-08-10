import React from "react";
import { Text, TextInput, TouchableOpacity, View, ActivityIndicator } from "react-native";
import { SimplePicker } from "../utils/pickers";
import { styles } from "../styles";

interface Props {
  attackType: "solo" | "rally";
  setAttackType: (t: "solo" | "rally") => void;

  attackerCapacity: string;
  setAttackerCapacity: (v: string) => void;

  defenderCapacity: string;
  setDefenderCapacity: (v: string) => void;

  sims: string;
  setSims: (v: string) => void;

  onRun: () => void;
  isRunning?: boolean;
  hideRunButton?: boolean;
}

export const ConfigSection: React.FC<Props> = (p) => (
  <View style={styles.configSection}>
    {/* Attack Type + Sim Count in one row */}
    <View style={[styles.row, styles.inlineRow]}> 
      <View style={{ flex: 1, paddingRight: 12 }}> 
        <Text style={styles.label}>Attack Type</Text>
        <View style={[styles.radioContainer, { marginTop: 8 }]}>
          {(["solo", "rally"] as const).map((opt) => (
            <TouchableOpacity
              key={opt}
              onPress={() => p.setAttackType(opt)}
              style={styles.radioOption}
            >
              <Text style={styles.radioLabel}>{opt === "solo" ? "Solo" : "Rally"}</Text>
              <View
                style={[
                  styles.radioButton,
                  p.attackType === opt && styles.radioButtonSelected,
                ]}
              >
                {p.attackType === opt && <View style={styles.radioButtonInner} />}
              </View>
            </TouchableOpacity>
          ))}
        </View>
      </View>
      <View style={{ flex: 1, flexDirection: "column" }}> 
        <Text style={styles.label}>Sim Count</Text>
        <TextInput
          style={[styles.input, { marginTop: 8 }]}
          value={p.sims}
          onChangeText={p.setSims}
          keyboardType="number-pad"
          placeholderTextColor="#7B8794"
          editable={!p.isRunning}
        />
      </View>
    </View>

    {/* capacities side-by-side, centered between */}
    <View style={[styles.row, styles.inlineRow]}> 
      <View style={styles.halfCol}>
        <Text style={styles.label}>
          Attacker {p.attackType === "rally" ? "Rally" : "March"} Capacity
        </Text>
        <TextInput
          style={[styles.input]}
          value={p.attackerCapacity}
          onChangeText={p.setAttackerCapacity}
          keyboardType="number-pad"
          placeholderTextColor="#7B8794"
          editable={!p.isRunning}
        />
      </View>
      <View style={styles.halfCol}>
        <Text style={styles.label}>
          Defender {p.attackType === "rally" ? "Rally" : "March"} Capacity
        </Text>
        <TextInput
          style={[styles.input]}
          value={p.defenderCapacity}
          onChangeText={p.setDefenderCapacity}
          keyboardType="number-pad"
          placeholderTextColor="#7B8794"
          editable={!p.isRunning}
        />
      </View>
    </View>

    {/* Sim count moved to the first row */}

    {!p.hideRunButton && (
      <TouchableOpacity
        onPress={p.onRun}
        disabled={!!p.isRunning}
        style={[styles.buttonContainer, p.isRunning && styles.disabledButton]}
      >
        {p.isRunning ? (
          <View style={{ flexDirection: "row", justifyContent: "center", alignItems: "center", gap: 8 }}>
            <ActivityIndicator color="#F1F5F9" />
            <Text style={styles.buttonText}>Running…</Text>
          </View>
        ) : (
          <Text style={styles.buttonText}>Run Simulation</Text>
        )}
      </TouchableOpacity>
    )}
  </View>
);
