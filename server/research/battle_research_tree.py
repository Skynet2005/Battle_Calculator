"""
battle_research.py

Structure and helpers for Whiteout Survival-style Battle Research data.

Notes
-----
- All stat values (e.g., "Troop Attack": 0.5) are percentage POINTS applied
  to Infantry, Lancer, and Marksman base stats unless a specific troop type
  is named (e.g., "Infantry Health", "Marksman Attack", etc.).
- The nested structure is:
    BATTLE_RESEARCH["Battle Research"][<Category Name>][<Tier Label>]
- Each node contains:
    - A numeric tier marker under a key equal to the category name
      (e.g., {"Weapons Prep": 1, ...})
    - "level": the level within the tier (1..n)
    - "power": power cost
    - 1 stat field (e.g., "Troop Attack", "Infantry Defense", etc.)

Utilities
---------
- get_category_names() -> list of categories
- get_tier_labels(category) -> list of tier labels (e.g., "Level 1", ...)
- get_nodes(category, tier_label) -> list[dict] of nodes
- find_stat(category, tier_label, level, stat_name) -> float | None
- flatten() -> list of rows: {category, tier_label, level, stat_name, value, power}
"""

from __future__ import annotations
from typing import Dict, List, Any, Iterable, Optional, TypedDict


BattleResearchTree = Dict[str, Dict[str, Dict[str, List[dict]]]]  # top-level shape


