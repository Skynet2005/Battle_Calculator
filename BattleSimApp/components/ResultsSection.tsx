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
import {
  Alert,
  ScrollView,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

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

  const procStats = detail.proc_stats ?? {};
  const passiveAtk = detail.passive_effects?.attacker ?? [];
  const passiveDef = detail.passive_effects?.defender ?? [];
  const bonusAtk = detail.bonuses?.attacker ?? {};
  const bonusDef = detail.bonuses?.defender ?? {};

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

  Object.entries(procStats).forEach(([key, count]) => {
    const m = key.match(/^(.*)-(atk|def)(?:-(infantry|lancer|marksman))?$/);
    if (!m) return;
    const [, skill, side, cls] = m;

    const pushHero = () =>
      (side === "atk" ? heroProcsAtk : heroProcsDef).push([skill, count]);

    if (cls && troopSkillSet.has(skill)) {
      /* troop skill */
      (side === "atk" ? troopProcsAtk : troopProcsDef)[
        cls as "infantry" | "lancer" | "marksman"
      ].push([skill, count]);
    } else {
      /* hero on-attack / on-turn skill */
      pushHero();
    }
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

  return (
    <ScrollView style={[styles.results, { maxHeight: 900 }]} nestedScrollEnabled>
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

      <View style={{ flexDirection: "row", width: "100%" }}>
        <SideBlock
          label="Attacker"
          colourStyle={styles.attackerText}
          detail={detail}
          winSide="attacker"
          passives={buildLines(passiveAtk, heroProcsAtk, pctAtk)}
          bonus={bonusAtk}
          troopProcs={troopProcsAtk}
          sideDetails={attacker}
        />
        <SideBlock
          label="Defender"
          colourStyle={styles.defenderText}
          detail={detail}
          winSide="defender"
          passives={buildLines(passiveDef, heroProcsDef, pctDef)}
          bonus={bonusDef}
          troopProcs={troopProcsDef}
          sideDetails={defender}
        />
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

      {/* Expedition-Skill impacts */}
      <Text style={styles.resultHeader}>Expedition-Skill Impacts</Text>
      <View style={styles.tableContainer}>
        <View style={styles.tableHeaderRow}>
          <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Name</Text>
          <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Percent</Text>
        </View>
        {(() => {
          // Parse passives to extract name and percent/stat
          const rows = passives.map((ln) => {
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
          // Pad to 9 rows
          while (rows.length < 9) rows.push({ name: "", percent: "" });
          return rows.slice(0, 9).map((row, i) => (
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
                <Text style={[styles.tableCell, { flex: 1 }]}>{sideDetails.kills?.[cls] ?? 0}</Text>
                <Text style={[styles.tableCell, { flex: 1 }]}>{sideDetails.survivors?.[cls] ?? 0}</Text>
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
        procs.map(([skill, n]) => (
          <View key={skill} style={styles.tableRow}>
            <Text style={[styles.tableCell, { flex: 2 }]}>{skill}</Text>
            <Text style={[styles.tableCell, { flex: 1 }]}>{n}</Text>
          </View>
        ))
      )}
    </View>
  </View>
);
