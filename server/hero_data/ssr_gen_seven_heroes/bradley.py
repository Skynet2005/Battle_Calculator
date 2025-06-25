bradley_hero = [
    {
        "hero-name": "Bradley",
        "hero-class": "marksman",
        "rarity": "SSR",
        "generation": 7,
        "base-stats": {
            "attack": 8656,
            "defense": 7126,
            "health": 53446,
            "marksman-attack": 6.5052,
            "marksman-defense": 6.5052
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Destructor",
                    "description": "Bradley primes his artillery with an extremely potent shell, dealing Attack * [300% / 330% / 360% / 390% / 420%] Area of Effect Damage.",
                    "level_percentage": {
                        "1": 3.00,
                        "2": 3.30,
                        "3": 3.60,
                        "4": 3.90,
                        "5": 4.20
                    }
                },
                "2": {
                    "skill-name": "Incendiary Shell",
                    "description": "Bradley fires a special incendiary shell, dealing Attack * [60% / 66% / 72% / 78% / 84%] Area of Effect Damage. The flaming crater in its wake also deals Attack * [15% / 16.5% / 18% / 19.5% / 21%] damage to enemies every 0.5s for 2s.",
                    "level_percentage": {
                        "1": 0.60,
                        "2": 0.66,
                        "3": 0.72,
                        "4": 0.78,
                        "5": 0.84
                    },
                    "dot_percentage": {
                        "1": 0.15,
                        "2": 0.165,
                        "3": 0.18,
                        "4": 0.195,
                        "5": 0.21
                    }
                },
                "3": {
                    "skill-name": "Audacious",
                    "description": "The prospect of death only energizes a seasoned warrior like Bradley, increasing his Attack by [8% / 12% / 16% / 20% / 24%].",
                    "level_percentage": {
                        "1": 0.08,
                        "2": 0.12,
                        "3": 0.16,
                        "4": 0.20,
                        "5": 0.24
                    }
                }
            },
            "expedition": {
                "1": {
                    "skill-name": "Veteran's Might",
                    "description": "Bradley's years of combat experience enables him to destroy enemies efficiently, increasing Attack by [5% / 10% / 15% / 20% / 25%] for all troops.",
                    "level_percentage": {
                        "1": 0.05,
                        "2": 0.10,
                        "3": 0.15,
                        "4": 0.20,
                        "5": 0.25
                    }
                },
                "2": {
                    "skill-name": "Power Shot",
                    "description": "Bradley uses his expertise in suppressive artillery against the enemy vanguard, increasing Damage Dealt to Lancers by [6% / 12% / 18% / 24% / 30%], and to Infantry by [5% / 10% / 15% / 20% / 25%] for all troops.",
                    "lancer_damage_percentage": {
                        "1": 0.06,
                        "2": 0.12,
                        "3": 0.18,
                        "4": 0.24,
                        "5": 0.30
                    },
                    "infantry_damage_percentage": {
                        "1": 0.05,
                        "2": 0.10,
                        "3": 0.15,
                        "4": 0.20,
                        "5": 0.25
                    }
                },
                "3": {
                    "skill-name": "Tactical Assistance",
                    "description": "Bradley will press every advantage against a beleaguered enemy, increasing Damage Dealt by [6% / 12% / 18% / 24% / 30%] for all troops for 2 turns every 4 turns.",
                    "level_percentage": {
                        "1": 0.06,
                        "2": 0.12,
                        "3": 0.18,
                        "4": 0.24,
                        "5": 0.30
                    }
                }
            }
        },
        "exclusive-weapon": {
            "name": "Thunder Cannon",
            "levels": [
                {
                    "level": 1,
                    "power": 96300,
                    "attack": 288,
                    "defense": 192,
                    "health": 2167,
                    "marksman-lethality": 0.1605,
                    "marksman-health": 0.1605,
                    "skills": {
                        "exploration": {
                            "skill-name": "Onslaught",
                            "description": "Shock and awe tactics can also boost morale. The 'Destructor' further increases Attack Speeds by 6% for Heroes and Escorts for 5s.",
                            "attack_speed_increase": 0.06
                        }
                    }
                },
                {
                    "level": 2,
                    "power": 163710,
                    "attack": 480,
                    "defense": 327,
                    "health": 3611,
                    "marksman-lethality": 0.3210,
                    "marksman-health": 0.3210,
                    "skills": {
                        "exploration": {
                            "skill-name": "Onslaught",
                            "description": "Shock and awe tactics can also boost morale. The 'Destructor' further increases Attack Speeds by 6% for Heroes and Escorts for 5s.",
                            "attack_speed_increase": 0.06
                        },
                        "expedition": {
                            "skill-name": "Siege Insight",
                            "description": "Bradley knows exactly where to place defenses as a siege expert, increasing Defender Troops' Attack by 5%.",
                            "defender_attack_increase": 0.05
                        }
                    }
                },
                {
                    "level": 3,
                    "power": 231120,
                    "attack": 673,
                    "defense": 462,
                    "health": 5056,
                    "marksman-lethality": 0.4815,
                    "marksman-health": 0.4815,
                    "skills": {
                        "exploration": {
                            "skill-name": "Onslaught",
                            "description": "Shock and awe tactics can also boost morale. The 'Destructor' further increases Attack Speeds by 8% for Heroes and Escorts for 5s.",
                            "attack_speed_increase": 0.08
                        },
                        "expedition": {
                            "skill-name": "Siege Insight",
                            "description": "Bradley knows exactly where to place defenses as a siege expert, increasing Defender Troops' Attack by 5%.",
                            "defender_attack_increase": 0.05
                        }
                    }
                },
                {
                    "level": 4,
                    "power": 298530,
                    "attack": 865,
                    "defense": 597,
                    "health": 6500,
                    "marksman-lethality": 0.6420,
                    "marksman-health": 0.6420,
                    "skills": {
                        "exploration": {
                            "skill-name": "Onslaught",
                            "description": "Shock and awe tactics can also boost morale. The 'Destructor' further increases Attack Speeds by 8% for Heroes and Escorts for 5s.",
                            "attack_speed_increase": 0.08
                        },
                        "expedition": {
                            "skill-name": "Siege Insight",
                            "description": "Bradley knows exactly where to place defenses as a siege expert, increasing Defender Troops' Attack by 7.5%.",
                            "defender_attack_increase": 0.075
                        }
                    }
                },
                {
                    "level": 5,
                    "power": 365940,
                    "attack": 1057,
                    "defense": 731,
                    "health": 7945,
                    "marksman-lethality": 0.8025,
                    "marksman-health": 0.8025,
                    "skills": {
                        "exploration": {
                            "skill-name": "Onslaught",
                            "description": "Shock and awe tactics can also boost morale. The 'Destructor' further increases Attack Speeds by 10% for Heroes and Escorts for 5s.",
                            "attack_speed_increase": 0.10
                        },
                        "expedition": {
                            "skill-name": "Siege Insight",
                            "description": "Bradley knows exactly where to place defenses as a siege expert, increasing Defender Troops' Attack by 7.5%.",
                            "defender_attack_increase": 0.075
                        }
                    }
                },
                {
                    "level": 6,
                    "power": 433350,
                    "attack": 1250,
                    "defense": 866,
                    "health": 9390,
                    "marksman-lethality": 0.9630,
                    "marksman-health": 0.9630,
                    "skills": {
                        "exploration": {
                            "skill-name": "Onslaught",
                            "description": "Shock and awe tactics can also boost morale. The 'Destructor' further increases Attack Speeds by 10% for Heroes and Escorts for 5s.",
                            "attack_speed_increase": 0.10
                        },
                        "expedition": {
                            "skill-name": "Siege Insight",
                            "description": "Bradley knows exactly where to place defenses as a siege expert, increasing Defender Troops' Attack by 10%.",
                            "defender_attack_increase": 0.10
                        }
                    }
                },
                {
                    "level": 7,
                    "power": 500760,
                    "attack": 1442,
                    "defense": 1001,
                    "health": 10834,
                    "marksman-lethality": 0.11235,
                    "marksman-health": 0.11235,
                    "skills": {
                        "exploration": {
                            "skill-name": "Onslaught",
                            "description": "Shock and awe tactics can also boost morale. The 'Destructor' further increases Attack Speeds by 12% for Heroes and Escorts for 5s.",
                            "attack_speed_increase": 0.12
                        },
                        "expedition": {
                            "skill-name": "Siege Insight",
                            "description": "Bradley knows exactly where to place defenses as a siege expert, increasing Defender Troops' Attack by 10%.",
                            "defender_attack_increase": 0.10
                        }
                    }
                },
                {
                    "level": 8,
                    "power": 568170,
                    "attack": 1634,
                    "defense": 1136,
                    "health": 12278,
                    "marksman-lethality": 0.12840,
                    "marksman-health": 0.12840,
                    "skills": {
                        "exploration": {
                            "skill-name": "Onslaught",
                            "description": "Shock and awe tactics can also boost morale. The 'Destructor' further increases Attack Speeds by 12% for Heroes and Escorts for 5s.",
                            "attack_speed_increase": 0.12
                        },
                        "expedition": {
                            "skill-name": "Siege Insight",
                            "description": "Bradley knows exactly where to place defenses as a siege expert, increasing Defender Troops' Attack by 12.5%.",
                            "defender_attack_increase": 0.125
                        }
                    }
                },
                {
                    "level": 9,
                    "power": 635580,
                    "attack": 1827,
                    "defense": 1271,
                    "health": 13723,
                    "marksman-lethality": 0.14445,
                    "marksman-health": 0.14445,
                    "skills": {
                        "exploration": {
                            "skill-name": "Onslaught",
                            "description": "Shock and awe tactics can also boost morale. The 'Destructor' further increases Attack Speeds by 14% for Heroes and Escorts for 5s.",
                            "attack_speed_increase": 0.14
                        },
                        "expedition": {
                            "skill-name": "Siege Insight",
                            "description": "Bradley knows exactly where to place defenses as a siege expert, increasing Defender Troops' Attack by 12.5%.",
                            "defender_attack_increase": 0.125
                        }
                    }
                },
                {
                    "level": 10,
                    "power": 722250,
                    "attack": 1752,
                    "defense": 1444,
                    "health": 10833,
                    "marksman-lethality": 0.16050,
                    "marksman-health": 0.16050,
                    "skills": {
                        "exploration": {
                            "skill-name": "Onslaught",
                            "description": "Shock and awe tactics can also boost morale. The 'Destructor' further increases Attack Speeds by 14% for Heroes and Escorts for 5s.",
                            "attack_speed_increase": 0.14
                        },
                        "expedition": {
                            "skill-name": "Siege Insight",
                            "description": "Bradley knows exactly where to place defenses as a siege expert, increasing Defender Troops' Attack by 15%.",
                            "defender_attack_increase": 0.15
                        }
                    }
                }
            ]
        }
    }
]

HERO = bradley_hero
