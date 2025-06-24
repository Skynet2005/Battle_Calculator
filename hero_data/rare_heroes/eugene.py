eugene_hero = [
    {
      "hero-name": "Eugene",
      "hero-class": "infantry",
      "rarity": "Rare",
      "generation": 1,
      "base-stats": {
        "attack": 1106,
        "defense": 2220,
        "health": 21644,
        "lethality": 0,
        "infantry-attack": 0.9007,
        "infantry-defense": 0.9007
      },
      "skills": {
        "exploration": {
          "1": {
            "skill-name": "Axe Whirl",
            "description": "Eugene's axe pirouette deals damage of Attack * percentage per 0.5s to nearby enemies for 3s.",
            "level_percentage": {
              "1": 0.8,
              "2": 0.88,
              "3": 0.96,
              "4": 1.04,
              "5": 1.1
            }
          },
          "2": {
            "skill-name": "Razor Sharp",
            "description": "Eugene's sharpened axe deals percentage more damage per second.",
            "level_percentage": {
              "1": 0.1,
              "2": 0.15,
              "3": 0.2,
              "4": 0.25,
              "5": 0.3
            }
          }
        },
        "expedition": {
          "1": {
            "skill-name": "Woodland Inheritor",
            "description": "Eugene's consummate knowledge of timber processing has raised City Sawmill Output by percentage.",
            "level_percentage": {
              "1": 0.05,
              "2": 0.1,
              "3": 0.15,
              "4": 0.2,
              "5": 0.25
            }
          },
          "2": {
            "skill-name": "Master Woodcutter",
            "description": "Eugene is always focused on achieving the perfect logging technique. + percentage Wood Gathering Speed on the map.",
            "level_percentage": {
              "1": 0.05,
              "2": 0.1,
              "3": 0.15,
              "4": 0.2,
              "5": 0.25
            }
          }
        }
      },
      "exclusive-weapon": None
    },
]

HERO = eugene_hero
