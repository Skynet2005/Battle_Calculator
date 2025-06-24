smith_hero = [
    {
      "hero-name": "Smith",
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
            "skill-name": "Hammer Burn",
            "description": "Smith swings his hammer forward in a devastating arc, dealing Attack * damage.",
            "level_percentage": {
              "1": 2.0,
              "2": 2.2,
              "3": 2.4,
              "4": 2.6,
              "5": 2.8
            }
          },
          "2": {
            "skill-name": "Armor Enhancement",
            "description": "Smith upgrades his armor to reduce damage taken by percentage.",
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
            "skill-name": "Burnished Iron",
            "description": "Smith's contagious passion for the art of crafting has raised City Iron Mine Output by percentage.",
            "level_percentage": {
              "1": 0.05,
              "2": 0.1,
              "3": 0.15,
              "4": 0.2,
              "5": 0.25
            }
          },
          "2": {
            "skill-name": "Craftsmanship",
            "description": "Smith has an extraordinary sixth sense when it comes to iron. + percentage Iron Gathering Speed on the map.",
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

HERO = smith_hero
