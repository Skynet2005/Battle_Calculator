export function clamp(value: number, min: number, max: number): number {
  if (Number.isNaN(value)) return min;
  return Math.max(min, Math.min(max, value));
}

export function sanitizePercentInputToFraction(input: string): string {
  const cleaned = String(input ?? "").replace(/[^0-9.]/g, "");
  const firstDot = cleaned.indexOf(".");
  const normalized =
    firstDot === -1
      ? cleaned
      : cleaned.slice(0, firstDot + 1) + cleaned.slice(firstDot + 1).replace(/\./g, "");
  let pct = parseFloat(normalized);
  if (Number.isNaN(pct)) return "";
  pct = clamp(pct, 0, 100);
  const frac = Math.round((pct / 100) * 1000) / 1000;
  return String(frac);
}

export function removeLevelWord(label: string): string {
  return String(label || "").replace(/level\s*/i, "").trim();
}


