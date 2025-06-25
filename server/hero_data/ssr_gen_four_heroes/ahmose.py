ahmose_hero = [
    {
        "hero-name": "Ahmose",
        "hero-class": "infantry",
        "rarity": "SSR",
        "generation": 4,
        "base-stats": {
            "attack": 3150,
            "defense": 4106,
            "health": 61604,
            "infantry-attack": 3.7029,
            "infantry-defense": 3.7029
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Cthugha's Protection",
                    "description": "Ahmose wield his robust shield, entering an invulnerable state (unable to move or cast skills, immune to control effects) and reducing damage taken by [30% / 40% / 50% / 60% / 70%] for nearby friendly troops for 2s.",
                    "level_percentage": {
                        "1": 0.30,
                        "2": 0.40,
                        "3": 0.50,
                        "4": 0.60,
                        "5": 0.70
                    }
                },
                "2": {
                    "skill-name": "Daybreak Knife",
                    "description": "Ahmose pierces the enemies at the front with a sharp spear, dealing Attack * [70% / 77% / 84% / 91% / 98%] damage, tearing apart the enemy's defense, and making enemies take 20% more damage for the next 2s.",
                    "level_percentage": {
                        "1": 0.70,
                        "2": 0.77,
                        "3": 0.84,
                        "4": 0.91,
                        "5": 0.98
                    }
                },
                "3": {
                    "skill-name": "Ancestral Blessing",
                    "description": "The energy of Fire Crystal, which is akin to the blessing of ancestors, heals Ahmose's wounds. After casting 'Cthugha's Protection', Ahmose will recover Attack * [30% / 33% / 36% / 39% / 42%] Health for 5s.",
                    "level_percentage": {
                        "1": 0.30,
                        "2": 0.33,
                        "3": 0.36,
                        "4": 0.39,
                        "5": 0.42
                    }
                }
            },
            "expedition": {
                "1": {
                    "skill-name": "Viper Formation",
                    "description": "Ahmose revives the lost art of ancient guardians. His Infantry pauses the attack once every four times, reducing damage taken by Lancers and Marksmen by [10% / 15% / 20% / 25% / 30%] and Infantry by [10% / 25% / 40% / 55% / 70%] for 2 turns.",
                    "level_percentage": {
                        "1": {"lancers_marksmen": 0.10, "infantry": 0.10},
                        "2": {"lancers_marksmen": 0.15, "infantry": 0.25},
                        "3": {"lancers_marksmen": 0.20, "infantry": 0.40},
                        "4": {"lancers_marksmen": 0.25, "infantry": 0.55},
                        "5": {"lancers_marksmen": 0.30, "infantry": 0.70}
                    }
                },
                "2": {
                    "skill-name": "Prayer of Flame",
                    "description": "Ahmose excels at raiding on fortified positions with well-coordinated Marksmen, increasing his Infantry's damage dealt by [100% / 125% / 150% / 175% / 200%] and Marksmen's damage dealt by [10% / 20% / 30% / 40% / 50%]. The effect decreases by 80% with each attack and is removed after the fifth.",
                    "level_percentage": {
                        "1": {"infantry": 1.00, "marksmen": 0.10},
                        "2": {"infantry": 1.25, "marksmen": 0.20},
                        "3": {"infantry": 1.50, "marksmen": 0.30},
                        "4": {"infantry": 1.75, "marksmen": 0.40},
                        "5": {"infantry": 2.00, "marksmen": 0.50}
                    }
                },
                "3": {
                    "skill-name": "Blade of Light",
                    "description": "Ahmose infuses friendly Infantry's weapons with the essence of Fire Crystals, increasing his infantries' damage dealt per attack by [12% / 24% / 36% / 48% / 60%] and the target's damage taken by [5% / 10% / 15% / 20% / 25%] for 1 turn.",
                    "level_percentage": {
                        "1": {"damage_dealt": 0.12, "damage_taken": 0.05},
                        "2": {"damage_dealt": 0.24, "damage_taken": 0.10},
                        "3": {"damage_dealt": 0.36, "damage_taken": 0.15},
                        "4": {"damage_dealt": 0.48, "damage_taken": 0.20},
                        "5": {"damage_dealt": 0.60, "damage_taken": 0.25}
                    }
                }
            }
        },
        "exclusive-weapon": {
            "name": "Guardian's Relic",
            "levels": [
                {
                    "level": 1,
                    "power": 55000,
                    "attack": 85,
                    "defense": 111,
                    "health": 1665,
                    "infantry-lethality": 0.0925,
                    "infantry-health": 0.0925,
                    "skills": {
                        "exploration": {
                            "skill-name": "Unyielding Determination",
                            "description": "Friendly Troop Attack +30% during Cthuga's Protection for 2.5s",
                            "level_percentage": 0.30
                        }
                    }
                },
                {
                    "level": 2,
                    "power": 94350,
                    "attack": 144,
                    "defense": 144,
                    "health": 2830,
                    "infantry-lethality": 0.1850,
                    "infantry-health": 0.1850,
                    "skills": {
                        "exploration": {
                            "skill-name": "Unyielding Determination",
                            "description": "Friendly Troop Attack +30% during Cthuga's Protection for 2.5s",
                            "level_percentage": 0.30
                        },
                        "expedition": {
                            "skill-name": "Oath of Guardian",
                            "description": "Defender Troop Health +5%",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 3,
                    "power": 133200,
                    "attack": 203,
                    "defense": 266,
                    "health": 3996,
                    "infantry-lethality": 0.2775,
                    "infantry-health": 0.2775,
                    "skills": {
                        "exploration": {
                            "skill-name": "Unyielding Determination",
                            "description": "Friendly Troop Attack +33% during Cthuga's Protection for 2.5s",
                            "level_percentage": 0.33
                        },
                        "expedition": {
                            "skill-name": "Oath of Guardian",
                            "description": "Defender Troop Health +5%",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 4,
                    "power": 172050,
                    "attack": 262,
                    "defense": 344,
                    "health": 5161,
                    "infantry-lethality": 0.3700,
                    "infantry-health": 0.3700,
                    "skills": {
                        "exploration": {
                            "skill-name": "Unyielding Determination",
                            "description": "Friendly Troop Attack +33% during Cthuga's Protection for 2.5s",
                            "level_percentage": 0.33
                        },
                        "expedition": {
                            "skill-name": "Oath of Guardian",
                            "description": "Defender Troop Health +7.5%",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 5,
                    "power": 210900,
                    "attack": 323,
                    "defense": 421,
                    "health": 6327,
                    "infantry-lethality": 0.4625,
                    "infantry-health": 0.4625,
                    "skills": {
                        "exploration": {
                            "skill-name": "Unyielding Determination",
                            "description": "Friendly Troop Attack +36% during Cthuga's Protection for 2.5s",
                            "level_percentage": 0.36
                        },
                        "expedition": {
                            "skill-name": "Oath of Guardian",
                            "description": "Defender Troop Health +7.5%",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 6,
                    "power": 249750,
                    "attack": 382,
                    "defense": 499,
                    "health": 7492,
                    "infantry-lethality": 0.5550,
                    "infantry-health": 0.5550,
                    "skills": {
                        "exploration": {
                            "skill-name": "Unyielding Determination",
                            "description": "Friendly Troop Attack +36% during Cthuga's Protection for 2.5s",
                            "level_percentage": 0.36
                        },
                        "expedition": {
                            "skill-name": "Oath of Guardian",
                            "description": "Defender Troop Health +10%",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 7,
                    "power": 288600,
                    "attack": 442,
                    "defense": 577,
                    "health": 8658,
                    "infantry-lethality": 0.6475,
                    "infantry-health": 0.6475,
                    "skills": {
                        "exploration": {
                            "skill-name": "Unyielding Determination",
                            "description": "Friendly Troop Attack +39% during Cthuga's Protection for 2.5s",
                            "level_percentage": 0.39
                        },
                        "expedition": {
                            "skill-name": "Oath of Guardian",
                            "description": "Defender Troop Health +10%",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 8,
                    "power": 327450,
                    "attack": 501,
                    "defense": 654,
                    "health": 9823,
                    "infantry-lethality": 0.7400,
                    "infantry-health": 0.7400,
                    "skills": {
                        "exploration": {
                            "skill-name": "Unyielding Determination",
                            "description": "Friendly Troop Attack +39% during Cthuga's Protection for 2.5s",
                            "level_percentage": 0.39
                        },
                        "expedition": {
                            "skill-name": "Oath of Guardian",
                            "description": "Defender Troop Health +12.5%",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 9,
                    "power": 366300,
                    "attack": 560,
                    "defense": 732,
                    "health": 10989,
                    "infantry-lethality": 0.8325,
                    "infantry-health": 0.8325,
                    "skills": {
                        "exploration": {
                            "skill-name": "Unyielding Determination",
                            "description": "Friendly Troop Attack +42% during Cthuga's Protection for 2.5s",
                            "level_percentage": 0.42
                        },
                        "expedition": {
                            "skill-name": "Oath of Guardian",
                            "description": "Defender Troop Health +12.5%",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 10,
                    "power": 416250,
                    "attack": 638,
                    "defense": 832,
                    "health": 12487,
                    "infantry-lethality": 0.9250,
                    "infantry-health": 0.9250,
                    "skills": {
                        "exploration": {
                            "skill-name": "Unyielding Determination",
                            "description": "Friendly Troop Attack +42% during Cthuga's Protection for 2.5s",
                            "level_percentage": 0.42
                        },
                        "expedition": {
                            "skill-name": "Oath of Guardian",
                            "description": "Defender Troop Health +15%",
                            "level_percentage": 0.15
                        }
                    }
                }
            ]
        }
    }
]

HERO = ahmose_hero
