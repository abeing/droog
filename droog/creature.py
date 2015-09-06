# Droog
# Copyright (C) 2015  Adam Miezianko
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""The creature module defines the general Creature class as well as individual
creature types."""

import logging
import random
from . import actor
from . import attack
from . import the
from . import world
from . import combat
from . import engine

LOG = logging.getLogger(__name__)


class Creature(actor.Actor):
    """The Creature class manages a creature's statistics and actions."""
    def __init__(self, glyph, name, initial_vowel=False):
        """Create a creature.

        The creature's initial attributes will all be two.

        glyph -- a single single character representation, for the map
        name -- a string representation, for elsewhere
        initial_vowel -- when true, use 'an', not 'a' in sentences
        """
        assert len(glyph) == 1
        self.glyph = glyph
        self.name = name
        self.initial_vowel = initial_vowel
        self._strength = 2
        self._dexterity = 2
        self._constitution = 2
        self.is_dead = False
        self.is_hero = False
        self.loc = (None, None)
        self.is_weakened = False
        self.is_hobbled = False
        self.is_stunned = False
        self.is_bleeding = False
        self.is_diseased = False
        self.blood = 10
        self.inventory = []
        super(Creature, self).__init__()

    def act(self):
        """Clear any conditions that clear at the start of the creature's turn.
        Currently that is stunned."""
        self.is_stunned = False

    def __repr__(self):
        """A string representation of the creature."""
        return self.name

    @property
    def strength(self):
        """Return creature's strength, modified by the weakened condition."""
        if self.is_weakened and self._strength > 1:
            return self._strength - 1
        return self._strength

    @strength.setter
    def strength(self, value):
        """Sets the creature's strength. If the value is invalid this will
        raise an AssertionError"""
        assert engine.is_valid_attribute(value)
        self._strength = value

    @property
    def dexterity(self):
        """Return creature's dexterity, modified by the hobbled consition."""
        if self.is_hobbled and self._dexterity > 1:
            return self._dexterity - 1
        return self._dexterity

    @dexterity.setter
    def dexterity(self, value):
        """Sets the creature's dexterity. If the value is invalid this will
        raise an AssertionError"""
        assert engine.is_valid_attribute(value)
        self._dexterity = value

    @property
    def constitution(self):
        """Creature's constitution."""
        if self.is_diseased and self._constitution > 1:
            return self._constitution - 1
        return self._constitution

    @constitution.setter
    def constitution(self, value):
        """Sets the creature's dexterity. If the value is invalid this will
        raise an AssertionError"""
        assert engine.is_valid_attribute(value)
        self._constitution = value


class Zombie(Creature):
    """Zombie creature."""
    def __init__(self, improvement=None):
        """Create a zombie.

        A zombie uses the average stat array and then raises one stat to three.
        improvement -- one of 'strength', 'dex', or 'con' to improve
        """
        strength = 2
        dexterity = 2
        constitution = 2
        if not improvement:
            improvement = random.choice(['strength', 'dexterity',
                                         'constitution'])
        name = "zombie"
        if improvement == 'strength':
            strength = 3
            name = "strong zombie"
        if improvement == 'dexterity':
            dexterity = 3
            name = "nimble zombie"
        if improvement == 'constitution':
            constitution = 3
            name = "hale zombie"
        self.attacks = [attack.make_bite(), attack.make_unarmed()]
        self.sense_range = 15
        super(Zombie, self).__init__('Z', name)
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution

    def act(self):
        """Zombies use the following decision tree:

        1) If adjacent to the hero, bite her.
        2) If within 15 steps of the hero, move towards her.
        3) Otherwise, move randomly."""
        super(Zombie, self).act()
        return ai_act(self)


class ZombieDog(Creature):
    """Zombie dog."""
    def __init__(self):
        self.attacks = [attack.make_bite(effectiveness=70)]
        self.sense_range = 30
        super(ZombieDog, self).__init__('d', 'zombie dog')
        self.strength = 2
        self.dexterity = 3
        self.constitution = 1

    def act(self):
        """Zombie dogs use the following decision tree:

        1) If adjacent to the hero, bite her.
        2) If within 30 steps of the hero, move towards her.
        3) Otherwise, move randomly."""
        super(ZombieDog, self).act()
        return ai_act(self)


class Cop(Creature):
    """Cop."""
    def __init__(self):
        super(Cop, self).__init__('C', 'cop')
        self.attacks = []
        self.sense_range = 1
        self.strength = 3
        self.dexterity = 1
        self.constitution = 3

    def act(self):
        """Cops use the following decision tree:

        1) If adjacent to the hero, punch her.
        2) If within 30 steps of the hero, move towards her.
        3) Otherwise, move randomly."""
        super(Cop, self).act()
        return 6


def ai_act(creature):
    """Act as a creature.

    Creatures use the following decision tree:

    1) If adjacent to the hero, bite her.
    2) If within 15 steps of the hero, move towards her.
    3) Otherwise, move randomly.
    """
    assert creature.loc

    dist = creature.loc.distance_to(the.world.hero_location)

    LOG.info("%r is %r from the hero.", creature.name, dist)

    # 1) If adjacent to the hero, bite her.
    if dist < 2:
        return combat.attack(creature, the.hero,
                             random.choice(creature.attacks))

    # 2) If within 15 steps of the hero, move towards her.
    elif dist < creature.sense_range:
        delta = creature.loc.delta_to(the.world.hero_location)

    # 3) Otherwise, move randomly.
    else:
        delta = world.random_delta()

    LOG.info("%r wants to move from %r by %r.", creature.name,
             creature.loc, delta)
    cost = the.world.move_creature(creature.loc, delta)
    if not cost == 0:
        return cost
    return 6  # If the creature fails to move, it stands around a while


def create_from_glyph(glyph):
    """Create a creature based on a glyph."""
    monster = None
    if glyph == 'Z':
        monster = Zombie()
    if glyph == 'd':
        monster = ZombieDog()
    if glyph == 'C':
        monster = Cop()
    return monster
