import * as Clipboard from "expo-clipboard";
import React from "react";
import { Alert, ScrollView, Text, TouchableOpacity, View, Platform } from "react-native";
import axios from "axios";

import { styles } from "../styles";
import { SideDetails, SimResult } from "../types";

/* ────────────────────────────────────────────────────────────── */

const troopSkillSet = new Set([
  // Infantry skills
  "Master Brawler",
  "Bands of Steel",
  "Crystal Shield",
  "Body of Light",
  // Lancer skills
  "Charge",
  "Ambusher",
  "Crystal Lance",
  "Incandescent Field",
  // Marksman skills
  "Ranged Strike",
  "Volley",
  "Crystal Gunpowder",
  "Flame Charge",
]);

type Props = {
  result: SimResult | null;
  onRerun: () => void;
};

export const ResultsSection: React.FC<Props> = ({ result, onRerun }) => {
  if (!result) return null;

  const detail: SimResult = (result as any).sample_battle ?? result;

  const procStats = (detail as any).proc_stats ?? { attacker: {}, defender: {} };

  const flattenPassives = (p: any): string[] =>
    p ? ([] as string[]).concat(...(Object.values(p) as string[][])) : [];
  const passiveAtk = flattenPassives((detail as any).passive_effects?.attacker);
  const passiveDef = flattenPassives((detail as any).passive_effects?.defender);

  const flattenBonus = React.useCallback((b: any) => {
    const out: Record<string, number> = {};
    if (!b) return out;
    Object.entries(b).forEach(([grp, stats]) => {
      if (grp === "All") return;
      Object.entries(stats as Record<string, number>).forEach(([stat, val]) => {
        out[`${grp.toLowerCase()}_${stat}`] = val as number;
      });
    });
    return out;
  }, []);
  const bonusAtk = flattenBonus((detail as any).bonuses?.attacker);
  const bonusDef = flattenBonus((detail as any).bonuses?.defender);

  const attacker: SideDetails | undefined = (detail as any).attacker;
  const defender: SideDetails | undefined = (detail as any).defender;

  /* build {skill -> pct} look-ups per side */
  const pctAtk: Record<string, number> = {};
  const pctDef: Record<string, number> = {};
  const harvestPcts = (side: SideDetails | undefined, out: Record<string, number>) => {
    if (!side) return;
    Object.values(side.heroes).forEach((h: any) =>
      Object.entries(h.skill_pcts ?? {}).forEach(([s, p]) => (out[s] = p as number)),
    );
  };
  harvestPcts(attacker, pctAtk);
  harvestPcts(defender, pctDef);

  /* split procStats → heroSkills  vs  troopSkills[class] */
  const heroProcsAtk: [string, number][] = [];
  const heroProcsDef: [string, number][] = [];
  const troopProcsAtk = { infantry: [], lancer: [], marksman: [] } as Record<
    "infantry" | "lancer" | "marksman",
    [string, number][]
  >;
  const troopProcsDef = { infantry: [], lancer: [], marksman: [] } as Record<
    "infantry" | "lancer" | "marksman",
    [string, number][]
  >;

  Object.entries(procStats.attacker || {}).forEach(([skill, clsMap]) => {
    Object.entries(clsMap as Record<string, number>).forEach(([cls, count]) => {
      if (troopSkillSet.has(skill)) {
        if (cls === "All") {
          (troopProcsAtk as any).infantry.push([skill, count]);
          (troopProcsAtk as any).lancer.push([skill, count]);
          (troopProcsAtk as any).marksman.push([skill, count]);
        } else if (cls !== "All") {
          (troopProcsAtk as any)[cls.toLowerCase()].push([skill, count]);
        }
      } else {
        heroProcsAtk.push([skill, count]);
      }
    });
  });
  Object.entries(procStats.defender || {}).forEach(([skill, clsMap]) => {
    Object.entries(clsMap as Record<string, number>).forEach(([cls, count]) => {
      if (troopSkillSet.has(skill)) {
        if (cls === "All") {
          (troopProcsDef as any).infantry.push([skill, count]);
          (troopProcsDef as any).lancer.push([skill, count]);
          (troopProcsDef as any).marksman.push([skill, count]);
        } else if (cls !== "All") {
          (troopProcsDef as any)[cls.toLowerCase()].push([skill, count]);
        }
      } else {
        heroProcsDef.push([skill, count]);
      }
    });
  });

  /* merge passives + hero procs, include % */
  const buildLines = (
    passives: string[],
    heroEntries: [string, number][],
    pctMap: Record<string, number>,
  ) =>
    passives.concat(
      heroEntries.map(([skill, n]) => {
        const pct = pctMap[skill];
        return pct !== undefined
          ? `${skill}: +${(pct * 100).toFixed(1)}% (triggered ${n}×)`
          : `${skill}: triggered ${n}×`;
      }),
    );

  /* copy helpers */
  const copyAll = () => {
    Clipboard.setStringAsync(JSON.stringify(detail, null, 2));
    Alert.alert("Copied", "All results copied to clipboard.");
  };
  
  const copyJson = () => {
    Clipboard.setStringAsync(JSON.stringify(detail, null, 2));
    Alert.alert("Copied", "JSON results copied to clipboard.");
  };
  
  const copyFormatted = () => {
    const formatted = formatBattleResults(detail);
    Clipboard.setStringAsync(formatted);
    Alert.alert("Copied", "Formatted results copied to clipboard.");
  };
  const [aiText, setAiText] = React.useState<string | null>(null);
  const [aiBusy, setAiBusy] = React.useState(false);
  const sendToAi = async () => {
    try {
      setAiBusy(true);
      const resp = await axios.post("http://localhost:8000/api/analyze", { result });
      setAiText(resp.data?.analysis || "No analysis returned.");
    } catch (e: any) {
      Alert.alert("Analysis Error", String(e.response?.data ?? e.message));
    } finally {
      setAiBusy(false);
    }
  };

  const [collapsed, setCollapsed] = React.useState({
    summary: false,
    power: false,
    attacker: false,
    defender: false,
    bonuses: false,
  });
  const sortAndLimit = (arr: [string, number][], topN = 10) => arr.slice().sort((a, b) => b[1] - a[1]).slice(0, topN);
  const heroLimit = 12; // show top hero procs
  const troopLimit = 8; // show top troop skills per class

  // Format battle results in a readable way
  const formatBattleResults = (res: SimResult) => {
    const lines: string[] = [];
    const detailAny: any = res as any;
    const atk: any = detailAny.attacker || {};
    const def: any = detailAny.defender || {};
    const p = res.power as any;

    const pctStr = (v: any) => `${Number(v || 0).toFixed(1)}%`;

    lines.push("BATTLE SIMULATION RESULTS");
    lines.push("=".repeat(50));
    lines.push("");

    if ((result as any).attacker_win_rate !== undefined) {
      lines.push("BATTLE OUTCOME:");
      lines.push(`  Attacker Win Rate: ${(((result as any).attacker_win_rate || 0) * 100).toFixed(1)}%`);
      lines.push(`  Defender Win Rate: ${(((result as any).defender_win_rate || 0) * 100).toFixed(1)}%`);
      lines.push(`  Average Attacker Survivors: ${Math.round((result as any).avg_attacker_survivors || 0)}`);
      lines.push(`  Average Defender Survivors: ${Math.round((result as any).avg_defender_survivors || 0)}`);
      lines.push("");
    }

    const base = (res as any).sample_battle || res;
    lines.push("SAMPLE BATTLE DETAILS:");
    lines.push(`  Winner: ${String((base as any).winner || '').toUpperCase()}`);
    if (typeof (base as any).rounds === 'number') lines.push(`  Rounds: ${(base as any).rounds}`);
    lines.push("");

    if (p) {
      lines.push("POWER SUMMARY:");
      lines.push(`  Attacker: ${p.attacker.start} → ${p.attacker.end}`);
      lines.push(`  Defender: ${p.defender.start} → ${p.defender.end}`);
      lines.push("");
    }

    if (atk.summary || def.summary) {
      lines.push("SIDE SUMMARIES:");
      if (atk.summary) lines.push(`  Attacker — start ${atk.summary.start}, end ${atk.summary.end}, losses ${atk.summary.losses} (${pctStr((atk.summary.loss_pct || 0) * 100)}), kills ${atk.summary.kills} (${pctStr((atk.summary.kill_pct || 0) * 100)})`);
      if (def.summary) lines.push(`  Defender — start ${def.summary.start}, end ${def.summary.end}, losses ${def.summary.losses} (${pctStr((def.summary.loss_pct || 0) * 100)}), kills ${def.summary.kills} (${pctStr((def.summary.kill_pct || 0) * 100)})`);
      lines.push("");
    }

    lines.push("ATTACKER Expedition-Skill Impacts");
    buildLines(passiveAtk, heroProcsAtk, pctAtk).forEach((s) => lines.push(`  - ${s}`));
    lines.push("DEFENDER Expedition-Skill Impacts");
    buildLines(passiveDef, heroProcsDef, pctDef).forEach((s) => lines.push(`  - ${s}`));

    return lines.join("\n");
  };

  return (
    <View style={{ width: "100%" }}>
      <View style={{ flexDirection: "row", marginBottom: 8 }}>
        <TouchableOpacity
          onPress={onRerun}
          style={[styles.buttonContainer, { backgroundColor: "#10B981", flex: 1 }]}
        >
          <Text style={styles.buttonText}>Re-Run Battle</Text>
        </TouchableOpacity>
      </View>
      <View style={[styles.actionsRow, { marginBottom: 16 }]}>
        <View style={{ flex: 1, marginRight: 8 }}>
          <TouchableOpacity
            onPress={copyAll}
            style={[styles.buttonContainer, { backgroundColor: "#6B7280" }]}
          >
            <Text style={styles.buttonText}>Copy All</Text>
          </TouchableOpacity>
        </View>
        <View style={{ flex: 1, marginRight: 8 }}>
          <TouchableOpacity
            onPress={copyJson}
            style={[styles.buttonContainer, { backgroundColor: "#059669" }]}
          >
            <Text style={styles.buttonText}>Copy JSON</Text>
          </TouchableOpacity>
        </View>
        <View style={{ flex: 1 }}>
          <TouchableOpacity
            onPress={copyFormatted}
            style={[styles.buttonContainer, { backgroundColor: "#DC2626" }]}
          >
            <Text style={styles.buttonText}>Copy Formatted</Text>
          </TouchableOpacity>
        </View>
      </View>
      {/* segmented control removed for now to minimize styles dependency */}

      {(result as any).attacker_win_rate !== undefined && (
        <View style={{ marginBottom: 16 }}>
          <View style={styles.sectionHeaderRow}>
            <Text style={styles.subHeader}>Simulation Summary</Text>
            <TouchableOpacity style={styles.sectionToggleBtn} onPress={() => setCollapsed((c) => ({ ...c, summary: !c.summary }))}>
              <Text style={styles.sectionToggleText}>{collapsed.summary ? "Expand" : "Collapse"}</Text>
            </TouchableOpacity>
          </View>
          {!collapsed.summary && (
          <View style={styles.tableContainer}>
            {/* Wide layout */}
            <View style={[styles.tableHeaderRow, { display: Platform.OS === 'web' ? 'flex' : 'none' }]}>
              <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Metric</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Value</Text>
            </View>
            <View style={[styles.tableRow, { display: Platform.OS === 'web' ? 'flex' : 'none' }]}>
              <Text style={[styles.tableCell, { flex: 2 }]}>Attacker Win Rate</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {(((result as any).attacker_win_rate ?? 0) * 100).toFixed(1)}%
              </Text>
            </View>
            <View style={[styles.tableRow, { display: Platform.OS === 'web' ? 'flex' : 'none' }]}>
              <Text style={[styles.tableCell, { flex: 2 }]}>Defender Win Rate</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {(((result as any).defender_win_rate ?? 0) * 100).toFixed(1)}%
              </Text>
            </View>
            <View style={[styles.tableRow, { display: Platform.OS === 'web' ? 'flex' : 'none' }]}>
              <Text style={[styles.tableCell, { flex: 2 }]}>Avg Attacker Survivors</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {Math.round((result as any).avg_attacker_survivors ?? 0)}
              </Text>
            </View>
            <View style={[styles.tableRow, { display: Platform.OS === 'web' ? 'flex' : 'none' }]}>
              <Text style={[styles.tableCell, { flex: 2 }]}>Avg Defender Survivors</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {Math.round((result as any).avg_defender_survivors ?? 0)}
              </Text>
            </View>
            {/* Stacked layout for small screens */}
            <View style={[styles.stackRow, { display: Platform.OS === 'web' ? 'none' : 'flex' }]}>
              <Text style={styles.stackLabel}>Attacker Win Rate</Text>
              <Text style={styles.stackValue}>{(((result as any).attacker_win_rate ?? 0) * 100).toFixed(1)}%</Text>
            </View>
            <View style={[styles.stackRow, { display: Platform.OS === 'web' ? 'none' : 'flex' }]}>
              <Text style={styles.stackLabel}>Defender Win Rate</Text>
              <Text style={styles.stackValue}>{(((result as any).defender_win_rate ?? 0) * 100).toFixed(1)}%</Text>
            </View>
            <View style={[styles.stackRow, { display: Platform.OS === 'web' ? 'none' : 'flex' }]}>
              <Text style={styles.stackLabel}>Avg Attacker Survivors</Text>
              <Text style={styles.stackValue}>{Math.round((result as any).avg_attacker_survivors ?? 0)}</Text>
            </View>
            <View style={[styles.stackRow, { display: Platform.OS === 'web' ? 'none' : 'flex' }]}>
              <Text style={styles.stackLabel}>Avg Defender Survivors</Text>
              <Text style={styles.stackValue}>{Math.round((result as any).avg_defender_survivors ?? 0)}</Text>
            </View>
          </View>
          )}
        </View>
      )}

      {(detail as any).power && (
        <View style={{ marginBottom: 16 }}>
          <View style={styles.sectionHeaderRow}>
            <Text style={styles.subHeader}>Power & Damage</Text>
            <TouchableOpacity style={styles.sectionToggleBtn} onPress={() => setCollapsed((c) => ({ ...c, power: !c.power }))}>
              <Text style={styles.sectionToggleText}>{collapsed.power ? "Expand" : "Collapse"}</Text>
            </TouchableOpacity>
          </View>
          {!collapsed.power && (
          <View style={styles.tableContainer}>
            {/* Wide layout */}
            <View style={[styles.tableHeaderRow, { display: Platform.OS === 'web' ? 'flex' : 'none' }]}>
              <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Metric</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Attacker</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Defender</Text>
            </View>
            {[
              { label: 'Start Power', a: (detail as any).power.attacker.start, d: (detail as any).power.defender.start },
              { label: 'End Power', a: (detail as any).power.attacker.end, d: (detail as any).power.defender.end },
              { label: 'Damage Dealt', a: (detail as any).power.attacker.dealt, d: (detail as any).power.defender.dealt },
              { label: 'Power Diff Start', a: (detail as any).power.difference.start, d: '' },
              { label: 'Power Diff End', a: (detail as any).power.difference.end, d: '' },
            ].map((row, idx) => (
              <View key={idx}>
                <View style={[styles.tableRow, { display: Platform.OS === 'web' ? 'flex' : 'none' }]}>
                  <Text style={[styles.tableCell, { flex: 2 }]}>{row.label}</Text>
                  <Text style={[styles.tableCell, { flex: 1 }]}>{row.a}</Text>
                  <Text style={[styles.tableCell, { flex: 1 }]}>{row.d}</Text>
                </View>
                <View style={[styles.stackRow, { display: Platform.OS === 'web' ? 'none' : 'flex' }]}>
                  <Text style={styles.stackLabel}>{row.label}</Text>
                  <Text style={styles.stackValue}>Attacker: {row.a}</Text>
                  {String(row.d).length > 0 && <Text style={styles.stackValue}>Defender: {row.d}</Text>}
                </View>
              </View>
            ))}
          </View>
          )}
        </View>
      )}

      <View style={[{ flexDirection: "row", width: "100%" }, Platform.OS === 'web' ? {} : {}]}>
        <View style={{ flex: 1, paddingHorizontal: 6, minWidth: 0 }}>
          <View style={styles.sectionHeaderRow}>
            <Text style={[styles.subHeader, styles.attackerLabel]}>Attacker</Text>
            <TouchableOpacity style={styles.sectionToggleBtn} onPress={() => setCollapsed((c) => ({ ...c, attacker: !c.attacker }))}>
              <Text style={styles.sectionToggleText}>{collapsed.attacker ? "Expand" : "Collapse"}</Text>
            </TouchableOpacity>
          </View>
          {!collapsed.attacker && (
            <SideBlock
              label="Attacker"
              colourStyle={styles.attackerLabel}
              detail={detail}
              winSide="attacker"
              passives={buildLines(passiveAtk, sortAndLimit(heroProcsAtk, heroLimit), pctAtk)}
              bonus={bonusAtk}
              troopProcs={{
                infantry: sortAndLimit(troopProcsAtk.infantry, troopLimit),
                lancer: sortAndLimit(troopProcsAtk.lancer, troopLimit),
                marksman: sortAndLimit(troopProcsAtk.marksman, troopLimit),
              }}
              sideDetails={attacker}
            />
          )}
        </View>
        <View style={{ flex: 1, paddingHorizontal: 6, minWidth: 0 }}>
          <View style={styles.sectionHeaderRow}>
            <Text style={[styles.subHeader, styles.defenderLabel]}>Defender</Text>
            <TouchableOpacity style={styles.sectionToggleBtn} onPress={() => setCollapsed((c) => ({ ...c, defender: !c.defender }))}>
              <Text style={styles.sectionToggleText}>{collapsed.defender ? "Expand" : "Collapse"}</Text>
            </TouchableOpacity>
          </View>
          {!collapsed.defender && (
            <SideBlock
              label="Defender"
              colourStyle={styles.defenderLabel}
              detail={detail}
              winSide="defender"
              passives={buildLines(passiveDef, sortAndLimit(heroProcsDef, heroLimit), pctDef)}
              bonus={bonusDef}
              troopProcs={{
                infantry: sortAndLimit(troopProcsDef.infantry, troopLimit),
                lancer: sortAndLimit(troopProcsDef.lancer, troopLimit),
                marksman: sortAndLimit(troopProcsDef.marksman, troopLimit),
              }}
              sideDetails={defender}
            />
          )}
        </View>
      </View>
      {/* AI Analysis */}
      <View style={{ marginTop: 12 }}>
        <TouchableOpacity onPress={sendToAi} style={[styles.buttonContainer, aiBusy && styles.disabledButton]} disabled={aiBusy}>
          <Text style={styles.buttonText}>{aiBusy ? "Analyzing…" : "Analyze Battle (AI)"}</Text>
        </TouchableOpacity>
        {aiText && (
          <View style={[styles.row, { backgroundColor: '#1F2937' }]}>
            <Text
              style={{
                color: '#E5E7EB',
                ...(Platform.OS === 'web'
                  ? {
                      whiteSpace: 'pre-wrap' as any,
                      fontFamily:
                        'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
                    }
                  : {}),
              }}
            >
              {aiText}
            </Text>
          </View>
        )}
      </View>
    </View>
  );
};

