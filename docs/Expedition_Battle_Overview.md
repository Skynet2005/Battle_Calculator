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

### Deep Dive into Skill Stacking in Rallies

Building on the core mechanics, skill stacking in Rally Formations (a key part of Expedition Battles) is nuanced and depends on whether the skills are from the Rally Captain or joiners, the skill type (e.g., flat bonuses, chance-based, or triggered effects), and hero specifics. Rallies allow up to 5 participants (1 captain + 4 joiners in most cases, expandable via research), with the captain's full squad determining baseline buffs and joiners contributing selectively. Only Expedition Skills (the right-side hero skills, focused on troop enhancements) apply in rallies—Exploration Skills (left-side, for hero direct damage) are irrelevant here.

#### How Skills Apply in Rallies
- **Rally Captain's Contribution**: The captain's entire 3-hero squad provides all their Expedition Skills (up to 9 total, 3 per hero). These apply globally to all troops in the rally, including joiners'. The captain's hero levels, gears, and widgets fully influence the buffs. For example, if the captain uses Jeronimo (Gen 3), all troops get +15% Rally Troop Attack from his widget.
- **Joiners' Contribution**: Only the **first Expedition Skill** (top skill) of the **lead hero** (first position in their march squad) from each joiner is considered. The game selects the **top 4 joiners** based on power or skill priority (highest level skills first), and only those 4 skills are added. Joiners' other heroes, gears, or widgets do **not** apply—only that single skill. This is why joiners often use "one-trick" setups like leading with Jessie for her damage boost.
- **Garrison (Defensive Rallies)**: Similar logic, but defensive-oriented. Skills stack from the garrison leader's squad and reinforcing joiners' top skills. Overlapping defensive skills (e.g., +Defense from multiple Patricks) generally add up.

