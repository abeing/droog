"""The creature module defines the general Creature class as well as individual
creature types."""

import actor
import engine
import random
import the
import world


class Creature(actor.Actor):
    """The Creature class manages a creature's statistics and actions."""
    def __init__(self, glyph, name, initial_vowel=False):
        """Creates a creature."""
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
        super(Creature, self).__init__()

    def act(self):
        """The creature acts. This placeholder method raises a
        NotImplementedError as there is no default creature action."""
        raise NotImplementedError("Creature.act() should be overridden.")

    def __repr__(self):
        """A string representation of the creature."""
        return self.name

    @property
    def strength(self):
        """Creature's strength."""
        return self._strength

    @strength.setter
    def strength(self, value):
        """Sets the creature's strength. If the value is invalid this will
        raise an AssertionError"""
        assert engine.is_valid_attribute(value)
        self._strength = value

    @property
    def dexterity(self):
        """Creature's dexterity."""
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
        return self._constitution

    @constitution.setter
    def constitution(self, value):
        """Sets the creature's dexterity. If the value is invalid this will
        raise an AssertionError"""
        assert engine.is_valid_attribute(value)
        self._constitution = value


class Zombie(Creature):
    """Zombie creature."""
    def __init__(self):
        super(Zombie, self).__init__('Z', 'zombie')

    def act(self):
        """Zombies use the following decision tree:

        1) If adjacent to the hero, bite her.
        2) If within 15 steps of the hero, move towards her.
        3) Otherwise, move randomly."""
        if self.loc:
            (old_y, old_x) = self.loc
            (hero_y, hero_x) = the.world.hero_location

            # 1) If adjacent to the hero, bite her.
            if world.distance_between(hero_y, hero_x, old_y, old_x) == 1:
                return engine.attack_bite(self, the.hero)

            # 2) If within 15 steps of the hero, move towards her.
            elif world.distance_between(hero_y, hero_x, old_y, old_x) < 15:
                delta_y = 1 if (hero_y - old_y > 0) else -1
                delta_x = 1 if (hero_x - old_x > 0) else -1

            # 3) Otherwise, move randomly.
            else:
                delta_y = random.choice([-1, 0, 1])
                delta_x = random.choice([-1, 0, 1])
            cost = the.world.move_creature(old_y, old_x, delta_y, delta_x)
            if not cost == 0:
                return cost
        return 6  # If the creature fails to move, it stands around a while
