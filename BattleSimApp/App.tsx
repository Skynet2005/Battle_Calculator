/**
 * Minimal, responsive app shell that pairs with the updated styles/components.
 * Fully self-contained and compatible with the new responsive UI primitives.
 */

import React from "react";
import axios from "axios";
import { Alert, ScrollView, Text, View } from "react-native";
import { styles, setTheme } from "./styles";
import type {
  Class, ClassSel, Hero, SimResult,
  ChiefGearTotals, ChiefCharmsTotals,
  ChiefSkinBonuses, DaybreakBonuses,
  ResearchSelection, ResearchBuffs,
  ChiefGearSelectionMap, ChiefCharmLevelsMap,
  SavedSettingsData, HeroGearSelectionByClass, AuthState
} from "./types";

import { ConfigSection } from "./components/ConfigSection";
import { SideSetup } from "./components/SideSetup";
import { ResultsSection } from "./components/ResultsSection";
import { TopBar } from "./components/TopBar";
import { ProfileModal } from "./components/ProfileModal";
import { CollapsibleSection } from "./components/CollapsibleSection";

export default function App() {
  // Theme + Profile
  const [isDark, setIsDark] = React.useState(true);
  const [profileOpen, setProfileOpen] = React.useState(false);
  const [auth, setAuth] = React.useState<AuthState>({ token: null, username: null });

  /* data lists */
  const [heroes, setHeroes] = React.useState<Hero[]>([]);
  const [troops, setTroops] = React.useState<string[]>([]);
  
  // Created Logic for review: separate filtered data by class for better organization
  const [heroesByClass, setHeroesByClass] = React.useState<{ [cls in Class]: Hero[] }>({
    Infantry: [],
    Lancer: [],
    Marksman: []
  });
  const [troopsByClass, setTroopsByClass] = React.useState<{ [cls in Class]: string[] }>({
    Infantry: [],
    Lancer: [],
    Marksman: []
  });

  /* config */
  const [attackType, setAttackType] = React.useState<"solo" | "rally">("solo");
  const [attackerCapacity, setAttackerCapacity] = React.useState("185010");
  const [defenderCapacity, setDefenderCapacity] = React.useState("185010");
  const [sims, setSims] = React.useState("1");

  /* selections */
  const emptySel: ClassSel = { Infantry: "", Lancer: "", Marksman: "" };
  const [atkH, setAtkH] = React.useState<ClassSel>({ Infantry: "Edith", Lancer: "Gordon", Marksman: "Hendrik" });
  const [defH, setDefH] = React.useState<ClassSel>({ Infantry: "Gatot", Lancer: "Sonya", Marksman: "Bradley" });
  const [atkT, setAtkT] = React.useState<ClassSel>({ Infantry: "Helios Infantry (FC10)", Lancer: "Helios Lancer (FC10)", Marksman: "Helios Marksman (FC10)" });
  const [defT, setDefT] = React.useState<ClassSel>({ Infantry: "Helios Infantry (FC10)", Lancer: "Helios Lancer (FC10)", Marksman: "Helios Marksman (FC10)" });
  const [atkSlots, setAtkSlots] = React.useState<{ [cls in Class]: string }>({ Infantry: "1", Lancer: "2", Marksman: "3" });
  const [defSlots, setDefSlots] = React.useState<{ [cls in Class]: string }>({ Infantry: "1", Lancer: "2", Marksman: "3" });
  const [atkEw, setAtkEw] = React.useState<{ [cls in Class]: string }>({ Infantry: "10", Lancer: "10", Marksman: "10" });
  const [defEw, setDefEw] = React.useState<{ [cls in Class]: string }>({ Infantry: "10", Lancer: "10", Marksman: "10" });
  const [atkRatios, setAtkRatios] = React.useState<{ [cls in Class]: string }>({ Infantry: "0.4", Lancer: "0.6", Marksman: "0" });
  const [defRatios, setDefRatios] = React.useState<{ [cls in Class]: string }>({ Infantry: "0.6", Lancer: "0.4", Marksman: "0" });

  /* chief gear + charms totals */
  const [atkGearTotals, setAtkGearTotals] = React.useState<ChiefGearTotals | null>(null);
  const [defGearTotals, setDefGearTotals] = React.useState<ChiefGearTotals | null>(null);
  const [atkCharmTotals, setAtkCharmTotals] = React.useState<ChiefCharmsTotals | null>(null);
  const [defCharmTotals, setDefCharmTotals] = React.useState<ChiefCharmsTotals | null>(null);

  // Persisted selections for Chief Gear & Charms (per side)
  const [atkGearSel, setAtkGearSel] = React.useState<ChiefGearSelectionMap | undefined>(undefined);
  const [defGearSel, setDefGearSel] = React.useState<ChiefGearSelectionMap | undefined>(undefined);
  const [atkCharmLvls, setAtkCharmLvls] = React.useState<ChiefCharmLevelsMap | undefined>(undefined);
  const [defCharmLvls, setDefCharmLvls] = React.useState<ChiefCharmLevelsMap | undefined>(undefined);

  /* research */
  const [atkResearchBuffs, setAtkResearchBuffs] = React.useState<ResearchBuffs | null>(null);
  const [defResearchBuffs, setDefResearchBuffs] = React.useState<ResearchBuffs | null>(null);
  const [atkResearchSel, setAtkResearchSel] = React.useState<ResearchSelection | null>(null);
  const [defResearchSel, setDefResearchSel] = React.useState<ResearchSelection | null>(null);

  /* chief skin bonuses */
  const [atkSkin, setAtkSkin] = React.useState<ChiefSkinBonuses>({ troops_lethality_pct: 0, troops_health_pct: 0, troops_defense_pct: 0, troops_attack_pct: 0 });
  const [defSkin, setDefSkin] = React.useState<ChiefSkinBonuses>({ troops_lethality_pct: 0, troops_health_pct: 0, troops_defense_pct: 0, troops_attack_pct: 0 });

  /* daybreak bonuses */
  const [atkDaybreak, setAtkDaybreak] = React.useState<DaybreakBonuses>({
    infantry_attack_pct: 0, infantry_defense_pct: 0, lancer_attack_pct: 0, lancer_defense_pct: 0,
    marksman_attack_pct: 0, marksman_defense_pct: 0, troops_attack_pct: 0, troops_defense_pct: 0, 
    troops_lethality_pct: 0, troops_health_pct: 0,
  });
  const [defDaybreak, setDefDaybreak] = React.useState<DaybreakBonuses>({
    infantry_attack_pct: 0, infantry_defense_pct: 0, lancer_attack_pct: 0, lancer_defense_pct: 0,
    marksman_attack_pct: 0, marksman_defense_pct: 0, troops_attack_pct: 0, troops_defense_pct: 0, 
    troops_lethality_pct: 0, troops_health_pct: 0,
  });

  /* support heroes (joiners) for rally */
  const [atkSupportHeroes, setAtkSupportHeroes] = React.useState<string[]>(["Jessie", "Jessie", "Jessie", "Jessie"]);
  const [defSupportHeroes, setDefSupportHeroes] = React.useState<string[]>(["Patrick", "Patrick", "Patrick", "Patrick"]);

  /* hero gear totals (legendary/mythic); optional */
  const [atkHeroGearTotals, setAtkHeroGearTotals] = React.useState<any | null>(null);
  const [defHeroGearTotals, setDefHeroGearTotals] = React.useState<any | null>(null);
  /* hero gear selections (legendary/mythic) */
  const [atkHeroGearSel, setAtkHeroGearSel] = React.useState<HeroGearSelectionByClass>({
    Infantry: {
      goggles: { type: "Infantry", level: 200, essence_level: 20 },
      boot: { type: "Infantry", level: 200, essence_level: 20 },
      glove: { type: "Infantry", level: 200, essence_level: 20 },
      belt: { type: "Infantry", level: 200, essence_level: 20 },
    },
    Lancer: {
      goggles: { type: "Lancer", level: 200, essence_level: 20 },
      boot: { type: "Lancer", level: 200, essence_level: 20 },
      glove: { type: "Lancer", level: 200, essence_level: 20 },
      belt: { type: "Lancer", level: 200, essence_level: 20 },
    },
    Marksman: {
      goggles: { type: "Marksman", level: 200, essence_level: 20 },
      boot: { type: "Marksman", level: 200, essence_level: 20 },
      glove: { type: "Marksman", level: 200, essence_level: 20 },
      belt: { type: "Marksman", level: 200, essence_level: 20 },
    },
  });
  const [defHeroGearSel, setDefHeroGearSel] = React.useState<HeroGearSelectionByClass>({
    Infantry: {
      goggles: { type: "Infantry", level: 200, essence_level: 20 },
      boot: { type: "Infantry", level: 200, essence_level: 20 },
      glove: { type: "Infantry", level: 200, essence_level: 20 },
      belt: { type: "Infantry", level: 200, essence_level: 20 },
    },
    Lancer: {
      goggles: { type: "Lancer", level: 200, essence_level: 20 },
      boot: { type: "Lancer", level: 200, essence_level: 20 },
      glove: { type: "Lancer", level: 200, essence_level: 20 },
      belt: { type: "Lancer", level: 200, essence_level: 20 },
    },
    Marksman: {
      goggles: { type: "Marksman", level: 200, essence_level: 20 },
      boot: { type: "Marksman", level: 200, essence_level: 20 },
      glove: { type: "Marksman", level: 200, essence_level: 20 },
      belt: { type: "Marksman", level: 200, essence_level: 20 },
    },
  });

  /* results */
  const [result, setResult] = React.useState<SimResult | null>(null);
  const [isRunning, setIsRunning] = React.useState(false);
  const lastPayloadRef = React.useRef<any>(null);

  // Listen for chief gear/charm totals posted from sections
  React.useEffect(() => {
    const onMsg = (e: any) => {
      const d = e?.detail || e;
      if (!d || !d.kind) return;
      if (d.kind === "chief-gear-totals") {
        if (d.side === "atk") setAtkGearTotals(d.totals);
        else setDefGearTotals(d.totals);
      } else if (d.kind === "chief-charms-totals") {
        if (d.side === "atk") setAtkCharmTotals(d.totals);
        else setDefCharmTotals(d.totals);
      } else if (d.kind === "hero-gear-totals") {
        if (d.side === "atk") setAtkHeroGearTotals(d.totals);
        else setDefHeroGearTotals(d.totals);
      }
    };
    (global as any).addEventListener?.("chief-gear-charms", onMsg);
    (global as any).onChiefGearCharms = onMsg;
    return () => {
      (global as any).removeEventListener?.("chief-gear-charms", onMsg);
      delete (global as any).onChiefGearCharms;
    };
  }, []);

  // fetch lists
  React.useEffect(() => {
    // Fetch all heroes and troops for backward compatibility
    axios.get<Hero[]>("http://localhost:8000/api/heroes").then(r => setHeroes(r.data)).catch(()=>{});
    axios.get<string[]>("http://localhost:8000/api/troops").then(r => setTroops(r.data)).catch(()=>{});
    
    // Fetch filtered data by class
    const fetchFilteredData = async () => {
      try {
        const [infantryHeroes, lancerHeroes, marksmanHeroes] = await Promise.all([
          axios.get<Hero[]>("http://localhost:8000/api/heroes/Infantry"),
          axios.get<Hero[]>("http://localhost:8000/api/heroes/Lancer"),
          axios.get<Hero[]>("http://localhost:8000/api/heroes/Marksman")
        ]);
        
        const [infantryTroops, lancerTroops, marksmanTroops] = await Promise.all([
          axios.get<string[]>("http://localhost:8000/api/troops/Infantry"),
          axios.get<string[]>("http://localhost:8000/api/troops/Lancer"),
          axios.get<string[]>("http://localhost:8000/api/troops/Marksman")
        ]);
        
        setHeroesByClass({
          Infantry: infantryHeroes.data,
          Lancer: lancerHeroes.data,
          Marksman: marksmanHeroes.data
        });
        
        setTroopsByClass({
          Infantry: infantryTroops.data,
          Lancer: lancerTroops.data,
          Marksman: marksmanTroops.data
        });
      } catch (error) {
        console.error("Error fetching filtered data:", error);
      }
    };
    
    fetchFilteredData();
  }, []);

  // helpers
  const orderHeroes = (sel: ClassSel, slots: { [cls in Class]: string }) => {
    const arr = ["", "", ""];
    (Object.keys(slots) as Class[]).forEach((cls) => { arr[parseInt(slots[cls], 10) - 1] = sel[cls]; });
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
    Object.fromEntries((Object.keys(o) as Class[]).map((k) => [k, parseFloat(o[k])]));

  // Remove nested breakdown objects before sending to API
  const flattenTotals = (totals: any | null | undefined) => {
    if (!totals) return undefined;
    const { breakdown, ...rest } = totals as any;
    return rest;
  };

  const buildPayload = () => ({
    attackerHeroes: orderHeroes(atkH, atkSlots),
    defenderHeroes: orderHeroes(defH, defSlots),
    attackerEwLevels: orderEw(atkEw, atkSlots),
    defenderEwLevels: orderEw(defEw, defSlots),
    attackerRatios: numObj(atkRatios),
    defenderRatios: numObj(defRatios),
    attackerCapacity: parseInt(attackerCapacity, 10),
    defenderCapacity: parseInt(defenderCapacity, 10),
    sims: parseInt(sims, 10),
    attackerTroops: atkT,
    defenderTroops: defT,
    attackerGear: flattenTotals(atkGearTotals),
    defenderGear: flattenTotals(defGearTotals),
    attackerCharms: flattenTotals(atkCharmTotals),
    defenderCharms: flattenTotals(defCharmTotals),
    attackerResearch: atkResearchBuffs || undefined,
    defenderResearch: defResearchBuffs || undefined,
    attackerChiefSkinBonuses: atkSkin,
    defenderChiefSkinBonuses: defSkin,
    attackerDaybreakBonuses: atkDaybreak,
    defenderDaybreakBonuses: defDaybreak,
    attackerHeroGear: atkHeroGearTotals || undefined,
    defenderHeroGear: defHeroGearTotals || undefined,
    attackerSupportHeroes: atkSupportHeroes.filter(h => h !== ""),
    defenderSupportHeroes: defSupportHeroes.filter(h => h !== ""),
  });

  const runSim = async () => {
    try {
      setIsRunning(true);
      // Created Logic for review: ensure City Buff totals (gear/charms) are computed before sim
      const ensureCityTotals = async () => {
        const gearSlots: Array<keyof ChiefGearSelectionMap> = ["Cap", "Coat", "Ring", "Watch", "Pants", "Weapon"] as any;
        const mkItems = (sel?: any) =>
          gearSlots
            .filter((s) => sel && sel[s] && sel[s].tier)
            .map((s) => ({ item: s, tier: sel[s].tier, stars: sel[s].stars ?? 0 }));

        // Normalize hero gear selection to API request shape
        // Ensure that stacking is always "additive" regardless of input
        const normalizeHeroGear = (sel: any) => ({
          infantry: {
            goggles: {
              level: sel?.Infantry?.goggles?.level ?? 200,
              essence_level: sel?.Infantry?.goggles?.essence_level ?? 20,
              stacking: "additive",
            },
            boot: {
              level: sel?.Infantry?.boot?.level ?? 200,
              essence_level: sel?.Infantry?.boot?.essence_level ?? 20,
              stacking: "additive",
            },
            glove: {
              level: sel?.Infantry?.glove?.level ?? 200,
              essence_level: sel?.Infantry?.glove?.essence_level ?? 20,
              stacking: "additive",
            },
            belt: {
              level: sel?.Infantry?.belt?.level ?? 200,
              essence_level: sel?.Infantry?.belt?.essence_level ?? 20,
              stacking: "additive",
            },
          },
          lancer: {
            goggles: {
              level: sel?.Lancer?.goggles?.level ?? 200,
              essence_level: sel?.Lancer?.goggles?.essence_level ?? 20,
              stacking: "additive",
            },
            boot: {
              level: sel?.Lancer?.boot?.level ?? 200,
              essence_level: sel?.Lancer?.boot?.essence_level ?? 20,
              stacking: "additive",
            },
            glove: {
              level: sel?.Lancer?.glove?.level ?? 200,
              essence_level: sel?.Lancer?.glove?.essence_level ?? 20,
              stacking: "additive",
            },
            belt: {
              level: sel?.Lancer?.belt?.level ?? 200,
              essence_level: sel?.Lancer?.belt?.essence_level ?? 20,
              stacking: "additive",
            },
          },
          marksman: {
            goggles: {
              level: sel?.Marksman?.goggles?.level ?? 200,
              essence_level: sel?.Marksman?.goggles?.essence_level ?? 20,
              stacking: "additive",
            },
            boot: {
              level: sel?.Marksman?.boot?.level ?? 200,
              essence_level: sel?.Marksman?.boot?.essence_level ?? 20,
              stacking: "additive",
            },
            glove: {
              level: sel?.Marksman?.glove?.level ?? 200,
              essence_level: sel?.Marksman?.glove?.essence_level ?? 20,
              stacking: "additive",
            },
            belt: {
              level: sel?.Marksman?.belt?.level ?? 200,
              essence_level: sel?.Marksman?.belt?.essence_level ?? 20,
              stacking: "additive",
            },
          },
        });

        const promises: Promise<any>[] = [];
        // Attacker gear totals
        if (!atkGearTotals && atkGearSel && mkItems(atkGearSel).length === gearSlots.length) {
          promises.push(
            axios.post("http://localhost:8000/api/gear/chief/calc", { items: mkItems(atkGearSel) })
              .then((r) => setAtkGearTotals(r.data))
              .catch(()=>{})
          );
        }
        // Defender gear totals
        if (!defGearTotals && defGearSel && mkItems(defGearSel).length === gearSlots.length) {
          promises.push(
            axios.post("http://localhost:8000/api/gear/chief/calc", { items: mkItems(defGearSel) })
              .then((r) => setDefGearTotals(r.data))
              .catch(()=>{})
          );
        }

        // Charms require levels_by_slot with 3 entries per slot
        const fullCharm = (lv: any) => {
          if (!lv) return false;
          return ["Cap","Coat","Ring","Watch","Pants","Weapon"].every((s) => Array.isArray(lv[s]) && lv[s].length === 3 && lv[s].every((n: any)=> (n||0) > 0));
        };
        if (!atkCharmTotals && fullCharm(atkCharmLvls)) {
          promises.push(
            axios.post("http://localhost:8000/api/gear/chief/charms/calc", { levels_by_slot: atkCharmLvls })
              .then((r) => setAtkCharmTotals(r.data))
              .catch(()=>{})
          );
        }
        if (!defCharmTotals && fullCharm(defCharmLvls)) {
          promises.push(
            axios.post("http://localhost:8000/api/gear/chief/charms/calc", { levels_by_slot: defCharmLvls })
              .then((r) => setDefCharmTotals(r.data))
              .catch(()=>{})
          );
        }

        // Hero gear (legendary/mythic) totals
        if (!atkHeroGearTotals && atkHeroGearSel) {
          promises.push(
            axios.post("http://localhost:8000/api/hero-gear/calc", normalizeHeroGear(atkHeroGearSel))
              .then((r) => setAtkHeroGearTotals(r.data))
              .catch(()=>{})
          );
        }
        if (!defHeroGearTotals && defHeroGearSel) {
          promises.push(
            axios.post("http://localhost:8000/api/hero-gear/calc", normalizeHeroGear(defHeroGearSel))
              .then((r) => setDefHeroGearTotals(r.data))
              .catch(()=>{})
          );
        }
        if (promises.length) {
          await Promise.all(promises);
        }
      };

      await ensureCityTotals();
      const payload = buildPayload();
      lastPayloadRef.current = payload;
      const r = await axios.post<SimResult>("http://localhost:8000/api/simulate", payload);
      setResult(r.data);
    } catch (e: any) {
      Alert.alert("Simulation Error", e?.response?.data?.detail || e?.message || "Unknown error");
    } finally {
      setIsRunning(false);
    }
  };
  const rerun = () => lastPayloadRef.current && runSim();

  // auto capacity when attackType toggles
  React.useEffect(() => {
    if (attackType === "solo") { 
      setAttackerCapacity("185010"); 
      setDefenderCapacity("185010");
      // Reset support heroes for solo mode
      setAtkSupportHeroes(["", "", "", ""]);
      setDefSupportHeroes(["", "", "", ""]);
    }
    else { 
      setAttackerCapacity("1377510"); 
      setDefenderCapacity("1377510");
      // Restore default support heroes for rally mode
      setAtkSupportHeroes(["Jessie", "Jessie", "Jessie", "Jessie"]);
      setDefSupportHeroes(["Patrick", "Patrick", "Patrick", "Patrick"]);
    }
  }, [attackType]);

  const toggleTheme = () => {
    const next = !isDark;
    setIsDark(next);
    setTheme(next ? "dark" : "light");
  };

  // Profile save/load helpers
  const collectSettings = (): SavedSettingsData => ({
    // Created Logic for review
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
    atkEwLevels: atkEw,
    defEwLevels: defEw,
    atkRatios,
    defRatios,
    atkSupport: atkSupportHeroes,
    defSupport: defSupportHeroes,
    atkResearch: atkResearchBuffs,
    defResearch: defResearchBuffs,
    atkResearchSelection: atkResearchSel,
    defResearchSelection: defResearchSel,
    atkGearSelection: atkGearSel || null,
    defGearSelection: defGearSel || null,
    atkCharmLevels: atkCharmLvls || null,
    defCharmLevels: defCharmLvls || null,
    atkChiefSkinBonuses: atkSkin,
    defChiefSkinBonuses: defSkin,
    atkDaybreakBonuses: atkDaybreak,
    defDaybreakBonuses: defDaybreak,
    atkHeroGearSelection: atkHeroGearSel,
    defHeroGearSelection: defHeroGearSel,
  });

  const applySettings = (d: SavedSettingsData) => {
    try {
      setAttackType(d.attackType ?? attackType);
      setAttackerCapacity(String(d.attackerCapacity ?? attackerCapacity));
      setDefenderCapacity(String(d.defenderCapacity ?? defenderCapacity));
      setSims(String(d.sims ?? sims));
      setAtkH(d.atkH ?? atkH);
      setDefH(d.defH ?? defH);
      setAtkT(d.atkT ?? atkT);
      setDefT(d.defT ?? defT);
      setAtkSlots(d.atkSlots ?? atkSlots);
      setDefSlots(d.defSlots ?? defSlots);
      setAtkEw(d.atkEwLevels ?? atkEw);
      setDefEw(d.defEwLevels ?? defEw);
      setAtkRatios(d.atkRatios ?? atkRatios);
      setDefRatios(d.defRatios ?? defRatios);
      setAtkSupportHeroes(d.atkSupport ?? atkSupportHeroes);
      setDefSupportHeroes(d.defSupport ?? defSupportHeroes);
      setAtkResearchSel(d.atkResearchSelection ?? atkResearchSel);
      setDefResearchSel(d.defResearchSelection ?? defResearchSel);
      setAtkResearchBuffs((d as any).atkResearch ?? atkResearchBuffs);
      setDefResearchBuffs((d as any).defResearch ?? defResearchBuffs);
      setAtkGearSel(d.atkGearSelection ?? atkGearSel);
      setDefGearSel(d.defGearSelection ?? defGearSel);
      setAtkCharmLvls(d.atkCharmLevels ?? atkCharmLvls);
      setDefCharmLvls(d.defCharmLevels ?? defCharmLvls);
      setAtkSkin(d.atkChiefSkinBonuses ?? atkSkin);
      setDefSkin(d.defChiefSkinBonuses ?? defSkin);
      if (d.atkDaybreakBonuses) setAtkDaybreak(d.atkDaybreakBonuses);
      if (d.defDaybreakBonuses) setDefDaybreak(d.defDaybreakBonuses);
      setAtkHeroGearSel(d.atkHeroGearSelection ?? atkHeroGearSel);
      setDefHeroGearSel(d.defHeroGearSelection ?? defHeroGearSel);
    } catch {}
  };

  return (
    <View style={styles.container}>
      <TopBar
        isAuthed={!!auth.token}
        username={auth.username ?? undefined}
        onProfilePress={() => setProfileOpen(true)}
        onToggleTheme={toggleTheme}
        isDark={isDark}
        onRun={runSim}
        isRunning={isRunning}
      />
      <ScrollView 
        style={styles.scrollableContent} 
        contentContainerStyle={{ paddingBottom: 48 }}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.content}>
          <Text style={styles.header}>WoS Battle Simulator</Text>

          {/* Config */}
          <CollapsibleSection title="Configuration" defaultOpen>
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
          </CollapsibleSection>

          {/* Attacker - Hero Formation & Ratios */}
          <CollapsibleSection title="Attacker - Hero Formation & Ratios" defaultOpen>
            <SideSetup
              side="atk"
              variant="formation"
              heroes={heroes}
              troops={troops}
              heroesByClass={heroesByClass}
              troopsByClass={troopsByClass}
              heroSel={atkH}
              troopSel={atkT}
              slotSel={atkSlots}
              ratioSel={atkRatios}
              ewLevelSel={atkEw}
              setHeroSel={setAtkH}
              setTroopSel={setAtkT}
              setSlotSel={setAtkSlots}
              setRatioSel={setAtkRatios}
              setEwLevelSel={setAtkEw}
              capacity={attackerCapacity}
              setCapacity={setAttackerCapacity}
              attackType={attackType}
              researchSelection={atkResearchSel}
              heroGearSelection={atkHeroGearSel as any}
              supportHeroes={atkSupportHeroes}
              onSupportHeroesChange={setAtkSupportHeroes}
            />
          </CollapsibleSection>

          {/* Attacker City Buffs */}
          <CollapsibleSection title="Attacker City Buffs" defaultOpen={false}>
            <SideSetup
              side="atk"
              variant="city"
              heroes={heroes}
              troops={troops}
              heroesByClass={heroesByClass}
              troopsByClass={troopsByClass}
              heroSel={atkH}
              troopSel={atkT}
              slotSel={atkSlots}
              ratioSel={atkRatios}
              ewLevelSel={atkEw}
              setHeroSel={setAtkH}
              setTroopSel={setAtkT}
              setSlotSel={setAtkSlots}
              setRatioSel={setAtkRatios}
              setEwLevelSel={setAtkEw}
              capacity={attackerCapacity}
              setCapacity={setAttackerCapacity}
              attackType={attackType}
              gearSelection={atkGearSel}
              onGearSelectionChange={(v)=> setAtkGearSel(v)}
              charmLevels={atkCharmLvls}
              onCharmLevelsChange={(v)=> setAtkCharmLvls(v)}
              chiefSkinBonuses={atkSkin}
              onChiefSkinBonusesChange={setAtkSkin}
              daybreakBonuses={atkDaybreak}
              onDaybreakChange={setAtkDaybreak}
              onResearchBuffsChange={(b)=> setAtkResearchBuffs(b)}
              onResearchSelectionChange={(rows)=> setAtkResearchSel(rows)}
              researchSelection={atkResearchSel}
              heroGearSelection={atkHeroGearSel as any}
              onHeroGearSelectionChange={(v)=> setAtkHeroGearSel(v)}
            />
          </CollapsibleSection>

          {/* Defender - Hero Formation & Ratios */}
          <CollapsibleSection title="Defender - Hero Formation & Ratios" defaultOpen>
            <SideSetup
              side="def"
              variant="formation"
              heroes={heroes}
              troops={troops}
              heroesByClass={heroesByClass}
              troopsByClass={troopsByClass}
              heroSel={defH}
              troopSel={defT}
              slotSel={defSlots}
              ratioSel={defRatios}
              ewLevelSel={defEw}
              setHeroSel={setDefH}
              setTroopSel={setDefT}
              setSlotSel={setDefSlots}
              setRatioSel={setDefRatios}
              setEwLevelSel={setDefEw}
              capacity={defenderCapacity}
              setCapacity={setDefenderCapacity}
              attackType={attackType}
              researchSelection={defResearchSel}
              heroGearSelection={defHeroGearSel as any}
              supportHeroes={defSupportHeroes}
              onSupportHeroesChange={setDefSupportHeroes}
            />
          </CollapsibleSection>

          {/* Defender City Buffs */}
          <CollapsibleSection title="Defender City Buffs" defaultOpen={false}>
            <SideSetup
              side="def"
              variant="city"
              heroes={heroes}
              troops={troops}
              heroesByClass={heroesByClass}
              troopsByClass={troopsByClass}
              heroSel={defH}
              troopSel={defT}
              slotSel={defSlots}
              ratioSel={defRatios}
              ewLevelSel={defEw}
              setHeroSel={setDefH}
              setTroopSel={setDefT}
              setSlotSel={setDefSlots}
              setRatioSel={setDefRatios}
              setEwLevelSel={setDefEw}
              capacity={defenderCapacity}
              setCapacity={setDefenderCapacity}
              attackType={attackType}
              gearSelection={defGearSel}
              onGearSelectionChange={(v)=> setDefGearSel(v)}
              charmLevels={defCharmLvls}
              onCharmLevelsChange={(v)=> setDefCharmLvls(v)}
              chiefSkinBonuses={defSkin}
              onChiefSkinBonusesChange={setDefSkin}
              daybreakBonuses={defDaybreak}
              onDaybreakChange={setDefDaybreak}
              onResearchBuffsChange={(b)=> setDefResearchBuffs(b)}
              onResearchSelectionChange={(rows)=> setDefResearchSel(rows)}
              researchSelection={defResearchSel}
              heroGearSelection={defHeroGearSel as any}
              onHeroGearSelectionChange={(v)=> setDefHeroGearSel(v)}
            />
          </CollapsibleSection>

          {/* Results */}
          {result && (
            <CollapsibleSection title="Results" defaultOpen>
              <ResultsSection result={result} onRerun={rerun} />
            </CollapsibleSection>
          )}
        </View>
      </ScrollView>
      <ProfileModal
        visible={profileOpen}
        onClose={() => setProfileOpen(false)}
        collectSettings={collectSettings}
        applySettings={applySettings}
        onAuthChange={(a)=> setAuth(a || { token: null, username: null })}
      />
    </View>
  );
}
