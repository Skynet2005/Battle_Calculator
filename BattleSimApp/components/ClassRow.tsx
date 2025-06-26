import React from "react";
import { Picker } from "@react-native-picker/picker";
import { Text, TextInput, View } from "react-native";
import { styles } from "../styles";
import { Hero, Class } from "../types";

interface Props {
  cls: Class;                     // "Infantry" | "Lancer" | "Marksman"
  side: "atk" | "def";
  heroes: Hero[];
  troops: string[];

  /* selections + setters */
  heroSel: string;
  troopSel: string;
  slot: string;
  ratio: string;
  setHero: (name: string) => void;
  setTroop: (name: string) => void;
  setSlot: (slot: string) => void;
  setRatio: (ratio: string) => void;
}

export const ClassRow: React.FC<Props> = (p) => {
  /* hero list filtered + grouped by gen */
  const heroItems = (() => {
    const list = p.heroes
      .filter((h) => h.charClass.toLowerCase() === p.cls.toLowerCase())
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
  })();

  const troopItems = p.troops
    .filter((n) =>
      n.toLowerCase().replace(/\s+/g, "").includes(p.cls.toLowerCase())
    )
    .map((n) => (
      <Picker.Item key={n} label={n} value={n} color="#FFFFFF" />
    ));

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
        >
          <Picker.Item label="1" value="1" color="#FFFFFF" />
          <Picker.Item label="2" value="2" color="#FFFFFF" />
          <Picker.Item label="3" value="3" color="#FFFFFF" />
        </Picker>
      </View>
      <Picker
        selectedValue={p.heroSel}
        onValueChange={p.setHero}
        style={[styles.picker, pickStyle]}
        dropdownIconColor="#FFFFFF"
        itemStyle={{ color: "#FFFFFF" }}
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
      >
        {troopItems}
      </Picker>

      {/* ratio */}
      <View style={styles.ratioRow}>
        <Text style={[styles.label, col]}>{p.cls} Ratio</Text>
        <TextInput
          style={styles.ratioInput}
          value={p.ratio}
          onChangeText={p.setRatio}
          keyboardType="decimal-pad"
          placeholder="0.0-1.0"
          placeholderTextColor="#7B8794"
        />
      </View>
    </View>
  );
};