#### Stacking Rules: Which Skills Stack and Which Don't
Stacking occurs when multiple identical or similar skills are present (e.g., from captain's squad + joiners). Not all skills stack additively or multiplicatively—some are capped, non-stackable, or probabilistic. Based on community breakdowns and guides, here's a breakdown:

- **Skills That Stack (Additive or Multiplicative)**:
  - **Flat Percentage Bonuses**: Most direct stat boosts stack additively. For example:
    - Jessie's "Carnage" (Gen 1: +75% normal attack damage for troops) stacks with multiples. If the captain has Jessie and 4 joiners lead with her, you get up to 5x +75% = +375% troop damage. This is why Jessie is meta for rallies like Bear Hunt—it's one of the few that fully stacks across joiners.
    - Jasser's similar damage boosts (Gen variants) also stack, often mentioned alongside Jessie as "stackable exceptions."
    - Reina's "Burning Passion" (Gen 4: +420% damage from all sources, including pets) stacks if multiple are present, but it's rarer due to her being a captain-focused hero.
    - Patrick's "Tough Guy" (Gen 1: +Troop Durability/Health) stacks for defense, adding layers of Health multipliers.
  - **Damage Multipliers**: "Increased Damage" effects (e.g., from heroes like Bradley or Hector) are additive within the same category. If three sources give +50% increased damage each, it's rolled into one +150% multiplier, then applied to base damage. This is multiplicative with other categories (e.g., +Attack from gears).
  - **Burn/Ignite Effects**: Flint's skill (20% chance to ignite, stacking 40% burn damage over 3 turns) can stack in effect if multiple triggers occur, amplifying DoT (Damage over Time) in prolonged battles.
  - **AOE or Support Skills**: Skills like Molly's Defense boosts or Sergey's Durability enhancements stack additively if from different heroes.

- **Skills That Do Not Stack**:
  - **Chance-Based or Probabilistic Skills**: These don't add probabilities—only the highest or first instance applies, or they trigger independently but without compounding chance. Examples:
    - Jabel's first Expedition skill (chance-based damage proc) doesn't stack; multiple joiners with it won't increase the % chance beyond the base.
    - % Chance for Double Strikes (e.g., from troop skills or heroes like Gwen) caps at the highest value; duplicates are ignored.
    - Bypass Chances (e.g., Lancers' % to hit backline) don't stack from hero sources—if a hero adds 10% bypass, multiples don't make it 20%.
  - **Unique or Capped Effects**: Some are one-instance only, like certain debuffs (e.g., -Enemy Defense from Mia) which apply once per battle, not stacking.
  - **Overlapping Identical Skills (Non-Exceptions)**: Most non-Jessie/Jasser skills don't stack if identical. For example, if multiple joiners lead with Jeronimo's Attack boost, only one applies (the highest level).
  - **Widget Bonuses**: These are captain-only and don't stack with joiners (since joiners' widgets don't apply).

- **General Stacking Formula Insights**:
  - Bonuses are often additive within types: Effective Multiplier = 1 + (Sum of % Bonuses / 100). Then multiplicative across categories (e.g., Attack Multiplier × Damage Multiplier).
  - Example: Base Damage = 100. Jessie stack (+300% from 4 sources) = 100 × 4 = 400. Then +50% from gears = 400 × 1.5 = 600.
  - Non-stacking chances: If two 10% chances for an effect, it remains 10% (not 20%), but each can trigger separately if independent.

In practice, optimize by having joiners use stackable skills like Jessie's for max damage output. Videos like  and  confirm chance-based don't stack, while flat damages do.

### Troop Levels, Tiers, and Skills Integration into Battles

Troops are divided into three types: Infantry (tanks), Lancers (support/bypass), and Marksmen (DPS). They progress through **tiers** (T1 to T11) and **levels** (1-10 per tier, with Fire Crystal enabling T11 and beyond). Higher tiers/levels directly scale core stats (Attack, Defense, Lethality, Health) and unlock **troop-specific skills** that add bonuses, probabilities, or effects to the damage algorithm. All troops in a march/rally must be the same tier (auto-promoted when unlocked), but mixed types are allowed.

#### Troop Tiers and Levels Overview
- **Tiers (T1-T11)**: Unlocked via upgrading troop camps (Infantry Camp, Lancer Camp, Marksman Camp). T1-T4 are basic; T5+ require higher Furnace levels and resources. T9-T11 are "Fire Crystal Troops," unlocked after Furnace Lv30+ and building the War Hall. Higher tiers multiply base stats (e.g., T10 has ~1.5x T9's base Attack/Defense). Promotion auto-upgrades all lower-tier troops.
- **Levels (1-10 per Tier)**: Leveled via camp upgrades. Each level adds incremental stat points (e.g., +10-20 Attack per level). Max level per tier is 10, but Fire Crystal allows "over-leveling" camps beyond Lv30 for T11 troops.
- **Fire Crystal Upgrades**: Post-Lv30 camps use Fire Crystals (gained from events, mining) to upgrade. Each FC level (1-10+) requires multiple upgrades (e.g., 5x per FC level). This auto-upgrades all troops to FC versions, adding exclusive skills and massive stat boosts (e.g., FC Lv1: +50% base stats). FC shards speed upgrades. Example: FC Infantry gains "Crystal Shield" (offsets incoming damage by %).

Stats scale: Base Stat = Tier Multiplier × Level Points. E.g., T10 Lv10 Infantry might have 500 Defense base, vs. T9 Lv10's 400. Then apply multipliers from heroes/pets.

#### Troop-Specific Skills and Battle Integration
Skills unlock at specific levels (e.g., Lv1, Lv7) and are passive, always active in Expedition Battles. They modify targeting, damage output, or durability within the algorithm. Battles are turn-based: Troops attack in cycles (Marksmen → Infantry → Lancers), with skills triggering probabilities each turn.

- **Infantry (Frontline Tanks)**:
  - **Role in Battles**: Absorb damage first (90% of initial targeting). High base Defense/Health; counters Lancers (+10% Attack vs. them). Weak to Marksmen (-10% effective Defense).
  - **Skills**:
    - Lv1: Melee Strike – +10% Damage to Lancers. Integrates as multiplier to Attack when targeting Lancers: Damage = Attack × 1.1 - Target Defense.
    - Lv7: Charge – 15% chance to stun Lancers for 1 turn (prevents counterattack). If triggers, skips Lancer damage phase.
    - Fire Crystal (FC Lv1+): Crystal Armor – Reduces incoming damage by 20-50% (scales with FC level). Applied pre-Defense: Incoming Damage × (1 - Reduction %).
  - **Stat Prioritization**: Defense > Health > Lethality (for bypassing if front collapses). Levels add tankiness, allowing more turns before death (losses start here).

- **Lancers (Balanced Support/Bypass)**:
  - **Role in Battles**: Midline; targets Marksmen primarily (+10% Attack vs. them). 10-20% base chance to bypass Infantry and hit Marksmen directly (increases with levels). Counters Marksmen but weak to Infantry.
  - **Skills**:
    - Lv1: Pierce – +10% Damage to Marksmen. Multiplier: Attack × 1.1 when hitting them.
    - Lv7: Bypass Assault – +10% chance to ignore frontline (total 20-30% at high levels). If triggers, redirects full damage to Marksmen, bypassing Infantry Defense. Algorithm: Roll RNG each turn; on success, Damage = Attack + Lethality direct to Marksmen Health.
    - Fire Crystal (FC Lv1+): Crystal Lance – +30% Lethality penetration (ignores more Defense). Adds to Lethality calc: Effective Lethality = Base × 1.3.
  - **Stat Prioritization**: Attack = Lethality > Health. Higher levels amplify bypass, shifting damage from tanks to DPS, collapsing enemy backlines faster.

- **Marksmen (Backline DPS)**:
  - **Role in Battles**: Ranged; targets Infantry first (+10% Attack vs. them). Vulnerable if front falls (then targeted by all). High output but low Defense/Health.
  - **Skills**:
    - Lv1: Ranged Strike – +10% Damage to Infantry. Multiplier: Attack × 1.1.
    - Lv7: Volley – 10% chance for double strike (hits twice in one turn). On trigger: Damage × 2 (after Defense/Lethality).
    - Fire Crystal (FC Lv1+): Crystal Gunpowder – 20% chance for +50% damage burst. Multiplier on trigger: Damage × 1.5.
  - **Stat Prioritization**: Attack > Lethality > Health (for survival if exposed). Levels boost output, with Volley adding RNG spikes to total damage.

#### How They Play into the Damage Algorithm
Troop skills feed directly into the core formula:
- **Effective Damage = (Attack × Type Bonus × Skill Multipliers - Defense) + (Lethality × Penetration)**.
  - Type Bonuses: +10% from counters (e.g., Marksmen vs. Infantry).
  - Skill Multipliers: E.g., +10% from Lv1 skills; probabilities like Volley roll per attack (10% for ×2).
  - Targeting with Skills: Lancers' bypass alters target, applying full damage to weaker units.
- **Health Depletion**: Skills prolong survival (e.g., Infantry Charge skips damage) or accelerate kills (e.g., Marksmen Volley bursts).
- **Tier/Level Impact**: Higher = higher bases, so multipliers amplify more (e.g., T11 with FC skills: +50% effective output vs. T10).
- **Formation Synergy**: 50% Infantry tanks for Marksmen (30%) to output safely; Lancers (20%) exploit bypass. In rallies, skills scale with troop numbers—more troops = more skill triggers.

This setup allows high-level troops to punch above tiers if skills align (e.g., Lv7+ Lancers bypassing to one-shot Marksmen).