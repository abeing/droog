import creature

hero = None


class Hero(creature.Creature):
    def __init__(self, name):
        """Creates the Hero."""
        super(Hero, self).__init__('@', name, 2, 2, 2)
        self.loc = None

    def __repr__(self):
        return "the Hero " + self.name


def initialize(name):
    """Create the hero object."""
    global hero
    hero = Hero(name)


def get_hero():
    """Return the hero object."""
    return hero
