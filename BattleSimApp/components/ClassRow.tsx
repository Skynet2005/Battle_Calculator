import React from "react";
import Slider from "@react-native-community/slider";
import { Picker } from "@react-native-picker/picker";
import { Text, TextInput, View, TouchableOpacity } from "react-native";
import { styles } from "../styles";
import { Hero, Class } from "../types";
import { clamp, sanitizePercentInputToFraction } from "../utils/format";

interface Props {
  cls: Class;                     // "Infantry" | "Lancer" | "Marksman"
  side: "atk" | "def";
  heroes: Hero[];
  troops: string[];

  /* selections + setters */
  heroSel: string;
  troopSel: string;
  slot: string;
  ewLevel: string;
  ratio: string;
  setHero: (name: string) => void;
  setTroop: (name: string) => void;
  setSlot: (slot: string) => void;
  setEwLevel: (lvl: string) => void;
  setRatio: (ratio: string) => void;
  disabled?: boolean;
  maxPercent?: number; // Created Logic for review: upper bound for slider based on remaining allowance per side
  countValue?: string;
  onCountChange?: (text: string) => void;
  onLoadCountFromRatio?: () => void;
}

export const ClassRow: React.FC<Props> = (p) => {
  /* hero list filtered + grouped by gen */
  const [heroQuery, setHeroQuery] = React.useState("");

  const heroItems = React.useMemo(() => {
    const list = p.heroes
      .filter((h) => h.charClass.toLowerCase() === p.cls.toLowerCase())
      .filter((h) =>
        heroQuery.trim() === ""
          ? true
          : h.name.toLowerCase().includes(heroQuery.toLowerCase())
      )
      .slice()
      .sort((a, b) => a.generation - b.generation);
    let lastGen: number | null = null;
    return list.flatMap((h) => {
      const arr: React.ReactElement[] = [];
      if (h.generation !== lastGen) {
        arr.push(
          <Picker.Item
            key={`hdr-${p.side}-${p.cls}-${h.generation}`}
            label={`-- Gen ${h.generation} --`}
            value=""
            enabled={false}
            color="#FFFFFF"
          />
        );
        lastGen = h.generation;
      }
      arr.push(
        <Picker.Item
          key={`${p.side}-${p.cls}-${h.name}`}
          label={h.name}
          value={h.name}
          color="#FFFFFF"
        />
      );
      return arr;
    });
  }, [p.heroes, p.cls, p.side]);

  const troopItems = React.useMemo(() => (
    p.troops
      .filter((n) => n.toLowerCase().replace(/\s+/g, "").includes(p.cls.toLowerCase()))
      .map((n) => (
        <Picker.Item key={n} label={n} value={n} color="#FFFFFF" />
      ))
  ), [p.troops, p.cls]);

  const col = p.side === "atk" ? styles.attackerLabel : styles.defenderLabel;
  const pickStyle =
    p.side === "atk" ? styles.attackerPicker : styles.defenderPicker;

  // Set default values if not already selected
  React.useEffect(() => {
    // Set default hero to the last one in the filtered list if none selected
    if (!p.heroSel && p.heroes.length > 0) {
      const filteredHeroes = p.heroes.filter(
        (h) => h.charClass.toLowerCase() === p.cls.toLowerCase()
      );
      if (filteredHeroes.length > 0) {
        // Find the hero with the highest generation
        const highestGenHero = filteredHeroes.reduce((prev, current) =>
          (current.generation > prev.generation) ? current : prev
        );
        p.setHero(highestGenHero.name);
      }
    }

    // Set default troop to the last one in the filtered list if none selected
    if (!p.troopSel && p.troops.length > 0) {
      const filteredTroops = p.troops.filter((n) =>
        n.toLowerCase().replace(/\s+/g, "").includes(p.cls.toLowerCase())
      );
      if (filteredTroops.length > 0) {
        const lastTroop = filteredTroops[filteredTroops.length - 1];
        p.setTroop(lastTroop);
      }
    }
  }, [p.cls, p.heroes, p.troops, p.heroSel, p.troopSel, p.setHero, p.setTroop]);

  const percentValue = (() => {
    const v = parseFloat(p.ratio || "0");
    return Number.isNaN(v) ? 0 : Math.round(v * 100);
  })();

  const trackColour = p.side === "atk" ? "#93C5FD" : "#FCA5A5";
  const thumbColour = p.side === "atk" ? "#2563EB" : "#DC2626";

  return (
    <View style={styles.row}>
      {/* hero picker */}
      <Text style={[styles.label, col]}>
        {p.cls} Hero {p.side === "atk" ? "(Attacker)" : "(Defender)"}
      </Text>
      <View style={styles.slotPickerContainer}>
        <Text style={[styles.slotLabel, col]}>Slot:</Text>
        <Picker
          selectedValue={p.slot}
          onValueChange={p.setSlot}
          style={[styles.slotPicker, pickStyle]}
          dropdownIconColor="#FFFFFF"
          itemStyle={{ color: "#FFFFFF" }}
          enabled={!p.disabled}
        >
          <Picker.Item label="1" value="1" color="#FFFFFF" />
          <Picker.Item label="2" value="2" color="#FFFFFF" />
          <Picker.Item label="3" value="3" color="#FFFFFF" />
        </Picker>
        <Text style={[styles.slotLabel, col, { marginLeft: 16 }]}>Exclusive Weapon Lv:</Text>
        <Picker
          selectedValue={p.ewLevel}
          onValueChange={p.setEwLevel}
          style={[styles.slotPicker, pickStyle, { width: 50 }]}
          dropdownIconColor="#FFFFFF"
          itemStyle={{ color: "#FFFFFF" }}
          enabled={!p.disabled}
        >
          {Array.from({ length: 10 }).map((_, i) => (
            <Picker.Item key={`ew-${i+1}`} label={`${i+1}`} value={`${i+1}`} color="#FFFFFF" />
          ))}
        </Picker>
      </View>
      <Picker
        key={`picker-${p.side}-${p.cls}-${heroQuery}`}
        selectedValue={p.heroSel}
        onValueChange={p.setHero}
        style={[styles.picker, pickStyle]}
        dropdownIconColor="#FFFFFF"
        itemStyle={{ color: "#FFFFFF" }}
        enabled={!p.disabled}
      >
        {heroItems}
      </Picker>

      {/* troop picker */}
      <Text style={[styles.label, col]}>{p.cls} Troop</Text>
      <Picker
        selectedValue={p.troopSel}
        onValueChange={p.setTroop}
        style={[styles.picker, pickStyle]}
        dropdownIconColor="#FFFFFF"
        itemStyle={{ color: "#FFFFFF" }}
        enabled={!p.disabled}
      >
        {troopItems}
      </Picker>

      {/* ratio */}
      <View style={styles.ratioRow}>
        <Text style={[styles.label, col]}>{p.cls} Ratio (%)</Text>
        <TextInput
          style={styles.ratioInput}
          value={String(percentValue)}
          onChangeText={(txt) => {
            const frac = sanitizePercentInputToFraction(txt);
            p.setRatio(frac);
          }}
          keyboardType="numeric"
          placeholder="0-100"
          placeholderTextColor="#7B8794"
          editable={!p.disabled}
        />
        <Text style={styles.percentLabel}>{percentValue}%</Text>
        <View style={styles.miniButtons}>
          <TouchableOpacity
            style={styles.miniButton}
            onPress={() => !p.disabled && p.setRatio(String(Math.max(0, Math.round(((percentValue - 1) / 100) * 1000) / 1000)))}
          >
            <Text style={styles.miniButtonText}>-</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.miniButton}
            onPress={() => !p.disabled && p.setRatio(String(Math.min(1, Math.round(((percentValue + 1) / 100) * 1000) / 1000)))}
          >
            <Text style={styles.miniButtonText}>+</Text>
          </TouchableOpacity>
        </View>
      </View>
      <View style={{ paddingHorizontal: 4 }}>
        <Slider
          minimumValue={0}
          maximumValue={p.maxPercent ?? 100}
          step={1}
          value={percentValue}
          onValueChange={(v: number) => {
            if (p.disabled) return;
            const pct = clamp(v, 0, 100);
            const frac = String(Math.round((pct / 100) * 1000) / 1000);
            p.setRatio(frac);
          }}
          minimumTrackTintColor={trackColour}
          maximumTrackTintColor="#4B5563"
          thumbTintColor={thumbColour}
          disabled={!!p.disabled}
        />
      </View>

      {/* troop count under ratio */}
      {p.onCountChange && (
        <View style={{ marginTop: 8 }}>
          <Text style={[styles.label, col]}>{p.cls} Count</Text>
          <View style={{ flexDirection: 'row', alignItems: 'center' }}>
            <TextInput
              style={[styles.input, { flex: 1 }]}
              value={p.countValue ?? ''}
              onChangeText={p.onCountChange}
              keyboardType="number-pad"
              editable={!p.disabled}
              placeholder="0"
              placeholderTextColor="#7B8794"
            />
            {p.onLoadCountFromRatio && (
              <TouchableOpacity
                style={[styles.miniButton, { marginLeft: 8 }]}
                onPress={() => !p.disabled && p.onLoadCountFromRatio?.()}
              >
                <Text style={styles.miniButtonText}>Load from ratio</Text>
              </TouchableOpacity>
            )}
          </View>
        </View>
      )}
    </View>
  );
};
