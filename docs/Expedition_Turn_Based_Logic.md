# **Expedition Battle Turn-Based Combat**

# **Turn-Based Combat Simulation Overview**

In Whiteout Survival, battles during marches or rallies (known as Expedition battles) are resolved through a hidden turn-based simulation on the server. When troops reach their target, the game instantly calculates the outcome as if a turn-by-turn fight occurred, though players don't watch it in real time.

In expedition combat, each turn represents one second of fighting. During a turn, both armies act simultaneously, exchanging attacks and skill effects. After computing actions and tallying damage, the next turn begins. This cycle continues until one side's troops are defeated, at which point the battle ends and generates a report. Because this simulation runs server-side in a split second, players only see the final battle report when their march or rally hits, making it appear instant.

This report captures the outcome of a multi-turn combat scenario that played out behind the scenes.

# **Hero Skills and Turn Timing**

Each hero's Expedition skills are integrated into this turn-based simulation. The game follows a "1 turn = 1 second" rule for all skill descriptions. When a hero skill says "triggers every X seconds," it activates on that corresponding turn interval.

```rust
Example 1:

Philly originally had an expedition skill that healed allies every 12 turns, meaning a
heal would occur on turn 12 and every 12 turns afterward. Skills with duration effects
translate directly into turns as well.

Example 2:

Greg's "Sword of Justice" skill provides a damage boost for 3 turns when activated,
while his "Deterrence of Law" debuff reduces enemy damage for 2 turns.

Example 3:

Flint, has a burn effect that ignites enemies, causing extra damage each turn for 3
turns after activation. The game tracks all these timed effects within the turn by turn
simulation, advancing a counter for each skill. When a skill's trigger turn arrives or
its duration expires, the engine applies or removes the effect accordingly.
```

All hero expedition skills, whether buffs, debuffs, or heals are calculated during their appropriate combat turns, even though players don't see these turns in real time.

# **Combat Sequence and Application of Effects**

Under the hood, an expedition battle unfolds in a repeated sequence of turns until conclusion. Each turn’s logic includes targeting, attacks, and the resolution of any skill effects:

1. Targeting and Action Selection:

    At the start of a turn, units on both sides pick targets and prepare attacks. By default, troops attack the opposing frontline first (e.g. infantry in front, then move to the next row once the front line is gone). Certain troop types or hero skills can override this.

    For example, high-level Lancers or specific skills might strike the enemy backline directly. Heroes present in the formation will also “use” any expedition skill effects that are due this turn.

    (Many hero skills are passive or chance based, meaning each turn every attack might roll a chance to trigger an effect like a stun or extra damage. Others are cyclic, activating on a fixed turn interval )

    Both sides effectively declare their actions simultaneously at the beginning of the turn .

2. Skill Effects and Damage Resolution:

    Next, the game applies any buffs or debuffs that occur at this turn before calculating damage.

    For example, if a hero’s skill provides a buff starting on turn N, that bonus will apply to attacks on turn N and remain for its duration (e.g. a 3-turn attack boost would apply on turn N and the next two turns).  Similarly, if an attack this turn triggers a debuff on the enemy (say, reducing their damage or stunning a unit for 1 turn), that debuff will affect the appropriate units immediately and/or in the subsequent turn.

    The engine then calculates all damage for the turn, accounting for each troop type’s Attack vs. the target’s Defense (troops must chew through the enemy’s defense stat before dealing health damage). Because combat is simultaneous, both armies inflict losses on each other within the same turn before any unit removal happens .

    After all attacks are processed and the damage from this turn is finalized, casualties are assigned: troops that lost all defense and health are removed from the battle. If a hero’s skill provides healing or shields on a turn, those would also be applied at the appropriate point, potentially keeping some troops alive longer (allowing them to fight into later turns).

3. Turn Transition:

    Once damage and effects from that round are resolved, the turn ends. The game checks if either army has been completely wiped out. If not, any ongoing status effects are updated for the next turn, durations on buffs/debuffs tick down by one, and any “per turn” damage over time effects deal their damage each new turn.

    The next turn then begins with the remaining forces. This iterative process continues, turn by turn, until one side’s troops are all defeated (or in rare cases, an encounter specific turn limit is reached).

    At that moment, the simulation stops and the victor is declared. All of this happens virtually instantaneously in the backend; by the time you open the battle report, the server has already played out 5, 10, 20+ turns of combat and applied every skill effect accordingly.


All hero expedition skills are applied regardless of whether you can “see” them in the report. The battle report will show aggregate stats (troop losses, total damage, etc.), but heroes’ contributions (buffs, bonus damage, etc.) occur independently of those summary stats. In a Rally with multiple people, even more skills come into play: the rally leader brings three heroes (up to 9 expedition skills), and additional rally participants each contribute the primary skill of their lead hero to the fight.

