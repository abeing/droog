"""The creature module defines the general Creature class as well as individual
creature types."""

import logging
import actor
import engine
import random
import the
import world
import attack

log = logging.getLogger(__name__)


class Creature(actor.Actor):
    """The Creature class manages a creature's statistics and actions."""
    def __init__(self, glyph, name, initial_vowel=False, str=2, dex=2, con=2):
        """Create a creature.

        glyph -- a single single character representation, for the map
        name -- a string representation, for elsewhere
        initial_vowel -- when true, use 'an', not 'a' in sentences
        str -- strength
        dex -- dexterity
        con -- constitution
        """
        assert len(glyph) == 1
        self.glyph = glyph
        self.name = name
        self.initial_vowel = initial_vowel
        self._strength = str
        self._dexterity = dex
        self._constitution = con
        self.is_dead = False
        self.is_hero = False
        self.loc = (None, None)
        self.is_weakened = False
        self.is_hobbled = False
        self.is_bleeding = False
        self.is_dazed = False
        self.is_diseased = False
        self.is_burning = False
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
        """Create a zombie.

        A zombie uses the average stat array and then raises one stat to three.
        """
        str = 2
        dex = 2
        con = 2
        improvement = random.choice(['str', 'dex', 'con'])
        if improvement == 'str':
            str = 3
            name = "strong zombie"
        if improvement == 'dex':
            dex = 3
            name = "fast zombie"
        if improvement == 'con':
            con = 3
            name = "hardy zombie"
        self.weapons = [attack.make_bite(), attack.make_unarmed()]
        super(Zombie, self).__init__('Z', name, str=str, dex=dex, con=con)

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
                return engine.attack(self, the.hero,
                                     random.choice(self.weapons))

            # 2) If within 15 steps of the hero, move towards her.
            elif world.distance_between(hero_y, hero_x, old_y, old_x) < 15:
                delta_y = 1 if (hero_y - old_y > 0) else -1
                delta_x = 1 if (hero_x - old_x > 0) else -1

            # 3) Otherwise, move randomly.
            else:
                delta_y = random.choice([-1, 0, 1])
                delta_x = random.choice([-1, 0, 1])

            log.info("%r wants to move from (%r, %r) by (%r, %r).",
                     self.name, old_y, old_x, delta_y, delta_x)
            cost = the.world.move_creature(old_y, old_x, delta_y, delta_x)
            if not cost == 0:
                return cost
        return 6  # If the creature fails to move, it stands around a while


class ZombieDog(Creature):
    """Zombie dog."""
    def __init__(self):
        self.weapon = attack.make_bite()
        super(ZombieDog, self).__init__('d', 'zombie dog', str=2, dex=3, con=1)

    def act(self):
        """Zombie dogs use the following decision tree:

        1) If adjacent to the hero, bite her.
        2) If within 30 steps of the hero, move towards her.
        3) Otherwise, move randomly."""
        if self.loc:
            (old_y, old_x) = self.loc
            log
            (hero_y, hero_x) = the.world.hero_location

            # 1) If adjacant to the hero, bite her.
            if world.distance_between(hero_y, hero_x, old_y, old_x) == 1:
                return engine.attack(self, the.hero, self.weapon)

            # 2) If within 30 steps of the hero, move towards her.
            elif world.distance_between(hero_y, hero_x, old_y, old_x) < 30:
                delta_y = 1 if (hero_y - old_y > 0) else -1
                delta_x = 1 if (hero_x - old_x > 0) else -1

            # 3) Otherwise, move randomly.
            else:
                delta_y = random.choice([-1, 0, 1])
                delta_x = random.choice([-1, 0, 1])

            log.info("%r wants to move from (%r, %r) by (%r, %r).",
                     self.name, old_y, old_x, delta_y, delta_x)
            cost = the.world.move_creature(old_y, old_x, delta_y, delta_x)
            if not cost == 0:
                return cost
        return 6  # If the creature fails to move, it stands areound a while.


class Cop(Creature):
    """Cop."""
    def __init__(self):
        super(Cop, self).__init__('C', 'cop', str=3, dex=1, con=3)

    def act(self):
        """Cops use the following decision tree:

        1) If adjacent to the hero, punch her.
        2) If within 30 steps of the hero, move towards her.
        3) Otherwise, move randomly."""
        if self.loc:
            (old_y, old_x) = self.loc
            (hero_y, hero_x) = the.world.hero_location

            # 1) If adjacant to the hero, bite her.
            if world.distance_between(hero_y, hero_x, old_y, old_x) == 1:
                pass  # Cops at the moment don't have an attck.

            # 2) If within 30 steps of the hero, move towards her.
            elif world.distance_between(hero_y, hero_x, old_y, old_x) < 30:
                delta_y = 1 if (hero_y - old_y > 0) else -1
                delta_x = 1 if (hero_x - old_x > 0) else -1

            # 3) Otherwise, move randomly.
            else:
                delta_y = random.choice([-1, 0, 1])
                delta_x = random.choice([-1, 0, 1])

            log.info("%r wants to move from (%r, %r) by (%r, %r).",
                     self.name, old_y, old_x, delta_y, delta_x)
            cost = the.world.move_creature(old_y, old_x, delta_y, delta_x)
            if not cost == 0:
                return cost
        return 6  # If the creature fails to move, it stands areound a while.
