Story and Environment
=====================

- Instead of taking place over seven days, takes place over seven hours to
  remove the need for food and water.
- Buildings are ruins, most will not have insides. There will be no multi-story
  buildings.

Creature Attributes
===================

Each creature has three base attributes: Strength, Dexterity and Constitution.
They range from +1 to +4 with only flavorful names visible in the UI.

| Attribute    | Low (+1) | Normal (+2) | High (+3) | Superhuman (+4)  |
|--------------|----------|-------------|-----------|------------------|
| Strength     |     Weak |           - |    Strong |        Herculean |
| Dexterity    |   Clumsy |           - |    Nimble |        Hermesian |
| Constitution |   Sickly |           - |      Hale |         Panacean |

**Strength** affects:
- melee offense
- melee defense

**Dexterity** affects:
- ranged offense
- melee defense
- action point efficiency

**Constitution** affects:
- blood clotting chance
- disease progress rate
- stun resistance

Items
=====

Weapons
-------

Weapons add to the offense role of an attack. Weapons inflict various effects
on their victims.

| Weapon            | Type   | Offense | Stun | Disease | Burning |
|-------------------|--------|---------|------|---------|---------|
| Unarmed           | Melee  |    0    |    X |       - |       - |
| Bite              | Melee  |   +1    |    - |       X |       - |
| Knife             | Melee  |   +2    |    - |       - |       - |
| Pistol            | Ranged |   +3    |    - |       - |       - |
| Rifle             | Ranged |   +4    |    - |       - |       - |
| Laser             | Ranged |   +5    |    - |       - |       X |

A creature that is **stunned** has his or her next turn moved back 20-50 minus
10 per their constitution score.

A **diseased** creature suffers a penalty to their constitution after a ten
minute incubation period. Once fully infected, the creature begins slowly
dying. The disease gets progressively worse, with no effect, three times every
hour times the victim's constitution.

**TODO**: Decide what burning does. It should be nasty.

Armor
-----

Armor are wearable items.

| Armor         | Effect                                 |
|---------------|----------------------------------------|
| Bionic        | Increases strength and dexterity       |
| Environmental | **TODO**: Some sort of survival effect |
| Battleweave   | Reduces damage roll by 2               |

Utility Items (WIP)
-------------------

**Local porter** allows the creature to teleport some distance at the cost of
some energy.

**Invisibility cloak** allows a creature to become invisible for some amount of
time for some amount of energy.

:question: **TODO** another item to make three because everything else is in
threes.

Consumables (WIP)
-----------------
- Ammunition
  - Pistol ammo : Needs research into a name.
  - Rifle ammo : Needs research into a name, fewer rounds to start and less
    common to find.
- Batteries
- Medicine Kit
  - Cures a wound.

Enemies
=======

**Zombies** are zombified humans and start with average stregth, dexterity and
constitution before recieving a bonus to one score. Their bites have a low (35%)
chance of causing disease. **TODO**: Give them a chance to spawn with an item.

**Zombie dogs** are zombified dogs and start with high dexterity, average
strength and low constitution. They can bite well but cannot use items. Their
bites have a higher chance (70%) of causing plague. **TODO**: They will also
move faster. 

**Cops** are robotic patrol officers. They start with high strength and
constitution but low dexterity. **TODO**: They have hardy armor and start 
with a weapon.

Combat Mechanics
================

Attacks
-------
Attacker rolls 1d6. The attack hits if the number is equal to or less than:

    3
    + Attacker Ability (Strength for melee, Dexterity for ranged)
    - Defender Ability (Strength for melee, Dexterity for ranged)
    + Weapon Offense
    - Ranged Penalty (1 for each 2 squares)

If an attack hits and defender is wounded, they die. If the defender does not have a wound, he or she rolls 1d4 and compares it to their constitution score.
On a result equal or less than the constitution, they gain a wound. Otherwise,
they die.

Time System
============

**Action Points** measure how much time an action that a creature may perform
takes. Each action point essentially amounts to one second. Highly dexterous
creatures receive a reduction in AP cost of actions. Slow creatures receive a
penalty (increase in AP cost).

| Dexterity | AP Modifier |
|-----------|-------------|
| Low       | -1          |
| Medium    | None        |
| High      | +1          |

Actions
-------

- Melee attack : 2 AP
- Ranged attack : 2 AP
- Aimed ranged attacks : 3 or 4 AP (undecided)
- Reload : ?? AP
- Walk one square orthogonally : 1 AP
- Walk one square diagonally : 1.5 AP (decimal part hidden from the player)
- Walk one square orhtogonally through rough terrain : 2 AP
- Walk one square diagonally through rought terrain : 3 AP
- Activate an item : ? AP

**TODO**: Check these movement costs.

Time Limit
----------

If 1 AP is 1 s then 7 hours is 60 s * 60 min/hr * 7 hr/game = 25,200 AP/game.

Is that too many? Let's look at Nethack:
- 40k-80k turns per game is reasonable
- < 30k to ascend is *fast*
- < 20k to ascend is *very fast*
- < 15k to ascend is attainable only by a few players
- 2,135 is the world record ascension
- 1.8M is the longest recorded game

In one day on nethack.alt.org:
- average failed game took 3,267.36 turns
- median failed game took 1,846 turns
- average ascension took 67,496 turns
- median ascension took 67,496 turns

At the moment a time limit of 25,200 AP seems reasonable at less then half a
nethack win.