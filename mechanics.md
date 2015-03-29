Story and Environment
=====================

- Instead of taking place over seven days, takes place over seven hours to
  remove the need for food and water.
- Buildings are ruins, most will not have insides. There will be no multi-story
  buildings.

Creature Attributes
===================

Each creature has three base attributes: Strength, Dexterity and Constitution.

Attributes range in value:
  - None (0)
  - Low (+1)
  - Average (+2)
  - High (+3)
  - Superhuman (+4)

Strength
  - Melee offense
  - Melee defense
  - Encumbrance limit :question:

Dexterity
  - Ranged offense
  - Melee defense
  - Action point efficiency

Constitution
  - Resistance to wounds :question:
  - Wounds to die

Items
=====

Weapons
-------

Weapons add to the offense role of an attack. All weapons do one wound of
damage on a successful attack. Wounds effect one of the core attributes. A
wound to strength inflicts the weakened condition. A wound to dexterity
inflicts the hobbled condition. A wound to constitution inflicts a condition
depending on the weapon.

| Weapon | Type   | Offense | Special Damage |
|--------|--------|---------|----------------|
| Fist   | Melee  |    0    | Daze           |
| Bite   | Melee  |   +1    | Disease        |
| Knife  | Melee  |   +2    | Bleed          |
| Pistol | Ranged |   +3    | Bleed          |
| Rifle  | Ranged |   +4    | Bleed          |
| Laser  | Ranged |   +5    | Burning        |

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
- Medicine Kit
  - Bandages remove the bleeding condition
  - Splints remove the hobbled condition
  - Serum delays the diseased condition

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
- Attacker rolls 1d6 + weapon offense + dexterity - range penalty :question: - defense 
  - Range Penalty : something like -1 per 5 or 10 squares as per weapon

Melee Attacks
-------------
- Melee offense is the higher of the attacker's strength and dexterity.
- Melee defense is the higher of the defender's strength and dexterity.
- Attacker rolls 1d6 + weapon offense + melee offense - melee defense
- On a 4 or higher, randomly determine one of the defenders stats, then:
  - For strength, apply weakened condition
  - For dexterity, apply hobbled condition
  - For constitution, apply the weapon's special damage
- On a 3 or less, determine a miss reason by adding to a list:
  - One "dodge" for each dexterity point the defender has.
  - One "parry" for each strength point the defender has.
  - Two "miss"
  - Choosing one of those.

Damage
------

If attack rolled 6 or more, 1 wound to a random stat.

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