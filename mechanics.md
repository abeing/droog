Story and Environment
=====================

- Instead of taking place over seven days, takes place over seven hours to
  remove the need for food and water.
- Buildings are ruins, most will not have insides. There will be no multi-story
  buildings.

Creature Statistics
===================

Each creature has three base statistics: Strength, Dexterity and Constitution.

Statistics range in value:
  - None (0)
  - Low (+1)
  - Average (+2)
  - High (+3)
  - Superhuman (+4)

Strength
  - Melee chance to hit
  - Melee damage
  - Encumbrance limit

Dexterity
  - Ranged chance to hit
  - Melee dodge

Constitution
  - Resistance to wounds
  - Wounds to die

Items
=====

Weapons
-------
- Fist : Melee, +1 Damage
- Knife : Melee, +2 Damage
- Pistol : Ranged, +1 Attack, +4 Damage
- Rifle : Ranged, +2 Attack, +4 Damage
- Lazer : Ranged, +1 Attack, +3 Damage, Ignores Armor

Armor
-----
- Bionic : Increases strength and dexterity
- :question: Environmental : ???
- Battle Armor : Reduces damage roll by 2

Utility Items
-------------

**Local porter** allows the creature to teleport some distance at the cost of
some energy.

**Invisibility cloak** allows a creature to become invisible for some amount of
time for some amount of energy.

:question: **TODO** another item to make three because everything else is in
threes.

Consumables
-----------
- Ammunition
  - Pistol ammo : Needs research into a name.
  - Rifle ammo : Needs research into a name, fewer rounds to start and less
    common to find.
- Batteries
- Medicine
  - First aid (balm | injection | potion | kit) : Cures wounds. Probably over
    time.

Enemies
=======

**Zombies** are zombified humans and start with average stregth, dexterity and
constitution before recieving a bonus to one score or with some lowish chance
(which increases over time) an item. *They can bite poorly*. Their bites have a
low chance of causing plague.

**Zombie dogs** are zombified dogs and start with high dexterity, average
strength and low constitution. They can bite well but cannot use items. They
will also move faster. Bites have a higher chance of causing plague.

**Cops** are robotic patrol officers. They have hardy armor and start with a
weapon. Other names I've considered: RoboCop, Ropal (Robotic Pal)

Combat Mechanics
================

Ranged Attacks
--------------
- To hit: 1d6 + Dexterity Bonus + Aiming Bonus - Range Penalty vs Size
  - Aiming Bonus : from weapon, doubled if using aimed shot action
  - Range Penalty : something like -1 per 5 or 10 squares as per weapon
  - Size : 4 to hit a human-sized creature, 2 to hit a COP, 6 to hit a dog
- Damage: 1d6 + Weapon Damage - Damage Reduction vs 2 * Con
  - Weapon damage : from the weapon
  - Damage reduction : from the armor or COP
  - If exceeds 2 * Con then target takes a wound
  - If exceeds 4 * Con then target dies

Melee Attacks
-------------
- To hit: 1d6 + Melee Stat - Target Melee Stat vs Size
  - Melee stat is the higher of strength or dexterity
- Damage: 1d6 + Strength + Weapon Damage - Damage Reduction vs Con * 2
  - If exceeds 2 * Con then target takes a wound
  - If exceeds 4 * Con then target dies

Time System
============

**Action Points** measure how much time an action that a creature may perform
takes. Each action point essentially amounts to one second. Highly dextrous
creatures recieve a reduction in AP cost of actions. Slow creatures recieve a
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
- Reload : ? AP
- Walk one square orthogonally : 1 AP
- Walk one square diagonally : 1.5 AP (decimal part hidden from the player)
- Walk one square orhtogonally through rough terrain : 2 AP
- Walk one square diagonally through rought terrain : 3 AP
- Activate an item : ? AP

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