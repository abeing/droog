class Tile:
    """Representation of a map tile."""
    def __init__(self, glyph, description, walkable):
        self.glyph = glyph
        self.description = description
        self.walkable = walkable
        self.creature = None


def make_street():
    return Tile('#', "a street", True)


def make_empty():
    return Tile(' ', "open space", True)


def make_shield():
    return Tile('~', "the shield", False)


def make_shield_generator():
    return Tile('G', "the shield generator", False)
