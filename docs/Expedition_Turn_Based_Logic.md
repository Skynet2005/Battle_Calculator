### Turn-Based Logic in Expedition Battles and Rallies

Expedition Battles in *Whiteout Survival* encompass world map engagements, including solo marches, resource raids, PvP attacks, and event-based fights like Bear Hunt or Castle Battles. Rallies are a collaborative subset where an alliance Rally Captain initiates the attack, and up to 4 joiners (expandable via research) contribute troops and limited skills. All these battles follow a turn-based simulation, where troops from both sides engage in cycles of targeting and damage dealing until one side's effective Health is depleted or a time limit/event condition ends the fight (e.g., 30 minutes for Bear Hunt rallies). Unlike real-time combat, turns are automated and simulated quickly, with outcomes detailed in battle reports. The logic emphasizes troop positioning (frontline to backline), counter matchups, and probabilistic skills, creating a rock-paper-scissors dynamic: Marksmen counter Infantry, Infantry counter Lancers, Lancers counter Marksmen.

Battles aren't strictly "one-turn" affairs (even in PvE like Bear Trap, where some sources describe it as such for simplicity); instead, they involve multiple simulated turns until resolution. For instance, in prolonged fights, turns continue with accumulating losses, prioritizing Infantry deaths first, then Lancers (around 20% Infantry remaining), and Marksmen last. In rallies, the captain's stats, heroes, and bonuses apply globally, overriding joiners' except for added skills and troop counts, amplifying the scale but adhering to the same turn logic.

#### Turn Order and Structure
Turns are cyclical and likely simultaneous per side (both attacker and defender act in each turn), though some community insights suggest a phased order based on troop types:
- **Initiation**: The battle starts with targeting selection, prioritizing the closest enemies. Infantry (frontline) absorbs initial hits, protecting midline Lancers and backline Marksmen.
- **Attack Sequence**: 
  - Marksmen often initiate damage due to their ranged nature, targeting Infantry first (with +10% bonus).
  - Infantry then counter, targeting Lancers (with +10% bonus).
  - Lancers close the cycle, targeting Marksmen (with +10% bonus), but with a 20% chance (from Level 7 Ambusher skill) to bypass Infantry and strike Marksmen directly.
