import React from "react";
import WebCompatibleSlider from "./WebCompatibleSlider";
import { Picker, PickerItem } from "./WebCompatiblePicker";
import { Text, TextInput, View, TouchableOpacity, useWindowDimensions } from "react-native";
import { styles } from "../styles";
import { Hero, Class, HeroGearClassSelection, HeroGearPieceSelection, HeroGearChangeHandler } from "../types";
import { clamp } from "../utils/format";

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
  onHeroChange: (cls: Class, hero: string) => void;
  onTroopChange: (cls: Class, troop: string) => void;
  onSlotChange: (cls: Class, slot: string) => void;
  onEwLevelChange: (cls: Class, level: string) => void;
  onRatioChange: (cls: Class, ratio: string) => void;

  /* counts */
  count: string;
  onCountChange: (cls: Class, count: string) => void;

  /* gear */
  gearSel: HeroGearClassSelection;
  onGearChange: HeroGearChangeHandler;

  /* charms */
  charmsSel: { [slot: string]: string };
  onCharmsChange: (slot: string, charm: string) => void;

  /* skins */
  skinSel: string;
  onSkinChange: (skin: string) => void;
}

export function ClassRow(p: Props) {
  const { width } = useWindowDimensions();
  const isVerySmall = width < 480;
  const isSmall = width < 768;
  const isTablet = width >= 768 && width < 1024;

  const sideLabel = p.side === "atk" ? styles.attackerLabel : styles.defenderLabel;
  const sidePicker = p.side === "atk" ? styles.attackerPicker : styles.defenderPicker;

  const heroOptions = p.heroes.filter(h => (h.charClass || "").toLowerCase() === p.cls.toLowerCase());

  return (
    <View style={[styles.panel]}>
      {/* Header */}
      <View style={[styles.inlineRow, { alignItems: "center", justifyContent: "space-between", marginBottom: 8 }]}>
        <Text style={[styles.subHeader, sideLabel]}>{p.cls} Setup</Text>
        <View style={[styles.pill]}>
          <Text style={styles.pillText}>{p.side === "atk" ? "Attacker" : "Defender"}</Text>
        </View>
      </View>

      {/* Selects */}
      <View style={styles.row}>
        <View style={styles.inlineRow}>
          <View style={{ flex: 1 }}>
            <Text style={styles.label}>Hero</Text>
            <Picker
              selectedValue={p.heroSel}
              onValueChange={(v) => p.onHeroChange(p.cls, String(v))}
              style={[isVerySmall ? styles.mobilePicker : styles.picker, sidePicker]}
            >
              <PickerItem label="— choose hero —" value="" />
              {heroOptions.map(h => <PickerItem key={h.name} label={h.name} value={h.name} />)}
            </Picker>
          </View>

          <View style={{ flex: 1 }}>
            <Text style={styles.label}>Troop Type</Text>
            <Picker
              selectedValue={p.troopSel}
              onValueChange={(v) => p.onTroopChange(p.cls, String(v))}
              style={[isVerySmall ? styles.mobilePicker : styles.picker, sidePicker]}
            >
              <PickerItem label="— choose troop —" value="" />
              {p.troops.map(t => <PickerItem key={`${p.cls}-${t}`} label={t} value={t} />)}
            </Picker>
          </View>
        </View>
      </View>

      {/* EW + Slot */}
      <View style={styles.row}>
        <View style={styles.inlineRow}>
          <View style={{ flex: 1 }}>
            <Text style={styles.label}>Exclusive Weapon Level</Text>
            <TextInput
              value={p.ewLevel}
              onChangeText={(v) => p.onEwLevelChange(p.cls, v.replace(/[^0-9]/g, ""))}
              keyboardType="number-pad"
              style={isVerySmall ? styles.mobileInput : styles.input}
              placeholder="1 - 10"
              placeholderTextColor="#7B8794"
            />
          </View>
          <View style={{ flex: 1 }}>
            <Text style={styles.label}>Formation Slot</Text>
            <TextInput
              value={p.slot}
              onChangeText={(v) => p.onSlotChange(p.cls, v.replace(/[^0-9]/g, ""))}
              keyboardType="number-pad"
              style={isVerySmall ? styles.mobileInput : styles.input}
              placeholder="1 - 3"
              placeholderTextColor="#7B8794"
            />
          </View>
        </View>
      </View>

      {/* Ratio */}
      <View style={styles.row}>
        <Text style={styles.label}>Troop Ratio</Text>
        <View style={[styles.inlineRow, { alignItems: "center" }]}>
          <WebCompatibleSlider
            value={parseFloat(p.ratio || "0")}
            minimumValue={0}
            maximumValue={1}
            step={0.01}
            onValueChange={(v) => p.onRatioChange(p.cls, String(Math.round(v * 1000) / 1000))}
            style={{ flex: 1 }}
            accessibilityLabel="Troop ratio slider"
          />
          <View style={styles.pill}>
            <Text style={styles.pillText}>{Math.round((parseFloat(p.ratio || "0") || 0) * 100)}%</Text>
          </View>
        </View>
      </View>

      {/* Count */}
      <View style={styles.row}>
        <Text style={styles.label}>Troop Count</Text>
        <TextInput
          value={p.count}
          onChangeText={(v) => p.onCountChange(p.cls, v.replace(/[^0-9]/g, ""))}
          keyboardType="number-pad"
          style={isVerySmall ? styles.mobileInput : styles.input}
          placeholder="0"
          placeholderTextColor="#7B8794"
        />
      </View>
    </View>
  );
}
