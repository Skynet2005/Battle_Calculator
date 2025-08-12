import React from "react";
import axios from "axios";
import { Picker, PickerItem } from "./WebCompatiblePicker";
import { Text, View, TouchableOpacity, ActivityIndicator } from "react-native";
import { styles } from "../styles";
import type { ResearchSelection, ResearchBuffs, ResearchNode, ResearchSelectionRow } from "../types";

type Side = "atk" | "def";

interface Props {
  side: Side;
  onChange: (buffs: ResearchBuffs) => void;
  onSelectionChange?: (rows: ResearchSelection) => void;
  value?: ResearchSelection | null;
}

interface CategoryState {
  category: string;
  tiers: string[];
  nodesByTier: Record<string, ResearchNode[]>;
  selectedTier: string;
  selectedLevel: number;
}

export const ResearchSection: React.FC<Props> = ({ side, onChange, onSelectionChange, value }) => {
  const [loading, setLoading] = React.useState(true);
  const [cats, setCats] = React.useState<CategoryState[]>([]);

  const sidePickStyle = side === "atk" ? styles.attackerPicker : styles.defenderPicker;
  const sideLabelStyle = side === "atk" ? styles.attackerLabel : styles.defenderLabel;

  // keep latest callbacks stable
  const onChangeRef = React.useRef(onChange);
  React.useEffect(() => { onChangeRef.current = onChange; }, [onChange]);
  const valueRef = React.useRef<ResearchSelection | null>(value || null);
  React.useEffect(() => { valueRef.current = value || null; }, [value]);

  const rowsEqual = (a?: ResearchSelection | null, b?: ResearchSelection | null): boolean => {
    if (!a && !b) return true;
    if (!a || !b) return false;
    if (a.length !== b.length) return false;
    const mapB = new Map(b.map((r) => [r.category, r]));
    for (const r of a) {
      const m = mapB.get(r.category);
      if (!m || m.selectedTier !== r.selectedTier || m.selectedLevel !== r.selectedLevel) return false;
    }
    return true;
  };

  const tierNum = (label: string) => parseInt((label.match(/(\d+)/)?.[1] || "0"), 10);

  // fetch research categories/tiers/nodes (concurrently) and pre-apply saved selection if provided
  React.useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        setLoading(true);
        const catResp = await axios.get<string[]>("http://localhost:8000/api/research/categories");
        const categories = catResp.data || [];

        const categoryStates = await Promise.all(
          categories.map(async (category) => {
            const tiersResp = await axios.get<string[]>("http://localhost:8000/api/research/tiers", { params: { category } });
            const tiers = tiersResp.data || [];

            const nodesEntries = await Promise.all(
              tiers.map(async (tier) => {
                const nodesResp = await axios.get<ResearchNode[]>("http://localhost:8000/api/research/nodes", { params: { category, tier } });
                return [tier, nodesResp.data || []] as const;
              })
            );
            const nodesByTier = Object.fromEntries(nodesEntries) as Record<string, ResearchNode[]>;

            // default to highest tier and max level in that tier
            const tierNums = tiers
              .map((t) => ({ t, n: parseInt((t.match(/(\d+)/)?.[1] || "0"), 10) }))
              .sort((a, b) => a.n - b.n);
            let selectedTier = tierNums.length ? tierNums[tierNums.length - 1].t : (tiers[tiers.length - 1] || "");
            let selectedLevel = (nodesByTier[selectedTier] || []).reduce((m, n) => Math.max(m, n.level), 0);

            // If external value contains a row for this category, clamp and use it
            const row = (value || []).find((r) => r.category === category);
            if (row) {
              const maxLevelInTier = (nodesByTier[row.selectedTier] || []).reduce((mx, n) => Math.max(mx, n.level), 0);
              selectedTier = row.selectedTier;
              selectedLevel = Math.min(row.selectedLevel, maxLevelInTier);
            }

            return { category, tiers, nodesByTier, selectedTier, selectedLevel } as CategoryState;
          })
        );

        if (!cancelled) setCats(categoryStates);
      } catch {
        if (!cancelled) setCats([]);
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    load();
    return () => { cancelled = true; };
  }, []);

  // Apply external selection (value) without causing loops
  const lastAppliedRef = React.useRef<ResearchSelection | null>(null);
  React.useEffect(() => {
    if (!value || value.length === 0) return;
    if (rowsEqual(lastAppliedRef.current, value)) return;
    // Only apply when categories have loaded
    setCats((prev) => {
      if (prev.length === 0) return prev;
      const current: ResearchSelection = prev.map((c) => ({ category: c.category, selectedTier: c.selectedTier, selectedLevel: c.selectedLevel }));
      if (rowsEqual(current, value)) return prev;
      const next = prev.map((x) => {
        const row = value.find((r) => r.category === x.category);
        if (!row) return x;
        const maxLevelInTier = (x.nodesByTier[row.selectedTier] || []).reduce((mx, n) => Math.max(mx, n.level), 0);
        const newLevel = Math.min(row.selectedLevel, maxLevelInTier);
        return { ...x, selectedTier: row.selectedTier, selectedLevel: newLevel };
      });
      lastAppliedRef.current = value;
      return next;
    });
  }, [value]);

  // Map a research node's stat into the aggregate buff object
  const applyNodeStat = React.useCallback((node: ResearchNode, add: (k: keyof ResearchBuffs, v: number) => void) => {
    const stat = String(node.stat_name || "").toLowerCase();
    const v = Number(node.value) || 0;
    if (stat.includes("troop attack") || stat.includes("troops attack")) {
      add("infantry_attack_pct", v); add("lancer_attack_pct", v); add("marksman_attack_pct", v);
    } else if (stat.includes("troop defense") || stat.includes("troops defense")) {
      add("infantry_defense_pct", v); add("lancer_defense_pct", v); add("marksman_defense_pct", v);
    } else if (stat.includes("troop health") || stat.includes("troops health")) {
      add("infantry_health_pct", v); add("lancer_health_pct", v); add("marksman_health_pct", v);
    } else if (stat.includes("troop lethality") || stat.includes("troops lethality")) {
      add("infantry_lethality_pct", v); add("lancer_lethality_pct", v); add("marksman_lethality_pct", v);
    } else if (stat.includes("infantry attack")) { add("infantry_attack_pct", v);
    } else if (stat.includes("infantry defense")) { add("infantry_defense_pct", v);
    } else if (stat.includes("infantry health")) { add("infantry_health_pct", v);
    } else if (stat.includes("infantry lethality")) { add("infantry_lethality_pct", v);
    } else if (stat.includes("lancer attack")) { add("lancer_attack_pct", v);
    } else if (stat.includes("lancer defense")) { add("lancer_defense_pct", v);
    } else if (stat.includes("lancer health")) { add("lancer_health_pct", v);
    } else if (stat.includes("lancer lethality")) { add("lancer_lethality_pct", v);
    } else if (stat.includes("marksman attack")) { add("marksman_attack_pct", v);
    } else if (stat.includes("marksman defense")) { add("marksman_defense_pct", v);
    } else if (stat.includes("marksman health")) { add("marksman_health_pct", v);
    } else if (stat.includes("marksman lethality")) { add("marksman_lethality_pct", v); }
  }, []);

  // calc buffs (stack highest level per tier, using the selected level for the selected tier)
  const recalc = React.useCallback(() => {
    const agg: ResearchBuffs = {};
    const add = (k: keyof ResearchBuffs, v: number) => { agg[k] = (agg[k] || 0) + v; };

    for (const cs of cats) {
      if (!cs.selectedTier || !cs.selectedLevel) continue;
      const selTierN = tierNum(cs.selectedTier);
      for (const t of cs.tiers) {
        const tN = tierNum(t);
        if (tN > selTierN) continue;
        const nodes = cs.nodesByTier[t] || [];
        let chosen: ResearchNode | undefined;
        if (tN < selTierN) {
          // pick highest level node in this tier
          chosen = nodes.reduce((best, n) => (n.level > (best?.level || 0) ? n : best), undefined as any);
        } else {
          // selected tier: pick the currently selected level
          chosen = nodes.find((n) => n.level === cs.selectedLevel);
        }
        if (chosen) applyNodeStat(chosen, add);
      }
    }

    onChangeRef.current(agg);
    const rowsNow: ResearchSelection = cats.map((c) => ({
      category: c.category, selectedTier: c.selectedTier, selectedLevel: c.selectedLevel
    }));
    // Avoid feedback loops: only notify parent if selection actually changed
    if (!rowsEqual(valueRef.current, rowsNow)) {
      onSelectionChange?.(rowsNow);
    }
  }, [cats]);

  React.useEffect(() => {
    if (!loading && cats.length > 0) {
      recalc();
    }
    // Only run when cats array identity changes or loading flips false
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [loading, cats]);

  if (loading) {
    return (
      <View style={styles.panel}>
        <Text style={styles.subHeader}>{side === "atk" ? "Attacker" : "Defender"} Battle Research</Text>
        <ActivityIndicator />
      </View>
    );
  }

  // Total stacked (highest per tier up to selected tier; selected tier uses selected level)
  const totalBuff = (cs: CategoryState) => {
    if (!cs.selectedTier || !cs.selectedLevel) return 0;
    const selTierN = tierNum(cs.selectedTier);
    let sum = 0;
    for (const t of cs.tiers) {
      const tN = tierNum(t);
      if (tN > selTierN) continue;
      const nodes = cs.nodesByTier[t] || [];
      let chosen: ResearchNode | undefined;
      if (tN < selTierN) {
        chosen = nodes.reduce((best, n) => (n.level > (best?.level || 0) ? n : best), undefined as any);
      } else {
        chosen = nodes.find((n) => n.level === cs.selectedLevel);
      }
      if (chosen) sum += Number(chosen.value) || 0;
    }
    return sum;
  };

  // Derive a readable stat label for a category (use selected node if present, else first node found)
  const categoryStatLabel = (cs: CategoryState): string => {
    const selectedNode = (cs.nodesByTier[cs.selectedTier] || []).find((n) => n.level === cs.selectedLevel);
    let raw = selectedNode?.stat_name;
    if (!raw) {
      for (const t of cs.tiers) {
        const nodes = cs.nodesByTier[t] || [];
        if (nodes.length > 0) { raw = nodes[0].stat_name; break; }
      }
    }
    return String(raw || "");
  };

  return (
    <View>
      {cats.map((c) => {
        const levels = (c.nodesByTier[c.selectedTier] || []).map((n) => n.level);
        const maxLevel = levels.length ? Math.max(...levels) : 0;
        return (
          <View key={c.category} style={styles.row}>
            <Text style={[styles.label, sideLabelStyle]}>{c.category}</Text>
            <View style={styles.inlineRow}>
              <View style={{ flex: 1 }}>
                <Text style={styles.helperText}>Tier</Text>
                <Picker
                  selectedValue={c.selectedTier}
                  onValueChange={(v) => {
                    const lvls = (c.nodesByTier[v] || []).map((n) => n.level);
                    const maxL = lvls.length ? Math.max(...lvls) : 0;
                    setCats((prev) => prev.map((x) => x.category === c.category ? { ...x, selectedTier: String(v), selectedLevel: maxL } : x));
                  }}
                  style={[styles.picker, sidePickStyle]}
                >
                  {c.tiers.map((t) => (
                    <PickerItem key={`${c.category}-${t}`} label={t} value={t} />
                  ))}
                </Picker>
              </View>
              <View style={{ flex: 1 }}>
                <Text style={styles.helperText}>Level</Text>
                <Picker
                  selectedValue={String(c.selectedLevel)}
                  onValueChange={(v) =>
                    setCats((prev) => prev.map((x) => x.category === c.category ? { ...x, selectedLevel: parseInt(String(v), 10) } : x))
                  }
                  style={[styles.picker, sidePickStyle]}
                >
                  {(c.nodesByTier[c.selectedTier] || []).map((n) => (
                    <PickerItem key={`lvl-${c.category}-${n.level}`} label={`${n.level}`} value={`${n.level}`} />
                  ))}
                </Picker>
              </View>
            </View>

            <View style={styles.totalBar}>
              {(() => {
                const selectedNode = (c.nodesByTier[c.selectedTier] || []).find((n) => n.level === c.selectedLevel);
                const statName = selectedNode?.stat_name || categoryStatLabel(c);
                const statVal = Number(selectedNode?.value || 0);
                const stacked = totalBuff(c);
                return (
                  <>
                    <Text style={styles.totalText}>Current Tier: {statName} +{statVal.toFixed(2)}%</Text>
                    <Text style={styles.totalText}>Total: {statName} +{stacked.toFixed(2)}%</Text>
                  </>
                );
              })()}
            </View>
          </View>
        );
      })}
    </View>
  );
};