- **Turn Progression**: Each turn, all surviving troops on a side attack their targets. If a troop type is depleted (e.g., all Infantry dead), the next line advances (Lancers become frontline). Battles end when one side has no troops left or Health totals zero. In rallies against bosses like the Raging Bear, turns continue until the rally's march returns or the event timer expires, with damage accumulated across turns.
- **RNG Elements**: Probabilistic skills (e.g., 10% chance for Marksmen double strike at Level 7) trigger per turn, adding variance. Hero Expedition Skills (e.g., stun chances from Molly) can skip enemy actions in a turn.
- **Rally-Specific Modifications**: Rallies scale turns with combined troop numbers (e.g., captain + joiners' troops act as one unified force). The captain's full squad (3 heroes, 9 skills) buffs all turns, while joiners add up to 4 top Expedition Skills (selected by highest level, e.g., Jessie's +75% damage stacks additively if multiple). This doesn't change turn order but enhances per-turn output. In Bear Hunt, positioning the captain close to the target minimizes travel time, allowing more rallies (and thus more simulated battles) within the 30-minute window.

| Phase in Turn | Troop Action | Key Influences |
|---------------|--------------|----------------|
| Targeting Selection | Closest first (Infantry absorbs) | Positioning, Lancer bypass (20% chance at Lv7+) |
| Damage Dealing | All troops attack selected targets | Counters (+10% bonus), Skills (e.g., double damage proc) |
| Resolution | Apply damage, check depletions | Defense mitigation, Lethality bypass, Hero buffs |
| Next Turn Prep | Advance lines if type depleted | Losses prioritize Inf > Lanc > Marks |

#### Targeting Logic
Targeting is proximity-based but modified by counters and skills:
- **Default**: Frontline (Infantry) targeted first by all enemy types.
- **Counters and Bypasses**:
  - Marksmen prioritize Infantry (+10% damage via Level 1 Ranged Strike).
  - Infantry prioritize Lancers (+10% damage via Level 1 Master Brawler).
  - Lancers prioritize Marksmen (+10% damage via Level 1 Charge), with 20% chance to ignore frontline (Level 7 Ambusher).
- **Hero and Skill Overrides**: Some Expedition Skills (e.g., from Gwen or Noah) enable AOE or targeted strikes, potentially hitting backlines early. In rallies, captain's skills like Reina's (+420% all-source damage) amplify these across turns, while joiners' stackable skills (e.g., multiple Jessies) boost overall output without altering targeting.
- **Formation Impact**: Recommended ratios affect exposure—e.g., attack rallies use 50% Infantry / 20% Lancers / 30% Marksmen to tank while outputting damage; defense uses 60% Infantry / 40% Lancers / 0% Marksmen for durability. In Bear Hunt, marksmen-heavy (e.g., 10% Inf / 30% Lanc / 60% Marks) maximizes damage as they have higher base Attack/Lethality, but requires frontline protection to survive turns.
- **Rally Nuance**: Against PvE bosses, targeting is fixed on the boss, but internal troop losses follow standard logic. In PvP rallies, enemy garrison formations counter yours, with battle reports showing turn-by-turn breakdowns.

#### Damage Calculation Per Turn
Damage is computed per troop attack in each turn, integrating stats, bonuses, and RNG. While exact developer formulas aren't public, community reverse-engineering from battle reports provides this approximate algorithm:

1. **Base Damage Setup**: For each attacking troop, calculate Effective Attack = Base Attack × (1 + % Bonuses from heroes/pets/gears) + Flat Bonuses. Include type counters (+10%).
2. **Mitigation and Bypass**:
   - Damage to Target = Effective Attack - (Target Defense × Mitigation Multipliers).
   - If Damage > Defense, excess depletes Health.
   - Add Lethality: Direct Health damage = Lethality × (1 + Penetration Bonuses), bypassing Defense entirely.
3. **Skill and RNG Application**: Roll for probabilities (e.g., Marksmen Level 7 Volley: 10% for ×2 damage; Lancers FC3 Crystal Lance: 10% double damage). Hero skills like Jessie's Carnage (+75% normal attack) multiply post-base.
4. **Aggregation and Losses**: Sum damage across all attacks. Troops die at 0 Health; losses reduce future turns' output linearly (e.g., 50% troops lost = 50% less damage next turn).
5. **Full Turn Formula Approximation**: Total Turn Damage ≈ (Avg. Troop Attack × Number of Troops × Counter Multiplier × Skill Avg.) - (Enemy Avg. Defense × Number of Enemies) + (Avg. Lethality × Bypass Factor × Troops).
   - Example: To arrive at a simple estimate for Bear Hunt (high-damage rally), players use Attack × Lethality as a proxy, aiming for 10-30M damage per rally with T10+ troops. For precise: Start with base (e.g., Marksmen base Attack 500), apply bonuses (e.g., +50% from Jeronimo = 750), subtract Defense (e.g., 300 mitigated = 450 to Health), add Lethality (200 direct). Multiply by troop count and RNG rolls.
- **Rally Enhancements**: Captain's widgets (e.g., Natalia's +15% Lethality) and gears apply to all; joiners' skills (e.g., 4x Jessie = +300% damage) stack additively. In Bear Hunt, damage focuses on marksmen due to higher base, with FC skills (e.g., 20% chance +50% damage) triggering per turn. Non-stacking skills (e.g., chance-based) take the highest value.
- **Special Cases**: In one-turn approximations (e.g., Bear Trap PvE), it's a burst calculation, but underlying turns simulate until boss Health chunk is removed. Battle reports reveal sequences, showing per-turn losses and total damage dealt/received.

#### Strategies and Insights
- **Optimization**: Use battle reports to analyze turns—adapt ratios (e.g., more marksmen for damage-heavy rallies) and heroes (newer gens like Reina for all-source boosts). In rallies, prioritize stackable joiner skills (Jessie/Jasser) and captain proximity for more attempts.
- **Common Pitfalls**: Ignoring counters leads to quick frontline collapse; low-level skills get overwritten in rallies.
- **Event-Specific**: Bear Hunt favors marksmen-heavy for max per-turn output; Castle Battles need balanced for sustained turns.

This logic allows for strategic depth, where high Lethality overcomes Defense walls, and formations dictate turn longevity.