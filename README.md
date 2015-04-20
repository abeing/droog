Droog
=====

Droog is a short, traditional roguelike, with brutal combat and limited
resources, set in a post-apocalyptic, zombified, ruined city.

Here's what we mean by this:
- A **short** game can be _won_ in under ten hours. Many will be shorter than
that!
- A **traditional roguelike** features permanent death, randomly-generated maps,
and turn-based action.
- **Brutal combat** means death is easy, healing is hard and hit points aren't
everything. In fact, in Droog, they don't exist.
- With **limited resources**, every item counts and every item is useful. There
aren't many of them, but finding one will feel great.
- A **post-apocalyptic, zombified, ruined city** is what it says on the tin.
Danger lurks behind every corner.

Installation
============

Once you have the git repository on your local machine, you can either use
pip to install to site-package or run the game from within the repository.

To install with pip:

```
sudo pip install .
```

To run without installing:

```
python -m droog.main
```

Make sure that you are above the droog source directory.

Character Creation
==================

When you start a new game of Droog, you will be asked to fill in certain parts
of Commander Splinter's narrative. The choices set your initial attributes and
starting equipment.

## Attributes

**Strong** characters are more effective at attacking with the knife or unarmed
attacks. There is no encumbrance system.

**Nimble** characters are more efficient in maneuvering and have better aim
with guns.

**Hale** characters resist the effects of poison and disease better. They also
bleed more slowly.

## Weapons

The **pistol** is accurate at medium ranges and has good zombie-stopping power.

The **rifle** is accurate at long ranges and has good zombie-stopping power.

## Other Items

The **local porter** can teleport the user short distances at the expense of
some battery power.

The **battery** powers various other equipment but does not have many uses by
itself.

**Grenades** don't exist. Or, they won't exist when other items exist, as right
now you only get three knives anyhow.

Controls
========

You move your hero using the standard vi keys along with diagonals.

```
y  k  u
 \ | /
h--@--l
 / | \
b  j  n
```

Attack using a currently-equipped melee weapon or using unarmed strikes by
moving into a space occupied by another creature.

## Inventory management

d - drop

## Other commands

/ look

m - message history

q - quit

? - help

The World
=========

The town of Baiersbronn is a relatively nondescript town in the Schwarzwald,
with one exception: it is the home of the mainframe running the artificial
intelligence which has engineering a bio virus into our authomated farms,
causing wide-spread zombism amonst humans.

Seen around Baiersbronn are a number of hostile creatures that protect the
mainframe from the hero.

**Zombies** are zombified humans. Their bites have a chance of spreading
zombism to the hero. They can pick up and use items. A zombie with a gun is
a dangerous thing.

**Zombie dogs** are zombified dogs with a deadly bite. They can outrun most
people and use scent to track their prey.
