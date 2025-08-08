/**
 * Orchestrates state & API; delegates UI to reusable components.
 * NO SECTION ABBREVIATED.
 */

import axios from "axios";
import React, { useEffect, useRef, useState } from "react";
import { ScrollView, Text, View, useWindowDimensions, ActivityIndicator, Alert, TouchableOpacity } from "react-native";

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
    Infantry: "0.4",
    Lancer: "0.6",
    Marksman: "0",
  });
  const [defRatios, setDefRatios] = useState<{ [cls in Class]: string }>({
    Infantry: "0.6",
    Lancer: "0.4",
    Marksman: "0",
  });

  /* results */
  const [result, setResult] = useState<SimResult | null>(null);
  const lastPayloadRef = useRef<any>(null);
  const [isRunning, setIsRunning] = useState(false);
  const scrollRef = useRef<ScrollView | null>(null);
  const [resultsY, setResultsY] = useState<number | null>(null);

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

  // Created Logic for review: Set default heroes per side once hero list loads
  useEffect(() => {
    if (heroes.length === 0) return;
    const isEmpty = (sel: ClassSel) => !sel.Infantry && !sel.Lancer && !sel.Marksman;

    const buildDefaults = (names: string[]): ClassSel => {
      const next: ClassSel = { Infantry: "", Lancer: "", Marksman: "" };
      names.forEach((name) => {
        const h = heroes.find((x) => x.name.toLowerCase() === name.toLowerCase());
        if (!h) return;
        const clsLower = (h.charClass || "").toLowerCase();
        const cls: Class =
          clsLower === "infantry" ? "Infantry" : clsLower === "lancer" ? "Lancer" : "Marksman";
        next[cls] = h.name;
      });
      return next;
    };

    const resolveHeroName = (name: string) =>
      heroes.find((x) => x.name.toLowerCase() === name.toLowerCase())?.name ?? name;

    if (isEmpty(atkH)) {
      setAtkH(buildDefaults(["Edith", "Gordon", "Hendrik"]));
    }
    if (isEmpty(defH)) {
      setDefH(buildDefaults(["Gatot", "Sonya", "Bradley"]));
    }

    // Created Logic for review: default joiners (attacker → 4 Jessies, defender → 4 Patricks)
    if (atkSupport.every((s) => !s)) {
      const jessie = resolveHeroName("Jessie");
      setAtkSupport([jessie, jessie, jessie, jessie]);
    }
    if (defSupport.every((s) => !s)) {
      const patrick = resolveHeroName("Patrick");
      setDefSupport([patrick, patrick, patrick, patrick]);
    }
  }, [heroes, atkH, defH, atkSupport, defSupport]);

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
  const apiCall = async (payload: any) => {
    // Created Logic for review: run button loading + error surfacing
    try {
      setIsRunning(true);
      const r = await axios.post<SimResult>("http://localhost:8000/api/simulate", payload);
      setResult(r.data);
    } catch (e: any) {
      console.error(e);
      Alert.alert("Sim Error", String(e.response?.data ?? e.message));
      setResult(null);
    } finally {
      setIsRunning(false);
    }
  };

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

  const resetAll = () => {
    // Created Logic for review: reset all selections and results
    setAttackType("solo");
    setAttackerCapacity("185010");
    setDefenderCapacity("185010");
    setSims("1");
    const empty: ClassSel = { Infantry: "", Lancer: "", Marksman: "" };
    setAtkH(empty);
    setDefH(empty);
    setAtkT(empty);
    setDefT(empty);
    setAtkSlots({ Infantry: "1", Lancer: "2", Marksman: "3" });
    setDefSlots({ Infantry: "1", Lancer: "2", Marksman: "3" });
    setAtkRatios({ Infantry: "0.4", Lancer: "0.6", Marksman: "0" });
    setDefRatios({ Infantry: "0.6", Lancer: "0.4", Marksman: "0" });
    setAtkSupport(["", "", "", ""]);
    setDefSupport(["", "", "", ""]);
    setResult(null);
    lastPayloadRef.current = null;
  };

  const swapSides = () => {
    // Created Logic for review: swap attacker and defender selections
    setAtkH(defH);
    setDefH(atkH);
    setAtkT(defT);
    setDefT(atkT);
    setAtkSlots(defSlots);
    setDefSlots(atkSlots);
    setAtkRatios(defRatios);
    setDefRatios(atkRatios);
    setAtkSupport(defSupport);
    setDefSupport(atkSupport);
    // keep capacities identical
  };

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
  const { width } = useWindowDimensions();
  const isSmall = width < 900;

  return (
    <ScrollView ref={scrollRef} style={styles.container} contentContainerStyle={{ paddingBottom: 80 }}>
      <Text style={styles.header}>Battle Simulator</Text>

      <View style={styles.content}>
      {/* quick summary pills */}
      <View style={styles.pillRow}>
        <View style={styles.pill}><Text style={styles.pillText}>{attackType === 'rally' ? 'Rally' : 'Solo'}</Text></View>
        <View style={styles.pill}><Text style={styles.pillText}>Sims: {sims}</Text></View>
        <View style={styles.pill}><Text style={styles.pillText}>Atk Cap: {attackerCapacity}</Text></View>
        <View style={styles.pill}><Text style={styles.pillText}>Def Cap: {defenderCapacity}</Text></View>
        {result && resultsY !== null && (
          <TouchableOpacity
            onPress={() => scrollRef.current?.scrollTo({ y: resultsY!, animated: true })}
            style={[styles.miniButton, { marginLeft: 'auto' }]}
          >
            <Text style={styles.miniButtonText}>Go to Results</Text>
          </TouchableOpacity>
        )}
      </View>
      <View style={isSmall ? styles.twoColStack : styles.twoColRow}>
        {/* Left Column: Attacker */}
        <View style={styles.col}>
          <View style={styles.panel}>
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
            disabled={isRunning}
            capacity={attackerCapacity}
            setCapacity={setAttackerCapacity}
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
                  disabled={isRunning}
                  onChange={(v) =>
                    setAtkSupport((s) => {
                      const arr = [...s];
                      arr[idx] = v;
                      return arr;
                    })
                  }
                />
              ))}
            </>
          )}
          </View>
        </View>

        {/* Right Column: Defender */}
        <View style={styles.col}>
          <View style={styles.panel}>
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
            disabled={isRunning}
            capacity={defenderCapacity}
            setCapacity={setDefenderCapacity}
          />

          {attackType === "rally" && (
            <>
              <Text style={styles.subHeader}>Defender Joiners</Text>
              {defSupport.map((sel, idx) => (
                <JoinerRow
                  key={`def-joiner-${idx}`}
                  side="def"
                  idx={idx}
                  heroes={heroes}
                  selected={sel}
                  disabled={isRunning}
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
          </View>
        </View>
      </View>

      {/* config + run at bottom */}
      <View style={styles.panel}>
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
          isRunning={isRunning}
        />
        <View style={styles.actionsRow}>
          <View style={{ flex: 1 }}>
            <TouchableOpacity onPress={swapSides} style={styles.secondaryButtonContainer}>
              <Text style={styles.buttonText}>Swap Sides</Text>
            </TouchableOpacity>
          </View>
          <View style={{ flex: 1 }}>
            <TouchableOpacity onPress={resetAll} style={styles.dangerButtonContainer}>
              <Text style={styles.buttonText}>Reset</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>

      {/* results */}
      <View onLayout={(e) => setResultsY(e.nativeEvent.layout.y)} />
      {isRunning && (
        <View style={[styles.panel, { alignItems: "center" }]}> 
          <ActivityIndicator size="large" color="#3B82F6" />
          <Text style={{ color: "#E5E7EB", marginTop: 8 }}>Running simulation…</Text>
        </View>
      )}
      {result && <ResultsSection result={result} onRerun={rerunSim} />}

      {/* quick re-run FAB */}
      <View style={styles.fab}>
        <TouchableOpacity onPress={rerunSim} style={styles.fabButton} disabled={isRunning || !lastPayloadRef.current}>
          <Text style={styles.buttonText}>{isRunning ? "Running…" : "Re-Run"}</Text>
        </TouchableOpacity>
      </View>
      </View>
    </ScrollView>
  );
}
