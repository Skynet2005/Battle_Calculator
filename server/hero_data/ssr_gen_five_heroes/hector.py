hector_hero = [
    {
        "hero-name": "Hector",
        "hero-class": "infantry",
        "rarity": "SSR",
        "generation": 5,
        "base-stats": {
            "attack": 3780,
            "defense": 4928,
            "health": 73926,
            "infantry-attack": 4.4435,
            "infantry-defense": 4.4435
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Sword Whirlwind",
                    "description": "Hector unleashes a whirlwind of swordplay, increasing Attack Speed by [80% / 90% / 100% / 110% / 120%] and becoming immune to Freeze, Stun and other control effect, for 4s.",
                    "level_percentage": {
                        "1": 0.80,
                        "2": 0.90,
                        "3": 1.00,
                        "4": 1.10,
                        "5": 1.20
                    }
                },
                "2": {
                    "skill-name": "Desperado",
                    "description": "Hector thrives with danger, reducing Damage Taken by [20% / 30% / 40% / 50% / 60%] under 50% health.",
                    "level_percentage": {
                        "1": 0.20,
                        "2": 0.30,
                        "3": 0.40,
                        "4": 0.50,
                        "5": 0.60
                    }
                },
                "3": {
                    "skill-name": "Adrenaline Surge",
                    "description": "Mortal peril is a powerful elixir to Hector's battle-hardened will. Hector gains + [16% / 24% / 32% / 40% / 48%] Attack under 50% Health.",
                    "level_percentage": {
                        "1": 0.16,
                        "2": 0.24,
                        "3": 0.32,
                        "4": 0.40,
                        "5": 0.48
                    }
                }
            },
            "expedition": {
                "1": {
                    "skill-name": "Survival Instincts",
                    "description": "A seasoned warrior with an uncanny knack for reading the battlefield, Hector's presence has a 40% chance of reducing damage taken by [10% / 20% / 30% / 40% / 50%] for all troops.",
                    "level_percentage": {
                        "1": 0.10,
                        "2": 0.20,
                        "3": 0.30,
                        "4": 0.40,
                        "5": 0.50
                    }
                },
                "2": {
                    "skill-name": "Rampant",
                    "description": "Hector excels at raiding on fortified positions with well-coordinated Marksmen, increasing his Infantry's damage dealt by [100% / 125% / 150% / 175% / 200%] and Marksmen's damage dealt by [10% / 20% / 30% / 40% / 50%]. The effect decreases by 80% with each attack and is removed after the fifth.",
                    "level_percentage": {
                        "1": {"infantry": 1.00, "marksmen": 0.10},
                        "2": {"infantry": 1.25, "marksmen": 0.20},
                        "3": {"infantry": 1.50, "marksmen": 0.30},
                        "4": {"infantry": 1.75, "marksmen": 0.40},
                        "5": {"infantry": 2.00, "marksmen": 0.50}
                    }
                },
                "3": {
                    "skill-name": "Blitz",
                    "description": "Hector has mastered the offensive strategy, granting all troops' attack a 25% chance of dealing [120% / 140% / 160% / 180% / 200%] damage.",
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
            "name": "Steel Fangs",
            "levels": [
                {
                    "level": 1,
                    "power": 66600,
                    "attack": 102,
                    "defense": 133,
                    "health": 1998,
                    "infantry-lethality": 0.1110,
                    "infantry-health": 0.1110,
                    "skills": {
                        "exploration": {
                            "skill-name": "Reaper's Embrace",
                            "description": "The heat of battle reforges a warrior's spirit, extending Hector's Sword Whirlwind by 1.5s and restores Hector's health by 7% of damage dealt.",
                            "level_percentage": 0.07
                        }
                    }
                },
                {
                    "level": 2,
                    "power": 113220,
                    "attack": 173,
                    "defense": 226,
                    "health": 3396,
                    "infantry-lethality": 0.2220,
                    "infantry-health": 0.2220,
                    "skills": {
                        "exploration": {
                            "skill-name": "Reaper's Embrace",
                            "description": "The heat of battle reforges a warrior's spirit, extending Hector's Sword Whirlwind by 1.5s and restores Hector's health by 7% of damage dealt.",
                            "level_percentage": 0.07
                        },
                        "expedition": {
                            "skill-name": "Goliath",
                            "description": "Hector excels at using terrain against attackers, increasing Defender Troops Attack by 5%.",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 3,
                    "power": 159840,
                    "attack": 244,
                    "defense": 319,
                    "health": 4795,
                    "infantry-lethality": 0.3330,
                    "infantry-health": 0.3330,
                    "skills": {
                        "exploration": {
                            "skill-name": "Reaper's Embrace",
                            "description": "The heat of battle reforges a warrior's spirit, extending Hector's Sword Whirlwind by 1.5s and restores Hector's health by 9% of damage dealt.",
                            "level_percentage": 0.09
                        },
                        "expedition": {
                            "skill-name": "Goliath",
                            "description": "Hector excels at using terrain against attackers, increasing Defender Troops Attack by 5%.",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 4,
                    "power": 206460,
                    "attack": 315,
                    "defense": 412,
                    "health": 6193,
                    "infantry-lethality": 0.4440,
                    "infantry-health": 0.4440,
                    "skills": {
                        "exploration": {
                            "skill-name": "Reaper's Embrace",
                            "description": "The heat of battle reforges a warrior's spirit, extending Hector's Sword Whirlwind by 1.5s and restores Hector's health by 9% of damage dealt.",
                            "level_percentage": 0.09
                        },
                        "expedition": {
                            "skill-name": "Goliath",
                            "description": "Hector excels at using terrain against attackers, increasing Defender Troops Attack by 7.5%.",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 5,
                    "power": 253080,
                    "attack": 388,
                    "defense": 506,
                    "health": 7592,
                    "infantry-lethality": 0.5550,
                    "infantry-health": 0.5550,
                    "skills": {
                        "exploration": {
                            "skill-name": "Reaper's Embrace",
                            "description": "The heat of battle reforges a warrior's spirit, extending Hector's Sword Whirlwind by 1.5s and restores Hector's health by 11% of damage dealt.",
                            "level_percentage": 0.11
                        },
                        "expedition": {
                            "skill-name": "Goliath",
                            "description": "Hector excels at using terrain against attackers, increasing Defender Troops Attack by 7.5%.",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 6,
                    "power": 299700,
                    "attack": 459,
                    "defense": 599,
                    "health": 8991,
                    "infantry-lethality": 0.6660,
                    "infantry-health": 0.6660,
                    "skills": {
                        "exploration": {
                            "skill-name": "Reaper's Embrace",
                            "description": "The heat of battle reforges a warrior's spirit, extending Hector's Sword Whirlwind by 1.5s and restores Hector's health by 11% of damage dealt.",
                            "level_percentage": 0.11
                        },
                        "expedition": {
                            "skill-name": "Goliath",
                            "description": "Hector excels at using terrain against attackers, increasing Defender Troops Attack by 10%.",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 7,
                    "power": 346320,
                    "attack": 530,
                    "defense": 692,
                    "health": 10389,
                    "infantry-lethality": 0.7770,
                    "infantry-health": 0.7770,
                    "skills": {
                        "exploration": {
                            "skill-name": "Reaper's Embrace",
                            "description": "The heat of battle reforges a warrior's spirit, extending Hector's Sword Whirlwind by 1.5s and restores Hector's health by 13% of damage dealt.",
                            "level_percentage": 0.13
                        },
                        "expedition": {
                            "skill-name": "Goliath",
                            "description": "Hector excels at using terrain against attackers, increasing Defender Troops Attack by 10%.",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 8,
                    "power": 392940,
                    "attack": 601,
                    "defense": 785,
                    "health": 11788,
                    "infantry-lethality": 0.8880,
                    "infantry-health": 0.8880,
                    "skills": {
                        "exploration": {
                            "skill-name": "Reaper's Embrace",
                            "description": "The heat of battle reforges a warrior's spirit, extending Hector's Sword Whirlwind by 1.5s and restores Hector's health by 13% of damage dealt.",
                            "level_percentage": 0.13
                        },
                        "expedition": {
                            "skill-name": "Goliath",
                            "description": "Hector excels at using terrain against attackers, increasing Defender Troops Attack by 12.5%.",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 9,
                    "power": 439560,
                    "attack": 672,
                    "defense": 879,
                    "health": 13186,
                    "infantry-lethality": 0.9990,
                    "infantry-health": 0.9990,
                    "skills": {
                        "exploration": {
                            "skill-name": "Reaper's Embrace",
                            "description": "The heat of battle reforges a warrior's spirit, extending Hector's Sword Whirlwind by 1.5s and restores Hector's health by 15% of damage dealt.",
                            "level_percentage": 0.15
                        },
                        "expedition": {
                            "skill-name": "Goliath",
                            "description": "Hector excels at using terrain against attackers, increasing Defender Troops Attack by 12.5%.",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 10,
                    "power": 499500,
                    "attack": 765,
                    "defense": 999,
                    "health": 14985,
                    "infantry-lethality": 1.1100,
                    "infantry-health": 1.1100,
                    "skills": {
                        "exploration": {
                            "skill-name": "Reaper's Embrace",
                            "description": "The heat of battle reforges a warrior's spirit, extending Hector's Sword Whirlwind by 1.5s and restores Hector's health by 15% of damage dealt.",
                            "level_percentage": 0.15
                        },
                        "expedition": {
                            "skill-name": "Goliath",
                            "description": "Hector excels at using terrain against attackers, increasing Defender Troops Attack by 15%.",
                            "level_percentage": 0.15
                        }
                    }
                }
            ]
        }
    }
]

HERO = hector_hero
