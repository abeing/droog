import actor

class Creature(actor.Actor):
    def __init__(self, glyph, name, str, dex, con):
        """Creates a creature."""
        self.glyph = glyph
        self.name = name
        self.str = str 
        self.dex = dex 
        self.con = con
        ap_max = 2 * self.dex
        super(Creature, self).__init__(ap_max, ap_max)

    def __repr__(self):
        return "creature named " + self.name

def make_hero(name):
    return Creature('@', name, 2, 3, 2)


def make_zombie():
    return Creature('Z', "a zombie", 2, 2, 2)


def make_dog():
    return Creature('d', "a zombie dog", 2, 3, 1)


def make_cop():
    return Creature('C', "a COP", 4, 1, 2)
