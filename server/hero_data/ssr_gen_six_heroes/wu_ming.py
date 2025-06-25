wu_ming_hero = [
    {
        "hero-name": "Wu Ming",
        "hero-class": "infantry",
        "rarity": "SSR",
        "generation": 6,
        "base-stats": {
            "attack": 4546,
            "defense": 5926,
            "health": 88910,
            "infantry-attack": 5.4043,
            "infantry-defense": 5.4043
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Cyclone Barrier",
                    "description": "Wu Ming twirls his staff at blinding speed and forms an unyielding barrier, dealing Attack * [100% / 110% / 120% / 130% / 140%] Area of Effect damage, gaining invulnerability for 2s.",
                    "level_percentage": {
                        "1": 1.00,
                        "2": 1.10,
                        "3": 1.20,
                        "4": 1.30,
                        "5": 1.40
                    }
                },
                "2": {
                    "skill-name": "Inner Clarity",
                    "description": "Wu Ming finds unparalleled clarity by silencing the chaos within, increasing Attack by [8% / 12% / 16% / 20% / 24%] and Defense by [16% / 24% / 32% / 40% / 48%] for 4s.",
                    "level_percentage_attack": {
                        "1": 0.08,
                        "2": 0.12,
                        "3": 0.16,
                        "4": 0.20,
                        "5": 0.24
                    },
                    "level_percentage_defense": {
                        "1": 0.16,
                        "2": 0.24,
                        "3": 0.32,
                        "4": 0.40,
                        "5": 0.48
                    }
                },
                "3": {
                    "skill-name": "Remote Impact",
                    "description": "Wu Ming hones his martial arts to perfection, dealing Attack * [20% / 22% / 24% / 26% / 28%] damage to a random enemy with every normal attack.",
                    "level_percentage": {
                        "1": 0.20,
                        "2": 0.22,
                        "3": 0.24,
                        "4": 0.26,
                        "5": 0.28
                    }
                }
            },
            "expedition": {
                "1": {
                    "skill-name": "Shadow's Evasion",
                    "description": "Wu Ming moves like a shadow, dodging and countering enemies, reducing his Infantry's damage taken from normal attacks by [5% / 10% / 15% / 20% / 25%] and from skills by [6% / 12% / 18% / 24% / 30%].",
                    "level_percentage_normal": {
                        "1": 0.05,
                        "2": 0.10,
                        "3": 0.15,
                        "4": 0.20,
                        "5": 0.25
                    },
                    "level_percentage_skill": {
                        "1": 0.06,
                        "2": 0.12,
                        "3": 0.18,
                        "4": 0.24,
                        "5": 0.30
                    }
                },
                "2": {
                    "skill-name": "Crescent Uplift",
                    "description": "Wu Ming spreads his wisdom and techniques, increasing damage dealt by [4% / 8% / 12% / 16% / 20%] for all troops.",
                    "level_percentage": {
                        "1": 0.04,
                        "2": 0.08,
                        "3": 0.12,
                        "4": 0.16,
                        "5": 0.20
                    }
                },
                "3": {
                    "skill-name": "Elemental Resonance",
                    "description": "Wu Ming leads everyone to heightened affinity with their combat techniques, increasing skill damage dealt by [5% / 10% / 15% / 20% / 25%] for all trooops.",
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
            "name": "Dragonslayer",
            "levels": [
                {
                    "level": 1,
                    "power": 80100,
                    "attack": 122,
                    "defense": 160,
                    "health": 2403,
                    "infantry-lethality": 0.1335,
                    "infantry-health": 0.1335,
                    "skills": {
                        "exploration": {
                            "skill-name": "Martial Zenith",
                            "description": "Wu Ming stands transcendent in the realm of martial arts, increasing damage dealt by 10%.",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 2,
                    "power": 136170,
                    "attack": 208,
                    "defense": 272,
                    "health": 4085,
                    "infantry-lethality": 0.2670,
                    "infantry-health": 0.2670,
                    "skills": {
                        "exploration": {
                            "skill-name": "Martial Zenith",
                            "description": "Wu Ming stands transcendent in the realm of martial arts, increasing damage dealt by 10%.",
                            "level_percentage": 0.10
                        },
                        "expedition": {
                            "skill-name": "Steel Discipline",
                            "description": "Wu Ming puts defender troops under stern tutelage, increasing Defender Troops' Defense by 5%.",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 3,
                    "power": 192240,
                    "attack": 293,
                    "defense": 384,
                    "health": 5767,
                    "infantry-lethality": 0.4005,
                    "infantry-health": 0.4005,
                    "skills": {
                        "exploration": {
                            "skill-name": "Martial Zenith",
                            "description": "Wu Ming stands transcendent in the realm of martial arts, increasing damage dealt by 15%.",
                            "level_percentage": 0.15
                        },
                        "expedition": {
                            "skill-name": "Steel Discipline",
                            "description": "Wu Ming puts defender troops under stern tutelage, increasing Defender Troops' Defense by 5%.",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 4,
                    "power": 248310,
                    "attack": 379,
                    "defense": 496,
                    "health": 7449,
                    "infantry-lethality": 0.5340,
                    "infantry-health": 0.5340,
                    "skills": {
                        "exploration": {
                            "skill-name": "Martial Zenith",
                            "description": "Wu Ming stands transcendent in the realm of martial arts, increasing damage dealt by 15%.",
                            "level_percentage": 0.15
                        },
                        "expedition": {
                            "skill-name": "Steel Discipline",
                            "description": "Wu Ming puts defender troops under stern tutelage, increasing Defender Troops' Defense by 7.5%.",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 5,
                    "power": 304380,
                    "attack": 467,
                    "defense": 608,
                    "health": 9131,
                    "infantry-lethality": 0.6675,
                    "infantry-health": 0.6675,
                    "skills": {
                        "exploration": {
                            "skill-name": "Martial Zenith",
                            "description": "Wu Ming stands transcendent in the realm of martial arts, increasing damage dealt by 20%.",
                            "level_percentage": 0.20
                        },
                        "expedition": {
                            "skill-name": "Steel Discipline",
                            "description": "Wu Ming puts defender troops under stern tutelage, increasing Defender Troops' Defense by 7.5%.",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 6,
                    "power": 360450,
                    "attack": 552,
                    "defense": 720,
                    "health": 10813,
                    "infantry-lethality": 0.8010,
                    "infantry-health": 0.8010,
                    "skills": {
                        "exploration": {
                            "skill-name": "Martial Zenith",
                            "description": "Wu Ming stands transcendent in the realm of martial arts, increasing damage dealt by 20%.",
                            "level_percentage": 0.20
                        },
                        "expedition": {
                            "skill-name": "Steel Discipline",
                            "description": "Wu Ming puts defender troops under stern tutelage, increasing Defender Troops' Defense by 10%.",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 7,
                    "power": 416520,
                    "attack": 638,
                    "defense": 833,
                    "health": 12495,
                    "infantry-lethality": 0.9345,
                    "infantry-health": 0.9345,
                    "skills": {
                        "exploration": {
                            "skill-name": "Martial Zenith",
                            "description": "Wu Ming stands transcendent in the realm of martial arts, increasing damage dealt by 25%.",
                            "level_percentage": 0.25
                        },
                        "expedition": {
                            "skill-name": "Steel Discipline",
                            "description": "Wu Ming puts defender troops under stern tutelage, increasing Defender Troops' Defense by 10%.",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 8,
                    "power": 472590,
                    "attack": 723,
                    "defense": 945,
                    "health": 14177,
                    "infantry-lethality": 0.10680,
                    "infantry-health": 0.10680,
                    "skills": {
                        "exploration": {
                            "skill-name": "Martial Zenith",
                            "description": "Wu Ming stands transcendent in the realm of martial arts, increasing damage dealt by 25%.",
                            "level_percentage": 0.25
                        },
                        "expedition": {
                            "skill-name": "Steel Discipline",
                            "description": "Wu Ming puts defender troops under stern tutelage, increasing Defender Troops' Defense by 12.5%.",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 9,
                    "power": 528660,
                    "attack": 809,
                    "defense": 1057,
                    "health": 15859,
                    "infantry-lethality": 0.12015,
                    "infantry-health": 0.12015,
                    "skills": {
                        "exploration": {
                            "skill-name": "Martial Zenith",
                            "description": "Wu Ming stands transcendent in the realm of martial arts, increasing damage dealt by 30%.",
                            "level_percentage": 0.30
                        },
                        "expedition": {
                            "skill-name": "Steel Discipline",
                            "description": "Wu Ming puts defender troops under stern tutelage, increasing Defender Troops' Defense by 12.5%.",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 10,
                    "power": 600750,
                    "attack": 921,
                    "defense": 1201,
                    "health": 18022,
                    "infantry-lethality": 0.13350,
                    "infantry-health": 0.13350,
                    "skills": {
                        "exploration": {
                            "skill-name": "Martial Zenith",
                            "description": "Wu Ming stands transcendent in the realm of martial arts, increasing damage dealt by 30%.",
                            "level_percentage": 0.30
                        },
                        "expedition": {
                            "skill-name": "Steel Discipline",
                            "description": "Wu Ming puts defender troops under stern tutelage, increasing Defender Troops' Defense by 15%.",
                            "level_percentage": 0.15
                        }
                    }
                }
            ]
        }
    }
]

HERO = wu_ming_hero
