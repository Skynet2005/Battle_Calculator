alonso_hero = [
    {
        "hero-name": "Alonso",
        "hero-class": "marksman",
        "rarity": "SSR Generation 2",
        "generation": 2,
        "base-stats": {
            "attack": 3235,
            "defense": 2664,
            "health": 19980,
            "marksman-attack": 2.4019,
            "marksman-defense": 2.4019
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Trapnet",
                    "description": "Alonso casts a wide net over the target area, dealing Attack * [200% / 220% / 240% / 260% / 280%] Area of Effect Damage and immobilizing enemies for 1.5s.",
                    "level_percentage": {
                        "1": 2.00,
                        "2": 2.20,
                        "3": 2.40,
                        "4": 2.60,
                        "5": 2.80
                    }
                },
                "2": {
                    "skill-name": "Tidal Force",
                    "description": "Alonso shoots a harpoon with tsunami-like force at a target, dealing Attack * [50% / 55% / 60% / 65% / 70%] Area of Effect Damage.",
                    "level_percentage": {
                        "1": 0.50,
                        "2": 0.55,
                        "3": 0.60,
                        "4": 0.65,
                        "5": 0.70
                    }
                },
                "3": {
                    "skill-name": "Harpoon Blast",
                    "description": "Alonso's heavy harpoon can really do some damage, stunning targets for [0.2s / 0.2s / 0.4s / 0.4s / 0.5s] after every [8 / 7 / 7 / 6 / 5] strikes.",
                    "level_stun_duration": {
                        "1": 0.2,
                        "2": 0.2,
                        "3": 0.4,
                        "4": 0.4,
                        "5": 0.5
                    },
                    "level_strikes": {
                        "1": 8,
                        "2": 7,
                        "3": 7,
                        "4": 6,
                        "5": 5
                    }
                }
            },
            "expedition": {
                "1": {
                    "skill-name": "Onslaught",
                    "description": "Alonso's strength, like a massive wave, grants all troops' attack a [4% / 8% / 12% / 16% / 20%] chance of stunning the target for 1 turn.",
                    "level_percentage": {
                        "1": 0.04,
                        "2": 0.08,
                        "3": 0.12,
                        "4": 0.16,
                        "5": 0.20
                    }
                },
                "2": {
                    "skill-name": "Iron Strength",
                    "description": "Alonso's indomitable will grants all troops' attack a 20% chance of reducing damage dealt by [10% / 20% / 30% / 40% / 50%] for all enemy troops for 2 turns.",
                    "level_percentage": {
                        "1": 0.10,
                        "2": 0.20,
                        "3": 0.30,
                        "4": 0.40,
                        "5": 0.50
                    }
                },
                "3": {
                    "skill-name": "Poison Harpoon",
                    "description": "Alonso coats weapons with lethal toxins, granting all troops' attack a 50% chance of dealing [10% / 20% / 30% / 40% / 50%] more damage.",
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
            "name": "Captain Ahab",
            "levels": [
                {
                    "level": 1,
                    "power": 36000,
                    "attack": 86,
                    "defense": 72,
                    "health": 540,
                    "marksman-lethality": 0.0600,
                    "marksman-health": 0.0600,
                    "skills": {
                        "exploration": {
                            "skill-name": "Ocean's Bounty",
                            "description": "Heal weakest hero by 5% with each basic attack",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 2,
                    "power": 61200,
                    "attack": 147,
                    "defense": 122,
                    "health": 918,
                    "marksman-lethality": 0.1200,
                    "marksman-health": 0.1200,
                    "skills": {
                        "exploration": {
                            "skill-name": "Ocean's Bounty",
                            "description": "Heal weakest hero by 5% with each basic attack",
                            "level_percentage": 0.05
                        },
                        "expedition": {
                            "skill-name": "Harpoon Enhancement",
                            "description": "Rally Troop Lethality +5%",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 3,
                    "power": 86400,
                    "attack": 208,
                    "defense": 172,
                    "health": 1296,
                    "marksman-lethality": 0.1800,
                    "marksman-health": 0.1800,
                    "skills": {
                        "exploration": {
                            "skill-name": "Ocean's Bounty",
                            "description": "Heal weakest hero by 7.5% with each basic attack",
                            "level_percentage": 0.075
                        },
                        "expedition": {
                            "skill-name": "Harpoon Enhancement",
                            "description": "Rally Troop Lethality +5%",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 4,
                    "power": 111600,
                    "attack": 271,
                    "defense": 223,
                    "health": 1674,
                    "marksman-lethality": 0.2400,
                    "marksman-health": 0.2400,
                    "skills": {
                        "exploration": {
                            "skill-name": "Ocean's Bounty",
                            "description": "Heal weakest hero by 7.5% with each basic attack",
                            "level_percentage": 0.075
                        },
                        "expedition": {
                            "skill-name": "Harpoon Enhancement",
                            "description": "Rally Troop Lethality +7.5%",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 5,
                    "power": 136800,
                    "attack": 332,
                    "defense": 273,
                    "health": 2052,
                    "marksman-lethality": 0.3000,
                    "marksman-health": 0.3000,
                    "skills": {
                        "exploration": {
                            "skill-name": "Ocean's Bounty",
                            "description": "Heal weakest hero by 10% with each basic attack",
                            "level_percentage": 0.10
                        },
                        "expedition": {
                            "skill-name": "Harpoon Enhancement",
                            "description": "Rally Troop Lethality +7.5%",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 6,
                    "power": 162000,
                    "attack": 393,
                    "defense": 324,
                    "health": 2430,
                    "marksman-lethality": 0.3600,
                    "marksman-health": 0.3600,
                    "skills": {
                        "exploration": {
                            "skill-name": "Ocean's Bounty",
                            "description": "Heal weakest hero by 10% with each basic attack",
                            "level_percentage": 0.10
                        },
                        "expedition": {
                            "skill-name": "Harpoon Enhancement",
                            "description": "Rally Troop Lethality +10%",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 7,
                    "power": 187200,
                    "attack": 454,
                    "defense": 374,
                    "health": 2808,
                    "marksman-lethality": 0.4200,
                    "marksman-health": 0.4200,
                    "skills": {
                        "exploration": {
                            "skill-name": "Ocean's Bounty",
                            "description": "Heal weakest hero by 12.5% with each basic attack",
                            "level_percentage": 0.125
                        },
                        "expedition": {
                            "skill-name": "Harpoon Enhancement",
                            "description": "Rally Troop Lethality +10%",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 8,
                    "power": 212400,
                    "attack": 516,
                    "defense": 424,
                    "health": 3186,
                    "marksman-lethality": 0.4800,
                    "marksman-health": 0.4800,
                    "skills": {
                        "exploration": {
                            "skill-name": "Ocean's Bounty",
                            "description": "Heal weakest hero by 12.5% with each basic attack",
                            "level_percentage": 0.125
                        },
                        "expedition": {
                            "skill-name": "Harpoon Enhancement",
                            "description": "Rally Troop Lethality +12.5%",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 9,
                    "power": 237600,
                    "attack": 577,
                    "defense": 475,
                    "health": 3564,
                    "marksman-lethality": 0.5400,
                    "marksman-health": 0.5400,
                    "skills": {
                        "exploration": {
                            "skill-name": "Ocean's Bounty",
                            "description": "Heal weakest hero by 15% with each basic attack",
                            "level_percentage": 0.15
                        },
                        "expedition": {
                            "skill-name": "Harpoon Enhancement",
                            "description": "Rally Troop Lethality +12.5%",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 10,
                    "power": 270000,
                    "attack": 655,
                    "defense": 540,
                    "health": 4050,
                    "marksman-lethality": 0.6000,
                    "marksman-health": 0.6000,
                    "skills": {
                        "exploration": {
                            "skill-name": "Ocean's Bounty",
                            "description": "Heal weakest hero by 15% with each basic attack",
                            "level_percentage": 0.15
                        },
                        "expedition": {
                            "skill-name": "Harpoon Enhancement",
                            "description": "Rally Troop Lethality +15%",
                            "level_percentage": 0.15
                        }
                    }
                }
            ]
        }
    }
]

HERO = alonso_hero
