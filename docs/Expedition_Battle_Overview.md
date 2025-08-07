### Overview of Expedition Battles and Rally Formations in Whiteout Survival

Whiteout Survival features two main battle categories: Exploration (e.g., Lighthouse missions, Arena, in‑game exploration tab fights) and Expedition (world map battles, including event attacks, solo marches, resource gathering, rallies against beasts or players, Castle Battles, and Fortress Battles). Expedition Battles are the focus here, as they encompass rallies and troop‑based combat. These are turn‑based engagements where troops select targets (typically the closest first), with positioning affecting outcomes: Infantry on the frontline absorbs damage, Lancers in the middle provide balanced support and can occasionally target backline units, and Marksmen in the rear deal ranged damage but are vulnerable if the front collapses.

Rally Formations are a subset of Expedition Battles, allowing alliances to combine forces for stronger attacks (PvE like Bear Hunt or PvP like Castle sieges). A rally is initiated by a Rally Captain (leader), with up to several joiners contributing troops. The captain's setup determines most buffs, while joiners add limited skills. Common troop ratios include:
- Attacking: 50% Infantry / 20% Lancers / 30% Marksmen (for balanced offense, with Infantry tanking and Marksmen outputting damage).
- Defending: 60% Infantry / 40% Lancers / 0% Marksmen (prioritizing durability).
- PvP variations: 30% Infantry / 30% Lancers / 40% Marksmen.

Rally capacity is boosted by upgrading the Command Center and researching "Regimental Expansion" in the Battle tech tree. In rallies, heroes do not deal direct damage but boost troop performance via Expedition Skills. Battles follow a cyclical damage flow: Marksmen target Infantry > Infantry targets Lancers > Lancers target Marksmen (with a 10‑20% chance for Lancers to bypass Infantry and hit Marksmen directly from Level 7+). Damage order prioritizes Infantry deaths first, then Lancers (starting at ~20% Infantry remaining), then Marksmen last. Use the "Balance Option" for consistent formations during high‑pressure scenarios.

### Core Stats and Their Roles

Troops have seven stats, but four are central to battles: Attack, Defense, Lethality, and Health. These scale with troop tiers (T1 to T11) and Fire Crystal levels (0‑10, unlocked after specific criteria like high Furnace levels). Higher tiers provide base point multipliers (e.g., T9 vs. T10 has a ~1‑2 point gap per stat, allowing stat boosts to overcome tier differences). Stats are multiplicative with bonuses.

- **Attack**: Determines base damage output. Limited by enemy Defense—damage only depletes Health after Defense is zeroed. Each troop type has bonuses: Marksmen +10% vs. Infantry, Lancers +10% vs. Marksmen, Infantry +10% vs. Lancers.
- **Defense**: Absorbs incoming damage before it hits Health. High Defense on frontline troops (e.g., Infantry) prolongs survival.
- **Lethality**: Bypasses enemy Defense to deal direct Health damage. Critical against high‑Defense foes; often prioritized for damage dealers like Marksmen.
- **Health**: Total hit points; troops die at zero. Influences longevity, especially for tanks.

Other stats:
- **Power**: Adds to account power but irrelevant in battles.
- **Speed**: Fixed at 11; affects map march speed (Wilderness March Speed is separate).
- **Load**: For resource carrying, not battles.

Stat interactions are situational—no single "best" stat. For example, high Attack counters low Defense, while high Lethality beats high Health. Base stats multiply by percentage bonuses (e.g., from heroes), creating effective values. In rallies, stats from the captain apply to all troops, overriding joiners' except for march size.

| Troop Type | Primary Role | Key Stats to Prioritize | Base Bonuses/Weaknesses |
|------------|--------------|-------------------------|-------------------------|
| Infantry  | Frontline Tank | Defense, Health (secondary: Attack, Lethality) | +10% Attack vs. Lancers; High base Defense/Health but weak offense. |
| Lancers   | Balanced Support | Attack, Lethality (balanced others) | +10% Attack vs. Marksmen; 20% chance to strike Marksmen behind Infantry (Level 7+); Deals 10% less to Infantry. |
| Marksmen  | Backline Damage Dealer | Attack, Lethality (secondary: Health) | +10% Attack vs. Infantry; 10% chance for double strikes (Level 7+); Vulnerable if frontline falls. |

Fire Crystal upgrades add skills like Crystal Shield (Infantry offsets damage) or Crystal Gunpowder (Marksmen +50% damage chance).

### Damage Calculation Algorithm

While exact formulas aren't officially disclosed, community analyses and wiki insights provide approximate algorithms based on battle reports. Damage is turn‑based, with troops attacking in order (Marksmen first on Infantry, etc.). Core formula approximations:

