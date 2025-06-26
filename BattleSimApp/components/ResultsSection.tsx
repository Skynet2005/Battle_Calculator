/**
 * ResultsSection
 * ==============
 * Displays a completed expedition simulation.
 * Nothing abbreviated – paste as-is.
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
import { SimResult, SideDetails } from "../types";

type Props = {
  result: SimResult;
  onRerun: () => void;
};

/* ────────────────────────────────────────────────────────────── */

export const ResultsSection: React.FC<Props> = ({ result, onRerun }) => {
  if (!result) return null;

  /* prefer the first sample if Monte-Carlo; otherwise use result */
  const detail: SimResult = result.sample_battle ?? result;

  const procStats   = detail.proc_stats        ?? {};
  const passiveAtk  = detail.passive_effects?.attacker ?? [];
  const passiveDef  = detail.passive_effects?.defender ?? [];
  const bonusAtk    = detail.bonuses?.attacker ?? {};
  const bonusDef    = detail.bonuses?.defender ?? {};

  /* helper to colour 0 survivors red */
  const SV = (n: number) => (
    <Text style={[styles.resultValue, n === 0 && styles.zeroText]}>{n}</Text>
  );

  /* copy JSON helper */
  const copyJSON = () => {
    Clipboard.setStringAsync(JSON.stringify(detail, null, 2));
    Alert.alert("Copied", "Detailed JSON copied to clipboard.");
  };

  /* safe accessors (could be undefined in single-run failure) */
  const attacker: SideDetails | undefined = (detail as any).attacker;
  const defender: SideDetails | undefined = (detail as any).defender;

  return (
    <ScrollView
      style={[styles.results, { maxHeight: 900 }]}
      nestedScrollEnabled
    >
      {/* ───── controls ───── */}
      <View style={{ flexDirection: "row", justifyContent: "space-between" }}>
        <TouchableOpacity
          onPress={onRerun}
          style={[styles.buttonContainer, { backgroundColor: "#10B981", flex: 1 }]}
        >
          <Text style={styles.buttonText}>Re-Run Battle</Text>
        </TouchableOpacity>

        <TouchableOpacity
          onPress={copyJSON}
          style={[
            styles.buttonContainer,
            { backgroundColor: "#6B7280", marginLeft: 12, flex: 1 },
          ]}
        >
          <Text style={styles.buttonText}>Copy JSON</Text>
        </TouchableOpacity>
      </View>

      {/* ═════════ Overview ═════════ */}
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

      {/* ═════════ Expedition-Skill Impacts ═════════ */}
      <Text style={styles.resultHeader}>Expedition-Skill Impacts</Text>
      <Text style={[styles.label, styles.attackerLabel]}>Attacker</Text>
      {passiveAtk.length ? (
        passiveAtk.map((ln: string, i: number) => (
          <Text key={i} style={styles.resultValue}>
            • {ln}
          </Text>
        ))
      ) : (
        <Text style={styles.resultValue}>— none —</Text>
      )}
      <Text style={[styles.label, styles.defenderLabel, { marginTop: 8 }]}>
        Defender
      </Text>
      {passiveDef.length ? (
        passiveDef.map((ln: string, i: number) => (
          <Text key={i} style={styles.resultValue}>
            • {ln}
          </Text>
        ))
      ) : (
        <Text style={styles.resultValue}>— none —</Text>
      )}

      {/* ═════════ Proc Counters ═════════ */}
      <Text style={styles.resultHeader}>Skill Proc Counts</Text>
      {Object.keys(procStats).length === 0 ? (
        <Text style={styles.resultValue}>— none —</Text>
      ) : (
        Object.entries(procStats).map(
          ([k, v]: [string, number]) => (
            <Text key={k} style={styles.resultValue}>
              {k}: {v}
            </Text>
          )
        )
      )}

      {/* ═════════ Attacker Block ═════════ */}
      {attacker && (
        <>
          <Text style={[styles.resultHeader, styles.attackerText]}>
            Attacker Details
          </Text>
          <Text style={styles.resultLabel}>
            Total Power: {attacker.total_power}
          </Text>
          {Object.entries(attacker.heroes).map(
            ([cls, h]: [string, any]) => (
              <View key={cls} style={{ marginVertical: 4, paddingLeft: 8 }}>
                <Text style={styles.resultValue}>
                  {cls}: {h.name} (Gen {h.generation}, {h.class})
                </Text>
                <Text style={styles.resultValue}>
                  {h.troop_level} | Pwr {h.troop_power} | Start{" "}
                  {h.count_start} ➜ {SV(h.count_end)}
                </Text>
                <Text style={styles.resultValue}>
                  Skills: {h.skills.length ? h.skills.join(", ") : "—"}
                </Text>
              </View>
            )
          )}
          <Text style={styles.resultHeader}>Kills by Type</Text>
          {Object.entries(attacker.kills).map(
            ([t, n]: [string, number]) => (
              <Text key={t} style={styles.resultValue}>
                {t}: {n}
              </Text>
            )
          )}
          <Text style={styles.resultHeader}>Survivors by Type</Text>
          {Object.entries(attacker.survivors).map(
            ([t, n]: [string, number]) => (
              <Text key={t} style={styles.resultValue}>
                {t}: {SV(n)}
              </Text>
            )
          )}
        </>
      )}

      {/* ═════════ Defender Block ═════════ */}
      {defender && (
        <>
          <Text style={[styles.resultHeader, styles.defenderText]}>
            Defender Details
          </Text>
          <Text style={styles.resultLabel}>
            Total Power: {defender.total_power}
          </Text>
          {Object.entries(defender.heroes).map(
            ([cls, h]: [string, any]) => (
              <View key={cls} style={{ marginVertical: 4, paddingLeft: 8 }}>
                <Text style={styles.resultValue}>
                  {cls}: {h.name} (Gen {h.generation}, {h.class})
                </Text>
                <Text style={styles.resultValue}>
                  {h.troop_level} | Pwr {h.troop_power} | Start{" "}
                  {h.count_start} ➜ {SV(h.count_end)}
                </Text>
                <Text style={styles.resultValue}>
                  Skills: {h.skills.length ? h.skills.join(", ") : "—"}
                </Text>
              </View>
            )
          )}
          <Text style={styles.resultHeader}>Kills by Type</Text>
          {Object.entries(defender.kills).map(
            ([t, n]: [string, number]) => (
              <Text key={t} style={styles.resultValue}>
                {t}: {n}
              </Text>
            )
          )}
          <Text style={styles.resultHeader}>Survivors by Type</Text>
          {Object.entries(defender.survivors).map(
            ([t, n]: [string, number]) => (
              <Text key={t} style={styles.resultValue}>
                {t}: {SV(n)}
              </Text>
            )
          )}
        </>
      )}

      {/* ═════════ Bonuses Table ═════════ */}
      <Text style={styles.resultHeader}>Cumulative % Bonuses</Text>
      <View style={styles.tableHeaderRow}>
        <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Stat</Text>
        <Text style={[styles.tableHeaderCell, { flex: 1 }]}>ATK</Text>
        <Text style={[styles.tableHeaderCell, { flex: 1 }]}>DEF</Text>
      </View>
      {Array.from(
        new Set([...Object.keys(bonusAtk), ...Object.keys(bonusDef)])
      ).map((stat: string) => (
        <View key={stat} style={styles.tableRow}>
          <Text style={[styles.tableCell, { flex: 2 }]}>{stat}</Text>
          <Text style={[styles.tableCell, { flex: 1 }]}>
            {((bonusAtk[stat] ?? 0) * 100).toFixed(1)}%
          </Text>
          <Text style={[styles.tableCell, { flex: 1 }]}>
            {((bonusDef[stat] ?? 0) * 100).toFixed(1)}%
          </Text>
        </View>
      ))}
    </ScrollView>
  );
};
