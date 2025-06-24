mia_hero = [
    {
        "hero-name": "Mia",
        "hero-class": "lancer",
        "rarity": "SSR Generation 3",
        "generation": 3,
        "base-stats": {
            "attack": 3330,
            "defense": 3330,
            "health": 33300,
            "lancer-attack": 2.9023,
            "lancer-defense": 2.9023
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Fate's Finale",
                    "description": "Mia throws a tarot card at enemies, dealing Attack * [270% / 297% / 324% / 351% / 378%] damage, and can either reduce the target's Attack by 20% for 2s, or stun the target for 1.5s.",
                    "level_percentage": {
                        "1": 2.70,
                        "2": 2.97,
                        "3": 3.24,
                        "4": 3.51,
                        "5": 3.78
                    }
                },
                "2": {
                    "skill-name": "Bad Omen",
                    "description": "Mia curses an enemy target, dealing fluctuating damage based on a \"base value\" of Mia's Attack * [50% / 55% / 60% / 65% / 70%]. The final damage dealt will be a random figure ranging from 5% to 600% of the \"base value\".",
                    "level_percentage": {
                        "1": 0.50,
                        "2": 0.55,
                        "3": 0.60,
                        "4": 0.65,
                        "5": 0.70
                    }
                },
                "3": {
                    "skill-name": "Guardian of Destiny",
                    "description": "Mia protects the hero with the lowest remaining Health and restores Health for the hero based on a \"base value\" of Mia's Attack * [100% / 110% / 120% / 130% / 140%]. The final Health restored will be a random figure ranging from 5% to 400% of the \"base value\".",
                    "level_percentage": {
                        "1": 1.00,
                        "2": 1.10,
                        "3": 1.20,
                        "4": 1.30,
                        "5": 1.40
                    }
                }
            },
            "expedition": {
                "1": {
                    "skill-name": "Bad Luck Streak",
                    "description": "Grants all troops' attack a 50% chance of cursing the target, increasing their damage taken by [10% / 20% / 30% / 40% / 50%].",
                    "level_percentage": {
                        "1": 0.10,
                        "2": 0.20,
                        "3": 0.30,
                        "4": 0.40,
                        "5": 0.50
                    }
                },
                "2": {
                    "skill-name": "Lucky Charm",
                    "description": "Mia brings good luck to the Troops, granting a 50% chance of boosting troops' Attack by [10% / 20% / 30% / 40% / 50%].",
                    "level_percentage": {
                        "1": 0.10,
                        "2": 0.20,
                        "3": 0.30,
                        "4": 0.40,
                        "5": 0.50
                    }
                },
                "3": {
                    "skill-name": "Ritual Deciphering",
                    "description": "Mia foresees potential dangers before battle, granting a 40% chance of reducing damage taken by [10% / 20% / 30% / 40% / 50%] for all troops.",
                    "level_percentage": {
                        "1": 0.10,
                        "2": 0.20,
                        "3": 0.30,
                        "4": 0.40,
                        "5": 0.50
                    }
                }
            }
        },
        "exclusive-weapon": {
            "name": "Fate Crystal",
            "levels": [
                {
                    "level": 1,
                    "power": 42000,
                    "attack": 84,
                    "defense": 84,
                    "health": 840,
                    "lancer-lethality": 7.0,
                    "lancer-health": 7.0,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vision of Truth",
                            "description": "Increases upper / lower limits of Mia's fluctuating skills by 30%",
                            "level_percentage": 0.30
                        }
                    }
                },
                {
                    "level": 2,
                    "power": 71400,
                    "attack": 142,
                    "defense": 142,
                    "health": 1428,
                    "lancer-lethality": 14.0,
                    "lancer-health": 14.0,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vision of Truth",
                            "description": "Increases upper / lower limits of Mia's fluctuating skills by 30%",
                            "level_percentage": 0.30
                        },
                        "expedition": {
                            "skill-name": "Rally of Fate",
                            "description": "Rally Troop Attack +5%",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 3,
                    "power": 100800,
                    "attack": 201,
                    "defense": 201,
                    "health": 2015,
                    "lancer-lethality": 21.0,
                    "lancer-health": 21.0,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vision of Truth",
                            "description": "Increases upper / lower limits of Mia's fluctuating skills by 60%",
                            "level_percentage": 0.60
                        },
                        "expedition": {
                            "skill-name": "Rally of Fate",
                            "description": "Rally Troop Attack +5%",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 4,
                    "power": 130200,
                    "attack": 260,
                    "defense": 260,
                    "health": 2604,
                    "lancer-lethality": 28.0,
                    "lancer-health": 28.0,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vision of Truth",
                            "description": "Increases upper / lower limits of Mia's fluctuating skills by 60%",
                            "level_percentage": 0.60
                        },
                        "expedition": {
                            "skill-name": "Rally of Fate",
                            "description": "Rally Troop Attack +7.5%",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 5,
                    "power": 159600,
                    "attack": 319,
                    "defense": 319,
                    "health": 3192,
                    "lancer-lethality": 35.0,
                    "lancer-health": 35.0,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vision of Truth",
                            "description": "Increases upper / lower limits of Mia's fluctuating skills by 90%",
                            "level_percentage": 0.90
                        },
                        "expedition": {
                            "skill-name": "Rally of Fate",
                            "description": "Rally Troop Attack +7.5%",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 6,
                    "power": 189000,
                    "attack": 378,
                    "defense": 378,
                    "health": 3779,
                    "lancer-lethality": 42.0,
                    "lancer-health": 42.0,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vision of Truth",
                            "description": "Increases upper / lower limits of Mia's fluctuating skills by 90%",
                            "level_percentage": 0.90
                        },
                        "expedition": {
                            "skill-name": "Rally of Fate",
                            "description": "Rally Troop Attack +10%",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 7,
                    "power": 218400,
                    "attack": 436,
                    "defense": 436,
                    "health": 4368,
                    "lancer-lethality": 49.0,
                    "lancer-health": 49.0,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vision of Truth",
                            "description": "Increases upper / lower limits of Mia's fluctuating skills by 120%",
                            "level_percentage": 1.20
                        },
                        "expedition": {
                            "skill-name": "Rally of Fate",
                            "description": "Rally Troop Attack +10%",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 8,
                    "power": 247800,
                    "attack": 495,
                    "defense": 495,
                    "health": 4956,
                    "lancer-lethality": 56.0,
                    "lancer-health": 56.0,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vision of Truth",
                            "description": "Increases upper / lower limits of Mia's fluctuating skills by 120%",
                            "level_percentage": 1.20
                        },
                        "expedition": {
                            "skill-name": "Rally of Fate",
                            "description": "Rally Troop Attack +12.5%",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 9,
                    "power": 277200,
                    "attack": 554,
                    "defense": 554,
                    "health": 5544,
                    "lancer-lethality": 63.0,
                    "lancer-health": 63.0,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vision of Truth",
                            "description": "Increases upper / lower limits of Mia's fluctuating skills by 150%",
                            "level_percentage": 1.50
                        },
                        "expedition": {
                            "skill-name": "Rally of Fate",
                            "description": "Rally Troop Attack +12.5%",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 10,
                    "power": 315000,
                    "attack": 630,
                    "defense": 630,
                    "health": 6300,
                    "lancer-lethality": 70.0,
                    "lancer-health": 70.0,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vision of Truth",
                            "description": "Increases upper / lower limits of Mia's fluctuating skills by 150%",
                            "level_percentage": 1.50
                        },
                        "expedition": {
                            "skill-name": "Rally of Fate",
                            "description": "Rally Troop Attack +15%",
                            "level_percentage": 0.15
                        }
                    }
                }
            ]
        }
    }
]

HERO = mia_hero
