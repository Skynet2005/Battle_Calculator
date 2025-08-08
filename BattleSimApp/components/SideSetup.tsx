import React from "react";
import { Text, View, TextInput } from "react-native";
import { ClassRow } from "./ClassRow";
import { Hero, Class, ClassSel } from "../types";
import { styles } from "../styles";

interface Props {
  side: "atk" | "def";
  heroes: Hero[];
  troops: string[];

  heroSel: ClassSel;
  troopSel: ClassSel;
  slotSel: { [cls in Class]: string };
  ratioSel: { [cls in Class]: string };

  /* setters for the four objects above */
  setHeroSel: React.Dispatch<React.SetStateAction<ClassSel>>;
  setTroopSel: React.Dispatch<React.SetStateAction<ClassSel>>;
  setSlotSel: React.Dispatch<
    React.SetStateAction<{ [cls in Class]: string }>
  >;
  setRatioSel: React.Dispatch<
    React.SetStateAction<{ [cls in Class]: string }>
  >;
  disabled?: boolean;
  capacity: string;
  setCapacity: (v: string) => void;
}

export const SideSetup: React.FC<Props> = (p) => {
  const sum = (Object.values(p.ratioSel) as string[])
    .map((v) => parseFloat(v || "0"))
    .reduce((a, b) => a + (isNaN(b) ? 0 : b), 0);
  const isOk = Math.abs(sum - 1) < 0.001;

  const classes: Class[] = ["Infantry", "Lancer", "Marksman"];
  const [counts, setCounts] = React.useState<{ [cls in Class]: string }>({ Infantry: "", Lancer: "", Marksman: "" });
  const [countsTouched, setCountsTouched] = React.useState(false);
  const capacityInt = parseInt(p.capacity, 10) || 0;

  React.useEffect(() => {
    if (countsTouched) return;
    const next: { [cls in Class]: string } = { Infantry: "", Lancer: "", Marksman: "" };
    (classes).forEach((cls) => {
      const r = Math.max(0, parseFloat(p.ratioSel[cls] || "0"));
      next[cls] = String(Math.round(capacityInt * r));
    });
    setCounts(next);
  }, [p.ratioSel.Infantry, p.ratioSel.Lancer, p.ratioSel.Marksman, capacityInt, countsTouched]);

  const onCountChange = (cls: Class, txt: string) => {
    const cleaned = txt.replace(/[^0-9]/g, "");
    setCounts((prev) => ({ ...prev, [cls]: cleaned }));
    setCountsTouched(true);
    const nums = classes.map((c) => parseInt(c === cls ? cleaned : (counts[c] || "0"), 10) || 0);
    const total = nums.reduce((a, b) => a + b, 0);
    if (total > 0) {
      const nextRatios: { [k in Class]: string } = { Infantry: "0", Lancer: "0", Marksman: "0" };
      classes.forEach((c, i) => {
        nextRatios[c] = String(Math.round((nums[i] / total) * 1000) / 1000);
      });
      p.setRatioSel(nextRatios);
    }
  };

  const sumCounts = classes.map((c) => parseInt(counts[c] || "0", 10) || 0).reduce((a, b) => a + b, 0);

  const normalize = () => {
    // Created Logic for review: normalize ratios to sum to 1
    const vals = (Object.values(p.ratioSel) as string[]).map((v) => Math.max(0, parseFloat(v || "0")));
    const total = vals.reduce((a, b) => a + (isNaN(b) ? 0 : b), 0);
    const safeTotal = total > 0 ? total : 1;
    const classes: Class[] = ["Infantry", "Lancer", "Marksman"];
    const next = { ...p.ratioSel } as { [cls in Class]: string };
    classes.forEach((cls, i) => {
      next[cls] = String(Math.round((vals[i] / safeTotal) * 1000) / 1000);
    });
    p.setRatioSel(next);
  };

  return (
    <>
      {(["Infantry", "Lancer", "Marksman"] as const).map((cls) => {
        const others = (["Infantry", "Lancer", "Marksman"] as const)
          .filter((c) => c !== cls)
          .map((c) => Math.max(0, parseFloat(p.ratioSel[c] || "0")))
          .reduce((a, b) => a + (isNaN(b) ? 0 : b), 0);
        const remainingPct = Math.max(0, Math.round((1 - others) * 100));
        const currentPct = Math.max(0, Math.round(parseFloat(p.ratioSel[cls] || "0") * 100));
        const maxPercent = Math.max(currentPct, remainingPct);
        return (
        <ClassRow
          key={`${p.side}-${cls}`}
          cls={cls}
          side={p.side}
          heroes={p.heroes}
          troops={p.troops}
          heroSel={p.heroSel[cls]}
          troopSel={p.troopSel[cls]}
          slot={p.slotSel[cls]}
          ratio={p.ratioSel[cls]}
          setHero={(v) =>
            p.setHeroSel((s) => ({ ...s, [cls]: v }))
          }
          setTroop={(v) =>
            p.setTroopSel((s) => ({ ...s, [cls]: v }))
          }
          setSlot={(v) =>
            p.setSlotSel((s) => ({ ...s, [cls]: v }))
          }
          setRatio={(v) =>
            p.setRatioSel((prev) => {
              // Created Logic for review: clamp per-side ratios so total <= 1 (<=100%)
              const classes: Class[] = ["Infantry", "Lancer", "Marksman"];
              const requested = Math.max(0, Math.min(1, parseFloat(v || "0")));
              const otherSum = classes
                .filter((c) => c !== cls)
                .map((c) => Math.max(0, parseFloat(prev[c] || "0")))
                .reduce((a, b) => a + (isNaN(b) ? 0 : b), 0);
              const maxAllowed = Math.max(0, 1 - otherSum);
              const finalVal = Math.min(requested, maxAllowed);
              const out = String(Math.round(finalVal * 1000) / 1000);
              return { ...prev, [cls]: out } as { [k in Class]: string };
            })
          }
          disabled={p.disabled}
          maxPercent={maxPercent}
          countValue={counts[cls]}
          onCountChange={(t) => onCountChange(cls, t)}
          onLoadCountFromRatio={() => {
            const r = Math.max(0, parseFloat(p.ratioSel[cls] || "0"));
            const c = String(Math.round(capacityInt * r));
            setCounts((prev) => ({ ...prev, [cls]: c }));
          }}
        />
        );
      })}
      <View style={styles.helperActionsRow}>
        <Text style={styles.linkTextSecondary} onPress={() => {
          const classes: Class[] = ["Infantry", "Lancer", "Marksman"];
          const val = String(Math.round((1/3) * 1000) / 1000);
          p.setRatioSel(Object.fromEntries(classes.map(c => [c, val])) as { [k in Class]: string });
        }}>Even Split</Text>
        <Text style={styles.linkText} onPress={() => {
          p.setRatioSel({ Infantry: "1", Lancer: "0", Marksman: "0" });
        }}>100% Infantry</Text>
        <Text style={styles.linkText} onPress={() => {
          p.setRatioSel({ Infantry: "0", Lancer: "1", Marksman: "0" });
        }}>100% Lancer</Text>
        <Text style={styles.linkText} onPress={() => {
          p.setRatioSel({ Infantry: "0", Lancer: "0", Marksman: "1" });
        }}>100% Marksman</Text>
        {!isOk && (
          <Text style={styles.linkTextDanger} onPress={normalize}>Normalize</Text>
        )}
      </View>
      <View style={styles.helperActionsRow}>
        <Text style={styles.linkTextSecondary} onPress={() => {
          // Load counts from current ratios and capacity
          setCountsTouched(false);
        }}>Reload all counts from ratios</Text>
        <Text style={styles.linkText} onPress={() => {
          // Adjust capacity to match sum of manual counts
          p.setCapacity(String(sumCounts));
        }}>Set Capacity = Sum of counts</Text>
      </View>
      <Text style={[styles.helperText, (sumCounts === capacityInt) ? styles.helperTextOk : styles.helperTextWarn]}>
        Sum of counts: {sumCounts} / Capacity: {capacityInt}
      </Text>
      <Text
        style={[
          styles.helperText,
          isOk ? styles.helperTextOk : styles.helperTextWarn,
        ]}
      >
        {p.side === "atk" ? "Attacker" : "Defender"} ratios sum: {sum.toFixed(3)}
      </Text>
      <View style={styles.progressBar}>
        <View style={[styles.progressFill, { width: `${Math.min(100, Math.max(0, sum * 100))}%`, backgroundColor: isOk ? '#10B981' : '#F59E0B' }]} />
      </View>
    </>
  );
};
