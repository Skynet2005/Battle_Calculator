magnus_hero = [
    {
        "hero-name": "Magnus",
        "hero-class": "infantry",
        "rarity": "SSR",
        "generation": 9,
        "expedition-skill-type": "combat",
        "available-from": {
            "server-day": 600,
            "source": "Hall of Heroes"
        },
        "base-stats": {
            "attack": 7901,
            "defense": 10300,
            "health": 153511,
            "infantry-attack": 9.4075,
            "infantry-defense": 9.4075
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Frozen Fury",
                    "description": "Magnus whirls twin axes, taunting nearby enemies to attack while dealing Attack * [60% / 66% / 72% / 78% / 84%] damage to the same foes every 0.5 seconds for 3 seconds.",
                    "level_percentage": {
                        "1": 0.60,
                        "2": 0.66,
                        "3": 0.72,
                        "4": 0.78,
                        "5": 0.84
                    }
                },
                "2": {
                    "skill-name": "Wind Tomahawk",
                    "description": "Magnus targets a hero with a devastating ax throw, reopening old wounds that deal a further Attack * [50% / 55% / 60% / 65% / 70%] damage for 3 seconds on top of Attack * [100% / 110% / 120% / 130% / 140%] initial damage.",
                    "initial_damage_percentage": {
                        "1": 1.00,
                        "2": 1.10,
                        "3": 1.20,
                        "4": 1.30,
                        "5": 1.40
                    },
                    "bleed_damage_percentage": {
                        "1": 0.50,
                        "2": 0.55,
                        "3": 0.60,
                        "4": 0.65,
                        "5": 0.70
                    }
                },
                "3": {
                    "skill-name": "Sunderer",
                    "description": "Magnus' normal attacks have a 30% chance of sundering opponent armor, dealing Attack * [50% / 55% / 60% / 65% / 70%] additional damage and reducing Defense by [5% / 10% / 15% / 20% / 25%] for 2 seconds.",
                    "damage_percentage": {
                        "1": 0.50,
                        "2": 0.55,
                        "3": 0.60,
                        "4": 0.65,
                        "5": 0.70
                    },
                    "defense_reduction_percentage": {
                        "1": 0.05,
                        "2": 0.10,
                        "3": 0.15,
                        "4": 0.20,
                        "5": 0.25
                    },
                    "trigger_chance": 0.30
                }
            },
            "expedition": {
                "1": {
                    "skill-name": "Rapacious",
                    "description": "Magnus rouses his troops with brutal intensity, boosting friendly Troop Attack by [5% / 10% / 15% / 20% / 25%].",
                    "level_percentage": {
                        "1": 0.05,
                        "2": 0.10,
                        "3": 0.15,
                        "4": 0.20,
                        "5": 0.25
                    }
                },
                "2": {
                    "skill-name": "Iron Phalanx",
                    "description": "A master of tight formations, Infantry under Magnus' command enjoy a 40% chance of gaining [10% / 20% / 30% / 40% / 50%] Defense when attacking for 1 turn.",
                    "level_percentage": {
                        "1": 0.10,
                        "2": 0.20,
                        "3": 0.30,
                        "4": 0.40,
                        "5": 0.50
                    },
                    "trigger_chance": 0.40
                },
                "3": {
                    "skill-name": "Iceman",
                    "description": "Magnus' intrepid adventuring skills provide a [2% / 4% / 6% / 8% / 10%] reduction in damage versus friendly Infantry while boosting friendly Marksmen damage by [2% / 4% / 6% / 8% / 10%].",
                    "level_percentage": {
                        "1": 0.02,
                        "2": 0.04,
                        "3": 0.06,
                        "4": 0.08,
                        "5": 0.10
                    },
                    "infantry_damage_reduction_percentage": {
                        "1": 0.02,
                        "2": 0.04,
                        "3": 0.06,
                        "4": 0.08,
                        "5": 0.10
                    },
                    "marksman_damage_boost_percentage": {
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
            "name": "Storm Axe",
            "max-stats": {
                "power": 1044000,
                "attack": 1600,
                "defense": 2088,
                "health": 31319,
                "infantry-lethality": 2.32,
                "infantry-health": 2.32
            },
            "skills": {
                "1": {
                    "skill-name": "Heroic Stock",
                    "description": "A true son of the tundra, Magnus' iron constitution reduces incoming damage by 15% while increasing Frozen Fury's Defense bonus by 75%.",
                    "damage_reduction": 0.15,
                    "frozen_fury_defense_bonus_increase": 0.75
                },
                "2": {
                    "skill-name": "Valoric Inspiration",
                    "description": "Ever the raconteur, Magnus' tales of Valhalla and ancient heroics inspires Defender Squads with 15% increased Health.",
                    "defender_health_increase": 0.15
                }
            }
        }
    }
]

HERO = magnus_hero