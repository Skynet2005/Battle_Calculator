/**
 * Orchestrates state & API; delegates UI to reusable components.
 * NO SECTION ABBREVIATED.
 */

import axios from "axios";
import React, { useEffect, useRef, useState } from "react";
import { ScrollView, Text } from "react-native";

import { styles } from "./styles";
import {
  Class,
  ClassSel,
  Hero,
  SimResult,
} from "./types";

import { ConfigSection } from "./components/ConfigSection";
import { ResultsSection } from "./components/ResultsSection";
import { SideSetup } from "./components/SideSetup";
import { JoinerRow } from "./components/JoinerRow";

/* ─────────────── Main Component ─────────────── */
export default function App() {
  /* data lists */
  const [heroes, setHeroes] = useState<Hero[]>([]);
  const [troops, setTroops] = useState<string[]>([]);

  /* config */
  const [attackType, setAttackType] = useState<"solo" | "rally">("solo");
  const [attackerCapacity, setAttackerCapacity] = useState("185010");
  const [defenderCapacity, setDefenderCapacity] = useState("185010");
  const [sims, setSims] = useState("1");

  /* selections */
  const emptySel: ClassSel = { Infantry: "", Lancer: "", Marksman: "" };
  const [atkH, setAtkH] = useState<ClassSel>(emptySel);
  const [defH, setDefH] = useState<ClassSel>(emptySel);
  const [atkT, setAtkT] = useState<ClassSel>(emptySel);
  const [defT, setDefT] = useState<ClassSel>(emptySel);

  const [atkSupport, setAtkSupport] = useState<string[]>(["", "", "", ""]);
  const [defSupport, setDefSupport] = useState<string[]>(["", "", "", ""]);

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
    Infantry: "0.45",
    Lancer: "0.35",
    Marksman: "0.2",
  });
  const [defRatios, setDefRatios] = useState<{ [cls in Class]: string }>({
    Infantry: "0.6",
    Lancer: "0.4",
    Marksman: "0",
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
    if (attackType === "solo") {
      setAttackerCapacity("185010");
      setDefenderCapacity("185010");
    } else {
      setAttackerCapacity("1377510");
      setDefenderCapacity("1377510");
    }
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
    attackerCapacity: parseInt(attackerCapacity, 10),
    defenderCapacity: parseInt(defenderCapacity, 10),
    sims: parseInt(sims, 10),
    attackerTroops: atkT,
    defenderTroops: defT,
    attackerSupportHeroes:
      attackType === "rally" ? atkSupport.filter((h) => h) : [],
    defenderSupportHeroes:
      attackType === "rally" ? defSupport.filter((h) => h) : [],
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

      {attackType === "rally" && (
        <>
          <Text style={styles.subHeader}>Attacker Joiners</Text>
          {atkSupport.map((sel, idx) => (
            <JoinerRow
              key={`atk-joiner-${idx}`}
              side="atk"
              idx={idx}
              heroes={heroes}
              selected={sel}
              onChange={(v) =>
                setAtkSupport((s) => {
                  const arr = [...s];
                  arr[idx] = v;
                  return arr;
                })
              }
            />
          ))}

          <Text style={styles.subHeader}>Defender Joiners</Text>
          {defSupport.map((sel, idx) => (
            <JoinerRow
              key={`def-joiner-${idx}`}
              side="def"
              idx={idx}
              heroes={heroes}
              selected={sel}
              onChange={(v) =>
                setDefSupport((s) => {
                  const arr = [...s];
                  arr[idx] = v;
                  return arr;
                })
              }
            />
          ))}
        </>
      )}

      {/* config + run */}
      <ConfigSection
        attackType={attackType}
        setAttackType={setAttackType}
        attackerCapacity={attackerCapacity}
        setAttackerCapacity={setAttackerCapacity}
        defenderCapacity={defenderCapacity}
        setDefenderCapacity={setDefenderCapacity}
        sims={sims}
        setSims={setSims}
        onRun={runSim}
      />

      {/* results */}
      {result && <ResultsSection result={result} onRerun={rerunSim} />}
    </ScrollView>
  );
}