The game’s engine factors in all these skills and their turn-based effects during the simulation. For example, in a big rally the lead hero might cycle a damage buff every few turns while another hero’s skill periodically stuns enemies and the backend will manage each of those timed effects turn by turn before producing the final outcome.

# **Number of Turns and Influencing Factors**

There is no fixed number of turns in a standard expedition battle.  The length is dynamically determined by the combatants’ strength, defenses, and any prolonging effects. The fight simply continues until one side runs out of troops .

If one army massively overpowers the other, the battle might last only a handful of turns (e.g. a strong march wiping out a weak target in 2–3 seconds/turns). In a more evenly matched or larger-scale battle, the turn count naturally increases because it takes longer to grind down all enemy units.

Community discussions confirm that “quite some turns” can occur in a normal fight, often well into double digits . For example, the fact that (prior to rework) Philly’s heal skill triggered on turn 12 indicates battles could regularly last a dozen or more rounds and savvy players with durable infantry could survive long enough to leverage that heal.

Each additional second/turn allows more hero skills to fire off; a tankier formation might purposely extend the fight duration to gain the advantage from buffs, heals or multiple skill cycles.

Several factors influence how many turns you’ll get in a battle:

- Troop Durability:

    High defense and health on frontline troops (like Infantry) means they survive more attack rounds, extending the battle. This is why having enough infantry “meat shield” can buy time for your damage dealers and for supportive hero skills to make an impact in later turns . Healing or damage-reduction skills can also prolong fights by keeping troops alive through additional cycles.

- Damage Output:

    Conversely, massive attack power or stacked damage buffs will end fights faster by killing enemy units quicker. Critical burst damage or strong per-turn damage effects (burns, poison, etc.) can shorten the number of turns needed to defeat the enemy.

- Hero Skill Timings:

    If your strategy relies on a big skill that activates on a specific turn (say a huge buff every 10th turn), the battle needs to last that long for it to matter. Most expedition skills are designed to have an impact within a reasonable timeframe. (Very long intervals have become uncommon – for instance, Philly’s 12-turn heal was considered too slow and was reworked in a later update.) In practice, many skills have interval or duration in the 2–5 turn range, ensuring they influence most battles.

- Rally vs. Solo:

    Rally battles with multiple armies tend to involve larger troop counts and more heroes, which can increase turn count. The added buff/debuff skills might also slow down how quickly damage is dealt (for example, enemy debuffs reducing their damage could make your troops survive longer, yielding more turns of combat before victory). Still, the fundamental rule remains: the battle runs until all of one side’s troops are gone, whether that takes 5 turns or 25 turns.


Certain PvE events might impose implicit limits on battle length, but even there the exact turns are not clearly exposed. For example, in the Alliance Bear Hunt event, players have observed that your rally will eventually end without killing the bear. This is usually because the bear decimates your troops, not because of an arbitrary timer.  Though the precise number of turns a bear rally lasts isn’t publicly known or shown in reports.

This uncertainty makes it hard to gauge heroes like Renee who have skills tied to specific turn intervals in that context.  Generally, outside of special PvE mechanics, there is no hard turn limit in normal PvP/PvE expedition battles; they last as long as needed for a decisive outcome.

In practice, most standard marches or rallies last on the order of seconds (often under 15–20 turns) because casualties mount quickly each round. The key takeaway is that the game’s engine plays out however many turns are required given the two sides’ stats and skills… fast-forwarding a full turn-based combat sequence and only then delivering the result to the players.

# **Conclusion**

- Behind the scenes, Whiteout Survival’s combat engine uses a turn-based logic to simulate expedition battles in an instant.
- Turn by turn, it calculates attacks, hero skill activations, buffs/debuffs, and casualties, essentially compressing what would be a many seconds long battle into a split second resolution. Hero skills that trigger every X turns or last Y turns are accounted for in this simulation, with their effects applied across the appropriate turns before the final outcome is determined.
- The number of turns the battle runs is dynamic, a function of troop strength, defenses, and skill effects rather than a fixed duration. By the time you read a battle report, the game has already processed a complete round by round battle scenario (e.g. 10 rounds of fighting), even though to you it felt instantaneous.
- In summary, the expedition battle system behaves like a fast-forwarded turn-based RPG battle: both sides trade blows in simulated seconds, applying all buffs, debuffs, and special skills in order, until one army falls. This ensures that all the strategic elements (formations, hero skills, troop stats) contribute to the result, even if you don’t watch the turns play out in real time.
- The design gives players the depth of turn-based combat calculation with the convenience of instant battle results… a win-win that delivers complex outcomes without making you sit through the fight.
