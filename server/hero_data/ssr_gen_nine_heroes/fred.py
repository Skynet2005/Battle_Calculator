fred_hero = [
    {
        "hero-name": "Fred",
        "hero-class": "lancer",
        "rarity": "SSR",
        "generation": 9,
        "expedition-skill-type": "combat",
        "available-from": {
            "server-day": 600,
            "source": "Lucky Wheel"
        },
        "base-stats": {
            "attack": 10300,
            "defense": 10300,
            "health": 103008,
            "lancer-attack": 9.4075,
            "lancer-defense": 9.4075
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Acid Rain",
                    "description": "Fred rains down his special acidic formulation on the target area, dealing Attack * [60% / 66% / 72% / 78% / 84%] damage every 0.5 seconds while increasing targets' damage taken by 15% for 3 seconds.",
                    "damage_percentage": {
                        "1": 0.60,
                        "2": 0.66,
                        "3": 0.72,
                        "4": 0.78,
                        "5": 0.84
                    },
                    "damage_interval_seconds": 0.5,
                    "duration_seconds": 3,
                    "damage_taken_increase": 0.15
                },
                "2": {
                    "skill-name": "Water Cannon",
                    "description": "Fred water-blasts the target, rinsing away their combat bonuses while dealing damage equal to Attack * [200% / 220% / 240% / 260% / 280%].",
                    "damage_percentage": {
                        "1": 2.00,
                        "2": 2.20,
                        "3": 2.40,
                        "4": 2.60,
                        "5": 2.80
                    },
                    "dispels_bonuses": True  # Created Logic for review: This skill removes combat bonuses from the target
                },
                "3": {
                    "skill-name": "Perfect Responder",
                    "description": "Fred performs better under extreme stress, increasing Attack by [8% / 12% / 16% / 20% / 24%] and Defense by [25% / 37.5% / 50% / 62.5% / 75%] when under 50% Health.",
                    "attack_increase_percentage": {
                        "1": 0.08,
                        "2": 0.12,
                        "3": 0.16,
                        "4": 0.20,
                        "5": 0.24
                    },
                    "defense_increase_percentage": {
                        "1": 0.25,
                        "2": 0.375,
                        "3": 0.50,
                        "4": 0.625,
                        "5": 0.75
                    },
                    "health_threshold": 0.50  # Created Logic for review: Buffs apply when health is below 50%
                }
            },
            "expedition": {
                "1": {
                    "skill-name": "Hydraulic Suppression",
                    "description": "Fred's water volleys destroy opponent momentum, reducing all enemy troops' lethality by [4% / 8% / 12% / 16% / 20%].",
                    "level_percentage": {
                        "1": 0.04,
                        "2": 0.08,
                        "3": 0.12,
                        "4": 0.16,
                        "5": 0.20
                    },
                    "lethality_reduction_percentage": {
                        "1": 0.04,
                        "2": 0.08,
                        "3": 0.12,
                        "4": 0.16,
                        "5": 0.20
                    }
                },
                "2": {
                    "skill-name": "Acidification",
                    "description": "Fred coats enemy Infantry shields with a special acidic blend, amplifying their damage taken by [4% / 8% / 12% / 16% / 20%].",
                    "level_percentage": {
                        "1": 0.04,
                        "2": 0.08,
                        "3": 0.12,
                        "4": 0.16,
                        "5": 0.20
                    },
                    "damage_taken_increase_percentage": {
                        "1": 0.04,
                        "2": 0.08,
                        "3": 0.12,
                        "4": 0.16,
                        "5": 0.20
                    },
                    "target": "enemy_infantry"
                },
                "3": {
                    "skill-name": "Floodbringer",
                    "description": "A master of pressure both hydraulic and tactical, Fred's Lancers deal [40% / 80% / 120% / 160% / 200%] additional damage every 4 strikes and reduce enemy troop damage dealt by [4% / 8% / 12% / 16% / 20%] on the next turn.",
                    "level_percentage": {
                        "1": 0.40,
                        "2": 0.80,
                        "3": 1.20,
                        "4": 1.60,
                        "5": 2.00
                    },
                    "additional_damage_percentage": {
                        "1": 0.40,
                        "2": 0.80,
                        "3": 1.20,
                        "4": 1.60,
                        "5": 2.00
                    },
                    "trigger_every_n_strikes": 4,
                    "enemy_damage_dealt_reduction_percentage": {
                        "1": 0.04,
                        "2": 0.08,
                        "3": 0.12,
                        "4": 0.16,
                        "5": 0.20
                    },
                    "reduction_duration_turns": 1
                }
            }
        },
        "exclusive-weapon": {
            "name": "Blazebearer",
            "max-stats": {
                "power": 1044000,
                "attack": 2088,
                "defense": 2088,
                "health": 20880,
                "lancer-lethality": 2.32,
                "lancer-health": 2.32
            },
            "skills": {
                "1": {
                    "skill-name": "Idealism",
                    "description": "The noble idealism of Fred's calling increases his attack by 24%, and increases his Defense by 10% for each bonus dispelled until the end of battle (max 5 stacks).",
                    "attack_increase": 0.24,
                    "defense_increase_per_dispel": 0.10,
                    "max_stacks": 5
                },
                "2": {
                    "skill-name": "Call of the Firefighter",
                    "description": "Few troops can remain unmoved by Fred's remarkable heroics, increasing Rally Troops' Attack by 15%.",
                    "rally_attack_increase": 0.15
                }
            }
        }
    }
]

HERO = fred_hero