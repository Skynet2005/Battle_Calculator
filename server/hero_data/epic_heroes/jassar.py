jassar_hero = [
    {
        "hero-name": "Jassar",
        "hero-class": "marksman",
        "rarity": "Epic",
        "generation": 1,
        "base-stats": {
            "attack": 2157,
            "defense": 2220,
            "health": 13320,
            "lethality": 0,
            "marksman-attack": 0.14011,
            "marksman-defense": 0.14011
        },
        "skills": {
            "exploration": {
                "1": {
                    "skill-name": "Triple Volley",
                    "description": "Jassar precisely aims and fires three consecutive bullets, dealing Attack * 100%, Attack * [125%/137.5%/150%/162.5%/175%], and Attack * [150%/165%/180%/195%/210%] damage respectively, with the third being area of effect damage.",
                    "level_percentage": {
                        "1": 1.00,
                        "2": 1.375,
                        "3": 1.50,
                        "4": 1.625,
                        "5": 1.75
                    }
                },
                "2": {
                    "skill-name": "Suppressive Fire",
                    "description": "Jassar relies on masterful marksmanship and overwhelming firepower to suppress the enemy, dealing Attack * [100%/110%/120%/130%/140%] damage and reducing the target's Attack Speed by [30%/35%/40%/45%/50%] for 2s.",
                    "level_percentage": {
                        "1": 1.00,
                        "2": 1.10,
                        "3": 1.20,
                        "4": 1.30,
                        "5": 1.40
                    }
                },
                "3": {
                    "skill-name": "Natural Precision",
                    "description": "Jassar's impeccable marksmanship has become second nature, increasing Attack by [8%/12%/16%/20%/24%].",
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
                    "skill-name": "Tactical Genius",
                    "description": "Jassar's combination of courage and wisdom enriches the army, increasing damage dealt by [5%/10%/15%/20%/25%] for all troops.",
                    "level_percentage": {
                        "1": 0.05,
                        "2": 0.10,
                        "3": 0.15,
                        "4": 0.20,
                        "5": 0.25
                    }
                },
                "2": {
                    "skill-name": "Enlightened Warfare",
                    "description": "Jassar's profound knowledge increases the city's Research Speed by [3%/6%/9%/12%/15%].",
                    "level_percentage": {
                        "1": 0.03,
                        "2": 0.06,
                        "3": 0.09,
                        "4": 0.12,
                        "5": 0.15
                    }
                }
            }
        },
        "exclusive-weapon": None
    }
]

HERO = jassar_hero