BATTLE_RESEARCH: BattleResearchTree = {
    "Battle Research": {
        "Weapons Prep": {
            "Level 1": [
                {"Weapons Prep": 1, "level": 1, "Troop Attack": 0.5, "power": 4200},
                {"Weapons Prep": 1, "level": 2, "Troop Attack": 1.0, "power": 8400},
                {"Weapons Prep": 1, "level": 3, "Troop Attack": 1.5, "power": 12600}
            ],
            "Level 2": [
                {"Weapons Prep": 2, "level": 1, "Troop Attack": 0.75, "power": 6300},
                {"Weapons Prep": 2, "level": 2, "Troop Attack": 1.5, "power": 12600},
                {"Weapons Prep": 2, "level": 3, "Troop Attack": 2.5, "power": 21000}
            ],
            "Level 3": [
                {"Weapons Prep": 3, "level": 1, "Troop Attack": 1, "power": 8400},
                {"Weapons Prep": 3, "level": 2, "Troop Attack": 2, "power": 16800},
                {"Weapons Prep": 3, "level": 3, "Troop Attack": 3, "power": 25200},
                {"Weapons Prep": 3, "level": 4, "Troop Attack": 4.5, "power": 33800}
            ],
            "Level 4": [
                {"Weapons Prep": 4, "level": 1, "Troop Attack": 1.75, "power": 14700},
                {"Weapons Prep": 4, "level": 2, "Troop Attack": 3.5, "power": 29400},
                {"Weapons Prep": 4, "level": 3, "Troop Attack": 5.25, "power": 44100},
                {"Weapons Prep": 4, "level": 4, "Troop Attack": 7, "power": 58800},
                {"Weapons Prep": 4, "level": 5, "Troop Attack": 10, "power": 84000}
            ],
            "Level 5": [
                {"Weapons Prep": 5, "level": 1, "Troop Attack": 2, "power": 16800},
                {"Weapons Prep": 5, "level": 2, "Troop Attack": 4, "power": 33600},
                {"Weapons Prep": 5, "level": 3, "Troop Attack": 6, "power": 50400},
                {"Weapons Prep": 5, "level": 4, "Troop Attack": 8, "power": 67200},
                {"Weapons Prep": 5, "level": 5, "Troop Attack": 10, "power": 84000},
                {"Weapons Prep": 5, "level": 6, "Troop Attack": 13.5, "power": 113400}
            ],
            "Level 6": [
                {"Weapons Prep": 6, "level": 1, "Troop Attack": 2.25, "power": 18900},
                {"Weapons Prep": 6, "level": 2, "Troop Attack": 4.5, "power": 37800},
                {"Weapons Prep": 6, "level": 3, "Troop Attack": 6.75, "power": 56700},
                {"Weapons Prep": 6, "level": 4, "Troop Attack": 9, "power": 75600},
                {"Weapons Prep": 6, "level": 5, "Troop Attack": 11.25, "power": 94500},
                {"Weapons Prep": 6, "level": 6, "Troop Attack": 15.25, "power": 128100}
            ]
        },
        "Reprisal Tactics": {
            "Level 1": [
                {"Reprisal Tactics": 1, "level": 1, "Infantry Attack": 1.25, "power": 1750},
                {"Reprisal Tactics": 1, "level": 2, "Infantry Attack": 2.5, "power": 3500},
                {"Reprisal Tactics": 1, "level": 3, "Infantry Attack": 4, "power": 5600}
            ],
            "Level 2": [
                {"Reprisal Tactics": 2, "level": 1, "Infantry Attack": 1.75, "power": 2450},
                {"Reprisal Tactics": 2, "level": 2, "Infantry Attack": 3.9, "power": 4900},
                {"Reprisal Tactics": 2, "level": 3, "Infantry Attack": 5.5, "power": 7700}
            ],
            "Level 3": [
                {"Reprisal Tactics": 3, "level": 1, "Infantry Attack": 12.5, "power": 3500},
                {"Reprisal Tactics": 3, "level": 2, "Infantry Attack": 5, "power": 7000},
                {"Reprisal Tactics": 3, "level": 3, "Infantry Attack": 7.5, "power": 10500},
                {"Reprisal Tactics": 3, "level": 4, "Infantry Attack": 11.5, "power": 16100}
            ],
            "Level 4": [
                {"Reprisal Tactics": 4, "level": 1, "Infantry Attack": 4, "power": 5600},
                {"Reprisal Tactics": 4, "level": 2, "Infantry Attack": 8, "power": 11200},
                {"Reprisal Tactics": 4, "level": 3, "Infantry Attack": 12, "power": 16800},
                {"Reprisal Tactics": 4, "level": 4, "Infantry Attack": 16, "power": 22400},
                {"Reprisal Tactics": 4, "level": 5, "Infantry Attack": 22.5, "power": 31500}
            ],
            "Level 5": [
                {"Reprisal Tactics": 5, "level": 1, "Infantry Attack": 4.75, "power": 6650},
                {"Reprisal Tactics": 5, "level": 2, "Infantry Attack": 9.5, "power": 13300},
                {"Reprisal Tactics": 5, "level": 3, "Infantry Attack": 14.25, "power": 19950},
                {"Reprisal Tactics": 5, "level": 4, "Infantry Attack": 19, "power": 26600},
                {"Reprisal Tactics": 5, "level": 5, "Infantry Attack": 23.75, "power": 33250},
                {"Reprisal Tactics": 5, "level": 6, "Infantry Attack": 31.75, "power": 44450}
            ],
            "Level 6": [
                {"Reprisal Tactics": 6, "level": 1, "Infantry Attack": 5.5, "power": 7700},
                {"Reprisal Tactics": 6, "level": 2, "Infantry Attack": 11, "power": 15400},
                {"Reprisal Tactics": 6, "level": 3, "Infantry Attack": 16.5, "power": 23100},
                {"Reprisal Tactics": 6, "level": 4, "Infantry Attack": 22, "power": 30800},
                {"Reprisal Tactics": 6, "level": 5, "Infantry Attack": 27.5, "power": 38500},
                {"Reprisal Tactics": 6, "level": 6, "Infantry Attack": 36.5, "power": 51100}
            ]
        },
        "Precision Targeting": {
            "Level 1": [
                {"Precision Targeting": 1, "level": 1, "Marksman Attack": 1.25, "power": 4375},
                {"Precision Targeting": 1, "level": 2, "Marksman Attack": 2.5, "power": 8750},
                {"Precision Targeting": 1, "level": 3, "Marksman Attack": 4, "power": 14000}
            ],
            "Level 2": [
                {"Precision Targeting": 2, "level": 1, "Marksman Attack": 1.75, "power": 6300},
                {"Precision Targeting": 2, "level": 2, "Marksman Attack": 3.5, "power": 12250},
                {"Precision Targeting": 2, "level": 3, "Marksman Attack": 5.5, "power": 19250}
            ],
            "Level 3": [
                {"Precision Targeting": 3, "level": 1, "Marksman Attack": 2.5, "power": 8750},
                {"Precision Targeting": 3, "level": 2, "Marksman Attack": 5, "power": 17500},
                {"Precision Targeting": 3, "level": 3, "Marksman Attack": 7.5, "power": 26250},
                {"Precision Targeting": 3, "level": 4, "Marksman Attack": 11.5, "power": 40250}
            ],
            "Level 4": [
                {"Precision Targeting": 4, "level": 1, "Marksman Attack": 4, "power": 14000},
                {"Precision Targeting": 4, "level": 2, "Marksman Attack": 8, "power": 28000},
                {"Precision Targeting": 4, "level": 3, "Marksman Attack": 12, "power": 42000},
                {"Precision Targeting": 4, "level": 4, "Marksman Attack": 16, "power": 56000},
                {"Precision Targeting": 4, "level": 5, "Marksman Attack": 22.5, "power": 78750}
            ],
            "Level 5": [
                {"Precision Targeting": 5, "level": 1, "Marksman Attack": 4.75, "power": 16625},
                {"Precision Targeting": 5, "level": 2, "Marksman Attack": 9.5, "power": 33250},
                {"Precision Targeting": 5, "level": 3, "Marksman Attack": 14.25, "power": 49875},
                {"Precision Targeting": 5, "level": 4, "Marksman Attack": 19, "power": 66500},
                {"Precision Targeting": 5, "level": 5, "Marksman Attack": 23.75, "power": 83125},
                {"Precision Targeting": 5, "level": 6, "Marksman Attack": 31.75, "power": 111125}
            ],
            "Level 6": [
                {"Precision Targeting": 6, "level": 1, "Marksman Attack": 5.5, "power": 19250},
                {"Precision Targeting": 6, "level": 2, "Marksman Attack": 11, "power": 38500},
                {"Precision Targeting": 6, "level": 3, "Marksman Attack": 16.5, "power": 57750},
                {"Precision Targeting": 6, "level": 4, "Marksman Attack": 22, "power": 77000},
                {"Precision Targeting": 6, "level": 5, "Marksman Attack": 27.5, "power": 96250},
                {"Precision Targeting": 6, "level": 6, "Marksman Attack": 36.5, "power": 127750}
            ]
        },
        "Skirmishing": {
            "Level 1": [
                {"Skirmishing": 1, "level": 1, "Lancer Attack": 1.25, "power": 4375},
                {"Skirmishing": 1, "level": 2, "Lancer Attack": 2.5, "power": 8750},
                {"Skirmishing": 1, "level": 3, "Lancer Attack": 4, "power": 14000}
            ],
            "Level 2": [
                {"Skirmishing": 2, "level": 1, "Lancer Attack": 1.75, "power": 6125},
                {"Skirmishing": 2, "level": 2, "Lancer Attack": 3.5, "power": 12250},
                {"Skirmishing": 2, "level": 3, "Lancer Attack": 5.5, "power": 19250}
            ],
            "Level 3": [
                {"Skirmishing": 3, "level": 1, "Lancer Attack": 2.5, "power": 8750},
                {"Skirmishing": 3, "level": 2, "Lancer Attack": 5, "power": 17500},
                {"Skirmishing": 3, "level": 3, "Lancer Attack": 7.5, "power": 26250},
                {"Skirmishing": 3, "level": 4, "Lancer Attack": 11.5, "power": 40250}
            ],
            "Level 4": [
                {"Skirmishing": 4, "level": 1, "Lancer Attack": 4, "power": 14000},
                {"Skirmishing": 4, "level": 2, "Lancer Attack": 8, "power": 28000},
                {"Skirmishing": 4, "level": 3, "Lancer Attack": 12, "power": 42000},
                {"Skirmishing": 4, "level": 4, "Lancer Attack": 16, "power": 56000},
                {"Skirmishing": 4, "level": 5, "Lancer Attack": 22.5, "power": 78750}
            ],
            "Level 5": [
                {"Skirmishing": 5, "level": 1, "Lancer Attack": 4.75, "power": 16625},
                {"Skirmishing": 5, "level": 2, "Lancer Attack": 9.5, "power": 33250},
                {"Skirmishing": 5, "level": 3, "Lancer Attack": 14.25, "power": 49875},
                {"Skirmishing": 5, "level": 4, "Lancer Attack": 19, "power": 66500},
                {"Skirmishing": 5, "level": 5, "Lancer Attack": 23.75, "power": 83125},
                {"Skirmishing": 5, "level": 6, "Lancer Attack": 31.75, "power": 111125}
            ],
            "Level 6": [
                {"Skirmishing": 6, "level": 1, "Lancer Attack": 5.5, "power": 19250},
                {"Skirmishing": 6, "level": 2, "Lancer Attack": 11, "power": 38500},
                {"Skirmishing": 6, "level": 3, "Lancer Attack": 16.5, "power": 57750},
                {"Skirmishing": 6, "level": 4, "Lancer Attack": 22, "power": 77000},
                {"Skirmishing": 6, "level": 5, "Lancer Attack": 27.5, "power": 96250},
                {"Skirmishing": 6, "level": 6, "Lancer Attack": 36.5, "power": 127750}
            ]
        },
        "Defensive Formations": {
            "Level 1": [
                {"Defensive Formations": 1, "level": 1, "Infantry Defense": 1.25, "power": 5625},
                {"Defensive Formations": 1, "level": 2, "Infantry Defense": 2.5, "power": 11250},
                {"Defensive Formations": 1, "level": 3, "Infantry Defense": 4, "power": 18000}
            ],
            "Level 2": [
                {"Defensive Formations": 2, "level": 1, "Infantry Defense": 1.75, "power": 7875},
                {"Defensive Formations": 2, "level": 2, "Infantry Defense": 3.5, "power": 15750},
                {"Defensive Formations": 2, "level": 3, "Infantry Defense": 5.5, "power": 24750}
            ],
            "Level 3": [
                {"Defensive Formations": 3, "level": 1, "Infantry Defense": 2.5, "power": 11250},
                {"Defensive Formations": 3, "level": 2, "Infantry Defense": 5, "power": 22500},
                {"Defensive Formations": 3, "level": 3, "Infantry Defense": 7.5, "power": 33750},
                {"Defensive Formations": 3, "level": 4, "Infantry Defense": 11.5, "power": 51750}
            ],
            "Level 4": [
                {"Defensive Formations": 4, "level": 1, "Infantry Defense": 4, "power": 18000},
                {"Defensive Formations": 4, "level": 2, "Infantry Defense": 8, "power": 36000},
                {"Defensive Formations": 4, "level": 3, "Infantry Defense": 12, "power": 54000},
                {"Defensive Formations": 4, "level": 4, "Infantry Defense": 16, "power": 72000},
                {"Defensive Formations": 4, "level": 5, "Infantry Defense": 22.5, "power": 101250}
            ],
            "Level 5": [
                {"Defensive Formations": 5, "level": 1, "Infantry Defense": 4.75, "power": 21375},
                {"Defensive Formations": 5, "level": 2, "Infantry Defense": 9.5, "power": 42750},
                {"Defensive Formations": 5, "level": 3, "Infantry Defense": 14.25, "power": 64125},
                {"Defensive Formations": 5, "level": 4, "Infantry Defense": 19, "power": 85500},
                {"Defensive Formations": 5, "level": 5, "Infantry Defense": 23.75, "power": 106875},
                {"Defensive Formations": 5, "level": 6, "Infantry Defense": 31.75, "power": 142875}
            ],
            "Level 6": [
                {"Defensive Formations": 6, "level": 1, "Infantry Defense": 5.5, "power": 24750},
                {"Defensive Formations": 6, "level": 2, "Infantry Defense": 11, "power": 49500},
                {"Defensive Formations": 6, "level": 3, "Infantry Defense": 16.5, "power": 74250},
                {"Defensive Formations": 6, "level": 4, "Infantry Defense": 22, "power": 99000},
                {"Defensive Formations": 6, "level": 5, "Infantry Defense": 27.5, "power": 123750},
                {"Defensive Formations": 6, "level": 6, "Infantry Defense": 36.5, "power": 164250}
            ]
        },
        "Picket Lines": {
            "Level 1": [
                {"Picket Lines": 1, "level": 1, "Marksman Defense": 1.25, "power": 3000},
                {"Picket Lines": 1, "level": 2, "Marksman Defense": 2.5, "power": 6000},
                {"Picket Lines": 1, "level": 3, "Marksman Defense": 4, "power": 9600}
            ],
            "Level 2": [
                {"Picket Lines": 2, "level": 1, "Marksman Defense": 1.75, "power": 4200},
                {"Picket Lines": 2, "level": 2, "Marksman Defense": 3.5, "power": 8400},
                {"Picket Lines": 2, "level": 3, "Marksman Defense": 5.5, "power": 13200}
            ],
            "Level 3": [
                {"Picket Lines": 3, "level": 1, "Marksman Defense": 2.5, "power": 6000},
                {"Picket Lines": 3, "level": 2, "Marksman Defense": 5, "power": 12000},
                {"Picket Lines": 3, "level": 3, "Marksman Defense": 7.5, "power": 18000},
                {"Picket Lines": 3, "level": 4, "Marksman Defense": 11.5, "power": 27600}
            ],
            "Level 4": [
                {"Picket Lines": 4, "level": 1, "Marksman Defense": 4, "power": 9600},
                {"Picket Lines": 4, "level": 2, "Marksman Defense": 8, "power": 19200},
                {"Picket Lines": 4, "level": 3, "Marksman Defense": 12, "power": 28800},
                {"Picket Lines": 4, "level": 4, "Marksman Defense": 16, "power": 38400},
                {"Picket Lines": 4, "level": 5, "Marksman Defense": 22.5, "power": 54000}
            ],
            "Level 5": [
                {"Picket Lines": 5, "level": 1, "Marksman Defense": 4.75, "power": 11400},
                {"Picket Lines": 5, "level": 2, "Marksman Defense": 9.5, "power": 22800},
                {"Picket Lines": 5, "level": 3, "Marksman Defense": 14.25, "power": 34200},
                {"Picket Lines": 5, "level": 4, "Marksman Defense": 19, "power": 45600},
                {"Picket Lines": 5, "level": 5, "Marksman Defense": 23.75, "power": 57000},
                {"Picket Lines": 5, "level": 6, "Marksman Defense": 31.75, "power": 76200}
            ],
            "Level 6": [
                {"Picket Lines": 6, "level": 1, "Marksman Defense": 5.5, "power": 13200},
                {"Picket Lines": 6, "level": 2, "Marksman Defense": 11, "power": 26400},
                {"Picket Lines": 6, "level": 3, "Marksman Defense": 16.5, "power": 39600},
                {"Picket Lines": 6, "level": 4, "Marksman Defense": 22, "power": 52800},
                {"Picket Lines": 6, "level": 5, "Marksman Defense": 27.5, "power": 66000},
                {"Picket Lines": 6, "level": 6, "Marksman Defense": 36.5, "power": 87600}
            ]
        },
        "Bulwark Formations": {
            "Level 1": [
                {"Bulwark Formations": 1, "level": 1, "Lancer Defense": 1.25, "power": 3000},
                {"Bulwark Formations": 1, "level": 2, "Lancer Defense": 2.5, "power": 6000},
                {"Bulwark Formations": 1, "level": 3, "Lancer Defense": 4, "power": 9600}
            ],
            "Level 2": [
                {"Bulwark Formations": 2, "level": 1, "Lancer Defense": 1.75, "power": 4200},
                {"Bulwark Formations": 2, "level": 2, "Lancer Defense": 3.5, "power": 8400},
                {"Bulwark Formations": 2, "level": 3, "Lancer Defense": 5.5, "power": 13200}
            ],
            "Level 3": [
                {"Bulwark Formations": 3, "level": 1, "Lancer Defense": 2.5, "power": 6000},
                {"Bulwark Formations": 3, "level": 2, "Lancer Defense": 5, "power": 12000},
                {"Bulwark Formations": 3, "level": 3, "Lancer Defense": 7.5, "power": 18000},
                {"Bulwark Formations": 3, "level": 4, "Lancer Defense": 11.5, "power": 27600}
            ],
            "Level 4": [
                {"Bulwark Formations": 4, "level": 1, "Lancer Defense": 4, "power": 9600},
                {"Bulwark Formations": 4, "level": 2, "Lancer Defense": 8, "power": 19200},
                {"Bulwark Formations": 4, "level": 3, "Lancer Defense": 12, "power": 28800},
                {"Bulwark Formations": 4, "level": 4, "Lancer Defense": 16, "power": 38400},
                {"Bulwark Formations": 4, "level": 5, "Lancer Defense": 22.5, "power": 54000}
            ],
            "Level 5": [
                {"Bulwark Formations": 5, "level": 1, "Lancer Defense": 4.75, "power": 11400},
                {"Bulwark Formations": 5, "level": 2, "Lancer Defense": 9.5, "power": 22800},
                {"Bulwark Formations": 5, "level": 3, "Lancer Defense": 14.25, "power": 34200},
                {"Bulwark Formations": 5, "level": 4, "Lancer Defense": 19, "power": 45600},
                {"Bulwark Formations": 5, "level": 5, "Lancer Defense": 23.75, "power": 57000},
                {"Bulwark Formations": 5, "level": 6, "Lancer Defense": 31.75, "power": 76200}
            ],
            "Level 6": [
                {"Bulwark Formations": 6, "level": 1, "Lancer Defense": 5.5, "power": 13200},
                {"Bulwark Formations": 6, "level": 2, "Lancer Defense": 11, "power": 26400},
                {"Bulwark Formations": 6, "level": 3, "Lancer Defense": 16.5, "power": 39600},
                {"Bulwark Formations": 6, "level": 4, "Lancer Defense": 22, "power": 52800},
                {"Bulwark Formations": 6, "level": 5, "Lancer Defense": 27.5, "power": 66000},
                {"Bulwark Formations": 6, "level": 6, "Lancer Defense": 36.5, "power": 87600}
            ]
        },
        "Special Defensive Training": {
            "Level 1": [
                {"Special Defensive Training": 1, "level": 1, "Troops Defense": 0.5, "power": 4200},
                {"Special Defensive Training": 1, "level": 2, "Troops Defense": 1.00, "power": 8400},
                {"Special Defensive Training": 1, "level": 3, "Troops Defense": 1.5, "power": 12600}
            ],
            "Level 2": [
                {"Special Defensive Training": 2, "level": 1, "Troops Defense": 0.75, "power": 6300},
                {"Special Defensive Training": 2, "level": 2, "Troops Defense": 1.50, "power": 12600},
                {"Special Defensive Training": 2, "level": 3, "Troops Defense": 2.50, "power": 21000}
            ],
            "Level 3": [
                {"Special Defensive Training": 3, "level": 1, "Troops Defense": 1, "power": 8400},
                {"Special Defensive Training": 3, "level": 2, "Troops Defense": 2, "power": 16800},
                {"Special Defensive Training": 3, "level": 3, "Troops Defense": 3, "power": 25200},
                {"Special Defensive Training": 3, "level": 4, "Troops Defense": 4.5, "power": 37800}
            ],
            "Level 4": [
                {"Special Defensive Training": 4, "level": 1, "Troops Defense": 1.75, "power": 14700},
                {"Special Defensive Training": 4, "level": 2, "Troops Defense": 3.5, "power": 29400},
                {"Special Defensive Training": 4, "level": 3, "Troops Defense": 5.25, "power": 44100},
                {"Special Defensive Training": 4, "level": 4, "Troops Defense": 7, "power": 56000},
                {"Special Defensive Training": 4, "level": 5, "Troops Defense": 10, "power": 84000}
            ],
            "Level 5": [
                {"Special Defensive Training": 5, "level": 1, "Troops Defense": 2, "power": 16800},
                {"Special Defensive Training": 5, "level": 2, "Troops Defense": 4, "power": 33600},
                {"Special Defensive Training": 5, "level": 3, "Troops Defense": 6, "power": 50400},
                {"Special Defensive Training": 5, "level": 4, "Troops Defense": 8, "power": 67200},
                {"Special Defensive Training": 5, "level": 5, "Troops Defense": 10, "power": 84000},
                {"Special Defensive Training": 5, "level": 6, "Troops Defense": 13.5, "power": 113400}
            ],
            "Level 6": [
                {"Special Defensive Training": 6, "level": 1, "Troops Defense": 2.25, "power": 18900},
                {"Special Defensive Training": 6, "level": 2, "Troops Defense": 4.5, "power": 37800},
                {"Special Defensive Training": 6, "level": 3, "Troops Defense": 6.75, "power": 56700},
                {"Special Defensive Training": 6, "level": 4, "Troops Defense": 9, "power": 75600},
                {"Special Defensive Training": 6, "level": 5, "Troops Defense": 11.25, "power": 94500},
                {"Special Defensive Training": 6, "level": 6, "Troops Defense": 15.25, "power": 128100}
            ]
        },
        "Survival Techniques": {
            "Level 1": [
                {"Survival Techniques": 1, "level": 1, "Troops Health": 0.5, "power": 4200},
                {"Survival Techniques": 1, "level": 2, "Troops Health": 1.0, "power": 8400},
                {"Survival Techniques": 1, "level": 3, "Troops Health": 1.5, "power": 12600}
            ],
            "Level 2": [
                {"Survival Techniques": 2, "level": 1, "Troops Health": 0.75, "power": 6300},
                {"Survival Techniques": 2, "level": 2, "Troops Health": 1.5, "power": 12600},
                {"Survival Techniques": 2, "level": 3, "Troops Health": 2.5, "power": 21000}
            ],
            "Level 3": [
                {"Survival Techniques": 3, "level": 1, "Troops Health": 1, "power": 8400},
                {"Survival Techniques": 3, "level": 2, "Troops Health": 2, "power": 16800},
                {"Survival Techniques": 3, "level": 3, "Troops Health": 3, "power": 25200},
                {"Survival Techniques": 3, "level": 4, "Troops Health": 4.5, "power": 37800}
            ],
            "Level 4": [
                {"Survival Techniques": 4, "level": 1, "Troops Health": 1.75, "power": 14700},
                {"Survival Techniques": 4, "level": 2, "Troops Health": 3.5, "power": 29400},
                {"Survival Techniques": 4, "level": 3, "Troops Health": 5.25, "power": 44100},
                {"Survival Techniques": 4, "level": 4, "Troops Health": 7, "power": 58800},
                {"Survival Techniques": 4, "level": 5, "Troops Health": 10, "power": 84000}
            ],
            "Level 5": [
                {"Survival Techniques": 5, "level": 1, "Troops Health": 2, "power": 16800},
                {"Survival Techniques": 5, "level": 2, "Troops Health": 4, "power": 33600},
                {"Survival Techniques": 5, "level": 3, "Troops Health": 6, "power": 50400},
                {"Survival Techniques": 5, "level": 4, "Troops Health": 8, "power": 67200},
                {"Survival Techniques": 5, "level": 5, "Troops Health": 10, "power": 84000},
                {"Survival Techniques": 5, "level": 6, "Troops Health": 13.5, "power": 113400}
            ],
            "Level 6": [
                {"Survival Techniques": 6, "level": 1, "Troops Health": 2.25, "power": 18900},
                {"Survival Techniques": 6, "level": 2, "Troops Health": 4.5, "power": 37800},
                {"Survival Techniques": 6, "level": 3, "Troops Health": 6.75, "power": 56700},
                {"Survival Techniques": 6, "level": 4, "Troops Health": 9, "power": 75600},
                {"Survival Techniques": 6, "level": 5, "Troops Health": 11.25, "power": 94500},
                {"Survival Techniques": 6, "level": 6, "Troops Health": 15.25, "power": 128100}
            ]
        },
        "Assault Techniques": {
            "Level 1": [
                {"Assault Techniques": 1, "level": 1, "Troops Lethality": 0.5, "power": 4200},
                {"Assault Techniques": 1, "level": 2, "Troops Lethality": 1.0, "power": 8400},
                {"Assault Techniques": 1, "level": 3, "Troops Lethality": 1.5, "power": 12600}
            ],
            "Level 2": [
                {"Assault Techniques": 2, "level": 1, "Troops Lethality": 0.75, "power": 6300},
                {"Assault Techniques": 2, "level": 2, "Troops Lethality": 1.5, "power": 12600},
                {"Assault Techniques": 2, "level": 3, "Troops Lethality": 2.5, "power": 21000}
            ],
            "Level 3": [
                {"Assault Techniques": 3, "level": 1, "Troops Lethality": 1, "power": 8400},
                {"Assault Techniques": 3, "level": 2, "Troops Lethality": 2, "power": 16800},
                {"Assault Techniques": 3, "level": 3, "Troops Lethality": 3, "power": 25200},
                {"Assault Techniques": 3, "level": 4, "Troops Lethality": 4.5, "power": 37800}
            ],
            "Level 4": [
                {"Assault Techniques": 4, "level": 1, "Troops Lethality": 1.75, "power": 14700},
                {"Assault Techniques": 4, "level": 2, "Troops Lethality": 3.5, "power": 29400},
                {"Assault Techniques": 4, "level": 3, "Troops Lethality": 5.25, "power": 44100},
                {"Assault Techniques": 4, "level": 4, "Troops Lethality": 7, "power": 58800},
                {"Assault Techniques": 4, "level": 5, "Troops Lethality": 10, "power": 84000}
            ],
            "Level 5": [
                {"Assault Techniques": 5, "level": 1, "Troops Lethality": 2, "power": 16800},
                {"Assault Techniques": 5, "level": 2, "Troops Lethality": 4, "power": 33600},
                {"Assault Techniques": 5, "level": 3, "Troops Lethality": 6, "power": 50400},
                {"Assault Techniques": 5, "level": 4, "Troops Lethality": 8, "power": 67200},
                {"Assault Techniques": 5, "level": 5, "Troops Lethality": 10, "power": 84000},
                {"Assault Techniques": 5, "level": 6, "Troops Lethality": 13.5, "power": 113400}
            ],
            "Level 6": [
                {"Assault Techniques": 6, "level": 1, "Troops Lethality": 2.25, "power": 18900},
                {"Assault Techniques": 6, "level": 2, "Troops Lethality": 4.5, "power": 37800},
                {"Assault Techniques": 6, "level": 3, "Troops Lethality": 6.75, "power": 56700},
                {"Assault Techniques": 6, "level": 4, "Troops Lethality": 9, "power": 75600},
                {"Assault Techniques": 6, "level": 5, "Troops Lethality": 11.25, "power": 94500},
                {"Assault Techniques": 6, "level": 6, "Troops Lethality": 15.25, "power": 128100}
            ]
        },
        "Close Combat": {
            "Level 1": [
                {"Close Combat": 1, "level": 1, "Infantry Lethality": 1.25, "power": 1750},
                {"Close Combat": 1, "level": 2, "Infantry Lethality": 2.5, "power": 3500},
                {"Close Combat": 1, "level": 3, "Infantry Lethality": 4, "power": 5600}
            ],
            "Level 2": [
                {"Close Combat": 2, "level": 1, "Infantry Lethality": 1.75, "power": 2450},
                {"Close Combat": 2, "level": 2, "Infantry Lethality": 3.5, "power": 4900},
                {"Close Combat": 2, "level": 3, "Infantry Lethality": 5.5, "power": 7700}
            ],
            "Level 3": [
                {"Close Combat": 3, "level": 1, "Infantry Lethality": 2.5, "power": 3500},
                {"Close Combat": 3, "level": 2, "Infantry Lethality": 5, "power": 7000},
                {"Close Combat": 3, "level": 3, "Infantry Lethality": 7.5, "power": 10500},
                {"Close Combat": 3, "level": 4, "Infantry Lethality": 11.5, "power": 16100}
            ],
            "Level 4": [
                {"Close Combat": 4, "level": 1, "Infantry Lethality": 4, "power": 5600},
                {"Close Combat": 4, "level": 2, "Infantry Lethality": 8, "power": 11200},
                {"Close Combat": 4, "level": 3, "Infantry Lethality": 12, "power": 16800},
                {"Close Combat": 4, "level": 4, "Infantry Lethality": 16, "power": 22400},
                {"Close Combat": 4, "level": 5, "Infantry Lethality": 22.5, "power": 31500}
            ],
            "Level 5": [
                {"Close Combat": 5, "level": 1, "Infantry Lethality": 4.75, "power": 6650},
                {"Close Combat": 5, "level": 2, "Infantry Lethality": 9.5, "power": 13300},
                {"Close Combat": 5, "level": 3, "Infantry Lethality": 14.25, "power": 19950},
                {"Close Combat": 5, "level": 4, "Infantry Lethality": 19, "power": 26600},
                {"Close Combat": 5, "level": 5, "Infantry Lethality": 23.75, "power": 33250},
                {"Close Combat": 5, "level": 6, "Infantry Lethality": 31.75, "power": 44450}
            ],
            "Level 6": [
                {"Close Combat": 6, "level": 1, "Infantry Lethality": 5.5, "power": 7700},
                {"Close Combat": 6, "level": 2, "Infantry Lethality": 11, "power": 15400},
                {"Close Combat": 6, "level": 3, "Infantry Lethality": 16.5, "power": 23100},
                {"Close Combat": 6, "level": 4, "Infantry Lethality": 22, "power": 30800},
                {"Close Combat": 6, "level": 5, "Infantry Lethality": 27.5, "power": 38500},
                {"Close Combat": 6, "level": 6, "Infantry Lethality": 36.5, "power": 51100}
            ]
        },
        "Targeted Sniping": {
            "Level 1": [
                {"Targeted Sniping": 1, "level": 1, "Marksman Lethality": 1.25, "power": 4375},
                {"Targeted Sniping": 1, "level": 2, "Marksman Lethality": 2.5, "power": 8750},
                {"Targeted Sniping": 1, "level": 3, "Marksman Lethality": 4, "power": 14000}
            ],
            "Level 2": [
                {"Targeted Sniping": 2, "level": 1, "Marksman Lethality": 1.75, "power": 6125},
                {"Targeted Sniping": 2, "level": 2, "Marksman Lethality": 3.5, "power": 12250},
                {"Targeted Sniping": 2, "level": 3, "Marksman Lethality": 5.5, "power": 19250}
            ],
            "Level 3": [
                {"Targeted Sniping": 3, "level": 1, "Marksman Lethality": 2.5, "power": 8750},
                {"Targeted Sniping": 3, "level": 2, "Marksman Lethality": 5, "power": 17500},
                {"Targeted Sniping": 3, "level": 3, "Marksman Lethality": 7.5, "power": 26250},
                {"Targeted Sniping": 3, "level": 4, "Marksman Lethality": 11.5, "power": 40250}
            ],
            "Level 4": [
                {"Targeted Sniping": 4, "level": 1, "Marksman Lethality": 4, "power": 14000},
                {"Targeted Sniping": 4, "level": 2, "Marksman Lethality": 8, "power": 28000},
                {"Targeted Sniping": 4, "level": 3, "Marksman Lethality": 12, "power": 42000},
                {"Targeted Sniping": 4, "level": 4, "Marksman Lethality": 16, "power": 56000},
                {"Targeted Sniping": 4, "level": 5, "Marksman Lethality": 22.5, "power": 78750}
            ],
            "Level 5": [
                {"Targeted Sniping": 5, "level": 1, "Marksman Lethality": 4.75, "power": 16625},
                {"Targeted Sniping": 5, "level": 2, "Marksman Lethality": 9.5, "power": 33250},
                {"Targeted Sniping": 5, "level": 3, "Marksman Lethality": 14.25, "power": 49875},
                {"Targeted Sniping": 5, "level": 4, "Marksman Lethality": 19, "power": 66500},
                {"Targeted Sniping": 5, "level": 5, "Marksman Lethality": 23.75, "power": 83125},
                {"Targeted Sniping": 5, "level": 6, "Marksman Lethality": 31.75, "power": 111125}
            ],
            "Level 6": [
                {"Targeted Sniping": 6, "level": 1, "Marksman Lethality": 5.5, "power": 19250},
                {"Targeted Sniping": 6, "level": 2, "Marksman Lethality": 11, "power": 38500},
                {"Targeted Sniping": 6, "level": 3, "Marksman Lethality": 16.5, "power": 57750},
                {"Targeted Sniping": 6, "level": 4, "Marksman Lethality": 22, "power": 77000},
                {"Targeted Sniping": 6, "level": 5, "Marksman Lethality": 27.5, "power": 96250},
                {"Targeted Sniping": 6, "level": 6, "Marksman Lethality": 36.5, "power": 127750}
            ]
        },
        "Lance Upgrade": {
            "Level 1": [
                {"Lance Upgrade": 1, "level": 1, "Lancer Lethality": 1.25, "power": 4375},
                {"Lance Upgrade": 1, "level": 2, "Lancer Lethality": 2.5, "power": 8750},
                {"Lance Upgrade": 1, "level": 3, "Lancer Lethality": 4, "power": 14000}
            ],
            "Level 2": [
                {"Lance Upgrade": 2, "level": 1, "Lancer Lethality": 1.75, "power": 6125},
                {"Lance Upgrade": 2, "level": 2, "Lancer Lethality": 3.5, "power": 12250},
                {"Lance Upgrade": 2, "level": 3, "Lancer Lethality": 5.5, "power": 19250}
            ],
            "Level 3": [
                {"Lance Upgrade": 3, "level": 1, "Lancer Lethality": 2.5, "power": 8750},
                {"Lance Upgrade": 3, "level": 2, "Lancer Lethality": 5, "power": 17500},
                {"Lance Upgrade": 3, "level": 3, "Lancer Lethality": 7.5, "power": 26250},
                {"Lance Upgrade": 3, "level": 4, "Lancer Lethality": 11.5, "power": 40250}
            ],
            "Level 4": [
                {"Lance Upgrade": 4, "level": 1, "Lancer Lethality": 4, "power": 14000},
                {"Lance Upgrade": 4, "level": 2, "Lancer Lethality": 8, "power": 28000},
                {"Lance Upgrade": 4, "level": 3, "Lancer Lethality": 12, "power": 42000},
                {"Lance Upgrade": 4, "level": 4, "Lancer Lethality": 16, "power": 56000},
                {"Lance Upgrade": 4, "level": 5, "Lancer Lethality": 22.5, "power": 78750}
            ],
            "Level 5": [
                {"Lance Upgrade": 5, "level": 1, "Lancer Lethality": 4.75, "power": 16625},
                {"Lance Upgrade": 5, "level": 2, "Lancer Lethality": 9.5, "power": 33250},
                {"Lance Upgrade": 5, "level": 3, "Lancer Lethality": 14.25, "power": 49875},
                {"Lance Upgrade": 5, "level": 4, "Lancer Lethality": 19, "power": 66500},
                {"Lance Upgrade": 5, "level": 5, "Lancer Lethality": 23.75, "power": 83125},
                {"Lance Upgrade": 5, "level": 6, "Lancer Lethality": 31.75, "power": 111125}
            ],
            "Level 6": [
                {"Lance Upgrade": 6, "level": 1, "Lancer Lethality": 5.5, "power": 19250},
                {"Lance Upgrade": 6, "level": 2, "Lancer Lethality": 11, "power": 38500},
                {"Lance Upgrade": 6, "level": 3, "Lancer Lethality": 16.5, "power": 57750},
                {"Lance Upgrade": 6, "level": 4, "Lancer Lethality": 22, "power": 77000},
                {"Lance Upgrade": 6, "level": 5, "Lancer Lethality": 27.5, "power": 96250},
                {"Lance Upgrade": 6, "level": 6, "Lancer Lethality": 36.5, "power": 127750}
            ]
        },
        "Shield Upgrade": {
            "Level 1": [
                {"Shield Upgrade": 1, "level": 1, "Infantry Health": 1.25, "power": 5625},
                {"Shield Upgrade": 1, "level": 2, "Infantry Health": 2.5, "power": 11250},
                {"Shield Upgrade": 1, "level": 3, "Infantry Health": 4, "power": 18000}
            ],
            "Level 2": [
                {"Shield Upgrade": 2, "level": 1, "Infantry Health": 1.75, "power": 7875},
                {"Shield Upgrade": 2, "level": 2, "Infantry Health": 3.5, "power": 15750},
                {"Shield Upgrade": 2, "level": 3, "Infantry Health": 5.5, "power": 24750}
            ],
            "Level 3": [
                {"Shield Upgrade": 3, "level": 1, "Infantry Health": 2.5, "power": 11250},
                {"Shield Upgrade": 3, "level": 2, "Infantry Health": 5, "power": 22500},
                {"Shield Upgrade": 3, "level": 3, "Infantry Health": 7.5, "power": 33750},
                {"Shield Upgrade": 3, "level": 4, "Infantry Health": 11.5, "power": 51750}
            ],
            "Level 4": [
                {"Shield Upgrade": 4, "level": 1, "Infantry Health": 4, "power": 18000},
                {"Shield Upgrade": 4, "level": 2, "Infantry Health": 8, "power": 36000},
                {"Shield Upgrade": 4, "level": 3, "Infantry Health": 12, "power": 54000},
                {"Shield Upgrade": 4, "level": 4, "Infantry Health": 16, "power": 72000},
                {"Shield Upgrade": 4, "level": 5, "Infantry Health": 22.5, "power": 101250}
            ],
            "Level 5": [
                {"Shield Upgrade": 5, "level": 1, "Infantry Health": 4.75, "power": 16625},
                {"Shield Upgrade": 5, "level": 2, "Infantry Health": 9.5, "power": 33250},
                {"Shield Upgrade": 5, "level": 3, "Infantry Health": 14.25, "power": 49875},
                {"Shield Upgrade": 5, "level": 4, "Infantry Health": 19, "power": 66500},
                {"Shield Upgrade": 5, "level": 5, "Infantry Health": 23.75, "power": 83125},
                {"Shield Upgrade": 5, "level": 6, "Infantry Health": 31.75, "power": 111125}
            ],
            "Level 6": [
                {"Shield Upgrade": 6, "level": 1, "Infantry Health": 5.5, "power": 24750},
                {"Shield Upgrade": 6, "level": 2, "Infantry Health": 11, "power": 49500},
                {"Shield Upgrade": 6, "level": 3, "Infantry Health": 16.5, "power": 74250},
                {"Shield Upgrade": 6, "level": 4, "Infantry Health": 22, "power": 99000},
                {"Shield Upgrade": 6, "level": 5, "Infantry Health": 27.5, "power": 123750},
                {"Shield Upgrade": 6, "level": 6, "Infantry Health": 36.5, "power": 164250}
            ]
        },
        "Marksman Armor": {
            "Level 1": [
                {"Marksman Armor": 1, "level": 1, "Marksman Health": 1.25, "power": 3000},
                {"Marksman Armor": 1, "level": 2, "Marksman Health": 2.5, "power": 6000},
                {"Marksman Armor": 1, "level": 3, "Marksman Health": 4, "power": 9600}
            ],
            "Level 2": [
                {"Marksman Armor": 2, "level": 1, "Marksman Health": 1.75, "power": 4200},
                {"Marksman Armor": 2, "level": 2, "Marksman Health": 3.5, "power": 8400},
                {"Marksman Armor": 2, "level": 3, "Marksman Health": 5.5, "power": 13200}
            ],
            "Level 3": [
                {"Marksman Armor": 3, "level": 1, "Marksman Health": 2.5, "power": 6000},
                {"Marksman Armor": 3, "level": 2, "Marksman Health": 5, "power": 12000},
                {"Marksman Armor": 3, "level": 3, "Marksman Health": 7.5, "power": 18000},
                {"Marksman Armor": 3, "level": 4, "Marksman Health": 11.5, "power": 27600}
            ],
            "Level 4": [
                {"Marksman Armor": 4, "level": 1, "Marksman Health": 4, "power": 9600},
                {"Marksman Armor": 4, "level": 2, "Marksman Health": 8, "power": 19200},
                {"Marksman Armor": 4, "level": 3, "Marksman Health": 12, "power": 28800},
                {"Marksman Armor": 4, "level": 4, "Marksman Health": 16, "power": 38400},
                {"Marksman Armor": 4, "level": 5, "Marksman Health": 22.5, "power": 54000}
            ],
            "Level 5": [
                {"Marksman Armor": 5, "level": 1, "Marksman Health": 4.75, "power": 11400},
                {"Marksman Armor": 5, "level": 2, "Marksman Health": 9.5, "power": 22800},
                {"Marksman Armor": 5, "level": 3, "Marksman Health": 14.25, "power": 34200},
                {"Marksman Armor": 5, "level": 4, "Marksman Health": 19, "power": 45600},
                {"Marksman Armor": 5, "level": 5, "Marksman Health": 23.75, "power": 57000},
                {"Marksman Armor": 5, "level": 6, "Marksman Health": 31.75, "power": 76200}
            ],
            "Level 6": [
                {"Marksman Armor": 6, "level": 1, "Marksman Health": 5.5, "power": 13200},
                {"Marksman Armor": 6, "level": 2, "Marksman Health": 11, "power": 26400},
                {"Marksman Armor": 6, "level": 3, "Marksman Health": 16.5, "power": 39600},
                {"Marksman Armor": 6, "level": 4, "Marksman Health": 22, "power": 52800},
                {"Marksman Armor": 6, "level": 5, "Marksman Health": 27.5, "power": 66000},
                {"Marksman Armor": 6, "level": 6, "Marksman Health": 36.5, "power": 87600}
            ]
        },
        "Lancer Armor": {
            "Level 1": [
                {"Lancer Armor": 1, "level": 1, "Lancer Health": 1.25, "power": 3000},
                {"Lancer Armor": 1, "level": 2, "Lancer Health": 2.5, "power": 6000},
                {"Lancer Armor": 1, "level": 3, "Lancer Health": 4, "power": 9600}
            ],
            "Level 2": [
                {"Lancer Armor": 2, "level": 1, "Lancer Health": 1.75, "power": 4200},
                {"Lancer Armor": 2, "level": 2, "Lancer Health": 3.5, "power": 8400},
                {"Lancer Armor": 2, "level": 3, "Lancer Health": 5.5, "power": 13200}
            ],
            "Level 3": [
                {"Lancer Armor": 3, "level": 1, "Lancer Health": 2.5, "power": 6000},
                {"Lancer Armor": 3, "level": 2, "Lancer Health": 5, "power": 12000},
                {"Lancer Armor": 3, "level": 3, "Lancer Health": 7.5, "power": 18000},
                {"Lancer Armor": 3, "level": 4, "Lancer Health": 11.5, "power": 27600}
            ],
            "Level 4": [
                {"Lancer Armor": 4, "level": 1, "Lancer Health": 4, "power": 9600},
                {"Lancer Armor": 4, "level": 2, "Lancer Health": 8, "power": 19200},
                {"Lancer Armor": 4, "level": 3, "Lancer Health": 12, "power": 28800},
                {"Lancer Armor": 4, "level": 4, "Lancer Health": 16, "power": 38400},
                {"Lancer Armor": 4, "level": 5, "Lancer Health": 22.5, "power": 54000}
            ],
            "Level 5": [
                {"Lancer Armor": 5, "level": 1, "Lancer Health": 4.75, "power": 11400},
                {"Lancer Armor": 5, "level": 2, "Lancer Health": 9.5, "power": 22800},
                {"Lancer Armor": 5, "level": 3, "Lancer Health": 14.25, "power": 34200},
                {"Lancer Armor": 5, "level": 4, "Lancer Health": 19, "power": 45600},
                {"Lancer Armor": 5, "level": 5, "Lancer Health": 23.75, "power": 57000},
                {"Lancer Armor": 5, "level": 6, "Lancer Health": 31.75, "power": 76200}
            ],
            "Level 6": [
                {"Lancer Armor": 6, "level": 1, "Lancer Health": 5.5, "power": 13200},
                {"Lancer Armor": 6, "level": 2, "Lancer Health": 11, "power": 26400},
                {"Lancer Armor": 6, "level": 3, "Lancer Health": 16.5, "power": 39600},
                {"Lancer Armor": 6, "level": 4, "Lancer Health": 22, "power": 52800},
                {"Lancer Armor": 6, "level": 5, "Lancer Health": 27.5, "power": 66000},
                {"Lancer Armor": 6, "level": 6, "Lancer Health": 36.5, "power": 87600}
            ]
        }
    }
}


