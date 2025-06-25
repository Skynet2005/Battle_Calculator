wayne_hero = [
    {
        "hero-name": "Wayne",
        "hero-class": "marksman",
        "rarity": "SSR",
        "generation": 6,
        "base-stats": {
            "attack": 7200,
            "defense": 5926,
            "health": 44454,
            "marksman-attack": 5.4043,
            "marksman-defense": 5.4043
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Hurricane Blowback",
                    "description": "Wayne throws a boomerang, dealing Attack * [100% / 110% / 120% / 130% / 140%] area of effect damage to enemies in a straight line. On its return, it deals the same amount of damage to enemies in its path.",
                    "level_percentage": {
                        "1": 1.00,
                        "2": 1.10,
                        "3": 1.20,
                        "4": 1.30,
                        "5": 1.40
                    }
                },
                "2": {
                    "skill-name": "Phantom Blitz",
                    "description": "Wayne draws and fires in the blink of an eye. Each normal attack has a [15% / 20% / 25% / 30% / 35%] chance of triggering another normal attack.",
                    "level_percentage": {
                        "1": 0.15,
                        "2": 0.20,
                        "3": 0.25,
                        "4": 0.30,
                        "5": 0.35
                    }
                },
                "3": {
                    "skill-name": "Noon Time!",
                    "description": "Wayne's impeccable aim grants a [3% / 6%/ 9% / 12% / 15%] Crit Rate on dealing damage.",
                    "level_percentage": {
                        "1": 0.03,
                        "2": 0.06,
                        "3": 0.09,
                        "4": 0.12,
                        "5": 0.15
                    }
                }
            },
            "expedition": {
                "1": {
                    "skill-name": "Thunder Strike",
                    "description": "Wayne's brilliant battle planning allows all troops to launch an extra attack every 4 turns, dealing [20% / 40% / 60% / 80% / 100%] damage.",
                    "level_percentage": {
                        "1": 0.20,
                        "2": 0.40,
                        "3": 0.60,
                        "4": 0.80,
                        "5": 1.00
                    }
                },
                "2": {
                    "skill-name": "Roundabout Hit",
                    "description": "Wayne's stratagems can pierce the thickest of defenses. On every other attack, his Marksmen deal [8% / 16%/ 24% / 32% / 40%] extra damage to enemy Lancers and [4% / 8% / 12% / 16% / 20%] extra damage to enemy Marksmen.",
                    "level_percentage": {
                        "1": {"lancers": 0.08, "marksmen": 0.04},
                        "2": {"lancers": 0.16, "marksmen": 0.08},
                        "3": {"lancers": 0.24, "marksmen": 0.12},
                        "4": {"lancers": 0.32, "marksmen": 0.16},
                        "5": {"lancers": 0.40, "marksmen": 0.20}
                    }
                },
                "3": {
                    "skill-name": "Fleet",
                    "description": "Wayne ensures no misstep goes unpunished with an eagle's eye for weakness, granting all troops' attacks a [5% / 10% / 15% / 20% / 25%] Crit Rate.",
                    "level_percentage": {
                        "1": 0.05,
                        "2": 0.10,
                        "3": 0.15,
                        "4": 0.20,
                        "5": 0.25
                    }
                }
            }
        },
        "exclusive-weapon": {
            "name": "Power Boomerang",
            "levels": [
                {
                    "level": 1,
                    "power": 80100,
                    "attack": 192,
                    "defense": 160,
                    "health": 1201,
                    "marksman-lethality": 0.1335,
                    "marksman-health": 0.1335,
                    "skills": {
                        "exploration": {
                            "skill-name": "Gunslinger",
                            "description": "Wayne unleashes a rapid five-shot barrage, dealing Attack * 40% damage to a random enemy. If the target is an Escort, there is a 40% chance of knockdown.",
                            "level_percentage": 0.40,
                            "knockdown_chance": 0.40
                        }
                    }
                },
                {
                    "level": 2,
                    "power": 136170,
                    "attack": 328,
                    "defense": 272,
                    "health": 2042,
                    "marksman-lethality": 0.2670,
                    "marksman-health": 0.2670,
                    "skills": {
                        "exploration": {
                            "skill-name": "Gunslinger",
                            "description": "Wayne unleashes a rapid five-shot barrage, dealing Attack * 40% damage to a random enemy. If the target is an Escort, there is a 40% chance of knockdown.",
                            "level_percentage": 0.40,
                            "knockdown_chance": 0.40
                        },
                        "expedition": {
                            "skill-name": "Offensive Defense",
                            "description": "Wayne's strategic brilliance increases Defender Troops' Lethality by 5%.",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 3,
                    "power": 192240,
                    "attack": 464,
                    "defense": 384,
                    "health": 2883,
                    "marksman-lethality": 0.4005,
                    "marksman-health": 0.4005,
                    "skills": {
                        "exploration": {
                            "skill-name": "Gunslinger",
                            "description": "Wayne unleashes a rapid five-shot barrage, dealing Attack * 44% damage to a random enemy. If the target is an Escort, there is a 55% chance of knockdown.",
                            "level_percentage": 0.44,
                            "knockdown_chance": 0.55
                        },
                        "expedition": {
                            "skill-name": "Offensive Defense",
                            "description": "Wayne's strategic brilliance increases Defender Troops' Lethality by 5%.",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 4,
                    "power": 248310,
                    "attack": 603,
                    "defense": 496,
                    "health": 3724,
                    "marksman-lethality": 0.5340,
                    "marksman-health": 0.5340,
                    "skills": {
                        "exploration": {
                            "skill-name": "Gunslinger",
                            "description": "Wayne unleashes a rapid five-shot barrage, dealing Attack * 44% damage to a random enemy. If the target is an Escort, there is a 55% chance of knockdown.",
                            "level_percentage": 0.44,
                            "knockdown_chance": 0.55
                        },
                        "expedition": {
                            "skill-name": "Offensive Defense",
                            "description": "Wayne's strategic brilliance increases Defender Troops' Lethality by 7.5%.",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 5,
                    "power": 304380,
                    "attack": 739,
                    "defense": 608,
                    "health": 4565,
                    "marksman-lethality": 0.6675,
                    "marksman-health": 0.6675,
                    "skills": {
                        "exploration": {
                            "skill-name": "Gunslinger",
                            "description": "Wayne unleashes a rapid five-shot barrage, dealing Attack * 48% damage to a random enemy. If the target is an Escort, there is a 55% chance of knockdown.",
                            "level_percentage": 0.48,
                            "knockdown_chance": 0.55
                        },
                        "expedition": {
                            "skill-name": "Offensive Defense",
                            "description": "Wayne's strategic brilliance increases Defender Troops' Lethality by 7.5%.",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 6,
                    "power": 360450,
                    "attack": 875,
                    "defense": 720,
                    "health": 5406,
                    "marksman-lethality": 0.8010,
                    "marksman-health": 0.8010,
                    "skills": {
                        "exploration": {
                            "skill-name": "Gunslinger",
                            "description": "Wayne unleashes a rapid five-shot barrage, dealing Attack * 48% damage to a random enemy. If the target is an Escort, there is a 55% chance of knockdown.",
                            "level_percentage": 0.48,
                            "knockdown_chance": 0.55
                        },
                        "expedition": {
                            "skill-name": "Offensive Defense",
                            "description": "Wayne's strategic brilliance increases Defender Troops' Lethality by 10%.",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 7,
                    "power": 416520,
                    "attack": 1011,
                    "defense": 833,
                    "health": 6247,
                    "marksman-lethality": 0.9345,
                    "marksman-health": 0.9345,
                    "skills": {
                        "exploration": {
                            "skill-name": "Gunslinger",
                            "description": "Wayne unleashes a rapid five-shot barrage, dealing Attack * 52% damage to a random enemy. If the target is an Escort, there is a 85% chance of knockdown.",
                            "level_percentage": 0.52,
                            "knockdown_chance": 0.85
                        },
                        "expedition": {
                            "skill-name": "Offensive Defense",
                            "description": "Wayne's strategic brilliance increases Defender Troops' Lethality by 10%.",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 8,
                    "power": 472590,
                    "attack": 1148,
                    "defense": 945,
                    "health": 7088,
                    "marksman-lethality": 0.10680,
                    "marksman-health": 0.10680,
                    "skills": {
                        "exploration": {
                            "skill-name": "Gunslinger",
                            "description": "Wayne unleashes a rapid five-shot barrage, dealing Attack * 52% damage to a random enemy. If the target is an Escort, there is a 85% chance of knockdown.",
                            "level_percentage": 0.52,
                            "knockdown_chance": 0.85
                        },
                        "expedition": {
                            "skill-name": "Offensive Defense",
                            "description": "Wayne's strategic brilliance increases Defender Troops' Lethality by 12.5%.",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 9,
                    "power": 528660,
                    "attack": 1285,
                    "defense": 1057,
                    "health": 7929,
                    "marksman-lethality": 0.12015,
                    "marksman-health": 0.12015,
                    "skills": {
                        "exploration": {
                            "skill-name": "Gunslinger",
                            "description": "Wayne unleashes a rapid five-shot barrage, dealing Attack * 56% damage to a random enemy. If the target is an Escort, there is a 100% chance of knockdown.",
                            "level_percentage": 0.56,
                            "knockdown_chance": 1.00
                        },
                        "expedition": {
                            "skill-name": "Offensive Defense",
                            "description": "Wayne's strategic brilliance increases Defender Troops' Lethality by 12.5%.",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 10,
                    "power": 600750,
                    "attack": 1457,
                    "defense": 1201,
                    "health": 9011,
                    "marksman-lethality": 0.13350,
                    "marksman-health": 0.13350,
                    "skills": {
                        "exploration": {
                            "skill-name": "Gunslinger",
                            "description": "Wayne unleashes a rapid five-shot barrage, dealing Attack * 56% damage to a random enemy. If the target is an Escort, there is a 100% chance of knockdown.",
                            "level_percentage": 0.56,
                            "knockdown_chance": 1.00
                        },
                        "expedition": {
                            "skill-name": "Offensive Defense",
                            "description": "Wayne's strategic brilliance increases Defender Troops' Lethality by 15%.",
                            "level_percentage": 0.15
                        }
                    }
                }
            ]
        }
    }
]

HERO = wayne_hero