/* ────────────────────────────────────────────────────────────── */
/* Helper components */
/* ────────────────────────────────────────────────────────────── */

type TroopProcs = Record<"infantry" | "lancer" | "marksman", [string, number][]>;
type SBProps = {
  label: "Attacker" | "Defender";
  colourStyle: any;
  detail: SimResult;
  winSide: "attacker" | "defender";
  passives: string[];
  bonus: Record<string, number>;
  troopProcs: TroopProcs;
  sideDetails?: SideDetails;
};

const SideBlock: React.FC<SBProps> = ({
  label,
  colourStyle,
  detail,
  winSide,
  passives,
  bonus,
  troopProcs,
  sideDetails,
}) => {
  const SV = (n: number) => (
    <Text style={[styles.resultValue, n === 0 && styles.zeroText]}>{n}</Text>
  );

  const [showAllImpacts, setShowAllImpacts] = React.useState(false);

  const maxKill = sideDetails
    ? Math.max(1, ...(["Infantry", "Lancer", "Marksman"] as const).map((c) => sideDetails.kills?.[c] ?? 0))
    : 1;
  const maxSurv = sideDetails
    ? Math.max(1, ...(["Infantry", "Lancer", "Marksman"] as const).map((c) => sideDetails.survivors?.[c] ?? 0))
    : 1;

  return (
    <View style={{ flex: 1, paddingHorizontal: 6, minWidth: 0 }}>
      {/* overview */}
      <Text style={[styles.resultHeader, colourStyle]}>{label} Overview</Text>
      <View style={styles.tableContainer}>
        <View style={styles.tableHeaderRow}>
          <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Winner</Text>
          <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Rounds</Text>
        </View>
        <View style={styles.tableRow}>
          <Text
            style={[
              styles.tableCell,
              (detail as any).winner === winSide ? colourStyle : undefined,
              { flex: 1 },
            ]}
          >
            {(detail as any).winner?.toString().toUpperCase()}
          </Text>
          <Text style={[styles.tableCell, { flex: 1 }]}>{(detail as any).rounds}</Text>
        </View>
      </View>

      {sideDetails && (
        <>
          <Text style={styles.subHeader}>Totals</Text>
          <View style={styles.tableContainer}>
            {/* Wide layout */}
            <View style={[styles.tableHeaderRow, { display: Platform.OS === 'web' ? 'flex' : 'none' }]}>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Start</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>End</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Losses</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Loss %</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Kills</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Kill %</Text>
            </View>
            <View style={[styles.tableRow, { display: Platform.OS === 'web' ? 'flex' : 'none' }]}>
              <Text style={[styles.tableCell, { flex: 1 }]}>{sideDetails.summary.start}</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>{sideDetails.summary.end}</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>{sideDetails.summary.losses}</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {(sideDetails.summary.loss_pct * 100).toFixed(1)}%
              </Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>{sideDetails.summary.kills}</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {(sideDetails.summary.kill_pct * 100).toFixed(1)}%
              </Text>
            </View>
            {/* Stacked for small screens */}
            {[
              { label: 'Start', v: sideDetails.summary.start },
              { label: 'End', v: sideDetails.summary.end },
              { label: 'Losses', v: sideDetails.summary.losses },
              { label: 'Loss %', v: `${(sideDetails.summary.loss_pct * 100).toFixed(1)}%` },
              { label: 'Kills', v: sideDetails.summary.kills },
              { label: 'Kill %', v: `${(sideDetails.summary.kill_pct * 100).toFixed(1)}%` },
            ].map((row, idx) => (
              <View key={idx} style={[styles.stackRow, { display: Platform.OS === 'web' ? 'none' : 'flex' }]}>
                <Text style={styles.stackLabel}>{row.label}</Text>
                <Text style={styles.stackValue}>{row.v as any}</Text>
              </View>
            ))}
          </View>
        </>
      )}

      {/* Expedition-Skill impacts */}
      <View style={styles.sectionHeaderRow}>
        <Text style={styles.resultHeader}>Expedition-Skill Impacts</Text>
        <TouchableOpacity style={styles.sectionToggleBtn} onPress={() => setShowAllImpacts((s) => !s)}>
          <Text style={styles.sectionToggleText}>{showAllImpacts ? "Show Top" : "Show All"}</Text>
        </TouchableOpacity>
      </View>
      <View style={styles.tableContainer}>
        {/* Wide layout */}
        <View style={[styles.tableHeaderRow, { display: Platform.OS === 'web' ? 'flex' : 'none' }]}>
          <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Name</Text>
          <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Percent</Text>
        </View>
        {(() => {
          let rows = passives.map((ln) => {
            let m = ln.match(/^(.*?): ([^+]+\+[-\d.]+%)(?:\s*\(enemy\))?/);
            if (m) return { name: m[1], percent: m[2].trim() };
            m = ln.match(/^(.*?): \+([-\d.]+)% \(triggered \d+×\)/);
            if (m) return { name: m[1], percent: `+${m[2]}%` };
            m = ln.match(/^(.*?): triggered \d+×/);
            if (m) return { name: m[1], percent: "" };
            return { name: ln, percent: "" };
          });
          if (!showAllImpacts) rows = rows.slice(0, 9);
          return rows.map((row, i) => (
            <View key={i}>
              <View style={[styles.tableRow, { display: Platform.OS === 'web' ? 'flex' : 'none' }]}>
                <Text style={[styles.tableCell, { flex: 2, textAlign: "left" }]}>{row.name}</Text>
                <Text style={[styles.tableCell, { flex: 2 }]}>{row.percent}</Text>
              </View>
              <View style={[styles.stackRow, { display: Platform.OS === 'web' ? 'none' : 'flex' }]}>
                <Text style={styles.stackLabel}>{row.name}</Text>
                {!!row.percent && <Text style={styles.stackValue}>{row.percent}</Text>}
              </View>
            </View>
          ));
        })()}
      </View>

      {/* troop skill tables */}
      {(["infantry", "lancer", "marksman"] as const).map((cls) => (
        <TroopTable key={cls} cls={cls} procs={troopProcs[cls]} />
      ))}

      {/* Kills and Survivors per Troop Type */}
      {sideDetails && (
        <>
          <Text style={styles.resultHeader}>Kills & Survivors</Text>
          <View style={styles.tableContainer}>
            <View style={styles.tableHeaderRow}>
              <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Troop Type</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Kills</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Survivors</Text>
            </View>
            {(["Infantry", "Lancer", "Marksman"] as const).map((cls) => (
              <View key={cls} style={styles.tableRow}>
                <Text style={[styles.tableCell, { flex: 2 }]}>{cls}</Text>
                <View style={[{ flex: 1, flexDirection: 'row', alignItems: 'center' }]}>
                  <Text style={[styles.tableCell, { flex: undefined, width: 50, textAlign: 'right' }]}>{sideDetails.kills?.[cls] ?? 0}</Text>
                  <View style={styles.barTrack}>
                    <View style={[styles.barFill, { width: `${Math.min(100, Math.round(((sideDetails.kills?.[cls] ?? 0) / maxKill) * 100))}%` }]} />
                  </View>
                </View>
                <View style={[{ flex: 1, flexDirection: 'row', alignItems: 'center' }]}>
                  <Text style={[styles.tableCell, { flex: undefined, width: 50, textAlign: 'right' }]}>{sideDetails.survivors?.[cls] ?? 0}</Text>
                  <View style={styles.barTrack}>
                    <View style={[styles.barFill, { width: `${Math.min(100, Math.round(((sideDetails.survivors?.[cls] ?? 0) / maxSurv) * 100))}%` }]} />
                  </View>
                </View>
              </View>
            ))}
          </View>

          {/* Details table */}
      <Text style={[styles.subHeader, colourStyle]}>
            {label} Details
          </Text>
          <View style={styles.tableContainer}>
            <View style={styles.tableHeaderRow}>
              <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Hero</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Gen</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Class</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>EW Lv</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Start</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>End</Text>
            </View>
            {Object.entries(sideDetails.heroes).map(([cls, h]: [string, any]) => (
              <View key={cls} style={styles.tableRow}>
                <Text style={[styles.tableCell, { flex: 2 }]}>{h.name}</Text>
                <Text style={[styles.tableCell, { flex: 1 }]}>{h.generation}</Text>
                <Text style={[styles.tableCell, { flex: 1 }]}>{cls}</Text>
                <Text style={[styles.tableCell, { flex: 1 }]}>
                  {h.exclusive_weapon?.level ?? "-"}
                </Text>
                <Text style={[styles.tableCell, { flex: 1 }]}>{SV(h.count_start as number)}</Text>
                <Text style={[styles.tableCell, { flex: 1 }]}>{SV(h.count_end as number)}</Text>
              </View>
            ))}
          </View>

          <Text style={styles.subHeader}>Hero Performance</Text>
          <View style={styles.tableContainer}>
            <View style={styles.tableHeaderRow}>
              <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Hero</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Lost</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Loss %</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Kills</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Kill %</Text>
            </View>
            {Object.entries(sideDetails.heroes).map(([cls, h]: [string, any]) => (
              <View key={cls} style={styles.tableRow}>
                <Text style={[styles.tableCell, { flex: 2 }]}>{h.name}</Text>
                <Text style={[styles.tableCell, { flex: 1 }]}>{SV(h.count_lost as number)}</Text>
                <View style={[{ flex: 1, flexDirection: 'row', alignItems: 'center' }]}>
                  <Text style={[styles.tableCell, { flex: undefined, width: 48, textAlign: 'right' }]}>{((h.loss_pct || 0) * 100).toFixed(1)}%</Text>
                  <View style={styles.barTrack}>
                    <View style={[styles.barFill, { width: `${Math.min(100, Math.round((h.loss_pct || 0) * 100))}%`, backgroundColor: '#F59E0B' }]} />
                  </View>
                </View>
                <Text style={[styles.tableCell, { flex: 1 }]}>{SV(h.kills as number)}</Text>
                <View style={[{ flex: 1, flexDirection: 'row', alignItems: 'center' }]}>
                  <Text style={[styles.tableCell, { flex: undefined, width: 48, textAlign: 'right' }]}>{((h.kill_pct || 0) * 100).toFixed(1)}%</Text>
                  <View style={styles.barTrack}>
                    <View style={[styles.barFill, { width: `${Math.min(100, Math.round((h.kill_pct || 0) * 100))}%`, backgroundColor: '#10B981' }]} />
                  </View>
                </View>
              </View>
            ))}
          </View>
        </>
      )}

      {/* cumulative bonuses */}
      <Text style={styles.subHeader}>Cumulative % Bonuses</Text>
      <View style={styles.tableContainer}>
        <View style={styles.tableHeaderRow}>
          <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Stat</Text>
          <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Value</Text>
        </View>
        {Object.keys(bonus).length === 0 ? (
          <View style={styles.tableRow}>
            <Text style={[styles.tableCell, { flex: 3 }]}>— none —</Text>
          </View>
        ) : (
          Object.entries(bonus).map(([stat, val]) => (
            <View key={stat} style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 2 }]}>{stat}</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {(val * 100).toFixed(1)}%
              </Text>
            </View>
          ))
        )}
      </View>
    </View>
  );
};

const TroopTable: React.FC<{
  cls: "infantry" | "lancer" | "marksman";
  procs: [string, number][];
}> = ({ cls, procs }) => (
  <View style={{ marginBottom: 8 }}>
    <Text style={styles.subHeader}>
      {cls.charAt(0).toUpperCase() + cls.slice(1)} Troop Skills
    </Text>
    <View style={styles.tableContainer}>
      <View style={styles.tableHeaderRow}>
        <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Skill</Text>
        <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Count</Text>
      </View>
      {procs.length === 0 ? (
        <View style={styles.tableRow}>
          <Text style={[styles.tableCell, { flex: 3 }]}>— none —</Text>
        </View>
      ) : (
        procs.map(([skill, n], index) => (
          <View key={skill} style={styles.tableRow}>
            <Text style={[styles.tableCell, { flex: 2, textAlign: 'left' }]}>{index + 1}. {skill}</Text>
            <Text style={[styles.tableCell, { flex: 1 }]}>{n}</Text>
          </View>
        ))
      )}
    </View>
  </View>
);