def get_category_names() -> List[str]:
    """Return available research category names."""
    return list(BATTLE_RESEARCH["Battle Research"].keys())


def get_tier_labels(category: str) -> List[str]:
    """Return available tier labels (e.g., 'Level 1', ...) for a category."""
    return list(BATTLE_RESEARCH["Battle Research"][category].keys())


def get_nodes(category: str, tier_label: str) -> List[dict]:
    """Return node dicts for a category/tier_label."""
    return list(BATTLE_RESEARCH["Battle Research"][category][tier_label])


def _stat_keys_for_node(category: str, node: dict) -> List[str]:
    """Infer which keys in a node are stat fields (exclude meta keys)."""
    meta = {"level", "power", category}
    return [k for k in node.keys() if k not in meta]


def find_stat(category: str, tier_label: str, level: int, stat_name: str) -> Optional[float]:
    """
    Get a specific stat value (percentage points) for a given category/tier/level.
    Returns None if not found.
    """
    for node in get_nodes(category, tier_label):
        if node.get("level") == level:
            # stat might be the only non-meta key
            if stat_name in node:
                return float(node[stat_name])
            # fallback: first stat-like key
            for k in _stat_keys_for_node(category, node):
                if k.lower() == stat_name.lower():
                    return float(node[k])
    return None


def flatten() -> List[dict]:
    """
    Flatten the entire tree into a list of rows:
    {category, tier_label, level, stat_name, value, power}
    """
    rows: List[dict] = []
    root = BATTLE_RESEARCH["Battle Research"]
    for category, tiers in root.items():
        for tier_label, nodes in tiers.items():
            for node in nodes:
                level = node["level"]
                power = node["power"]
                for k in _stat_keys_for_node(category, node):
                    rows.append(
                        {
                            "category": category,
                            "tier_label": tier_label,
                            "level": level,
                            "stat_name": k,
                            "value": float(node[k]),
                            "power": power,
                        }
                    )
    return rows


__all__ = [
    "BATTLE_RESEARCH",
    "get_category_names",
    "get_tier_labels",
    "get_nodes",
    "find_stat",
    "flatten",
]


if __name__ == "__main__":
    # Quick sanity checks / demo
    print("Categories:", get_category_names())
    print("Weapons Prep, Level 3, level=2, Troop Attack ->",
          find_stat("Weapons Prep", "Level 3", 2, "Troop Attack"))
    print("Flattened rows sample (first 5):")
    for row in flatten()[:5]:
        print(row)
