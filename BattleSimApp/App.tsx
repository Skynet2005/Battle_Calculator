/**
 * Orchestrates state & API; delegates UI to reusable components.
 * NO SECTION ABBREVIATED.
 */

import { Picker } from "@react-native-picker/picker";
import axios from "axios";
import React, { useEffect, useRef, useState } from "react";
import { ScrollView, Text } from "react-native";

import { styles } from "./styles";
import {
  Hero,
  ClassSel,
  SimResult,
  Class,
} from "./types";

import { SideSetup } from "./components/SideSetup";
import { ConfigSection } from "./components/ConfigSection";
import { ResultsSection } from "./components/ResultsSection";

/* ─────────────── Main Component ─────────────── */
export default function App() {
  /* data lists */
  const [heroes, setHeroes] = useState<Hero[]>([]);
  const [troops, setTroops] = useState<string[]>([]);

  /* config */
  const [attackType, setAttackType] = useState<"solo" | "rally">("solo");
  const [capacity, setCapacity] = useState("185010");
  const [sims, setSims] = useState("1");

  /* selections */
  const emptySel: ClassSel = { Infantry: "", Lancer: "", Marksman: "" };
  const [atkH, setAtkH] = useState<ClassSel>(emptySel);
  const [defH, setDefH] = useState<ClassSel>(emptySel);
  const [atkT, setAtkT] = useState<ClassSel>(emptySel);
  const [defT, setDefT] = useState<ClassSel>(emptySel);

  const [atkSlots, setAtkSlots] = useState<{ [cls in Class]: string }>({
    Infantry: "1",
    Lancer: "2",
    Marksman: "3",
  });
  const [defSlots, setDefSlots] = useState<{ [cls in Class]: string }>({
    Infantry: "1",
    Lancer: "2",
    Marksman: "3",
  });
  const [atkRatios, setAtkRatios] = useState<{ [cls in Class]: string }>({
    Infantry: "0.5",
    Lancer: "0.3",
    Marksman: "0.2",
  });
  const [defRatios, setDefRatios] = useState<{ [cls in Class]: string }>({
    Infantry: "0.5",
    Lancer: "0.3",
    Marksman: "0.2",
  });

  /* results */
  const [result, setResult] = useState<SimResult | null>(null);
  const lastPayloadRef = useRef<any>(null);

  /* -------------- fetch lists -------------- */
  useEffect(() => {
    axios
      .get<Hero[]>("http://localhost:8000/api/heroes")
      .then((res) => setHeroes(res.data))
      .catch((e) => console.error(e));

    axios
      .get<string[]>("http://localhost:8000/api/troops")
      .then((res) => setTroops(res.data))
      .catch((e) => console.error(e));
  }, []);

  useEffect(() => {
    setCapacity(attackType === "solo" ? "185010" : "1377510");
  }, [attackType]);

  /* -------------- API helpers -------------- */
  const apiCall = (payload: any) =>
    axios
      .post<SimResult>("http://localhost:8000/api/simulate", payload)
      .then((r) => setResult(r.data))
      .catch((e) => {
        console.error(e);
        alert("Sim Error: " + (e.response?.data ?? e.message));
        setResult(null);
      });

  const buildPayload = () => ({
    attackerHeroes: orderHeroes(atkH, atkSlots),
    defenderHeroes: orderHeroes(defH, defSlots),
    attackerRatios: numObj(atkRatios),
    defenderRatios: numObj(defRatios),
    totalCapacity: parseInt(capacity, 10),
    sims: parseInt(sims, 10),
    attackerTroops: atkT,
    defenderTroops: defT,
  });

  const runSim = () => {
    const payload = buildPayload();
    lastPayloadRef.current = payload;
    apiCall(payload);
  };
  const rerunSim = () =>
    lastPayloadRef.current && apiCall(lastPayloadRef.current);

  /* helpers */
  const orderHeroes = (sel: ClassSel, slots: { [cls in Class]: string }) => {
    const arr = ["", "", ""];
    (Object.keys(slots) as Class[]).forEach(
      (cls) => (arr[parseInt(slots[cls], 10) - 1] = sel[cls])
    );
    return arr;
  };
  const numObj = (o: { [cls in Class]: string }) =>
    Object.fromEntries(
      (Object.keys(o) as Class[]).map((k) => [k, parseFloat(o[k])])
    );

  /* -------------- JSX -------------- */
  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={{ paddingBottom: 40 }}
    >
      <Text style={styles.header}>Battle Simulator</Text>

      {/* attacker & defender setups */}
      <Text style={styles.subHeader}>Attacker Setup</Text>
      <SideSetup
        side="atk"
        heroes={heroes}
        troops={troops}
        heroSel={atkH}
        troopSel={atkT}
        slotSel={atkSlots}
        ratioSel={atkRatios}
        setHeroSel={setAtkH}
        setTroopSel={setAtkT}
        setSlotSel={setAtkSlots}
        setRatioSel={setAtkRatios}
      />

      <Text style={styles.subHeader}>Defender Setup</Text>
      <SideSetup
        side="def"
        heroes={heroes}
        troops={troops}
        heroSel={defH}
        troopSel={defT}
        slotSel={defSlots}
        ratioSel={defRatios}
        setHeroSel={setDefH}
        setTroopSel={setDefT}
        setSlotSel={setDefSlots}
        setRatioSel={setDefRatios}
      />

      {/* config + run */}
      <ConfigSection
        attackType={attackType}
        setAttackType={setAttackType}
        capacity={capacity}
        setCapacity={setCapacity}
        sims={sims}
        setSims={setSims}
        onRun={runSim}
      />

      {/* results */}
      {result && <ResultsSection result={result} onRerun={rerunSim} />}
    </ScrollView>
  );
}
