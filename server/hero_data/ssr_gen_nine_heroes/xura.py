xura_hero = [
    {
        "hero-name": "Xura",
        "hero-class": "marksman",
        "rarity": "SSR",
        "generation": 9,
        "expedition-skill-type": "combat",
        "available-from": {
            "server-day": 600,
            "source": "Daily Deals / SvS / King of Icefield"
        },
        "base-stats": {
            "attack": 12513,
            "defense": 10300,
            "health": 77255,
            "marksman-attack": 9.4075,
            "marksman-defense": 9.4075
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Life Dance",
                    "description": "Xura summons divine aid by dance invocation, healing all friendly heroes' health equal to Attack * [20% / 40% / 60% / 80% / 100%] per second while reducing their damage taken by 30% for 3 seconds. Xura is immune to control effects throughout.",
                    "heal_percentage_per_second": {
                        "1": 0.20,
                        "2": 0.40,
                        "3": 0.60,
                        "4": 0.80,
                        "5": 1.00
                    },
                    "damage_reduction": 0.30,
                    "duration_seconds": 3,
                    "immune_to_control": True
                },
                "2": {
                    "skill-name": "Sporebind",
                    "description": "Xura infects the target with a deadly spore, dealing Attack * [100% / 110% / 120% / 130% / 140%] damage each time the target attacks, lasts for 3 seconds.",
                    "damage_percentage": {
                        "1": 1.00,
                        "2": 1.10,
                        "3": 1.20,
                        "4": 1.30,
                        "5": 1.40
                    },
                    "duration_seconds": 3
                },
                "3": {
                    "skill-name": "Numbing Dart",
                    "description": "A blow dart lotion increases Xura's Attack by [4% / 6% / 8% / 10% / 12%] with a 20% chance per dart of immobilizing the target for 1 second.",
                    "attack_increase_percentage": {
                        "1": 0.04,
                        "2": 0.06,
                        "3": 0.08,
                        "4": 0.10,
                        "5": 0.12
                    },
                    "immobilize_chance": 0.20,
                    "immobilize_duration_seconds": 1
                }
            },
            "expedition": {
                "1": {
                    "skill-name": "Fungal Fog",
                    "description": "Xura releases an underground fungi that quickly multiplies to block enemy vision, reducing damage dealt to friendly troops by [4% / 8% / 12% / 16% / 20%].",
                    "level_percentage": {
                        "1": 0.04,
                        "2": 0.08,
                        "3": 0.12,
                        "4": 0.16,
                        "5": 0.20
                    },
                    "damage_reduction_percentage": {
                        "1": 0.04,
                        "2": 0.08,
                        "3": 0.12,
                        "4": 0.16,
                        "5": 0.20
                    }
                },
                "2": {
                    "skill-name": "Piercing Arrow",
                    "description": "Being able to identify the weak spots in the enemy's armor, Xura's Marksmen deal [20% / 40% / 60% / 80% / 100%] additional damage every 2 strikes and make their target take [5% / 10% / 15% / 20% / 25%] more damage for 1 turn.",
                    "level_percentage": {
                        "1": 0.20,
                        "2": 0.40,
                        "3": 0.60,
                        "4": 0.80,
                        "5": 1.00
                    },
                    "additional_damage_percentage": {
                        "1": 0.20,
                        "2": 0.40,
                        "3": 0.60,
                        "4": 0.80,
                        "5": 1.00
                    },
                    "trigger_every_n_strikes": 2,
                    "target_damage_taken_increase_percentage": {
                        "1": 0.05,
                        "2": 0.10,
                        "3": 0.15,
                        "4": 0.20,
                        "5": 0.25
                    },
                    "target_damage_taken_duration_turns": 1
                },
                "3": {
                    "skill-name": "Unorthodoxy",
                    "description": "Xura's unorthodox tactics are quite disruptive, increasing Marksmen's damage dealt by [3% / 6% / 9% / 12% / 15%] while reducing their damage taken by [2% / 4% / 6% / 8% / 10%].",
                    "level_percentage": {
                        "1": 0.03,
                        "2": 0.06,
                        "3": 0.09,
                        "4": 0.12,
                        "5": 0.15
                    },
                    "marksman_damage_increase_percentage": {
                        "1": 0.03,
                        "2": 0.06,
                        "3": 0.09,
                        "4": 0.12,
                        "5": 0.15
                    },
                    "marksman_damage_reduction_percentage": {
                        "1": 0.02,
                        "2": 0.04,
                        "3": 0.06,
                        "4": 0.08,
                        "5": 0.10
                    }
                }
            }
        },
        "exclusive-weapon": {
            "name": "Witch Mask",
            "max-stats": {
                "power": 1044000,
                "attack": 2533,
                "defense": 2088,
                "health": 15659,
                "marksman-lethality": 2.32,
                "marksman-health": 2.32
            },
            "skills": {
                "1": {
                    "skill-name": "Bar Cry",
                    "description": "Xura exhorts an Attack ally with a tribal war dance, increasing their damage dealt by 60% for 4 seconds in Exploration.",
                    "damage_increase_percentage": 0.60,
                    "duration_seconds": 4,
                    "mode": "exploration"
                },
                "2": {
                    "skill-name": "Gaiac Hymn",
                    "description": "Xura exhorts the City's Defenders with ancient hymns to Gaia, increasing their Attack by 15% in Expedition.",
                    "attack_increase_percentage": 0.15,
                    "mode": "expedition"
                }
            }
        }
    }
]

HERO = xura_hero