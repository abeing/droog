import actor
import engine


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


class ZombieDog(Creature):
    def __init__(self):
        super(ZombieDog, self).__init__('d', 'zombie dog', 2, 3, 1)


class COP(Creature):
    def __init__(self):
        super(COP, self).__init__('C', 'COP', 4, 1, 2)


def make_hero(name):
    hero = Creature('@', name, 2, 3, 2)
    hero._is_hero = True
    return hero