- **Basic Damage**: Damage = (Attacker's Attack × Multipliers) - (Target's Defense × Multipliers). If Defense > Damage, no Health loss; excess depletes Health.
- **Lethality Integration**: Effective Damage = (Attack × (1 - Defense Mitigation)) + (Lethality × Bypass Factor). Lethality ignores Defense, dealing direct Health damage (e.g., ~10‑30% bypass in high‑level rallies). Simplified community view: Damage ≈ Attack × Lethality (for quick estimates in events like Bear Hunt, where 10‑30M damage per rally is common with T10+ troops).
  
  To arrive at this: Start with base Attack output, subtract mitigated portion (Defense reduces it proportionally, e.g., if Defense is 50% of Attack, halve damage), then add Lethality as unmitigated Health hits. Multipliers include bonuses (see below).

- **Special Bonuses Formula**: Effective Stat = (Base Stat % × Special Bonus Multiplier) + Additive Bonus %.
  Example: 400% base Attack with 15% special bonus (e.g., from hero widget) = (400 × 1.15) + 15 = 475% (18.75% effective increase). Stacks additively after multiplication. For 50% total bonuses on 400% base: (400 × 1.5) + 50 = 650%.
  
  Derivation: Bonuses are multiplicative on base, then additive for flat increases. This amplifies high bases (e.g., 500% base with 50% bonuses = 800%).

- **Full Battle Algorithm Steps**:
  1. Calculate effective stats: Base × (1 + % Bonuses) + Flat Bonuses.
  2. Determine targeting: Closest first, with probabilities (e.g., Lancers 20% chance to hit Marksmen).
  3. Apply damage per turn: Attacker Damage vs. Target Defense → Remaining to Health + Lethality direct to Health.
  4. Factor troop numbers: More troops scale damage linearly (e.g., 2x troops ≈ 2x output, but losses reduce over turns).
  5. Hero/Pet Skills: Add probabilistic extras (e.g., double damage chance).
  6. Outcome: Simulate until one side's Health totals zero, with losses prioritizing Infantry > Lancers > Marksmen.

In rallies, captain's stats/bonuses apply globally; joiners add 4 top Expedition Skills (selected by highest level, non‑stacking for most heroes). High stat gaps can overcome tier differences (e.g., T9 with +100% Lethality beats T10). Use battle reports to reverse‑engineer: e.g., if Lancers kill more Marksmen than expected, it's due to bypass skills.

### Sources That Feed Into Battles

All sources multiply or add to core stats, with heroes/pets central in Expedition mode.

- **Heroes and Expedition Skills**:
  - Heroes provide up to 9 buffs in rallies (3 right‑side skills from captain's 3‑hero squad). Joiners add 4 top first skills (from lead hero, selected by level 1‑5; stackable for some like Jessie/Jasser).
  - Widgets (hero‑exclusive gears): +5‑15% special bonuses (e.g., Jeronimo: +15% Rally Troop Attack). Level 10 widgets cost 275 per hero, season‑specific.
  - Examples:
    - Offensive: Jeronimo (+15% Attack), Reina (+15% Lethality, +420% damage to all sources), Jessie (+75% normal attack damage, but only troops).
    - Defensive: Molly (+Defense), Patrick (+Health/Durability), Sergey (+Troop Durability).
    - Gen‑specific bests: Gen 1 F2P (Molly/Bahiti/Sergey), Gen 4 (Reina for joiners).
  - Skills activate probabilistically in squads (e.g., AOE from Noah/Gwen hits Lancers early). Higher VIP (e.g., VIP10: +12% Attack) and skill levels amplify.
  - Gears: Exclusive hero gear at Lv10 adds 5 Expedition/5 Exploration levels; Chief Gear/Charm upgrades boost overall (prioritize Mythic from Arena Shop).

- **Pet Skills**:
  - Pets provide activatable buffs for offense (Attack/Lethality), defense (Defense/Health), or support. Exclusive abilities enhance during events (e.g., extra damage attacks in rallies). Equip for specific buffs like +Attack in Bear Hunt. No detailed formulas, but they add to "damage dealt" multipliers (e.g., Reina's skill includes pet damage).

- **Other Sources**:
  - **Research**: Battle tech tree (e.g., +Attack/Lethality techs).
  - **Chief Gear/Charms**: Upgrades/refines for quality boosts (e.g., +25k Infantry stats).
  - **Territory Bonuses**: Alliance Territory provides % stats (view in Alliance > Territory).
  - **Time‑Limited Buffs**: Gem‑bought or rewards (e.g., Troops Damage Up II: +% Damage, non‑stacking same types, active in events until team update).
  - **Gems and Facilities**: Gem buffs (e.g., 20% 12‑hour Attack), Daybreak Island buildings for Attack/Lethality.
  - **Trap Enhancements** (events like Bear Hunt): +5‑25% Attack via donations.

In rallies, captain sources dominate; joiners only add skills and troops. For defense (garrisons), strongest chief's stats apply, with joiners switching to defensive heroes (e.g., Patrick for +Defense).

