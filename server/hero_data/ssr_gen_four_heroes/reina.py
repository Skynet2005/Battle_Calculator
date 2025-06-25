reina_hero = [
    {
        "hero-name": "Reina",
        "hero-class": "lancer",
        "rarity": "SSR",
        "generation": 4,
        "base-stats": {
            "attack": 4106,
            "defense": 4106,
            "health": 41070,
            "lancer-attack": 3.7029,
            "lancer-defense": 3.7029
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Phantom Assault",
                    "description": "Reina conjures an illusion enemy forces from behind, dealing Attack * [300% / 330% / 360% / 390% / 420%] Area of Effect Damage.",
                    "level_percentage": {
                        "1": 3.00,
                        "2": 3.30,
                        "3": 3.60,
                        "4": 3.90,
                        "5": 4.20
                    }
                },
                "2": {
                    "skill-name": "Vanishing Technique",
                    "description": "Reina has a [5% / 10% / 15% / 20% / 25%] chance of confusing the opponent with illusion and dodging the damage when receiving a Normal Attack.",
                    "level_percentage": {
                        "1": 0.05,
                        "2": 0.10,
                        "3": 0.15,
                        "4": 0.20,
                        "5": 0.25
                    }
                },
                "3": {
                    "skill-name": "Poison of Demon",
                    "description": "Reina inflicts illusion on enemy targets (hero first), dealing damage equal to Attack * [100% / 110% / 120% / 130% / 140%] and immobilising them for 1.5s.",
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
                    "skill-name": "Assassin's Instinct",
                    "description": "Reina targets enemy weak spots, increasing normal attack damage by [10% / 15% / 20% / 25% / 30%] for all troops.",
                    "level_percentage": {
                        "1": 0.10,
                        "2": 0.15,
                        "3": 0.20,
                        "4": 0.25,
                        "5": 0.30
                    }
                },
                "2": {
                    "skill-name": "Swift Jive",
                    "description": "Reina's adept leadership grants all troops a [4% / 8% / 12% / 16% / 20%] chance of dodging normal attacks.",
                    "level_percentage": {
                        "1": 0.04,
                        "2": 0.08,
                        "3": 0.12,
                        "4": 0.16,
                        "5": 0.20
                    }
                },
                "3": {
                    "skill-name": "Shadow Blade",
                    "description": "With Reina's clever tactics, her Lancers have a 25% chance of performing an extra attack, dealing [120% / 140% / 160% / 180% / 200%] damage.",
                    "level_percentage": {
                        "1": 1.20,
                        "2": 1.40,
                        "3": 1.60,
                        "4": 1.80,
                        "5": 2.00
                    }
                }
            }
        },
        "exclusive-weapon": {
            "name": "Raikiri",
            "levels": [
                {
                    "level": 1,
                    "power": 55000,
                    "attack": 111,
                    "defense": 111,
                    "health": 1110,
                    "lancer-lethality": 0.0925,
                    "lancer-health": 0.0925,
                    "skills": {
                        "exploration": {
                            "skill-name": "Silhouette Strike",
                            "description": "40% chance of an extra attack dealing Attack * 25% damage alongside a normal attack",
                            "level_percentage": 0.25
                        }
                    }
                },
                {
                    "level": 2,
                    "power": 94350,
                    "attack": 188,
                    "defense": 188,
                    "health": 1887,
                    "lancer-lethality": 0.1850,
                    "lancer-health": 0.1850,
                    "skills": {
                        "exploration": {
                            "skill-name": "Silhouette Strike",
                            "description": "40% chance of an extra attack dealing Attack * 25% damage alongside a normal attack",
                            "level_percentage": 0.25
                        },
                        "expedition": {
                            "skill-name": "Fiery Invasion",
                            "description": "Rally Troop Lethality +5%",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 3,
                    "power": 133200,
                    "attack": 266,
                    "defense": 266,
                    "health": 2664,
                    "lancer-lethality": 0.2775,
                    "lancer-health": 0.2775,
                    "skills": {
                        "exploration": {
                            "skill-name": "Silhouette Strike",
                            "description": "40% chance of an extra attack dealing Attack * 30% damage alongside a normal attack",
                            "level_percentage": 0.30
                        },
                        "expedition": {
                            "skill-name": "Fiery Invasion",
                            "description": "Rally Troop Lethality +5%",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 4,
                    "power": 172050,
                    "attack": 344,
                    "defense": 344,
                    "health": 3441,
                    "lancer-lethality": 0.3700,
                    "lancer-health": 0.3700,
                    "skills": {
                        "exploration": {
                            "skill-name": "Silhouette Strike",
                            "description": "40% chance of an extra attack dealing Attack * 30% damage alongside a normal attack",
                            "level_percentage": 0.30
                        },
                        "expedition": {
                            "skill-name": "Fiery Invasion",
                            "description": "Rally Troop Lethality +7.5%",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 5,
                    "power": 210900,
                    "attack": 421,
                    "defense": 421,
                    "health": 4218,
                    "lancer-lethality": 0.4625,
                    "lancer-health": 0.4625,
                    "skills": {
                        "exploration": {
                            "skill-name": "Silhouette Strike",
                            "description": "40% chance of an extra attack dealing Attack * 35% damage alongside a normal attack",
                            "level_percentage": 0.35
                        },
                        "expedition": {
                            "skill-name": "Fiery Invasion",
                            "description": "Rally Troop Lethality +7.5%",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 6,
                    "power": 249750,
                    "attack": 499,
                    "defense": 499,
                    "health": 4995,
                    "lancer-lethality": 0.5550,
                    "lancer-health": 0.5550,
                    "skills": {
                        "exploration": {
                            "skill-name": "Silhouette Strike",
                            "description": "40% chance of an extra attack dealing Attack * 35% damage alongside a normal attack",
                            "level_percentage": 0.35
                        },
                        "expedition": {
                            "skill-name": "Fiery Invasion",
                            "description": "Rally Troop Lethality +10%",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 7,
                    "power": 288600,
                    "attack": 577,
                    "defense": 577,
                    "health": 5772,
                    "lancer-lethality": 0.6475,
                    "lancer-health": 0.6475,
                    "skills": {
                        "exploration": {
                            "skill-name": "Silhouette Strike",
                            "description": "40% chance of an extra attack dealing Attack * 40% damage alongside a normal attack",
                            "level_percentage": 0.40
                        },
                        "expedition": {
                            "skill-name": "Fiery Invasion",
                            "description": "Rally Troop Lethality +10%",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 8,
                    "power": 327450,
                    "attack": 654,
                    "defense": 654,
                    "health": 6549,
                    "lancer-lethality": 0.7400,
                    "lancer-health": 0.7400,
                    "skills": {
                        "exploration": {
                            "skill-name": "Silhouette Strike",
                            "description": "40% chance of an extra attack dealing Attack * 40% damage alongside a normal attack",
                            "level_percentage": 0.40
                        },
                        "expedition": {
                            "skill-name": "Fiery Invasion",
                            "description": "Rally Troop Lethality +12.5%",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 9,
                    "power": 366300,
                    "attack": 732,
                    "defense": 732,
                    "health": 7326,
                    "lancer-lethality": 0.8325,
                    "lancer-health": 0.8325,
                    "skills": {
                        "exploration": {
                            "skill-name": "Silhouette Strike",
                            "description": "40% chance of an extra attack dealing Attack * 45% damage alongside a normal attack",
                            "level_percentage": 0.45
                        },
                        "expedition": {
                            "skill-name": "Fiery Invasion",
                            "description": "Rally Troop Lethality +12.5%",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 10,
                    "power": 416250,
                    "attack": 832,
                    "defense": 832,
                    "health": 8325,
                    "lancer-lethality": 0.9250,
                    "lancer-health": 0.9250,
                    "skills": {
                        "exploration": {
                            "skill-name": "Silhouette Strike",
                            "description": "40% chance of an extra attack dealing Attack * 45% damage alongside a normal attack",
                            "level_percentage": 0.45
                        },
                        "expedition": {
                            "skill-name": "Fiery Invasion",
                            "description": "Rally Troop Lethality +15%",
                            "level_percentage": 0.15
                        }
                    }
                }
            ]
        }
    }
]

HERO = reina_hero
