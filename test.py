# battle_simulation_test.py
# TODO: Add all the Troop Type Skills as well.. Each has it's unique skills that trigger.

from battle_mechanics import (
    TroopDefinition, TroopGroup, BonusSource,
    Hero, Skill, ExclusiveWeapon,
    BattleReportInput, simulate_battle, monte_carlo_battle
)

# Define troop definitions
infantry_fc5 = TroopDefinition(
    name="Infantry (FC5)",
    power=1000,
    attack=200,
    defense=300,
    lethality=0.1,
    health=500,
    stat_bonuses={"attack": 0.05, "defense": 0.05}
)

marksman_fc5 = TroopDefinition(
    name="Marksman (FC5)",
    power=900,
    attack=350,
    defense=150,
    lethality=0.15,
    health=400,
    stat_bonuses={"attack": 0.08, "lethality": 0.05}
)

lancer_fc5 = TroopDefinition(
    name="Lancer (FC5)",
    power=950,
    attack=250,
    defense=200,
    lethality=0.12,
    health=450,
    stat_bonuses={"attack": 0.06, "health": 0.07}
)

# Define hero skills
charlie_skills = {
    "exploration": [
        Skill(name="Demolition Expert", multiplier=1.4, proc_chance=0.2),
        Skill(name="Grenadier", multiplier=0.8, proc_chance=0.15)
    ],
    "expedition": [
        Skill(name="Demolitions Expert", multiplier=0.05, proc_chance=0.0),
        Skill(name="Coal Extraction", multiplier=0.0, proc_chance=0.0)
    ]
}

walis_skills = {
    "exploration": [
        Skill(name="Earthshake", multiplier=0.03, proc_chance=0.25),
        Skill(name="Echoing Boost", multiplier=0.3, proc_chance=0.25),
        Skill(name="Jungle-Born Agility", multiplier=0.2, proc_chance=0.0)
    ],
    "expedition": [
        Skill(name="Tactical Deception", multiplier=0.16, proc_chance=0.0),
        Skill(name="Huntsman's Gift", multiplier=0.0, proc_chance=0.0)
    ]
}

# Define heroes
charlie_hero = Hero(
    name="Charlie",
    char_class="marksman",
    rarity="Rare",
    generation=1,
    base_stats={
        "attack": 1200,
        "defense": 800,
        "health": 10000,
        "marksman-attack": 0.12,
        "marksman-defense": 0.08
    },
    skills=charlie_skills,
    exclusive_weapon=None
)

walis_hero = Hero(
    name="Walis Bokan",
    char_class="lancer",
    rarity="Epic",
    generation=1,
    base_stats={
        "attack": 1776,
        "defense": 2220,
        "health": 17760,
        "lancer-attack": 0.14011,
        "lancer-defense": 0.14011
    },
    skills=walis_skills,
    exclusive_weapon=None
)

# Create troop groups
attacker_groups = [
    TroopGroup(infantry_fc5, count=10000),
    TroopGroup(marksman_fc5, count=8000),
    TroopGroup(lancer_fc5, count=6000)
]

defender_groups = [
    TroopGroup(infantry_fc5, count=12000),
    TroopGroup(marksman_fc5, count=7000),
    TroopGroup(lancer_fc5, count=5000)
]

# Create bonus sources
attacker_bonus = BonusSource(
    hero=charlie_hero,
    city_buffs={"attack": 0.20, "defense": 0.15, "health": 0.10},
    territory_buffs={"attack": 0.05, "lethality": 0.03},
    pet_buffs={"health": 0.05}
)

defender_bonus = BonusSource(
    hero=walis_hero,
    city_buffs={"defense": 0.25, "health": 0.15},
    territory_buffs={"defense": 0.08},
    pet_buffs={"attack": 0.03}
)

# Create battle report input
report = BattleReportInput(
    attacker_troops=attacker_groups,
    defender_troops=defender_groups,
    attacker_bonus=attacker_bonus,
    defender_bonus=defender_bonus,
    skill_trigger_counts={"Demolition Expert": 3, "Grenadier": 2}
)

# Run deterministic simulation
result = simulate_battle(report)
print("Deterministic battle result:")
print(f"Winner: {result['winner']}")
print(f"Attacker survivors: {result['attacker_survivors']}")
print(f"Defender survivors: {result['defender_survivors']}")
print(f"Battle rounds: {result['rounds']}")

# Run Monte Carlo simulation
mc_results = monte_carlo_battle(report, n_sims=1000)
print("\nMonte Carlo simulation results (1000 runs):")
print(f"Attacker win rate: {mc_results['attacker_win_rate']:.2%}")
print(f"Defender win rate: {mc_results['defender_win_rate']:.2%}")
print(f"Average attacker survivors: {mc_results['avg_attacker_survivors']:.1f}")
print(f"Average defender survivors: {mc_results['avg_defender_survivors']:.1f}")
