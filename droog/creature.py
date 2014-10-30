import actor
import engine
import random
import the


class Creature(actor.Actor):
    def __init__(self, glyph, name, str, dex, con):
        """Creates a creature."""
        assert(len(glyph) == 1)
        self.glyph = glyph
        self.name = name
        assert(engine.is_valid_attribute(str))
        self.str = str
        assert(engine.is_valid_attribute(dex))
        self.dex = dex
        assert(engine.is_valid_attribute(con))
        self.con = con
        self.loc = None
        super(Creature, self).__init__()

    def act(self):
        """The creature acts. This placeholder method raises a
        NotImplementedError as there is no default creature action."""
        raise NotImplementedError("Creature.act() should be overridden.")

    def __repr__(self):
        """A string representation of the creature."""
        return self.name


class Zombie(Creature):
    def __init__(self):
        super(Zombie, self).__init__('Z', 'zombie', 2, 2, 2)

    def act(self):
        """Zombies use the following decision tree:

        1) If adjacent to the hero, bite her.
        2) If within 15 steps of the hero, move towards her.
        3) Otherwise, move randomly."""
        if self.loc:
            (old_y, old_x) = self.loc
            (hero_y, hero_x) = the.world.hero_location

            # 1) If adjacent to the hero, bite her.
            if the.world.distance_between(hero_y, hero_x, old_y, old_x) == 1:
                return engine.attack_bite(self, the.hero)

            # 2) If within 15 steps of the hero, move towards her.
            elif the.world.distance_between(hero_y, hero_x, old_y, old_x) < 15:
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


class ZombieDog(Creature):
    def __init__(self):
        super(ZombieDog, self).__init__('d', 'zombie dog', 2, 3, 1)


class COP(Creature):
    def __init__(self):
        super(COP, self).__init__('C', 'COP', 4, 1, 2)
