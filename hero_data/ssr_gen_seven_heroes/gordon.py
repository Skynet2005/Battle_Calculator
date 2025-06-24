gordon_hero = [
    {
        "hero-name": "Gordon",
        "hero-class": "lancer",
        "rarity": "SSR",
        "generation": 7,
        "base-stats": {
            "attack": 7126,
            "defense": 7126,
            "health": 71262,
            "lancer-attack": 6.5052,
            "lancer-defense": 6.5052
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Poison Blast",
                    "description": "Gordon throws a vase that disintegrates into a toxic mist, dealing Attack * [50% / 55% / 60% / 65% / 70%] damage to nearby enemies every 0.5s for 3s.",
                    "level_percentage": {
                        "1": 0.50,
                        "2": 0.55,
                        "3": 0.60,
                        "4": 0.65,
                        "5": 0.70
                    }
                },
                "2": {
                    "skill-name": "Toxic Molotov",
                    "description": "Gordon hurls a chemical flask with precision and poisons the target, dealing Attack * [25% / 27.5% / 30% / 32.5% / 35%] damage every 0.5s and increasing its Damage Taken by [5% / 10% / 15% / 20% / 25%] for 2s.",
                    "level_percentage": {
                        "1": 0.25,
                        "2": 0.275,
                        "3": 0.30,
                        "4": 0.325,
                        "5": 0.35
                    },
                    "damage_taken_increase": {
                        "1": 0.05,
                        "2": 0.10,
                        "3": 0.15,
                        "4": 0.20,
                        "5": 0.25
                    }
                },
                "3": {
                    "skill-name": "Tolerization",
                    "description": "Gordon's body has adapted to toxic over-exposure by generating new responses, increasing his Defense by [25% / 37.5% / 50% / 62.5% / 75%].",
                    "level_percentage": {
                        "1": 0.25,
                        "2": 0.375,
                        "3": 0.50,
                        "4": 0.625,
                        "5": 0.75
                    }
                }
            },
            "expedition": {
                "1": {
                    "skill-name": "Venom Infusion",
                    "description": "Gordon dips Lancers' weapons in venom. Every 2 attacks, Lancers deal [20% / 40% / 60% / 80% / 100%] extra damage and apply poison to the target for 1 turn. Poisoned enemies deal [4% / 8% / 12% / 16% / 20%] less damage.",
                    "level_percentage": {
                        "1": 0.20,
                        "2": 0.40,
                        "3": 0.60,
                        "4": 0.80,
                        "5": 1.00
                    },
                    "damage_reduction": {
                        "1": 0.04,
                        "2": 0.08,
                        "3": 0.12,
                        "4": 0.16,
                        "5": 0.20
                    }
                },
                "2": {
                    "skill-name": "Chemical Terror",
                    "description": "Gordon's envenomed weapons terrorizes the field, increasing Lancers' Damage Dealt by [30% / 60% / 90% / 120% / 150%] and reducing Damage Dealt by [6% / 12% / 18% / 24% / 30%] for all enemy troops for 1 turn, every 3 turns.",
                    "level_percentage": {
                        "1": 0.30,
                        "2": 0.60,
                        "3": 0.90,
                        "4": 1.20,
                        "5": 1.50
                    },
                    "enemy_damage_reduction": {
                        "1": 0.06,
                        "2": 0.12,
                        "3": 0.18,
                        "4": 0.24,
                        "5": 0.30
                    }
                },
                "3": {
                    "skill-name": "Toxic Release",
                    "description": "Gordon generates a defensive bio-toxic fog, confusing enemy frontline infantry, increasing their Damage Taken by [6% / 12% / 18% / 24% / 30%], while blocking enemy Marksmen's line of sight to reduce their Damage Dealt by [6% / 12% / 18% / 24% / 30%] for 2 turns every 4 turns.",
                    "damage_taken_increase": {
                        "1": 0.06,
                        "2": 0.12,
                        "3": 0.18,
                        "4": 0.24,
                        "5": 0.30
                    },
                    "marksmen_damage_reduction": {
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
            "name": "Bonecrux Venom",
            "levels": [
                {
                    "level": 1,
                    "power": 96300,
                    "attack": 327,
                    "defense": 192,
                    "health": 1926,
                    "lancer-lethality": 0.1605,
                    "lancer-health": 0.1605,
                    "skills": {
                        "exploration": {
                            "skill-name": "Potion #1325",
                            "description": "Gordon's chemical arsenal increases his Damage Dealt by 5% and reduces the Attack of Poisoned targets by 15%.",
                            "damage_dealt_increase": 0.05,
                            "poisoned_attack_reduction": 0.15
                        }
                    }
                },
                {
                    "level": 2,
                    "power": 163710,
                    "attack": 327,
                    "defense": 327,
                    "health": 3224,
                    "lancer-lethality": 0.3210,
                    "lancer-health": 0.3210,
                    "skills": {
                        "exploration": {
                            "skill-name": "Potion #1325",
                            "description": "Gordon's chemical arsenal increases his Damage Dealt by 5% and reduces the Attack of Poisoned targets by 15%.",
                            "damage_dealt_increase": 0.05,
                            "poisoned_attack_reduction": 0.15
                        },
                        "expedition": {
                            "skill-name": "Bio Assault",
                            "description": "Gordon privileges his allies with special envenomed weaponry, increasing Rally Squads' Lethality by 5%.",
                            "rally_lethality_increase": 0.05
                        }
                    }
                },
                {
                    "level": 3,
                    "power": 231120,
                    "attack": 462,
                    "defense": 462,
                    "health": 4622,
                    "lancer-lethality": 0.4815,
                    "lancer-health": 0.4815,
                    "skills": {
                        "exploration": {
                            "skill-name": "Potion #1325",
                            "description": "Gordon's chemical arsenal increases his Damage Dealt by 10% and reduces the Attack of Poisoned targets by 15%.",
                            "damage_dealt_increase": 0.10,
                            "poisoned_attack_reduction": 0.15
                        },
                        "expedition": {
                            "skill-name": "Bio Assault",
                            "description": "Gordon privileges his allies with special envenomed weaponry, increasing Rally Squads' Lethality by 5%.",
                            "rally_lethality_increase": 0.05
                        }
                    }
                },
                {
                    "level": 4,
                    "power": 298530,
                    "attack": 597,
                    "defense": 597,
                    "health": 5970,
                    "lancer-lethality": 0.6420,
                    "lancer-health": 0.6420,
                    "skills": {
                        "exploration": {
                            "skill-name": "Potion #1325",
                            "description": "Gordon's chemical arsenal increases his Damage Dealt by 10% and reduces the Attack of Poisoned targets by 15%.",
                            "damage_dealt_increase": 0.10,
                            "poisoned_attack_reduction": 0.15
                        },
                        "expedition": {
                            "skill-name": "Bio Assault",
                            "description": "Gordon privileges his allies with special envenomed weaponry, increasing Rally Squads' Lethality by 7.5%.",
                            "rally_lethality_increase": 0.075
                        }
                    }
                },
                {
                    "level": 5,
                    "power": 365940,
                    "attack": 731,
                    "defense": 731,
                    "health": 7316,
                    "lancer-lethality": 0.8025,
                    "lancer-health": 0.8025,
                    "skills": {
                        "exploration": {
                            "skill-name": "Potion #1325",
                            "description": "Gordon's chemical arsenal increases his Damage Dealt by 15% and reduces the Attack of Poisoned targets by 15%.",
                            "damage_dealt_increase": 0.15,
                            "poisoned_attack_reduction": 0.15
                        },
                        "expedition": {
                            "skill-name": "Bio Assault",
                            "description": "Gordon privileges his allies with special envenomed weaponry, increasing Rally Squads' Lethality by 7.5%.",
                            "rally_lethality_increase": 0.075
                        }
                    }
                },
                {
                    "level": 6,
                    "power": 433350,
                    "attack": 866,
                    "defense": 866,
                    "health": 8662,
                    "lancer-lethality": 0.9630,
                    "lancer-health": 0.9630,
                    "skills": {
                        "exploration": {
                            "skill-name": "Potion #1325",
                            "description": "Gordon's chemical arsenal increases his Damage Dealt by 15% and reduces the Attack of Poisoned targets by 15%.",
                            "damage_dealt_increase": 0.15,
                            "poisoned_attack_reduction": 0.15
                        },
                        "expedition": {
                            "skill-name": "Bio Assault",
                            "description": "Gordon privileges his allies with special envenomed weaponry, increasing Rally Squads' Lethality by 10%.",
                            "rally_lethality_increase": 0.10
                        }
                    }
                },
                {
                    "level": 7,
                    "power": 500760,
                    "attack": 1001,
                    "defense": 1001,
                    "health": 10008,
                    "lancer-lethality": 0.11235,
                    "lancer-health": 0.11235,
                    "skills": {
                        "exploration": {
                            "skill-name": "Potion #1325",
                            "description": "Gordon's chemical arsenal increases his Damage Dealt by 20% and reduces the Attack of Poisoned targets by 15%.",
                            "damage_dealt_increase": 0.20,
                            "poisoned_attack_reduction": 0.15
                        },
                        "expedition": {
                            "skill-name": "Bio Assault",
                            "description": "Gordon privileges his allies with special envenomed weaponry, increasing Rally Squads' Lethality by 10%.",
                            "rally_lethality_increase": 0.10
                        }
                    }
                },
                {
                    "level": 8,
                    "power": 568170,
                    "attack": 1136,
                    "defense": 1136,
                    "health": 11354,
                    "lancer-lethality": 0.12840,
                    "lancer-health": 0.12840,
                    "skills": {
                        "exploration": {
                            "skill-name": "Potion #1325",
                            "description": "Gordon's chemical arsenal increases his Damage Dealt by 20% and reduces the Attack of Poisoned targets by 15%.",
                            "damage_dealt_increase": 0.20,
                            "poisoned_attack_reduction": 0.15
                        },
                        "expedition": {
                            "skill-name": "Bio Assault",
                            "description": "Gordon privileges his allies with special envenomed weaponry, increasing Rally Squads' Lethality by 12.5%.",
                            "rally_lethality_increase": 0.125
                        }
                    }
                },
                {
                    "level": 9,
                    "power": 635580,
                    "attack": 1271,
                    "defense": 1271,
                    "health": 12699,
                    "lancer-lethality": 0.14445,
                    "lancer-health": 0.14445,
                    "skills": {
                        "exploration": {
                            "skill-name": "Potion #1325",
                            "description": "Gordon's chemical arsenal increases his Damage Dealt by 25% and reduces the Attack of Poisoned targets by 15%.",
                            "damage_dealt_increase": 0.25,
                            "poisoned_attack_reduction": 0.15
                        },
                        "expedition": {
                            "skill-name": "Bio Assault",
                            "description": "Gordon privileges his allies with special envenomed weaponry, increasing Rally Squads' Lethality by 12.5%.",
                            "rally_lethality_increase": 0.125
                        }
                    }
                },
                {
                    "level": 10,
                    "power": 722250,
                    "attack": 1444,
                    "defense": 1444,
                    "health": 14445,
                    "lancer-lethality": 0.16050,
                    "lancer-health": 0.16050,
                    "skills": {
                        "exploration": {
                            "skill-name": "Potion #1325",
                            "description": "Gordon's chemical arsenal increases his Damage Dealt by 25% and reduces the Attack of Poisoned targets by 15%.",
                            "damage_dealt_increase": 0.25,
                            "poisoned_attack_reduction": 0.15
                        },
                        "expedition": {
                            "skill-name": "Bio Assault",
                            "description": "Gordon privileges his allies with special envenomed weaponry, increasing Rally Squads' Lethality by 15%.",
                            "rally_lethality_increase": 0.15
                        }
                    }
                }
            ]
        }
    }
]

HERO = gordon_hero
