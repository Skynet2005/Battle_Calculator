import React from "react";
import axios from "axios";
import { View, Text, TouchableOpacity, ActivityIndicator } from "react-native";
import { Picker } from "@react-native-picker/picker";
import { removeLevelWord } from "../utils/format";
import { styles } from "../styles";
import { ResearchBuffs, ResearchNode, ResearchSelection, ResearchSelectionRow } from "../types";

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
  const [collapsed, setCollapsed] = React.useState(false);
  
  // Styling
  const col = side === "atk" ? styles.attackerLabel : styles.defenderLabel;
  const pickStyle = side === "atk" ? styles.attackerPicker : styles.defenderPicker;
  
  // Keep latest onChange in a ref to avoid effect loops from changing function identity
  const onChangeRef = React.useRef(onChange);
  React.useEffect(() => {
    onChangeRef.current = onChange;
  }, [onChange]);

  // Track last emitted selection rows to avoid infinite loops
  const lastRowsRef = React.useRef<ResearchSelection | null>(null);
  
  // Track current cats state to avoid dependency issues
  const catsRef = React.useRef(cats);
  React.useEffect(() => {
    catsRef.current = cats;
  }, [cats]);

  const rowsFromCats = React.useCallback((): ResearchSelection => (
    cats.map((c) => ({ category: c.category, selectedTier: c.selectedTier, selectedLevel: c.selectedLevel }))
  ), [cats]);

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

  // Helper functions
  const tierNum = (label: string) => parseInt((label.match(/(\d+)/)?.[1] || "0"), 10);
  
  const includedNodes = (cs: CategoryState): ResearchNode[] => {
    if (!cs.selectedTier || !cs.selectedLevel) return [];
    const selTierN = tierNum(cs.selectedTier);
    const out: ResearchNode[] = [];
    
    for (const t of cs.tiers) {
      const tN = tierNum(t);
      for (const node of cs.nodesByTier[t] || []) {
        if (tN < selTierN || (tN === selTierN && node.level <= cs.selectedLevel)) {
          out.push(node);
        }
      }
    }
    
    // Sort by tier number then level
    return out.sort((a, b) => {
      const an = tierNum(a.tier_label);
      const bn = tierNum(b.tier_label);
      if (an !== bn) return an - bn;
      return a.level - b.level;
    });
  };

  // Data fetching
  React.useEffect(() => {
    let cancelled = false;
    
    const run = async () => {
      try {
        setLoading(true);
        const catResp = await axios.get<string[]>("http://localhost:8000/api/research/categories");
        const categories = catResp.data || [];
        const out: CategoryState[] = [];
        
        for (const category of categories) {
          const tiersResp = await axios.get<string[]>("http://localhost:8000/api/research/tiers", { params: { category } });
          const tiers = tiersResp.data || [];
          const nodesByTier: Record<string, ResearchNode[]> = {};
          
          for (const tier of tiers) {
            const nodesResp = await axios.get<ResearchNode[]>("http://localhost:8000/api/research/nodes", { params: { category, tier } });
            nodesByTier[tier] = nodesResp.data || [];
          }
          
          // Pick highest tier (by numeric suffix in label) and highest level
          const tierNums = tiers
            .map((t) => ({ t, n: parseInt((t.match(/(\d+)/)?.[1] || "0"), 10) }))
            .sort((a, b) => a.n - b.n);
          const highestTier = tierNums.length ? tierNums[tierNums.length - 1].t : (tiers[tiers.length - 1] || "");
          const levels = nodesByTier[highestTier]?.map((n) => n.level) || [];
          const maxLevel = levels.length ? Math.max(...levels) : 0;
          
          out.push({ category, tiers, nodesByTier, selectedTier: highestTier, selectedLevel: maxLevel });
        }
        
        if (!cancelled) {
          setCats(out);
          setLoading(false);
        }
      } catch (e) {
        if (!cancelled) {
          setCats([]);
          setLoading(false);
        }
      }
    };
    
    run();
    
    return () => {
      cancelled = true;
    };
  }, []);

  // Apply external selection value when provided
  const lastAppliedValueRef = React.useRef<ResearchSelection | null>(null);

  React.useEffect(() => {
    if (!value || value.length === 0) return;
    
    const currentCats = catsRef.current;
    if (currentCats.length === 0) return;
    
    // Skip if this value is already the last applied one
    if (rowsEqual(lastAppliedValueRef.current, value)) return;
    
    // Create current selection directly without calling rowsFromCats
    const current: ResearchSelection = currentCats.map((c) => ({ 
      category: c.category, 
      selectedTier: c.selectedTier, 
      selectedLevel: c.selectedLevel 
    }));
    
    // Skip if already in sync
    if (rowsEqual(current, value)) return;
    
    let changed = false;
    const next = currentCats.map((x) => {
      const row = value.find((r) => r.category === x.category);
      if (!row) return x;
      const maxLevelInTier = (x.nodesByTier[row.selectedTier] || []).reduce((mx, n) => Math.max(mx, n.level), 0);
      const newLevel = Math.min(row.selectedLevel, maxLevelInTier);
      if (x.selectedTier !== row.selectedTier || x.selectedLevel !== newLevel) {
        changed = true;
        return { ...x, selectedTier: row.selectedTier, selectedLevel: newLevel };
      }
      return x;
    });
    
    if (changed) {
      lastAppliedValueRef.current = value;
      setCats(next);
    }
  }, [value]); // Only depend on value to prevent infinite loop

  // Calculate buffs whenever selection changes
  const recalc = React.useCallback(() => {
    const agg: ResearchBuffs = {};
    const add = (k: keyof ResearchBuffs, v: number) => {
      agg[k] = (agg[k] || 0) + v;
    };

    for (const cs of cats) {
      if (!cs.selectedTier || !cs.selectedLevel) continue;
      const selTierN = tierNum(cs.selectedTier);
      
      for (const t of cs.tiers) {
        const tN = tierNum(t);
        const nodes = cs.nodesByTier[t] || [];
        
        for (const node of nodes) {
          // Include fully all levels for tiers below selected; include up to selectedLevel for selected tier
          if (tN < selTierN || (tN === selTierN && node.level <= cs.selectedLevel)) {
            const stat = String(node.stat_name || "").toLowerCase();
            const v = Number(node.value) || 0;
            
            // Apply buffs based on stat name
            if (stat.includes("troop attack") || stat.includes("troops attack")) {
              add("infantry_attack_pct", v);
              add("lancer_attack_pct", v);
              add("marksman_attack_pct", v);
            } else if (stat.includes("troop defense") || stat.includes("troops defense")) {
              add("infantry_defense_pct", v);
              add("lancer_defense_pct", v);
              add("marksman_defense_pct", v);
            } else if (stat.includes("troop health") || stat.includes("troops health")) {
              add("infantry_health_pct", v);
              add("lancer_health_pct", v);
              add("marksman_health_pct", v);
            } else if (stat.includes("troop lethality") || stat.includes("troops lethality")) {
              add("infantry_lethality_pct", v);
              add("lancer_lethality_pct", v);
              add("marksman_lethality_pct", v);
            } else if (stat.includes("infantry attack")) {
              add("infantry_attack_pct", v);
            } else if (stat.includes("infantry defense")) {
              add("infantry_defense_pct", v);
            } else if (stat.includes("infantry health")) {
              add("infantry_health_pct", v);
            } else if (stat.includes("infantry lethality")) {
              add("infantry_lethality_pct", v);
            } else if (stat.includes("lancer attack")) {
              add("lancer_attack_pct", v);
            } else if (stat.includes("lancer defense")) {
              add("lancer_defense_pct", v);
            } else if (stat.includes("lancer health")) {
              add("lancer_health_pct", v);
            } else if (stat.includes("lancer lethality")) {
              add("lancer_lethality_pct", v);
            } else if (stat.includes("marksman attack")) {
              add("marksman_attack_pct", v);
            } else if (stat.includes("marksman defense")) {
              add("marksman_defense_pct", v);
            } else if (stat.includes("marksman health")) {
              add("marksman_health_pct", v);
            } else if (stat.includes("marksman lethality")) {
              add("marksman_lethality_pct", v);
            }
          }
        }
      }
    }
    
    onChangeRef.current(agg);
    // emit selection rows only if changed
    const rowsNow = rowsFromCats();
    if (!rowsEqual(lastRowsRef.current, rowsNow)) {
      lastRowsRef.current = rowsNow;
      try { onSelectionChange?.(rowsNow); } catch {}
    }
  }, [cats]);

  // Trigger recalculation when data is loaded
  React.useEffect(() => {
    if (!loading) recalc();
  }, [loading, recalc]);

  // Loading state
  if (loading) {
    return (
      <View style={styles.panel}>
        <View style={styles.sectionHeaderRow}>
          <Text style={styles.resultHeader}>Battle Research</Text>
        </View>
        <ActivityIndicator color="#3B82F6" />
      </View>
    );
  }

  // Render category row with two columns
  const renderCategoryRow = (rowIdx: number) => {
    const left = cats[rowIdx * 2];
    const right = cats[rowIdx * 2 + 1];
    
    return (
      <View key={`row-${rowIdx}`} style={styles.twoColRow}>
        {left && renderCategoryColumn(left)}
        {right && renderCategoryColumn(right)}
      </View>
    );
  };

  // Render single category column
  const renderCategoryColumn = (category: CategoryState) => {
    return (
      <View style={styles.halfCol}>
        <View style={styles.row}>
          <Text style={[styles.label, col]}>{category.category}</Text>
          <View style={styles.slotPickerContainer}>
            <Text style={[styles.slotLabel, col]}>Tier</Text>
            <Picker
              selectedValue={category.selectedTier}
              onValueChange={(v) => {
                setCats((prev) => prev.map((x) => (
                  x.category === category.category 
                    ? { 
                        ...x, 
                        selectedTier: v, 
                        selectedLevel: (x.nodesByTier[v]?.map((n) => n.level).reduce((a, b) => Math.max(a, b), 0) || 0) 
                      } 
                    : x
                )));
              }}
              style={[styles.picker, pickStyle, { width: 50 }]}
              dropdownIconColor="#FFFFFF"
            >
              {category.tiers.map((t) => (
                 <Picker.Item
                  key={`${category.category}-${t}`}
                   label={removeLevelWord(t)}
                  value={t}
                  color="#FFFFFF"
                />
              ))}
            </Picker>
            <Text style={[styles.slotLabel, col, { marginLeft: 12 }]}>Level</Text>
            <Picker
              selectedValue={String(category.selectedLevel)}
              onValueChange={(v) => setCats((prev) => prev.map((x) => (
                x.category === category.category 
                  ? { ...x, selectedLevel: parseInt(String(v), 10) } 
                  : x
              )))}
              style={[styles.picker, pickStyle, { width: 50 }]}
              dropdownIconColor="#FFFFFF"
            >
              {(category.nodesByTier[category.selectedTier] || []).map((n) => (
                <Picker.Item 
                  key={`lvl-${category.category}-${n.level}`} 
                  label={`${n.level}`} 
                  value={`${n.level}`} 
                  color="#FFFFFF" 
                />
              ))}
            </Picker>
          </View>
          {renderStatSummary(category)}
        </View>
      </View>
    );
  };

  // Render stat summary for a category
  const renderStatSummary = (category: CategoryState) => {
    const inc = includedNodes(category);
    const total = inc.reduce((s, n) => s + (Number(n.value) || 0), 0);
    const stat = inc[0]?.stat_name || "";
    
    return (
      <View style={{ marginTop: 8 }}>
        <Text style={{ color: "#E5E7EB" }}>{stat ? `${stat}: ${total.toFixed(2)}%` : ""}</Text>
      </View>
    );
  };

  return (
    <View style={styles.panel}>
      <View style={styles.sectionHeaderRow}>
        <Text style={styles.resultHeader}>Battle Research</Text>
        <TouchableOpacity style={styles.sectionToggleBtn} onPress={() => setCollapsed((c) => !c)}>
          <Text style={styles.sectionToggleText}>{collapsed ? "Expand" : "Collapse"}</Text>
        </TouchableOpacity>
      </View>
      
      {!collapsed && Array.from({ length: Math.ceil(cats.length / 2) }).map((_, rowIdx) => renderCategoryRow(rowIdx))}
      
      {!collapsed && (
        <View style={styles.inlineRow}>
          <TouchableOpacity onPress={() => {
            // Reset defaults to highest per category
            setCats((prev) => prev.map((x) => {
              const levels = x.nodesByTier[x.selectedTier]?.map((n) => n.level) || [];
              const maxLevel = levels.length ? Math.max(...levels) : 0;
              return { ...x, selectedLevel: maxLevel };
            }));
          }}>
            <Text style={styles.linkText}>Max All</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={() => {
            // Clear all (set level 0 -> ignored)
            setCats((prev) => prev.map((x) => ({ ...x, selectedLevel: 0 })));
          }}>
            <Text style={styles.linkTextDanger}>Clear All</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
};
