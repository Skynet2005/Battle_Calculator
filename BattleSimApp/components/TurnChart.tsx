import React from "react";
import { View, Platform } from "react-native";

// Platform-adaptive Victory import: use 'victory' on web and 'victory-native' on native
// Created Logic for review: resolve undefined component error on web when importing from victory-native
// eslint-disable-next-line @typescript-eslint/no-var-requires
const VictoryLib: any = Platform.OS === "web" ? require("victory") : require("victory-native");
const {
  VictoryChart,
  VictoryAxis,
  VictoryLine,
  VictoryScatter,
  VictoryTooltip,
  VictoryLegend,
  VictoryStack,
  VictoryArea,
} = VictoryLib;

type EventPoint = { x: number; y: number; label: string };
type SeriesPoint = { x: number; y: number };

export type TurnTimeline = {
  turn: number;
  attacker: { base?: number; Infantry?: number; Lancer?: number; Marksman?: number; extra?: number };
  defender: { base?: number; Infantry?: number; Lancer?: number; Marksman?: number; extra?: number };
  events: { side: "atk" | "def"; skill: string; class: string; amount?: number }[];
}[];

export const TurnChart: React.FC<{
  timeline: TurnTimeline;
  side: "attacker" | "defender";
  showClasses?: boolean;
  height?: number;
  variant?: "line" | "stacked" | "bar";
}> = ({ timeline, side, showClasses = true, height = 320, variant = "stacked" }) => {
  if (!timeline || timeline.length === 0) return null;

  // Use base only for total curve so class lines remain visible (extra is shown via proc markers)
  const tot = (s: any) => s?.base ?? 0;
  const key = side;

  const totalSeries: SeriesPoint[] = timeline.map((t) => ({
    x: t.turn,
    y: tot(t[key]),
  }));

  const clsSeries = (c: "Infantry" | "Lancer" | "Marksman") =>
    timeline.map((t) => ({ x: t.turn, y: t[key]?.[c] ?? 0 }));

  const inf = clsSeries("Infantry");
  const lan = clsSeries("Lancer");
  const mar = clsSeries("Marksman");

  // Skill markers on the total curve
  const procDots: EventPoint[] = timeline.flatMap((t) => {
    const y = tot(t[key]);
    const evs = t.events.filter((e) => e.side === (side === "attacker" ? "atk" : "def"));
    const names = Array.from(new Set(evs.map((e) => e.skill)));
    return names.map((name) => ({ x: t.turn, y, label: `${name} (T${t.turn})` }));
  });

  // Colors and formatting for dark background
  const colorTotal = "#e5e7eb";     // gray-200
  const colorInf = "#60a5fa";       // blue-400
  const colorLan = "#f59e0b";       // amber-500
  const colorMar = "#34d399";       // emerald-400
  const colorGrid = "#334155";      // slate-700
  const colorAxis = "#9ca3af";      // gray-400

  const fmt = (n: number) => {
    if (n >= 1_000_000_000) return `${(n / 1_000_000_000).toFixed(1)}B`;
    if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
    if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k`;
    return `${Math.round(n)}`;
  };

  const allY = [...totalSeries, ...inf, ...lan, ...mar].map((p) => (typeof p.y === "number" ? p.y : 0));
  const maxY = Math.max(1, ...allY);

  return (
    <View style={{ width: "100%", height }}>
      <VictoryChart
        padding={{ top: 12, bottom: 46, left: 72, right: 24 }}
        domainPadding={{ x: 14, y: 8 }}
        domain={{ y: [0, maxY * 1.05] }}
      >
        <VictoryAxis
          label="Turn"
          style={{
            axis: { stroke: colorGrid },
            tickLabels: { fill: colorAxis, fontSize: 10 },
            grid: { stroke: colorGrid, opacity: 0.4 },
            axisLabel: { padding: 30, fill: colorAxis },
          }}
        />
        <VictoryAxis
          dependentAxis
          tickFormat={(t: number) => fmt(t)}
          label="Damage"
          style={{
            axis: { stroke: colorGrid },
            tickLabels: { fill: colorAxis, fontSize: 10 },
            grid: { stroke: colorGrid, opacity: 0.4 },
            axisLabel: { padding: 44, fill: colorAxis },
          }}
        />

        {/* Class contributions */}
        {showClasses && variant === "stacked" && (
          <VictoryStack>
            <VictoryArea data={inf} style={{ data: { fill: colorInf, fillOpacity: 0.25, stroke: colorInf, strokeWidth: 2 } }} />
            <VictoryArea data={lan} style={{ data: { fill: colorLan, fillOpacity: 0.25, stroke: colorLan, strokeWidth: 2 } }} />
            <VictoryArea data={mar} style={{ data: { fill: colorMar, fillOpacity: 0.25, stroke: colorMar, strokeWidth: 2 } }} />
          </VictoryStack>
        )}

        {/* Total overlay */}
        <VictoryLine data={totalSeries} style={{ data: { stroke: colorTotal, strokeWidth: 2.2, strokeOpacity: 0.6 } }} />

        {/* Per-class overlays + markers for visibility (line variant) */}
        {showClasses && variant === "line" && (
          <>
            <VictoryLine data={inf} style={{ data: { stroke: colorInf, strokeWidth: 3 } }} />
            <VictoryScatter
              data={inf}
              size={2.8}
              style={{ data: { fill: colorInf } }}
              labels={({ datum }: { datum: any }) => (datum.y ? `Infantry ${fmt(datum.y)}` : "")}
              labelComponent={<VictoryTooltip dy={-8} style={{ fontSize: 10 }} />}
            />

            <VictoryLine data={lan} style={{ data: { stroke: colorLan, strokeWidth: 3 } }} />
            <VictoryScatter
              data={lan}
              size={2.8}
              style={{ data: { fill: colorLan } }}
              labels={({ datum }: { datum: any }) => (datum.y ? `Lancer ${fmt(datum.y)}` : "")}
              labelComponent={<VictoryTooltip dy={-8} style={{ fontSize: 10 }} />}
            />

            <VictoryLine data={mar} style={{ data: { stroke: colorMar, strokeWidth: 3 } }} />
            <VictoryScatter
              data={mar}
              size={2.8}
              style={{ data: { fill: colorMar } }}
              labels={({ datum }: { datum: any }) => (datum.y ? `Marksman ${fmt(datum.y)}` : "")}
              labelComponent={<VictoryTooltip dy={-8} style={{ fontSize: 10 }} />}
            />
          </>
        )}

        {/* Proc markers */}
        <VictoryScatter
          data={procDots}
          size={3.5}
          style={{ data: { fill: "#f472b6" } }}
          labels={({ datum }: { datum: any }) => datum.label}
          labelComponent={<VictoryTooltip dy={-10} style={{ fontSize: 10 }} />}
        />

        <VictoryLegend
          x={72}
          y={6}
          orientation="horizontal"
          gutter={14}
          itemsPerRow={4}
          style={{ labels: { fill: colorAxis, fontSize: 11 } }}
          data={[
            { name: "Total", symbol: { type: "minus", fill: colorTotal } },
            ...(showClasses
              ? [
                  { name: "Infantry", symbol: { type: "minus", fill: colorInf } },
                  { name: "Lancer", symbol: { type: "minus", fill: colorLan } },
                  { name: "Marksman", symbol: { type: "minus", fill: colorMar } },
                ]
              : []),
            { name: "Skill procs", symbol: { type: "circle", fill: "#f472b6" } },
          ]}
        />
      </VictoryChart>
    </View>
  );
};

// Combined overlay chart: Attacker vs Defender totals on one graph
export const CombinedTurnChart: React.FC<{
  timeline: TurnTimeline;
  height?: number;
}> = ({ timeline, height = 320 }) => {
  if (!timeline || timeline.length === 0) return null;

  const tot = (s: any) => s?.base ?? 0;
  const att: SeriesPoint[] = timeline.map((t) => ({ x: t.turn, y: tot(t.attacker) }));
  const def: SeriesPoint[] = timeline.map((t) => ({ x: t.turn, y: tot(t.defender) }));

  const colorAtt = "#10b981"; // emerald-500
  const colorDef = "#ef4444"; // red-500
  const colorGrid = "#334155"; // slate-700
  const colorAxis = "#9ca3af"; // gray-400

  const fmt = (n: number) => {
    if (n >= 1_000_000_000) return `${(n / 1_000_000_000).toFixed(1)}B`;
    if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
    if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k`;
    return `${Math.round(n)}`;
  };

  const maxY = Math.max(1, ...att.map((p) => p.y), ...def.map((p) => p.y));

  return (
    <View style={{ width: "100%", height }}>
      <VictoryChart padding={{ top: 12, bottom: 46, left: 72, right: 24 }} domainPadding={{ x: 14, y: 8 }} domain={{ y: [0, maxY * 1.05] }}>
        <VictoryAxis
          label="Turn"
          style={{ axis: { stroke: colorGrid }, tickLabels: { fill: colorAxis, fontSize: 10 }, grid: { stroke: colorGrid, opacity: 0.4 }, axisLabel: { padding: 30, fill: colorAxis } }}
        />
        <VictoryAxis
          dependentAxis
          tickFormat={(t: number) => fmt(t)}
          label="Damage"
          style={{ axis: { stroke: colorGrid }, tickLabels: { fill: colorAxis, fontSize: 10 }, grid: { stroke: colorGrid, opacity: 0.4 }, axisLabel: { padding: 44, fill: colorAxis } }}
        />

        <VictoryLine data={att} style={{ data: { stroke: colorAtt, strokeWidth: 3 } }} />
        <VictoryScatter
          data={att}
          size={2.8}
          style={{ data: { fill: colorAtt } }}
          labels={({ datum }: { datum: any }) => (datum.y ? `Attacker ${fmt(datum.y)}` : "")}
          labelComponent={<VictoryTooltip dy={-8} style={{ fontSize: 10 }} />}
        />

        <VictoryLine data={def} style={{ data: { stroke: colorDef, strokeWidth: 3 } }} />
        <VictoryScatter
          data={def}
          size={2.8}
          style={{ data: { fill: colorDef } }}
          labels={({ datum }: { datum: any }) => (datum.y ? `Defender ${fmt(datum.y)}` : "")}
          labelComponent={<VictoryTooltip dy={-8} style={{ fontSize: 10 }} />}
        />

        <VictoryLegend
          x={72}
          y={6}
          orientation="horizontal"
          gutter={14}
          itemsPerRow={4}
          style={{ labels: { fill: colorAxis, fontSize: 11 } }}
          data={[
            { name: "Attacker", symbol: { type: "minus", fill: colorAtt } },
            { name: "Defender", symbol: { type: "minus", fill: colorDef } },
          ]}
        />
      </VictoryChart>
    </View>
  );
};