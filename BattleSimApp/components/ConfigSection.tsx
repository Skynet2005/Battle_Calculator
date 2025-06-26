import React from "react";
import { Text, TextInput, TouchableOpacity, View } from "react-native";
import { styles } from "../styles";

interface Props {
  attackType: "solo" | "rally";
  setAttackType: (t: "solo" | "rally") => void;

  capacity: string;
  setCapacity: (v: string) => void;

  sims: string;
  setSims: (v: string) => void;

  onRun: () => void;
}

export const ConfigSection: React.FC<Props> = (p) => (
  <View style={styles.configSection}>
    {/* solo/rally radio */}
    <View style={styles.row}>
      <Text style={styles.label}>Attack Type</Text>
      <View style={styles.radioContainer}>
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

    {/* capacity + sims */}
    {[
      {
        label: p.attackType === "rally" ? "Rally Capacity" : "March Capacity",
        val: p.capacity,
        setter: p.setCapacity,
      },
      { label: "Sim Count", val: p.sims, setter: p.setSims },
    ].map((cfg) => (
      <View key={cfg.label} style={styles.row}>
        <Text style={styles.label}>{cfg.label}</Text>
        <TextInput
          style={styles.input}
          value={cfg.val}
          onChangeText={cfg.setter}
          keyboardType="number-pad"
          placeholderTextColor="#7B8794"
        />
      </View>
    ))}

    {/* run button */}
    <TouchableOpacity onPress={p.onRun} style={styles.buttonContainer}>
      <Text style={styles.buttonText}>Run Simulation</Text>
    </TouchableOpacity>
  </View>
);
