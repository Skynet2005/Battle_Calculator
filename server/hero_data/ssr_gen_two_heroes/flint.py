flint_hero = [
    {
        "hero-name": "Flint",
        "hero-class": "infantry",
        "rarity": "SSR Generation 2",
        "generation": 2,
        "base-stats": {
            "attack": 2043,
            "defense": 2664,
            "health": 39960,
            "infantry-attack": 2.4019,
            "infantry-defense": 2.4019
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Fires of Vengeance",
                    "description": "Flint's fire-breathing attack deals Attack * [60% / 66% / 72% / 78% / 84%] damage every 0.5s and amplifies damage taken by the target by [10% / 15%/ 20% / 25% / 30%] for 2s.",
                    "level_percentage": {
                        "1": 0.60,
                        "2": 0.66,
                        "3": 0.72,
                        "4": 0.78,
                        "5": 0.84
                    },
                    "level_amplify": {
                        "1": 0.10,
                        "2": 0.15,
                        "3": 0.20,
                        "4": 0.25,
                        "5": 0.30
                    }
                },
                "2": {
                    "skill-name": "Incinerator",
                    "description": "Pain only boosts Flint's potential. Flint immediately regains [20% / 25% / 30% / 35% / 40%] of his max Health when Health is below 50%. Can only activate once per battle.",
                    "level_percentage": {
                        "1": 0.20,
                        "2": 0.25,
                        "3": 0.30,
                        "4": 0.35,
                        "5": 0.40
                    }
                },
                "3": {
                    "skill-name": "Heat Diffusion",
                    "description": "The warmth of Flint's fire represents hope in troubling times, boosting your heroes' Attack Speed by [3% / 4% / 5% / 6% / 7%].",
                    "level_percentage": {
                        "1": 0.03,
                        "2": 0.04,
                        "3": 0.05,
                        "4": 0.06,
                        "5": 0.07
                    }
                }
            },
            "expedition": {
                "1": {
                    "skill-name": "Pyromaniac",
                    "description": "Every flame, no matter how small, can ignite a roaring fire. Flint grants all troops' attack a 20% chance of setting the target on fire, dealing [8% / 16% / 24% / 32% / 40%] damage per turn for 3 turns.",
                    "level_percentage": {
                        "1": 0.08,
                        "2": 0.16,
                        "3": 0.24,
                        "4": 0.32,
                        "5": 0.40
                    }
                },
                "2": {
                    "skill-name": "Burning Resolve",
                    "description": "Flint's fire not only dispels the cold but also ignites the passion for battle, increasing Attack by [5% / 10% / 15% / 20% / 25%] for all troops.",
                    "level_percentage": {
                        "1": 0.05,
                        "2": 0.10,
                        "3": 0.15,
                        "4": 0.20,
                        "5": 0.25
                    }
                },
                "3": {
                    "skill-name": "Immolation",
                    "description": "Flint's burning vengeance threatens all foes, granting all troops' attack a 50% chance of increasing enemy troops' damage taken by [10% / 20% / 30% / 40% / 50%].",
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
            "name": "Dragonbane",
            "levels": [
                {
                    "level": 1,
                    "power": 36000,
                    "attack": 55,
                    "defense": 72,
                    "health": 1080,
                    "infantry-lethality": 0.0600,
                    "infantry-health": 0.0600,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vengeful Task",
                            "description": "Flint Attack +8% until end of battle once Incinerator has been triggered",
                            "level_percentage": 0.08
                        }
                    }
                },
                {
                    "level": 2,
                    "power": 61200,
                    "attack": 93,
                    "defense": 122,
                    "health": 1836,
                    "infantry-lethality": 0.1200,
                    "infantry-health": 0.1200,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vengeful Task",
                            "description": "Flint Attack +8% until end of battle once Incinerator has been triggered",
                            "level_percentage": 0.08
                        },
                        "expedition": {
                            "skill-name": "Dragonbreath",
                            "description": "Defender Troop Attack +5%",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 3,
                    "power": 86400,
                    "attack": 132,
                    "defense": 172,
                    "health": 2592,
                    "infantry-lethality": 0.1800,
                    "infantry-health": 0.1800,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vengeful Task",
                            "description": "Flint Attack +12% until end of battle once Incinerator has been triggered",
                            "level_percentage": 0.12
                        },
                        "expedition": {
                            "skill-name": "Dragonbreath",
                            "description": "Defender Troop Attack +5%",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 4,
                    "power": 111600,
                    "attack": 170,
                    "defense": 223,
                    "health": 3348,
                    "infantry-lethality": 0.2400,
                    "infantry-health": 0.2400,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vengeful Task",
                            "description": "Flint Attack +12% until end of battle once Incinerator has been triggered",
                            "level_percentage": 0.12
                        },
                        "expedition": {
                            "skill-name": "Dragonbreath",
                            "description": "Defender Troop Attack +7.5%",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 5,
                    "power": 136800,
                    "attack": 210,
                    "defense": 273,
                    "health": 4104,
                    "infantry-lethality": 0.3000,
                    "infantry-health": 0.3000,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vengeful Task",
                            "description": "Flint Attack +16% until end of battle once Incinerator has been triggered",
                            "level_percentage": 0.16
                        },
                        "expedition": {
                            "skill-name": "Dragonbreath",
                            "description": "Defender Troop Attack +7.5%",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 6,
                    "power": 162000,
                    "attack": 248,
                    "defense": 324,
                    "health": 4860,
                    "infantry-lethality": 0.3600,
                    "infantry-health": 0.3600,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vengeful Task",
                            "description": "Flint Attack +16% until end of battle once Incinerator has been triggered",
                            "level_percentage": 0.16
                        },
                        "expedition": {
                            "skill-name": "Dragonbreath",
                            "description": "Defender Troop Attack +10%",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 7,
                    "power": 187200,
                    "attack": 286,
                    "defense": 374,
                    "health": 5616,
                    "infantry-lethality": 0.4200,
                    "infantry-health": 0.4200,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vengeful Task",
                            "description": "Flint Attack +20% until end of battle once Incinerator has been triggered",
                            "level_percentage": 0.20
                        },
                        "expedition": {
                            "skill-name": "Dragonbreath",
                            "description": "Defender Troop Attack +10%",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 8,
                    "power": 212400,
                    "attack": 325,
                    "defense": 424,
                    "health": 6372,
                    "infantry-lethality": 0.4800,
                    "infantry-health": 0.4800,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vengeful Task",
                            "description": "Flint Attack +20% until end of battle once Incinerator has been triggered",
                            "level_percentage": 0.20
                        },
                        "expedition": {
                            "skill-name": "Dragonbreath",
                            "description": "Defender Troop Attack +12.5%",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 9,
                    "power": 237600,
                    "attack": 363,
                    "defense": 475,
                    "health": 7128,
                    "infantry-lethality": 0.5400,
                    "infantry-health": 0.5400,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vengeful Task",
                            "description": "Flint Attack +24% until end of battle once Incinerator has been triggered",
                            "level_percentage": 0.24
                        },
                        "expedition": {
                            "skill-name": "Dragonbreath",
                            "description": "Defender Troop Attack +12.5%",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 10,
                    "power": 270000,
                    "attack": 414,
                    "defense": 540,
                    "health": 8100,
                    "infantry-lethality": 0.6000,
                    "infantry-health": 0.6000,
                    "skills": {
                        "exploration": {
                            "skill-name": "Vengeful Task",
                            "description": "Flint Attack +24% until end of battle once Incinerator has been triggered",
                            "level_percentage": 0.24
                        },
                        "expedition": {
                            "skill-name": "Dragonbreath",
                            "description": "Defender Troop Attack +15%",
                            "level_percentage": 0.15
                        }
                    }
                }
            ]
        }
    }
]

HERO = flint_hero
