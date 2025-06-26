/**
 * ResultsSection
 * ------------------------------------------------------------
 * • Displays one battle's outcome (or the sample from a Monte-Carlo run)
 * • Shows per-skill proc counts
 * • Highlights 0-survivor rows in red
 * • "Re-Run Battle" button repeats the last request payload
 * ------------------------------------------------------------
 */

import * as Clipboard from "expo-clipboard";
import React from "react";
import { Text, TouchableOpacity, View } from "react-native";
import { styles } from "../styles";
import { Class, SimResult } from "../types";

interface Props {
  result: SimResult;
  onRerun: () => void;
}

export const ResultsSection: React.FC<Props> = ({ result, onRerun }) => {
  if (!result) return null;

  const [copied, setCopied] = React.useState(false);

  /* prefer sample_battle when multi-sim, else root fields */
  const detail =
    result.sample_battle ?? ({
      winner: result.winner!,
      rounds: result.rounds!,
      attacker: result.attacker!,
      defender: result.defender!,
      proc_stats: result.proc_stats ?? {},
    } as Required<SimResult>["sample_battle"]);

  const procStats = detail.proc_stats ?? {};

  // Helper to export results as text
  const exportText = () => {
    let text = "";
    text += `Battle Overview\n`;
    text += `Winner: ${detail.winner.toUpperCase()}\n`;
    text += `Rounds: ${detail.rounds}\n\n`;

    // Attacker
    text += `Attacker Details\n`;
    text += `Total Power: ${detail.attacker.total_power}\n`;
    text += `Heroes:\n`;
    Object.entries(detail.attacker.heroes).forEach(([cls, info]) => {
      const hero = info as any;
      text += `  ${cls}: ${hero.name} (Gen ${hero.generation}, ${hero.class})\n`;
      text += `    ${hero.troop_level} | Pwr ${hero.troop_power} | Start ${hero.count_start} -> End ${hero.count_end}\n`;
      text += `    Skills: ${hero.skills.length ? hero.skills.join(", ") : "—"}\n`;
    });
    text += `Kills by Type:\n`;
    (Object.keys(detail.attacker.kills) as Class[]).forEach((cls) => {
      text += `  ${cls}: ${detail.attacker.kills[cls] ?? 0}\n`;
    });
    text += `Survivors by Type:\n`;
    (Object.keys(detail.attacker.survivors) as Class[]).forEach((cls) => {
      text += `  ${cls}: ${detail.attacker.survivors[cls] ?? 0}\n`;
    });
    text += `Proc Counts (Attacker):\n`;
    [
      { label: "Infantry", skills: ["Crystal Shield", "Body of Light"] },
      { label: "Lancer", skills: ["Ambusher", "Crystal Lance", "Incandescent Field"] },
      { label: "Marksman", skills: ["Volley", "Crystal Gunpowder", "Flame Charge"] },
    ].forEach(({ label, skills }) => {
      text += `  ${label}:\n`;
      let found = false;
      skills.forEach((skill) => {
        const key = Object.entries(procStats).find(
          ([k]) => k === `${skill}-atk`
        );
        if (key) {
          text += `    ${skill}: ${key[1]}\n`;
          found = true;
        }
      });
      if (!found) text += `    — none recorded —\n`;
    });
    text += `\n`;

    // Defender
    text += `Defender Details\n`;
    text += `Total Power: ${detail.defender.total_power}\n`;
    text += `Heroes:\n`;
    Object.entries(detail.defender.heroes).forEach(([cls, info]) => {
      const hero = info as any;
      text += `  ${cls}: ${hero.name} (Gen ${hero.generation}, ${hero.class})\n`;
      text += `    ${hero.troop_level} | Pwr ${hero.troop_power} | Start ${hero.count_start} -> End ${hero.count_end}\n`;
      text += `    Skills: ${hero.skills.length ? hero.skills.join(", ") : "—"}\n`;
    });
    text += `Kills by Type:\n`;
    (Object.keys(detail.defender.kills) as Class[]).forEach((cls) => {
      text += `  ${cls}: ${detail.defender.kills[cls] ?? 0}\n`;
    });
    text += `Survivors by Type:\n`;
    (Object.keys(detail.defender.survivors) as Class[]).forEach((cls) => {
      text += `  ${cls}: ${detail.defender.survivors[cls] ?? 0}\n`;
    });
    text += `Proc Counts (Defender):\n`;
    [
      { label: "Infantry", skills: ["Crystal Shield", "Body of Light"] },
      { label: "Lancer", skills: ["Ambusher", "Crystal Lance", "Incandescent Field"] },
      { label: "Marksman", skills: ["Volley", "Crystal Gunpowder", "Flame Charge"] },
    ].forEach(({ label, skills }) => {
      text += `  ${label}:\n`;
      let found = false;
      skills.forEach((skill) => {
        const key = Object.entries(procStats).find(
          ([k]) => k === `${skill}-def`
        );
        if (key) {
          text += `    ${skill}: ${key[1]}\n`;
          found = true;
        }
      });
      if (!found) text += `    — none recorded —\n`;
    });
    Clipboard.setStringAsync(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  /* helper to colour survivor # red at 0 */
  const SV = (n: number) => (
    <Text style={[styles.resultValue, n === 0 && styles.zeroText]}>{n}</Text>
  );

  /* ------------------------------------------------------------------ */
  return (
    <>
      {/* ───────── Re-Run Button ───────── */}
      <TouchableOpacity
        onPress={onRerun}
        style={[styles.buttonContainer, { backgroundColor: "#10B981" }]}
      >
        <Text style={styles.buttonText}>Re-Run Battle</Text>
      </TouchableOpacity>

      <View style={styles.results}>
        {/* ───────── Overview ───────── */}
        <Text style={styles.resultHeader}>Battle Overview</Text>
        <View style={styles.resultRow}>
          <Text style={styles.resultLabel}>Winner:</Text>
          <Text
            style={[
              styles.resultValue,
              detail.winner === "attacker"
                ? styles.attackerText
                : styles.defenderText,
            ]}
          >
            {detail.winner.toUpperCase()}
          </Text>
        </View>
        <View style={styles.resultRow}>
          <Text style={styles.resultLabel}>Rounds:</Text>
          <Text style={styles.resultValue}>{detail.rounds}</Text>
        </View>

        {/* ═════════ ATTACKER ═════════ */}
        <Text style={[styles.resultHeader, styles.attackerText]}>
          Attacker Details
        </Text>
        <Text style={styles.resultLabel}>
          Total Power: {detail.attacker.total_power}
        </Text>
        {/* Table for Attacker Heroes */}
        <View style={styles.tableContainer}>
          <View style={styles.tableHeaderRow}>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Class</Text>
            <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Hero (Gen, Class)</Text>
            <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Troop Lvl | Power</Text>
            <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Start ➜ End</Text>
            <Text style={[styles.tableHeaderCell, { flex: 3 }]}>Skills</Text>
          </View>
          {Object.entries(detail.attacker.heroes).map(([cls, info]) => (
            <View key={cls} style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 1 }]}>{cls}</Text>
              <Text style={[styles.tableCell, { flex: 2 }]}>{info.name} (Gen {info.generation}, {info.class})</Text>
              <Text style={[styles.tableCell, { flex: 2 }]}>{info.troop_level} | Pwr {info.troop_power}</Text>
              <Text style={[styles.tableCell, { flex: 2 }]}>
                {info.count_start} ➜ <Text style={info.count_end === 0 ? styles.zeroText : null}>{info.count_end}</Text>
              </Text>
              <Text style={[styles.tableCell, { flex: 3 }]}>{info.skills.length ? info.skills.join(", ") : "—"}</Text>
            </View>
          ))}
        </View>
        {/* Kills / Survivors Table for Attacker */}
        <View style={styles.tableContainer}>
          <View style={styles.tableHeaderRow}>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Class</Text>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Kills</Text>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Survivors</Text>
          </View>
          {(Object.keys(detail.attacker.kills) as Class[]).map((cls) => (
            <View key={cls} style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 1 }]}>{cls}</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>{detail.attacker.kills[cls] ?? 0}</Text>
              <Text style={[styles.tableCell, { flex: 1 }, (detail.attacker.survivors[cls] ?? 0) === 0 && styles.zeroText]}>
                {detail.attacker.survivors[cls] ?? 0}
              </Text>
            </View>
          ))}
        </View>
        {/* Proc Counts (Attacker) */}
        <Text style={styles.resultHeader}>Proc Counts (Attacker)</Text>
        {/* Infantry Procs */}
        <Text style={[styles.label, styles.attackerLabel]}>Infantry</Text>
        <View style={styles.tableContainer}>
          <View style={styles.tableHeaderRow}>
            <Text style={[styles.tableHeaderCell, { flex: 3 }]}>Skill</Text>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Count</Text>
          </View>
          {(() => {
            const skills = ["Crystal Shield", "Body of Light"];
            const procs = Object.entries(procStats)
              .filter(([k]) => k.endsWith('-atk') && skills.includes(k.replace(/-atk$/, '')));
            return procs.length === 0 ? (
              <View style={styles.tableRow}>
                <Text style={[styles.tableCell, { flex: 4 }]}>— none recorded —</Text>
              </View>
            ) : (
              skills.map(skill => {
                const entry = procs.find(([k]) => k.startsWith(skill));
                return (
                  <View key={skill} style={styles.tableRow}>
                    <Text style={[styles.tableCell, { flex: 3 }]}>{skill}</Text>
                    <Text style={[styles.tableCell, { flex: 1 }]}>{entry ? entry[1] : 0}</Text>
                  </View>
                );
              })
            );
          })()}
        </View>
        {/* Lancer Procs */}
        <Text style={[styles.label, styles.attackerLabel]}>Lancer</Text>
        <View style={styles.tableContainer}>
          <View style={styles.tableHeaderRow}>
            <Text style={[styles.tableHeaderCell, { flex: 3 }]}>Skill</Text>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Count</Text>
          </View>
          {(() => {
            const skills = ["Ambusher", "Crystal Lance", "Incandescent Field"];
            const procs = Object.entries(procStats)
              .filter(([k]) => k.endsWith('-atk') && skills.includes(k.replace(/-atk$/, '')));
            return procs.length === 0 ? (
              <View style={styles.tableRow}>
                <Text style={[styles.tableCell, { flex: 4 }]}>— none recorded —</Text>
              </View>
            ) : (
              skills.map(skill => {
                const entry = procs.find(([k]) => k.startsWith(skill));
                return (
                  <View key={skill} style={styles.tableRow}>
                    <Text style={[styles.tableCell, { flex: 3 }]}>{skill}</Text>
                    <Text style={[styles.tableCell, { flex: 1 }]}>{entry ? entry[1] : 0}</Text>
                  </View>
                );
              })
            );
          })()}
        </View>
        {/* Marksman Procs */}
        <Text style={[styles.label, styles.attackerLabel]}>Marksman</Text>
        <View style={styles.tableContainer}>
          <View style={styles.tableHeaderRow}>
            <Text style={[styles.tableHeaderCell, { flex: 3 }]}>Skill</Text>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Count</Text>
          </View>
          {(() => {
            const skills = ["Volley", "Crystal Gunpowder", "Flame Charge"];
            const procs = Object.entries(procStats)
              .filter(([k]) => k.endsWith('-atk') && skills.includes(k.replace(/-atk$/, '')));
            return procs.length === 0 ? (
              <View style={styles.tableRow}>
                <Text style={[styles.tableCell, { flex: 4 }]}>— none recorded —</Text>
              </View>
            ) : (
              skills.map(skill => {
                const entry = procs.find(([k]) => k.startsWith(skill));
                return (
                  <View key={skill} style={styles.tableRow}>
                    <Text style={[styles.tableCell, { flex: 3 }]}>{skill}</Text>
                    <Text style={[styles.tableCell, { flex: 1 }]}>{entry ? entry[1] : 0}</Text>
                  </View>
                );
              })
            );
          })()}
        </View>

        {/* ═════════ DEFENDER ═════════ */}
        <Text style={[styles.resultHeader, styles.defenderText]}>
          Defender Details
        </Text>
        <Text style={styles.resultLabel}>
          Total Power: {detail.defender.total_power}
        </Text>
        {/* Table for Defender Heroes */}
        <View style={styles.tableContainer}>
          <View style={styles.tableHeaderRow}>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Class</Text>
            <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Hero (Gen, Class)</Text>
            <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Troop Lvl | Power</Text>
            <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Start ➜ End</Text>
            <Text style={[styles.tableHeaderCell, { flex: 3 }]}>Skills</Text>
          </View>
          {Object.entries(detail.defender.heroes).map(([cls, info]) => (
            <View key={cls} style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 1 }]}>{cls}</Text>
              <Text style={[styles.tableCell, { flex: 2 }]}>{info.name} (Gen {info.generation}, {info.class})</Text>
              <Text style={[styles.tableCell, { flex: 2 }]}>{info.troop_level} | Pwr {info.troop_power}</Text>
              <Text style={[styles.tableCell, { flex: 2 }]}>
                {info.count_start} ➜ <Text style={info.count_end === 0 ? styles.zeroText : null}>{info.count_end}</Text>
              </Text>
              <Text style={[styles.tableCell, { flex: 3 }]}>{info.skills.length ? info.skills.join(", ") : "—"}</Text>
            </View>
          ))}
        </View>
        {/* Kills / Survivors Table for Defender */}
        <View style={styles.tableContainer}>
          <View style={styles.tableHeaderRow}>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Class</Text>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Kills</Text>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Survivors</Text>
          </View>
          {(Object.keys(detail.defender.kills) as Class[]).map((cls) => (
            <View key={cls} style={styles.tableRow}>
              <Text style={[styles.tableCell, { flex: 1 }]}>{cls}</Text>
              <Text style={[styles.tableCell, { flex: 1 }]}>{detail.defender.kills[cls] ?? 0}</Text>
              <Text style={[styles.tableCell, { flex: 1 }, (detail.defender.survivors[cls] ?? 0) === 0 && styles.zeroText]}>
                {detail.defender.survivors[cls] ?? 0}
              </Text>
            </View>
          ))}
        </View>
        {/* Proc Counts (Defender) */}
        <Text style={styles.resultHeader}>Proc Counts (Defender)</Text>
        {/* Infantry Procs */}
        <Text style={[styles.label, styles.defenderLabel]}>Infantry</Text>
        <View style={styles.tableContainer}>
          <View style={styles.tableHeaderRow}>
            <Text style={[styles.tableHeaderCell, { flex: 3 }]}>Skill</Text>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Count</Text>
          </View>
          {(() => {
            const skills = ["Crystal Shield", "Body of Light"];
            const procs = Object.entries(procStats)
              .filter(([k]) => k.endsWith('-def') && skills.includes(k.replace(/-def$/, '')));
            return procs.length === 0 ? (
              <View style={styles.tableRow}>
                <Text style={[styles.tableCell, { flex: 4 }]}>— none recorded —</Text>
              </View>
            ) : (
              skills.map(skill => {
                const entry = procs.find(([k]) => k.startsWith(skill));
                return (
                  <View key={skill} style={styles.tableRow}>
                    <Text style={[styles.tableCell, { flex: 3 }]}>{skill}</Text>
                    <Text style={[styles.tableCell, { flex: 1 }]}>{entry ? entry[1] : 0}</Text>
                  </View>
                );
              })
            );
          })()}
        </View>
        {/* Lancer Procs */}
        <Text style={[styles.label, styles.defenderLabel]}>Lancer</Text>
        <View style={styles.tableContainer}>
          <View style={styles.tableHeaderRow}>
            <Text style={[styles.tableHeaderCell, { flex: 3 }]}>Skill</Text>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Count</Text>
          </View>
          {(() => {
            const skills = ["Ambusher", "Crystal Lance", "Incandescent Field"];
            const procs = Object.entries(procStats)
              .filter(([k]) => k.endsWith('-def') && skills.includes(k.replace(/-def$/, '')));
            return procs.length === 0 ? (
              <View style={styles.tableRow}>
                <Text style={[styles.tableCell, { flex: 4 }]}>— none recorded —</Text>
              </View>
            ) : (
              skills.map(skill => {
                const entry = procs.find(([k]) => k.startsWith(skill));
                return (
                  <View key={skill} style={styles.tableRow}>
                    <Text style={[styles.tableCell, { flex: 3 }]}>{skill}</Text>
                    <Text style={[styles.tableCell, { flex: 1 }]}>{entry ? entry[1] : 0}</Text>
                  </View>
                );
              })
            );
          })()}
        </View>
        {/* Marksman Procs */}
        <Text style={[styles.label, styles.defenderLabel]}>Marksman</Text>
        <View style={styles.tableContainer}>
          <View style={styles.tableHeaderRow}>
            <Text style={[styles.tableHeaderCell, { flex: 3 }]}>Skill</Text>
            <Text style={[styles.tableHeaderCell, { flex: 1 }]}>Count</Text>
          </View>
          {(() => {
            const skills = ["Volley", "Crystal Gunpowder", "Flame Charge"];
            const procs = Object.entries(procStats)
              .filter(([k]) => k.endsWith('-def') && skills.includes(k.replace(/-def$/, '')));
            return procs.length === 0 ? (
              <View style={styles.tableRow}>
                <Text style={[styles.tableCell, { flex: 4 }]}>— none recorded —</Text>
              </View>
            ) : (
              skills.map(skill => {
                const entry = procs.find(([k]) => k.startsWith(skill));
                return (
                  <View key={skill} style={styles.tableRow}>
                    <Text style={[styles.tableCell, { flex: 3 }]}>{skill}</Text>
                    <Text style={[styles.tableCell, { flex: 1 }]}>{entry ? entry[1] : 0}</Text>
                  </View>
                );
              })
            );
          })()}
        </View>
      </View>

      {/* Export Button at the bottom */}
      <TouchableOpacity
        onPress={exportText}
        style={[styles.buttonContainer, { backgroundColor: "#6366F1" }]}
      >
        <Text style={styles.buttonText}>Export Results as Text</Text>
      </TouchableOpacity>
      {copied && (
        <Text style={{ color: "#10B981", textAlign: "center", marginTop: 4 }}>
          Results copied to clipboard!
        </Text>
      )}
    </>
  );
};
