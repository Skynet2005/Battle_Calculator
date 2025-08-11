"""
Lancer Belt Calculator Module

This module calculates Lancer Health (LH) stats for mythical belt gear.
It handles gear level, mastery forging, essence stones, and different stacking modes.
The calculator supports essence level input (0-20) to determine the appropriate multiplier.
It also includes Lancer Attack and Defense Empowerment bonuses at specific levels.
"""

from typing import Dict, List, Literal, TypedDict, Union
from math import floor

# Type definitions
StackMode = Literal["additive", "multiplicative"]

class LHResult(TypedDict):
    level: int                       # 0..200
    baseLH: float                    # Base Lancer Health from table (%)
    masteryForged: bool              # Whether mastery forging is applied
    masteryLevel: int                # 0..20
    essenceLevel: int                # 0..20
    masteryMultiplier: float         # from table (e.g., 0.0..2.0)
    essenceMultiplier: float         # from table (e.g., 0.0..2.0)
    effectiveMultiplier: float       # (1 + m + e) or (1+m)*(1+e)
    totalLH: float                   # baseLH * effectiveMultiplier (%)
    stacking: StackMode
    lancer_health_pct: float         # Total Lancer Health percentage for front end
    lancer_attack_pct: float         # Lancer Attack Empowerment bonus (%)
    lancer_defense_pct: float        # Lancer Defense Empowerment bonus (%)
    lancer_power: int                # Lancer Power (placeholder for future implementation)

"""
Mastery/Essence multiplier table (level -> multiplier).
Matches your "Mastery | Multiplier" rows exactly.
0→0.0, 1→0.1, ..., 20→2.0
"""
ESSENCE_STONE_LEVEL = [
    0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
    1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9,
    2.0
]

"""
Belt (Mythical) — Lancer Health (%) by gear level.
Index = level (0..200), value = base LH% at that level (before mastery/essence multipliers).
Copied 1:1 from your Level→Stats table.
"""
BELT_LH_BY_LEVEL = [
    3.33, 3.80, 4.26, 4.73, 5.20, 5.66, 6.13, 6.60, 7.06, 7.53,
    8.00, 8.46, 8.93, 9.40, 9.86, 10.33, 10.80, 11.26, 11.73, 12.20,
    12.66, 13.13, 13.60, 14.06, 14.53, 15.00, 15.46, 15.93, 16.40, 16.86,
    17.33, 17.80, 18.26, 18.73, 19.20, 19.66, 20.13, 20.60, 21.06, 21.53,
    22.00, 22.46, 22.93, 23.40, 23.86, 24.33, 24.80, 25.26, 25.73, 26.20,
    26.66, 27.13, 27.60, 28.06, 28.53, 29.00, 29.46, 29.93, 30.40, 30.86,
    31.33, 31.80, 32.26, 32.73, 33.20, 33.66, 34.13, 34.60, 35.06, 35.53,
    36.00, 36.46, 36.93, 37.40, 37.86, 38.33, 38.80, 39.26, 39.73, 40.20,
    40.66, 41.13, 41.60, 42.06, 42.53, 43.00, 43.46, 43.93, 44.40, 44.86,
    45.33, 45.80, 46.26, 46.73, 47.20, 47.66, 48.13, 48.60, 49.06, 49.53,
    50.00, 50.50, 51.00, 51.50, 52.00, 52.50, 53.00, 53.50, 54.00, 54.50,
    55.00, 55.50, 56.00, 56.50, 57.00, 57.50, 58.00, 58.50, 59.00, 59.50,
    60.00, 60.50, 61.00, 61.50, 62.00, 62.50, 63.00, 63.50, 64.00, 64.50,
    65.00, 65.50, 66.00, 66.50, 67.00, 67.50, 68.00, 68.50, 69.00, 69.50,
    70.00, 70.50, 71.00, 71.50, 72.00, 72.50, 73.00, 73.50, 74.00, 74.50,
    75.00, 75.50, 76.00, 76.50, 77.00, 77.50, 78.00, 78.50, 79.00, 79.50,
    80.00, 80.50, 81.00, 81.50, 82.00, 82.50, 83.00, 83.50, 84.00, 84.50,
    85.00, 85.50, 86.00, 86.50, 87.00, 87.50, 88.00, 88.50, 89.00, 89.50,
    90.00, 90.50, 91.00, 91.50, 92.00, 92.50, 93.00, 93.50, 94.00, 94.50,
    95.00, 95.50, 96.00, 96.50, 97.00, 97.50, 98.00, 98.50, 99.00, 99.50,
    100.00
]

def clamp(n: float, min_val: int, max_val: int) -> int:
    return min(max(floor(n), min_val), max_val)

def round2(n: float) -> float:
    return round(n * 100) / 100

"""
Core calculator.
- If masteryForged=False, ignores mastery/essence and returns base.
- If masteryForged=True, applies both mastery and essence multipliers.
- stacking="additive": total = base * (1 + mastery + essence)
- stacking="multiplicative": total = base * (1 + mastery) * (1 + essence)
- Adds Lancer Attack/Defense Empowerment bonuses at specific levels:
  - Level 120: +20% Lancer Attack
  - Level 160: +30% Lancer Defense
  - Level 200: +50% Lancer Attack (stacks with level 120 bonus)
"""
def calc_belt_lancer_lh(
    level: int,
    mastery_forged: bool,
    mastery_level: int = 0,
    essence_level: int = 0,
    stacking: StackMode = "additive"
) -> LHResult:
    lvl = clamp(level, 0, 200)
    base_lh = BELT_LH_BY_LEVEL[lvl]

    m_lvl = clamp(mastery_level, 0, 20) if mastery_forged else 0
    e_lvl = clamp(essence_level, 0, 20) if mastery_forged else 0

    m_mul = ESSENCE_STONE_LEVEL[m_lvl]
    e_mul = ESSENCE_STONE_LEVEL[e_lvl]

    if stacking == "additive":
        effective_multiplier = 1 + m_mul + e_mul
    else:  # multiplicative
        effective_multiplier = (1 + m_mul) * (1 + e_mul)

    total_lh = round2(base_lh * effective_multiplier)
    
    # Calculate lancer_health_pct for front end
    lancer_health_pct = total_lh
    
    # Calculate Lancer Attack and Defense Empowerment bonuses based on level
    lancer_attack_pct = 0.0
    lancer_defense_pct = 0.0
    lancer_power = 0
    
    # Level 120: +20% Lancer Attack
    if lvl >= 120:
        lancer_attack_pct += 20.0
    
    # Level 160: +30% Lancer Defense
    if lvl >= 160:
        lancer_defense_pct += 30.0
    
    # Level 200: +50% Lancer Attack (stacks with level 120 bonus)
    if lvl >= 200:
        lancer_attack_pct += 50.0

    return {
        "level": lvl,
        "baseLH": base_lh,
        "masteryForged": mastery_forged,
        "masteryLevel": m_lvl,
        "essenceLevel": e_lvl,
        "masteryMultiplier": m_mul,
        "essenceMultiplier": e_mul,
        "effectiveMultiplier": effective_multiplier,
        "totalLH": total_lh,
        "stacking": stacking,
        "lancer_health_pct": lancer_health_pct,
        "lancer_attack_pct": lancer_attack_pct,
        "lancer_defense_pct": lancer_defense_pct,
        "lancer_power": lancer_power
    }
