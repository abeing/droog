import actor


class Creature(actor.Actor):
    def __init__(self, glyph, name, str, dex, con):
        """Creates a creature."""
        self.glyph = glyph
        self.name = name
        self.str = str
        self.dex = dex
        self.con = con
        self._is_hero = False
        self.loc = None
        super(Creature, self).__init__(self.dex)
        self.act_func = default_ai

    def __repr__(self):
        if self._is_hero:
            return "the Hero " + self.name
        return "creature named " + self.name


def make_zombie():
    return Creature('Z', "a zombie", 2, 2, 2)


def make_dog():
    return Creature('d', "a zombie dog", 2, 3, 1)


def make_cop():
    return Creature('C', "a COP", 4, 1, 2)


def default_ai():
    """Does nothing."""
    return 8
