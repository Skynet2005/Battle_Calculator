// App.tsx

import { Picker } from "@react-native-picker/picker";
import axios from "axios";
import React, { useEffect, useState } from "react";
import {
  Button,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View
} from "react-native";

// -----------------------------
// Types
// -----------------------------
type Hero = {
  name: string;
  charClass: string;
  generation: number;
};

type TroopBreakdown = {
  [type: string]: number;
};

type SideDetails = {
  heroes: {
    [type: string]: {
      name: string;
      class: string;
      generation: number;
      skills: string[];
      troop_level: string;
      troop_power: number;
      troop_count: number;
    };
  };
  total_power: number;
  kills: TroopBreakdown;
  survivors: TroopBreakdown;
};

type SimResult = {
  winner?: string;
  rounds?: number;
  attacker_win_rate?: number;
  defender_win_rate?: number;
  avg_attacker_survivors?: number;
  avg_defender_survivors?: number;
  sample_battle?: {
    winner?: string;
    rounds?: number;
    attacker: SideDetails;
    defender: SideDetails;
  };
  attacker?: SideDetails;
  defender?: SideDetails;
};

// -----------------------------
// Main Component
// -----------------------------
export default function App() {
  // Data lists
  const [heroes, setHeroes] = useState<Hero[]>([]);
  const [troops, setTroops] = useState<string[]>([]);

  // Config
  const [attackType, setAttackType] = useState<"solo" | "rally">("solo");
  const [capacity, setCapacity] = useState("185010");
  const [sims, setSims] = useState("1"); // default to 1 for full breakdown

  // Selections
  const emptySel = { Infantry: "", Lancer: "", Marksman: "" };
  const [atkH, setAtkH] = useState<typeof emptySel>(emptySel);
  const [defH, setDefH] = useState<typeof emptySel>(emptySel);
  const [atkT, setAtkT] = useState<typeof emptySel>(emptySel);
  const [defT, setDefT] = useState<typeof emptySel>(emptySel);

  // Slots & Ratios
  const [atkSlots, setAtkSlots] = useState({ Infantry: "1", Lancer: "2", Marksman: "3" });
  const [defSlots, setDefSlots] = useState({ Infantry: "1", Lancer: "2", Marksman: "3" });
  const [atkRatios, setAtkRatios] = useState({ Infantry: "0.5", Lancer: "0.3", Marksman: "0.2" });
  const [defRatios, setDefRatios] = useState({ Infantry: "0.5", Lancer: "0.3", Marksman: "0.2" });

  const [result, setResult] = useState<SimResult | null>(null);

  // Fetch heroes & troops
  useEffect(() => {
    axios.get<Hero[]>("http://localhost:8000/api/heroes")
      .then(res => setHeroes(res.data))
      .catch(err => console.error("Error loading heroes:", err));

    axios.get<string[]>("http://localhost:8000/api/troops")
      .then(res => setTroops(res.data))
      .catch(err => console.error("Error loading troops:", err));
  }, []);

  // Update capacity on attackType change
  useEffect(() => {
    setCapacity(attackType === "solo" ? "185010" : "1377510");
  }, [attackType]);

  // Helpers to render pickers (unchanged)
  const renderHeroItems = (cls: keyof typeof emptySel, side: "atk" | "def") => {
    const list = heroes
      .filter(h => h.charClass.toLowerCase() === cls.toLowerCase())
      .sort((a, b) => a.generation - b.generation);

    let lastGen: number | null = null;
    return list.flatMap(h => {
      const items: React.ReactElement[] = [];
      if (h.generation !== lastGen) {
        items.push(
          <Picker.Item
            key={`hdr-${side}-${cls}-${h.generation}`}
            label={`-- Gen ${h.generation} --`}
            value=""
            enabled={false}
            color="#FFFFFF"
          />
        );
        lastGen = h.generation;
      }
      items.push(
        <Picker.Item
          key={`${side}-${cls}-${h.name}`}
          label={h.name}
          value={h.name}
          color="#FFFFFF"
        />
      );
      return items;
    });
  };

  const renderPickers = (side: "atk" | "def") =>
    (["Infantry", "Lancer", "Marksman"] as const).map(cls => {
      const filteredTroops = troops.filter(name =>
        name.toLowerCase().replace(/\s+/g, "").includes(cls.toLowerCase())
      );
      return (
        <View key={`${side}-${cls}`} style={styles.row}>
          <Text style={[styles.label, side==="atk"?styles.attackerLabel:styles.defenderLabel]}>
            {cls} Hero {side==="atk"?"(Attacker)":"(Defender)"}
          </Text>
          <View style={styles.slotPickerContainer}>
            <Text style={[styles.slotLabel, side==="atk"?styles.attackerLabel:styles.defenderLabel]}>
              Slot:
            </Text>
            <Picker
              selectedValue={side==="atk"?atkSlots[cls]:defSlots[cls]}
              onValueChange={val => {
                const setter = side==="atk"?setAtkSlots:setDefSlots;
                setter(prev => ({ ...prev, [cls]: val }));
              }}
              style={[styles.slotPicker, side==="atk"?styles.attackerPicker:styles.defenderPicker]}
              dropdownIconColor="#FFFFFF"
              itemStyle={{ color: "#FFFFFF" }}
            >
              <Picker.Item label="1" value="1" color="#FFFFFF"/>
              <Picker.Item label="2" value="2" color="#FFFFFF"/>
              <Picker.Item label="3" value="3" color="#FFFFFF"/>
            </Picker>
          </View>
          <Picker
            selectedValue={side==="atk"?atkH[cls]:defH[cls]}
            onValueChange={val => {
              const setter = side==="atk"?setAtkH:setDefH;
              setter(prev => ({ ...prev, [cls]: val }));
            }}
            style={[styles.picker, side==="atk"?styles.attackerPicker:styles.defenderPicker]}
            dropdownIconColor="#FFFFFF"
            itemStyle={{ color: "#FFFFFF" }}
          >
            <Picker.Item label={`Select ${cls} Hero`} value="" color="#FFFFFF"/>
            {renderHeroItems(cls, side)}
          </Picker>

          <Text style={[styles.label, side==="atk"?styles.attackerLabel:styles.defenderLabel]}>
            {cls} Troop
          </Text>
          <Picker
            selectedValue={side==="atk"?atkT[cls]:defT[cls]}
            onValueChange={val => {
              const setter = side==="atk"?setAtkT:setDefT;
              setter(prev => ({ ...prev, [cls]: val }));
            }}
            style={[styles.picker, side==="atk"?styles.attackerPicker:styles.defenderPicker]}
            dropdownIconColor="#FFFFFF"
            itemStyle={{ color: "#FFFFFF" }}
          >
            <Picker.Item label={`Select ${cls} FC`} value="" color="#FFFFFF"/>
            {filteredTroops.map(name => (
              <Picker.Item key={name} label={name} value={name} color="#FFFFFF"/>
            ))}
          </Picker>

          <View style={styles.ratioRow}>
            <Text style={[styles.label, side==="atk"?styles.attackerLabel:styles.defenderLabel]}>
              {cls} Ratio
            </Text>
            <TextInput
              style={styles.ratioInput}
              value={side==="atk"?atkRatios[cls]:defRatios[cls]}
              onChangeText={val => {
                const setter = side==="atk"?setAtkRatios:setDefRatios;
                setter(prev => ({ ...prev, [cls]: val }));
              }}
              keyboardType="decimal-pad"
              placeholder="0.0–1.0"
              placeholderTextColor="#7B8794"
            />
          </View>
        </View>
      );
    });

  // -----------------------------
  // Run Simulation
  // -----------------------------
  const runSim = () => {
    // order by slot, validate, build payload...
    const orderBySlot = (heroObj: typeof emptySel, slotObj: typeof atkSlots) => {
      const arr = ["", "", ""];
      Object.entries(slotObj).forEach(([cls, slot]) => {
        arr[parseInt(slot, 10)-1] = heroObj[cls as keyof typeof heroObj];
      });
      return arr;
    };
    const orderedAtk = orderBySlot(atkH, atkSlots);
    const orderedDef = orderBySlot(defH, defSlots);

    const validate = () => {
      if (orderedAtk.some(h => !h) || orderedDef.some(h => !h)) {
        alert("Select all heroes.");
        return false;
      }
      if (Object.values(atkT).some(t=>!t) || Object.values(defT).some(t=>!t)) {
        alert("Select all troops.");
        return false;
      }
      const a = Object.values(atkRatios).map(Number),
            d = Object.values(defRatios).map(Number);
      if (a.some(isNaN)||d.some(isNaN)
        || Math.abs(a.reduce((x,y)=>x+y,0)-1)>1e-6
        || Math.abs(d.reduce((x,y)=>x+y,0)-1)>1e-6) {
        alert("Ratios must be numbers summing to 1.0");
        return false;
      }
      if (isNaN(+capacity)||isNaN(+sims)) {
        alert("Capacity and sims must be numbers.");
        return false;
      }
      return true;
    };
    if (!validate()) return;

    const payload = {
      attackerHeroes: orderedAtk,
      defenderHeroes: orderedDef,
      attackerRatios: {
        Infantry: parseFloat(atkRatios.Infantry),
        Lancer:    parseFloat(atkRatios.Lancer),
        Marksman:  parseFloat(atkRatios.Marksman),
      },
      defenderRatios: {
        Infantry: parseFloat(defRatios.Infantry),
        Lancer:    parseFloat(defRatios.Lancer),
        Marksman:  parseFloat(defRatios.Marksman),
      },
      totalCapacity: parseInt(capacity,10),
      sims:          parseInt(sims,10),
      attackerTroops: atkT,
      defenderTroops: defT,
    };

    axios.post<SimResult>("http://localhost:8000/api/simulate", payload)
      .then(res => setResult(res.data))
      .catch(err => {
        console.error(err);
        alert("Sim failed: " + (err.response?.data || err.message));
        setResult(null);
      });
  };

  // -----------------------------
  // JSX Return
  // -----------------------------
  return (
    <ScrollView style={styles.container} contentContainerStyle={{ paddingBottom: 40 }}>
      <Text style={styles.header}>Battle Simulator</Text>

      <Text style={styles.subHeader}>Attacker Setup</Text>
      {renderPickers("atk")}

      <Text style={styles.subHeader}>Defender Setup</Text>
      {renderPickers("def")}

      <View style={styles.configSection}>
        <View style={styles.row}>
          <Text style={styles.label}>Attack Type</Text>
          <View style={styles.radioContainer}>
            <TouchableOpacity onPress={()=>setAttackType("solo")} style={styles.radioOption}>
              <Text style={styles.radioLabel}>Solo</Text>
              <View style={[styles.radioButton, attackType==="solo"&&styles.radioButtonSelected]}>
                {attackType==="solo"&&<View style={styles.radioButtonInner}/>}
              </View>
            </TouchableOpacity>
            <TouchableOpacity onPress={()=>setAttackType("rally")} style={styles.radioOption}>
              <Text style={styles.radioLabel}>Rally</Text>
              <View style={[styles.radioButton, attackType==="rally"&&styles.radioButtonSelected]}>
                {attackType==="rally"&&<View style={styles.radioButtonInner}/>}
              </View>
            </TouchableOpacity>
          </View>
        </View>

        <View style={styles.row}>
          <Text style={styles.label}>{attackType==="rally"?"Rally Capacity":"March Capacity"}</Text>
          <TextInput
            style={styles.input}
            value={capacity}
            onChangeText={setCapacity}
            keyboardType="number-pad"
            placeholderTextColor="#7B8794"
          />
        </View>

        <View style={styles.row}>
          <Text style={styles.label}>Sim Count</Text>
          <TextInput
            style={styles.input}
            value={sims}
            onChangeText={setSims}
            keyboardType="number-pad"
            placeholderTextColor="#7B8794"
          />
        </View>

        <View style={styles.buttonContainer}>
          <Button title="Run Simulation" onPress={runSim} color="#3B82F6"/>
        </View>
      </View>

      {result && (() => {
        // prefer detailed sample if present
        const detail = result.sample_battle ?? {
          winner: result.winner,
          rounds: result.rounds,
          attacker: result.attacker!,
          defender: result.defender!,
        };

        return (
          <View style={styles.results}>
            {/* Overview */}
            <Text style={styles.resultHeader}>Battle Overview</Text>
            <View style={styles.resultRow}>
              <Text style={styles.resultLabel}>Winner:</Text>
              <Text style={[styles.resultValue, detail.winner=== "attacker"?styles.attackerText:styles.defenderText]}>
                {detail.winner?.toUpperCase() ?? "—"}
              </Text>
            </View>
            <View style={styles.resultRow}>
              <Text style={styles.resultLabel}>Rounds:</Text>
              <Text style={styles.resultValue}>{detail.rounds}</Text>
            </View>

            {/* Attacker Breakdown */}
            <Text style={[styles.resultHeader, styles.attackerText]}>
              Attacker Details
            </Text>
            <Text style={styles.resultLabel}>
              Total Power: {detail.attacker.total_power}
            </Text>
            {Object.entries(detail.attacker.heroes).map(([type, info])=>(
              <View key={type} style={{ marginVertical: 4, paddingLeft: 8 }}>
                <Text style={styles.resultValue}>
                  {type}: {info.name} (Gen {info.generation}, {info.class})
                </Text>
                <Text style={styles.resultValue}>
                  {info.troop_level} | Power {info.troop_power} | Count {info.troop_count}
                </Text>
                <Text style={styles.resultValue}>
                  Skills: {info.skills.join(", ") || "None"}
                </Text>
              </View>
            ))}

            {/* Kills & Survivors */}
            <Text style={styles.resultHeader}>Kills by Type</Text>
            {Object.entries(detail.attacker.kills).map(([t, n])=>(
              <Text key={t} style={styles.resultValue}>
                {t}: {n}
              </Text>
            ))}
            <Text style={styles.resultHeader}>Survivors by Type</Text>
            {Object.entries(detail.attacker.survivors).map(([t, n])=>(
              <Text key={t} style={styles.resultValue}>
                {t}: {n}
              </Text>
            ))}

            {/* Defender Breakdown */}
            <Text style={[styles.resultHeader, styles.defenderText]}>
              Defender Details
            </Text>
            <Text style={styles.resultLabel}>
              Total Power: {detail.defender.total_power}
            </Text>
            {Object.entries(detail.defender.heroes).map(([type, info])=>(
              <View key={type} style={{ marginVertical: 4, paddingLeft: 8 }}>
                <Text style={styles.resultValue}>
                  {type}: {info.name} (Gen {info.generation}, {info.class})
                </Text>
                <Text style={styles.resultValue}>
                  {info.troop_level} | Power {info.troop_power} | Count {info.troop_count}
                </Text>
                <Text style={styles.resultValue}>
                  Skills: {info.skills.join(", ") || "None"}
                </Text>
              </View>
            ))}

            {/* Kills & Survivors */}
            <Text style={styles.resultHeader}>Kills by Type</Text>
            {Object.entries(detail.defender.kills).map(([t, n])=>(
              <Text key={t} style={styles.resultValue}>
                {t}: {n}
              </Text>
            ))}
            <Text style={styles.resultHeader}>Survivors by Type</Text>
            {Object.entries(detail.defender.survivors).map(([t, n])=>(
              <Text key={t} style={styles.resultValue}>
                {t}: {n}
              </Text>
            ))}

          </View>
        );
      })()}
    </ScrollView>
  );
}

