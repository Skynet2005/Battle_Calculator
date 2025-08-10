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
  ChiefGearTotals,
  ChiefCharmsTotals,
  ChiefSkinBonuses,
} from "./types";

import { ConfigSection } from "./components/ConfigSection";
import { ResultsSection } from "./components/ResultsSection";
import { SideSetup } from "./components/SideSetup";
import { JoinerRow } from "./components/JoinerRow";
import { ResearchSection } from "./components/ResearchSection";
import { ProfileSection } from "./components/ProfileSection";

/* ─────────────── Main Component ─────────────── */
export default function App() {
  const [isAuthed, setIsAuthed] = useState<boolean>(false);
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
  // Exclusive Weapon Levels per class (1-10)
  const [atkEwLevels, setAtkEwLevels] = useState<{ [cls in Class]: string }>({
    Infantry: "10",
    Lancer: "10",
    Marksman: "10",
  });
  const [defEwLevels, setDefEwLevels] = useState<{ [cls in Class]: string }>({
    Infantry: "10",
    Lancer: "10",
    Marksman: "10",
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

  // Chief Gear & Charms totals per side
  const [atkGearTotals, setAtkGearTotals] = useState<ChiefGearTotals | null>(null);
  const [defGearTotals, setDefGearTotals] = useState<ChiefGearTotals | null>(null);
  const [atkCharmTotals, setAtkCharmTotals] = useState<ChiefCharmsTotals | null>(null);
  const [defCharmTotals, setDefCharmTotals] = useState<ChiefCharmsTotals | null>(null);
  const [atkResearch, setAtkResearch] = useState<any | null>(null);
  const [defResearch, setDefResearch] = useState<any | null>(null);
  const [atkResearchSel, setAtkResearchSel] = useState<any | null>(null);
  const [defResearchSel, setDefResearchSel] = useState<any | null>(null);
  const [atkGearSel, setAtkGearSel] = useState<Record<string, { tier: string; stars: number }> | null>(null);
  const [defGearSel, setDefGearSel] = useState<Record<string, { tier: string; stars: number }> | null>(null);
  const [atkCharmLvls, setAtkCharmLvls] = useState<Record<string, [number, number, number]> | null>(null);
  const [defCharmLvls, setDefCharmLvls] = useState<Record<string, [number, number, number]> | null>(null);

  // Chief Skin bonuses
  const [atkChiefSkinBonuses, setAtkChiefSkinBonuses] = useState<ChiefSkinBonuses>({
    troops_lethality_pct: 0,
    troops_health_pct: 0,
    troops_defense_pct: 0,
    troops_attack_pct: 0,
  });
  const [defChiefSkinBonuses, setDefChiefSkinBonuses] = useState<ChiefSkinBonuses>({
    troops_lethality_pct: 0,
    troops_health_pct: 0,
    troops_defense_pct: 0,
    troops_attack_pct: 0,
  });

  useEffect(() => {
    // Created Logic for review: capture totals posted from SideSetup sections
    const onMsg = (e: any) => {
      const data = e?.detail || e;
      if (!data || !data.kind) return;
      if (data.kind === 'chief-gear-totals') {
        if (data.side === 'atk') setAtkGearTotals(data.totals);
        else setDefGearTotals(data.totals);
      }
      if (data.kind === 'chief-charms-totals') {
        if (data.side === 'atk') setAtkCharmTotals(data.totals);
        else setDefCharmTotals(data.totals);
      }
    };
    (global as any).addEventListener?.('chief-gear-charms', onMsg);
    (global as any).onChiefGearCharms = onMsg;

    return () => {
      (global as any).removeEventListener?.('chief-gear-charms', onMsg);
      delete (global as any).onChiefGearCharms;
    };
  }, []);

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
    attackerEwLevels: orderEw(atkEwLevels, atkSlots),
    defenderEwLevels: orderEw(defEwLevels, defSlots),
    attackerRatios: numObj(atkRatios),
    defenderRatios: numObj(defRatios),
    attackerCapacity: parseInt(attackerCapacity, 10),
    defenderCapacity: parseInt(defenderCapacity, 10),
    sims: parseInt(sims, 10),
    attackerTroops: atkT,
    defenderTroops: defT,
    // Send class-specific fields so backend can apply per-class without totals
    attackerGear: atkGearTotals
      ? {
          infantry_attack_pct: atkGearTotals.infantry_attack_pct,
          infantry_defense_pct: atkGearTotals.infantry_defense_pct,
          lancer_attack_pct: atkGearTotals.lancer_attack_pct,
          lancer_defense_pct: atkGearTotals.lancer_defense_pct,
          marksman_attack_pct: atkGearTotals.marksman_attack_pct,
          marksman_defense_pct: atkGearTotals.marksman_defense_pct,
        }
      : undefined,
    defenderGear: defGearTotals
      ? {
          infantry_attack_pct: defGearTotals.infantry_attack_pct,
          infantry_defense_pct: defGearTotals.infantry_defense_pct,
          lancer_attack_pct: defGearTotals.lancer_attack_pct,
          lancer_defense_pct: defGearTotals.lancer_defense_pct,
          marksman_attack_pct: defGearTotals.marksman_attack_pct,
          marksman_defense_pct: defGearTotals.marksman_defense_pct,
        }
      : undefined,
    attackerCharms: atkCharmTotals
      ? {
          infantry_lethality_pct: atkCharmTotals.infantry_lethality_pct,
          infantry_health_pct: atkCharmTotals.infantry_health_pct,
          lancer_lethality_pct: atkCharmTotals.lancer_lethality_pct,
          lancer_health_pct: atkCharmTotals.lancer_health_pct,
          marksman_lethality_pct: atkCharmTotals.marksman_lethality_pct,
          marksman_health_pct: atkCharmTotals.marksman_health_pct,
        }
      : undefined,
    defenderCharms: defCharmTotals
      ? {
          infantry_lethality_pct: defCharmTotals.infantry_lethality_pct,
          infantry_health_pct: defCharmTotals.infantry_health_pct,
          lancer_lethality_pct: defCharmTotals.lancer_lethality_pct,
          lancer_health_pct: defCharmTotals.lancer_health_pct,
          marksman_lethality_pct: defCharmTotals.marksman_lethality_pct,
          marksman_health_pct: defCharmTotals.marksman_health_pct,
        }
      : undefined,
    attackerResearch: atkResearch || undefined,
    defenderResearch: defResearch || undefined,
    attackerChiefSkinBonuses: atkChiefSkinBonuses,
    defenderChiefSkinBonuses: defChiefSkinBonuses,
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
    setAtkEwLevels({ Infantry: "10", Lancer: "10", Marksman: "10" });
    setDefEwLevels({ Infantry: "10", Lancer: "10", Marksman: "10" });
    setAtkRatios({ Infantry: "0.4", Lancer: "0.6", Marksman: "0" });
    setDefRatios({ Infantry: "0.6", Lancer: "0.4", Marksman: "0" });
    setAtkSupport(["", "", "", ""]);
    setDefSupport(["", "", "", ""]);
    setResult(null);
    lastPayloadRef.current = null;
    setAtkGearSel(null);
    setDefGearSel(null);
    setAtkCharmLvls(null);
    setDefCharmLvls(null);
    setAtkChiefSkinBonuses({
      troops_lethality_pct: 0,
      troops_health_pct: 0,
      troops_defense_pct: 0,
      troops_attack_pct: 0,
    });
    setDefChiefSkinBonuses({
      troops_lethality_pct: 0,
      troops_health_pct: 0,
      troops_defense_pct: 0,
      troops_attack_pct: 0,
    });
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
    setAtkEwLevels(defEwLevels);
    setDefEwLevels(atkEwLevels);
    setAtkChiefSkinBonuses(defChiefSkinBonuses);
    setDefChiefSkinBonuses(atkChiefSkinBonuses);
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
  const orderEw = (ew: { [cls in Class]: string }, slots: { [cls in Class]: string }) => {
    const arr = [0, 0, 0];
    (Object.keys(slots) as Class[]).forEach((cls) => {
      const idx = parseInt(slots[cls], 10) - 1;
      const lvl = Math.max(1, Math.min(10, parseInt(ew[cls] || "10", 10) || 10));
      arr[idx] = lvl;
    });
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
      {/* Splash Login/Register gate */}
      {!isAuthed && (
        <View style={[styles.panel, { marginBottom: 12 }]}> 
          <Text style={styles.subHeader}>Welcome</Text>
          <Text style={styles.helperText}>Please Login or Register to continue.</Text>
          <ProfileSection
            minimal
            collectSettings={() => ({} as any)}
            applySettings={() => {}}
            onAuthChange={(a) => setIsAuthed(!!(a && a.token))}
          />
        </View>
      )}

      {isAuthed && (
      <ProfileSection
        collectSettings={() => ({
          attackType,
          attackerCapacity,
          defenderCapacity,
          sims,
          atkH,
          defH,
          atkT,
          defT,
          atkSlots,
          defSlots,
          atkEwLevels,
          defEwLevels,
          atkRatios,
          defRatios,
          atkSupport,
          defSupport,
          atkResearch,
          defResearch,
          atkResearchSelection: atkResearchSel || undefined,
          defResearchSelection: defResearchSel || undefined,
          atkGearSelection: atkGearSel || undefined,
          defGearSelection: defGearSel || undefined,
          atkCharmLevels: atkCharmLvls || undefined,
          defCharmLevels: defCharmLvls || undefined,
          atkChiefSkinBonuses,
          defChiefSkinBonuses,
        })}
        applySettings={(d) => {
          setAttackType(d.attackType);
          setAttackerCapacity(d.attackerCapacity);
          setDefenderCapacity(d.defenderCapacity);
          setSims(d.sims);
          setAtkH(d.atkH);
          setDefH(d.defH);
          setAtkT(d.atkT);
          setDefT(d.defT);
          setAtkSlots(d.atkSlots);
          setDefSlots(d.defSlots);
          setAtkEwLevels(d.atkEwLevels);
          setDefEwLevels(d.defEwLevels);
          setAtkRatios(d.atkRatios);
          setDefRatios(d.defRatios);
          setAtkSupport(d.atkSupport);
          setDefSupport(d.defSupport);
          setAtkResearch(d.atkResearch ?? null);
          setDefResearch(d.defResearch ?? null);
          if (d.atkResearchSelection) setAtkResearchSel(d.atkResearchSelection);
          if (d.defResearchSelection) setDefResearchSel(d.defResearchSelection);
          if (d.atkGearSelection) setAtkGearSel(d.atkGearSelection);
          if (d.defGearSelection) setDefGearSel(d.defGearSelection);
          if (d.atkCharmLevels) setAtkCharmLvls(d.atkCharmLevels);
          if (d.defCharmLevels) setDefCharmLvls(d.defCharmLevels);
          if (d.atkChiefSkinBonuses) setAtkChiefSkinBonuses(d.atkChiefSkinBonuses);
          if (d.defChiefSkinBonuses) setDefChiefSkinBonuses(d.defChiefSkinBonuses);
        }}
        onAuthChange={(a) => setIsAuthed(!!(a && a.token))}
      />)}
      {isAuthed && (
      <View style={[styles.panel, { marginBottom: 12 }]}> 
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
          hideRunButton
        />
      </View>)}
      
      {isAuthed && (
      <View style={isSmall ? styles.twoColStack : styles.twoColRow}>
        <View style={styles.col}>
          <ResearchSection side="atk" onChange={(b) => setAtkResearch(b)} onSelectionChange={(rows)=> setAtkResearchSel(rows)} value={atkResearchSel} />
        </View>
        <View style={styles.col}>
          <ResearchSection side="def" onChange={(b) => setDefResearch(b)} onSelectionChange={(rows)=> setDefResearchSel(rows)} value={defResearchSel} />
        </View>
      </View>)}

      {isAuthed && (
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
            ewLevelSel={atkEwLevels}
            setHeroSel={setAtkH}
            setTroopSel={setAtkT}
            setSlotSel={setAtkSlots}
            setRatioSel={setAtkRatios}
            setEwLevelSel={setAtkEwLevels}
            disabled={isRunning}
            capacity={attackerCapacity}
            setCapacity={setAttackerCapacity}
            gearSelection={atkGearSel || undefined}
            onGearSelectionChange={(m) => setAtkGearSel(m)}
            charmLevels={atkCharmLvls || undefined}
            onCharmLevelsChange={(m) => setAtkCharmLvls(m)}
            chiefSkinBonuses={atkChiefSkinBonuses}
            onChiefSkinBonusesChange={setAtkChiefSkinBonuses}
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
            ewLevelSel={defEwLevels}
            setHeroSel={setDefH}
            setTroopSel={setDefT}
            setSlotSel={setDefSlots}
            setRatioSel={setDefRatios}
            setEwLevelSel={setDefEwLevels}
            disabled={isRunning}
            capacity={defenderCapacity}
            setCapacity={setDefenderCapacity}
            gearSelection={defGearSel || undefined}
            onGearSelectionChange={(m) => setDefGearSel(m)}
            charmLevels={defCharmLvls || undefined}
            onCharmLevelsChange={(m) => setDefCharmLvls(m)}
            chiefSkinBonuses={defChiefSkinBonuses}
            onChiefSkinBonusesChange={setDefChiefSkinBonuses}
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
      </View>)}

      {isAuthed && (
      <View style={[styles.panel, { marginTop: 12 }]}>
        <TouchableOpacity onPress={runSim} disabled={!!isRunning} style={[styles.buttonContainer, isRunning && styles.disabledButton]}>
          <Text style={styles.buttonText}>{isRunning ? "Running…" : "Run Simulation"}</Text>
        </TouchableOpacity>
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
      </View>)}

      {isAuthed && (<View onLayout={(e) => setResultsY(e.nativeEvent.layout.y)} />)}
      {isAuthed && isRunning && (
        <View style={[styles.panel, { alignItems: "center" }]}> 
          <ActivityIndicator size="large" color="#3B82F6" />
          <Text style={{ color: "#E5E7EB", marginTop: 8 }}>Running simulation…</Text>
        </View>
      )}
      {isAuthed && result && <ResultsSection result={result} onRerun={rerunSim} />}

      {isAuthed && (
      <View style={styles.fab}>
        <TouchableOpacity onPress={rerunSim} style={styles.fabButton} disabled={isRunning || !lastPayloadRef.current}>
          <Text style={styles.buttonText}>{isRunning ? "Running…" : "Re-Run"}</Text>
        </TouchableOpacity>
      </View>)}
      </View>
    </ScrollView>
  );
}
