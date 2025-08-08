/**
 * ResultsSection
 * ==============
 * • Expedition-Skill Impacts now shows *passives + hero skills* only.
 * • Built-in troop skills (Crystal Shield, Volley, etc.) are routed to three
 *   separate tables again: Infantry, Lancer, Marksman.
 * FULL FILE – no sections abbreviated.
 */

import * as Clipboard from "expo-clipboard";
import React from "react";
import { Alert, ScrollView, Text, TouchableOpacity, View, Platform } from "react-native";
import axios from "axios";

import { styles } from "../styles";
import { SideDetails, SimResult } from "../types";

/* ────────────────────────────────────────────────────────────── */

  const troopSkillSet = new Set([
  "Crystal Shield",
  "Body of Light",
  "Crystal Lance",
  "Incandescent Field",
  "Volley",
  "Crystal Gunpowder",
]);

type Props = {
  result: SimResult;
  onRerun: () => void;
};

export const ResultsSection: React.FC<Props> = ({ result, onRerun }) => {
  if (!result) return null;

  const detail: SimResult = (result as any).sample_battle ?? result;

  const procStats = detail.proc_stats ?? { attacker: {}, defender: {} };

  const flattenPassives = (p: any): string[] =>
    p ? ([] as string[]).concat(...(Object.values(p) as string[][])) : [];
  const passiveAtk = flattenPassives(detail.passive_effects?.attacker);
  const passiveDef = flattenPassives(detail.passive_effects?.defender);

  const flattenBonus = (b: any) => {
    const out: Record<string, number> = {};
    if (!b) return out;
    Object.entries(b).forEach(([grp, stats]) => {
      Object.entries(stats as Record<string, number>).forEach(([stat, val]) => {
        out[grp === "All" ? stat : `${grp.toLowerCase()}_${stat}`] = val as number;
      });
    });
    return out;
  };
  const bonusAtk = flattenBonus(detail.bonuses?.attacker);
  const bonusDef = flattenBonus(detail.bonuses?.defender);

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
      if (cls !== "All" && troopSkillSet.has(skill)) {
        (troopProcsAtk as any)[cls.toLowerCase()].push([skill, count]);
      } else {
        heroProcsAtk.push([skill, count]);
      }
    });
  });
  Object.entries(procStats.defender || {}).forEach(([skill, clsMap]) => {
    Object.entries(clsMap as Record<string, number>).forEach(([cls, count]) => {
      if (cls !== "All" && troopSkillSet.has(skill)) {
        (troopProcsDef as any)[cls.toLowerCase()].push([skill, count]);
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

  /* copy helper */
  const copyAll = () => {
    Clipboard.setStringAsync(JSON.stringify(detail, null, 2));
    Alert.alert("Copied", "All results copied to clipboard.");
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
  const [viewMode, setViewMode] = React.useState<'compact' | 'detailed'>('detailed');
  const sortAndLimit = (arr: [string, number][], topN = 10) => arr.slice().sort((a, b) => b[1] - a[1]).slice(0, topN);

  return (
    <ScrollView style={[styles.results, { maxHeight: 900 }]} nestedScrollEnabled={Platform.OS !== "web"}>
      <View style={{ flexDirection: "row", marginBottom: 8 }}>
        <TouchableOpacity
          onPress={onRerun}
          style={[styles.buttonContainer, { backgroundColor: "#10B981", flex: 1 }]}
        >
          <Text style={styles.buttonText}>Re-Run Battle</Text>
        </TouchableOpacity>
      </View>
      <TouchableOpacity
        onPress={copyAll}
        style={[styles.buttonContainer, { backgroundColor: "#6B7280", marginBottom: 16 }]}
      >
        <Text style={styles.buttonText}>Copy All Results</Text>
      </TouchableOpacity>
      <View style={styles.segmented}>
        <TouchableOpacity
          style={[styles.segmentedBtn, viewMode === 'detailed' ? styles.segmentedBtnActive : null]}
          onPress={() => setViewMode('detailed')}
        >
          <Text style={[styles.segmentedText, viewMode === 'detailed' ? styles.segmentedTextActive : null]}>Detailed</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.segmentedBtn, viewMode === 'compact' ? styles.segmentedBtnActive : null]}
          onPress={() => setViewMode('compact')}
        >
          <Text style={[styles.segmentedText, viewMode === 'compact' ? styles.segmentedTextActive : null]}>Compact</Text>
        </TouchableOpacity>
      </View>

      {result.attacker_win_rate !== undefined && (
        <View style={{ marginBottom: 16 }}>
          <View style={styles.sectionHeaderRow}>
            <Text style={styles.resultHeader}>Simulation Summary</Text>
            <TouchableOpacity style={styles.sectionToggleBtn} onPress={() => setCollapsed((c) => ({ ...c, summary: !c.summary }))}>
              <Text style={styles.sectionToggleText}>{collapsed.summary ? "Expand" : "Collapse"}</Text>
            </TouchableOpacity>
          </View>
          {!collapsed.summary && (
          <View style={styles.tableContainer}>
            <View style={styles.tableHeaderRow}>
              <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Metric</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Value</Text>
            </View>
            <View style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 2 }]}>Attacker Win Rate</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {((result.attacker_win_rate ?? 0) * 100).toFixed(1)}%
              </Text>
            </View>
            <View style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 2 }]}>Defender Win Rate</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {((result.defender_win_rate ?? 0) * 100).toFixed(1)}%
              </Text>
            </View>
            <View style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 2 }]}>Avg Attacker Survivors</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {Math.round(result.avg_attacker_survivors ?? 0)}
              </Text>
            </View>
            <View style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 2 }]}>Avg Defender Survivors</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {Math.round(result.avg_defender_survivors ?? 0)}
              </Text>
            </View>
          </View>
          )}
        </View>
      )}

      {detail.power && (
        <View style={{ marginBottom: 16 }}>
          <View style={styles.sectionHeaderRow}>
            <Text style={styles.resultHeader}>Power & Damage</Text>
            <TouchableOpacity style={styles.sectionToggleBtn} onPress={() => setCollapsed((c) => ({ ...c, power: !c.power }))}>
              <Text style={styles.sectionToggleText}>{collapsed.power ? "Expand" : "Collapse"}</Text>
            </TouchableOpacity>
          </View>
          {!collapsed.power && (
          <View style={styles.tableContainer}>
            <View style={styles.tableHeaderRow}>
              <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Metric</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Attacker</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Defender</Text>
            </View>
            <View style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 2 }]}>Start Power</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {detail.power.attacker.start}
              </Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {detail.power.defender.start}
              </Text>
            </View>
            <View style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 2 }]}>End Power</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {detail.power.attacker.end}
              </Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {detail.power.defender.end}
              </Text>
            </View>
            <View style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 2 }]}>Damage Dealt</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {detail.power.attacker.dealt}
              </Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {detail.power.defender.dealt}
              </Text>
            </View>
            <View style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 2 }]}>Power Diff Start</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {detail.power.difference.start}
              </Text>
              <Text style={[styles.tableCell, { flex: 1 }]}></Text>
            </View>
            <View style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 2 }]}>Power Diff End</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>
                {detail.power.difference.end}
              </Text>
              <Text style={[styles.tableCell, { flex: 1 }]}></Text>
            </View>
          </View>
          )}
        </View>
      )}

      <View style={[{ flexDirection: "row", width: "100%" }, Platform.OS === 'web' ? {} : {}]}>
        <View style={{ flex: 1, paddingHorizontal: 6, minWidth: 0 }}>
          <View style={styles.sectionHeaderRow}>
            <Text style={[styles.resultHeader, styles.attackerText]}>Attacker</Text>
            <TouchableOpacity style={styles.sectionToggleBtn} onPress={() => setCollapsed((c) => ({ ...c, attacker: !c.attacker }))}>
              <Text style={styles.sectionToggleText}>{collapsed.attacker ? "Expand" : "Collapse"}</Text>
            </TouchableOpacity>
          </View>
          {!collapsed.attacker && (
        <SideBlock
          label="Attacker"
          colourStyle={styles.attackerText}
          detail={detail}
          winSide="attacker"
            passives={buildLines(passiveAtk, sortAndLimit(heroProcsAtk, viewMode === 'compact' ? 6 : 12), pctAtk)}
          bonus={bonusAtk}
            troopProcs={{
              infantry: sortAndLimit(troopProcsAtk.infantry, viewMode === 'compact' ? 4 : 8),
              lancer: sortAndLimit(troopProcsAtk.lancer, viewMode === 'compact' ? 4 : 8),
              marksman: sortAndLimit(troopProcsAtk.marksman, viewMode === 'compact' ? 4 : 8),
            }}
          sideDetails={attacker}
          />
          )}
        </View>
        <View style={{ flex: 1, paddingHorizontal: 6, minWidth: 0 }}>
          <View style={styles.sectionHeaderRow}>
            <Text style={[styles.resultHeader, styles.defenderText]}>Defender</Text>
            <TouchableOpacity style={styles.sectionToggleBtn} onPress={() => setCollapsed((c) => ({ ...c, defender: !c.defender }))}>
              <Text style={styles.sectionToggleText}>{collapsed.defender ? "Expand" : "Collapse"}</Text>
            </TouchableOpacity>
          </View>
          {!collapsed.defender && (
        <SideBlock
          label="Defender"
          colourStyle={styles.defenderText}
          detail={detail}
          winSide="defender"
            passives={buildLines(passiveDef, sortAndLimit(heroProcsDef, viewMode === 'compact' ? 6 : 12), pctDef)}
          bonus={bonusDef}
            troopProcs={{
              infantry: sortAndLimit(troopProcsDef.infantry, viewMode === 'compact' ? 4 : 8),
              lancer: sortAndLimit(troopProcsDef.lancer, viewMode === 'compact' ? 4 : 8),
              marksman: sortAndLimit(troopProcsDef.marksman, viewMode === 'compact' ? 4 : 8),
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
            <Text style={{ color: '#E5E7EB' }}>{aiText}</Text>
          </View>
        )}
      </View>
    </ScrollView>
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
              detail.winner === winSide ? colourStyle : undefined,
              { flex: 1 },
            ]}
          >
            {detail.winner.toUpperCase()}
          </Text>
          <Text style={[styles.tableCell, { flex: 1 }]}>{detail.rounds}</Text>
        </View>
      </View>

      {sideDetails && (
        <>
          <Text style={styles.subHeader}>Totals</Text>
          <View style={styles.tableContainer}>
            <View style={styles.tableHeaderRow}>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Start</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>End</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Losses</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Loss %</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Kills</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Kill %</Text>
            </View>
            <View style={styles.tableRow}>
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
        <View style={styles.tableHeaderRow}>
          <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Name</Text>
          <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Percent</Text>
        </View>
        {(() => {
          // Parse passives to extract name and percent/stat
          let rows = passives.map((ln) => {
            // Match: SkillName: stat +xx.x% (optional: (enemy))
            let m = ln.match(/^(.*?): ([^+]+\+[-\d.]+%)(?:\s*\(enemy\))?/);
            if (m) {
              return { name: m[1], percent: m[2].trim() };
            }
            // Match: SkillName: +xx.x% (triggered n×)
            m = ln.match(/^(.*?): \+([-\d.]+)% \(triggered \d+×\)/);
            if (m) {
              return { name: m[1], percent: `+${m[2]}%` };
            }
            // Match: SkillName: triggered n×
            m = ln.match(/^(.*?): triggered \d+×/);
            if (m) {
              return { name: m[1], percent: "" };
            }
            // fallback: whole string as name
            return { name: ln, percent: "" };
          });
          if (!showAllImpacts) {
            // limit to top 9 visible
            rows = rows.slice(0, 9);
            while (rows.length < 9) rows.push({ name: "", percent: "" });
          }
          return rows.map((row, i) => (
            <View key={i} style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 2, textAlign: "left" }]}>{row.name}</Text>
              <Text style={[styles.tableCell, { flex: 2 }]}>{row.percent}</Text>
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

          {/* Move Details table here */}
          <Text style={[styles.resultHeader, colourStyle]}>
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
                <Text style={[styles.tableCell, { flex: 1 }]}>{SV(h.count_start)}</Text>
                <Text style={[styles.tableCell, { flex: 1 }]}>{SV(h.count_end)}</Text>
              </View>
            ))}
          </View>

          <Text style={styles.resultHeader}>Hero Performance</Text>
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
              <Text style={[styles.tableCell, { flex: 1 }]}>{SV(h.count_lost)}</Text>
              <View style={[{ flex: 1, flexDirection: 'row', alignItems: 'center' }]}>
                <Text style={[styles.tableCell, { flex: undefined, width: 48, textAlign: 'right' }]}>{(h.loss_pct * 100).toFixed(1)}%</Text>
                <View style={styles.barTrack}>
                  <View style={[styles.barFill, { width: `${Math.min(100, Math.round(h.loss_pct * 100))}%`, backgroundColor: '#F59E0B' }]} />
                </View>
              </View>
              <Text style={[styles.tableCell, { flex: 1 }]}>{SV(h.kills)}</Text>
              <View style={[{ flex: 1, flexDirection: 'row', alignItems: 'center' }]}>
                <Text style={[styles.tableCell, { flex: undefined, width: 48, textAlign: 'right' }]}>{(h.kill_pct * 100).toFixed(1)}%</Text>
                <View style={styles.barTrack}>
                  <View style={[styles.barFill, { width: `${Math.min(100, Math.round(h.kill_pct * 100))}%`, backgroundColor: '#10B981' }]} />
                </View>
              </View>
              </View>
            ))}
          </View>
        </>
      )}

      {/* cumulative bonuses */}
      <Text style={styles.resultHeader}>Cumulative % Bonuses</Text>
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