// -----------------------------
// Styles
// -----------------------------
const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: "#1F2937"
  },
  header: {
    fontSize: 28,
    textAlign: "center",
    marginBottom: 16,
    color: "#F1F5F9",
    fontWeight: "bold"
  },
  subHeader: {
    color: "#F1F5F9",
    fontSize: 14,
    marginTop: 8,
    marginBottom: 4,
    fontWeight: "600"
  },
  row: {
    marginBottom: 16,
    backgroundColor: "#374151",
    padding: 12,
    borderRadius: 8,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 2
  },
  label: {
    marginBottom: 8,
    fontSize: 16,
    color: "#E5E7EB",
    fontWeight: "500"
  },
  attackerLabel: {
    color: "#93C5FD"
  },
  defenderLabel: {
    color: "#FCA5A5"
  },
  picker: {
    height: 48,
    borderWidth: 1,
    borderColor: "#4B5563",
    marginBottom: 12,
    backgroundColor: "#374151",
    borderRadius: 4,
    color: "#FFFFFF"
  },
  attackerPicker: {
    borderColor: "#1E40AF",
    backgroundColor: "#1E3A8A"
  },
  defenderPicker: {
    borderColor: "#7F1D1D",
    backgroundColor: "#991B1B"
  },
  input: {
    height: 48,
    borderWidth: 1,
    borderColor: "#4B5563",
    paddingHorizontal: 12,
    borderRadius: 4,
    backgroundColor: "#374151",
    fontSize: 16,
    color: "#E5E7EB"
  },
  configSection: {
    marginTop: 8,
    marginBottom: 16
  },
  buttonContainer: {
    marginTop: 16,
    marginBottom: 8
  },
  results: {
    marginTop: 24,
    padding: 16,
    backgroundColor: "#374151",
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: "#3B82F6",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3,
    elevation: 4
  },
  resultHeader: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#F1F5F9",
    marginBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#4B5563",
    paddingBottom: 8
  },
  resultText: {
    fontSize: 16,
    marginBottom: 8,
    color: "#E5E7EB"
  },
  winnerText: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#F1F5F9",
    marginBottom: 16
  },
  resultRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 8,
    paddingVertical: 4,
    borderBottomWidth: 1,
    borderBottomColor: "#4B5563"
  },
  resultLabel: {
    fontSize: 16,
    color: "#9CA3AF",
    flex: 1
  },
  resultValue: {
    fontSize: 16,
    fontWeight: "500",
    color: "#E5E7EB",
    flex: 1,
    textAlign: "right"
  },
  attackerText: {
    color: "#93C5FD"
  },
  defenderText: {
    color: "#FCA5A5"
  },
  radioContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 8,
    marginBottom: 8
  },
  radioOption: {
    flexDirection: "row",
    alignItems: "center",
    marginRight: 24
  },
  radioLabel: {
    color: "#E5E7EB",
    fontSize: 16,
    marginRight: 8
  },
  radioButton: {
    width: 22,
    height: 22,
    borderRadius: 11,
    borderWidth: 2,
    borderColor: "#3B82F6",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#1F2937",
    marginRight: 4
  },
  radioButtonSelected: {
    borderColor: "#F59E42",
    backgroundColor: "#2563EB"
  },
  radioButtonInner: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: "#F59E42"
  },
  slotPickerContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 12
  },
  slotLabel: {
    fontSize: 16,
    marginRight: 8,
    fontWeight: "500"
  },
  slotPicker: {
    width: 100,
    height: 40,
    borderWidth: 1,
    borderRadius: 4,
    color: "#FFFFFF"
  },
  ratioRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 8
  },
  ratioInput: {
    flex: 1,
    height: 40,
    marginLeft: 12,
    paddingHorizontal: 8,
    borderWidth: 1,
    borderColor: "#4B5563",
    borderRadius: 4,
    backgroundColor: "#374151",
    color: "#E5E7EB"
  }
});
