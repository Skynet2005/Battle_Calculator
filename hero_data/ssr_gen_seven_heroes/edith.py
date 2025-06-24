edith_hero = [
    {
        "hero-name": "Edith",
        "hero-class": "infantry",
        "rarity": "SSR",
        "generation": 7,
        "base-stats": {
            "attack": 5466,
            "defense": 7126,
            "health": 106892,
            "infantry-attack": 6.5052,
            "infantry-defense": 6.5052
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Ironclad Punch",
                    "description": "Mr. Tin unleashes ironclad fury against Edith's assailants, punching all enemies in a fan-shaped area ahead, dealing Attack * [100% / 110% / 120% / 130% / 140%] damage and stuns the targets by 1s, while increasing his own Attack by [20% / 40% / 60% / 80% / 100%] for 2s.",
                    "level_percentage": {
                        "1": 1.00,
                        "2": 1.10,
                        "3": 1.20,
                        "4": 1.30,
                        "5": 1.40
                    },
                    "level_percentage_attack_boost": {
                        "1": 0.20,
                        "2": 0.40,
                        "3": 0.60,
                        "4": 0.80,
                        "5": 1.00
                    }
                },
                "2": {
                    "skill-name": "Escape Capsule",
                    "description": "Mr. Tin ejects his core as an escape capsule for Edith at 0 Health, detonating the rest of his body in a fiery explosion, dealing Attack * [200% / 220% / 240% / 260% / 280%] damage to nearby enemies.",
                    "level_percentage": {
                        "1": 2.00,
                        "2": 2.20,
                        "3": 2.40,
                        "4": 2.60,
                        "5": 2.80
                    }
                },
                "3": {
                    "skill-name": "Preemptive Alerts",
                    "description": "Edith's battlefield intel warns Mr. Tin of potential dangers, granting him a [10% / 20% / 30% / 40% / 50%] chance of reducing Damage Taken by 50%.",
                    "level_percentage": {
                        "1": 0.10,
                        "2": 0.20,
                        "3": 0.30,
                        "4": 0.40,
                        "5": 0.50
                    }
                }
            },
            "expedition": {
                "1": {
                    "skill-name": "Strategic Balance",
                    "description": "Mr Tin's colossal presence automatically shields friendly ranged units, reducing Damage Taken by [4% / 8% / 12% / 16% / 20%] for Marksmen, and suppressess the enemy, increasing Damage Dealt by [4% / 8% / 12% / 16% / 20%] for Lancers.",
                    "level_percentage_damage_reduction": {
                        "1": 0.04,
                        "2": 0.08,
                        "3": 0.12,
                        "4": 0.16,
                        "5": 0.20
                    },
                    "level_percentage_damage_boost": {
                        "1": 0.04,
                        "2": 0.08,
                        "3": 0.12,
                        "4": 0.16,
                        "5": 0.20
                    }
                },
                "2": {
                    "skill-name": "Ironclad",
                    "description": "Mr Tin's metallic body functions as a fortified wall on the field, reducing damage taken by [4% / 8% / 12% / 16% / 20%] for Infantry.",
                    "level_percentage": {
                        "1": 0.04,
                        "2": 0.08,
                        "3": 0.12,
                        "4": 0.16,
                        "5": 0.20
                    }
                },
                "3": {
                    "skill-name": "Steel Sentinel",
                    "description": "Edith's mobile defense system is reliable, increasing Health by [5% / 10% / 15% / 20% / 25%] for all troops.",
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
            "name": "Charm Toolkit",
            "levels": [
                {
                    "level": 1,
                    "power": 96300,
                    "attack": 147,
                    "defense": 192,
                    "health": 2889,
                    "infantry-lethality": 0.1605,
                    "infantry-health": 0.1605,
                    "skills": {
                        "exploration": {
                            "skill-name": "Pocket Engineer",
                            "description": "Edith takes care of Mr. Tin and restores an amount of Health (15% of Max Health) to Mr. Tin when first under 50% Health while increasing Defense by 10% until the end of Battle.",
                            "level_percentage": 0.15,
                            "defense_boost": 0.10
                        }
                    }
                },
                {
                    "level": 2,
                    "power": 163710,
                    "attack": 250,
                    "defense": 327,
                    "health": 4911,
                    "infantry-lethality": 0.3210,
                    "infantry-health": 0.3210,
                    "skills": {
                        "exploration": {
                            "skill-name": "Pocket Engineer",
                            "description": "Edith takes care of Mr. Tin and restores an amount of Health (15% of Max Health) to Mr. Tin when first under 50% Health while increasing Defense by 10% until the end of Battle.",
                            "level_percentage": 0.15,
                            "defense_boost": 0.10
                        },
                        "expedition": {
                            "skill-name": "Fortworks",
                            "description": "Edith and Mr. Tin are a formidable defensive duo, increasing Defender Troops' Health by 5%.",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 3,
                    "power": 231120,
                    "attack": 353,
                    "defense": 462,
                    "health": 6933,
                    "infantry-lethality": 0.4815,
                    "infantry-health": 0.4815,
                    "skills": {
                        "exploration": {
                            "skill-name": "Pocket Engineer",
                            "description": "Edith takes care of Mr. Tin and restores an amount of Health (20% of Max Health) to Mr. Tin when first under 50% Health while increasing Defense by 15% until the end of Battle.",
                            "level_percentage": 0.20,
                            "defense_boost": 0.15
                        },
                        "expedition": {
                            "skill-name": "Fortworks",
                            "description": "Edith and Mr. Tin are a formidable defensive duo, increasing Defender Troops' Health by 5%.",
                            "level_percentage": 0.05
                        }
                    }
                },
                {
                    "level": 4,
                    "power": 298530,
                    "attack": 455,
                    "defense": 597,
                    "health": 8955,
                    "infantry-lethality": 0.6420,
                    "infantry-health": 0.6420,
                    "skills": {
                        "exploration": {
                            "skill-name": "Pocket Engineer",
                            "description": "Edith takes care of Mr. Tin and restores an amount of Health (20% of Max Health) to Mr. Tin when first under 50% Health while increasing Defense by 15% until the end of Battle.",
                            "level_percentage": 0.20,
                            "defense_boost": 0.15
                        },
                        "expedition": {
                            "skill-name": "Fortworks",
                            "description": "Edith and Mr. Tin are a formidable defensive duo, increasing Defender Troops' Health by 7.5%.",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 5,
                    "power": 365940,
                    "attack": 561,
                    "defense": 731,
                    "health": 10978,
                    "infantry-lethality": 0.8025,
                    "infantry-health": 0.8025,
                    "skills": {
                        "exploration": {
                            "skill-name": "Pocket Engineer",
                            "description": "Edith takes care of Mr. Tin and restores an amount of Health (25% of Max Health) to Mr. Tin when first under 50% Health while increasing Defense by 20% until the end of Battle.",
                            "level_percentage": 0.25,
                            "defense_boost": 0.20
                        },
                        "expedition": {
                            "skill-name": "Fortworks",
                            "description": "Edith and Mr. Tin are a formidable defensive duo, increasing Defender Troops' Health by 7.5%.",
                            "level_percentage": 0.075
                        }
                    }
                },
                {
                    "level": 6,
                    "power": 433350,
                    "attack": 664,
                    "defense": 866,
                    "health": 13000,
                    "infantry-lethality": 0.9630,
                    "infantry-health": 0.9630,
                    "skills": {
                        "exploration": {
                            "skill-name": "Pocket Engineer",
                            "description": "Edith takes care of Mr. Tin and restores an amount of Health (25% of Max Health) to Mr. Tin when first under 50% Health while increasing Defense by 20% until the end of Battle.",
                            "level_percentage": 0.25,
                            "defense_boost": 0.20
                        },
                        "expedition": {
                            "skill-name": "Fortworks",
                            "description": "Edith and Mr. Tin are a formidable defensive duo, increasing Defender Troops' Health by 10%.",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 7,
                    "power": 500760,
                    "attack": 767,
                    "defense": 1001,
                    "health": 15023,
                    "infantry-lethality": 0.11235,
                    "infantry-health": 0.11235,
                    "skills": {
                        "exploration": {
                            "skill-name": "Pocket Engineer",
                            "description": "Edith takes care of Mr. Tin and restores an amount of Health (30% of Max Health) to Mr. Tin when first under 50% Health while increasing Defense by 25% until the end of Battle.",
                            "level_percentage": 0.30,
                            "defense_boost": 0.25
                        },
                        "expedition": {
                            "skill-name": "Fortworks",
                            "description": "Edith and Mr. Tin are a formidable defensive duo, increasing Defender Troops' Health by 10%.",
                            "level_percentage": 0.10
                        }
                    }
                },
                {
                    "level": 8,
                    "power": 568170,
                    "attack": 869,
                    "defense": 1136,
                    "health": 17045,
                    "infantry-lethality": 0.12840,
                    "infantry-health": 0.12840,
                    "skills": {
                        "exploration": {
                            "skill-name": "Pocket Engineer",
                            "description": "Edith takes care of Mr. Tin and restores an amount of Health (30% of Max Health) to Mr. Tin when first under 50% Health while increasing Defense by 25% until the end of Battle.",
                            "level_percentage": 0.30,
                            "defense_boost": 0.25
                        },
                        "expedition": {
                            "skill-name": "Fortworks",
                            "description": "Edith and Mr. Tin are a formidable defensive duo, increasing Defender Troops' Health by 12.5%.",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 9,
                    "power": 635580,
                    "attack": 972,
                    "defense": 1271,
                    "health": 19067,
                    "infantry-lethality": 0.14445,
                    "infantry-health": 0.14445,
                    "skills": {
                        "exploration": {
                            "skill-name": "Pocket Engineer",
                            "description": "Edith takes care of Mr. Tin and restores an amount of Health (35% of Max Health) to Mr. Tin when first under 50% Health while increasing Defense by 30% until the end of Battle.",
                            "level_percentage": 0.35,
                            "defense_boost": 0.30
                        },
                        "expedition": {
                            "skill-name": "Fortworks",
                            "description": "Edith and Mr. Tin are a formidable defensive duo, increasing Defender Troops' Health by 12.5%.",
                            "level_percentage": 0.125
                        }
                    }
                },
                {
                    "level": 10,
                    "power": 722250,
                    "attack": 1107,
                    "defense": 1444,
                    "health": 21667,
                    "infantry-lethality": 0.16050,
                    "infantry-health": 0.16050,
                    "skills": {
                        "exploration": {
                            "skill-name": "Pocket Engineer",
                            "description": "Edith takes care of Mr. Tin and restores an amount of Health (35% of Max Health) to Mr. Tin when first under 50% Health while increasing Defense by 30% until the end of Battle.",
                            "level_percentage": 0.35,
                            "defense_boost": 0.30
                        },
                        "expedition": {
                            "skill-name": "Fortworks",
                            "description": "Edith and Mr. Tin are a formidable defensive duo, increasing Defender Troops' Health by 15%.",
                            "level_percentage": 0.15
                        }
                    }
                }
            ]
        }
    }
]

HERO = edith_hero
