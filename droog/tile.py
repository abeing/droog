"""Droog - Tile

Provides a Tile class and functions to create certain types of tiles."""

class Tile(object):
    """Representation of a map tile."""
    def __init__(self, glyph, description, walkable):
        self.glyph = glyph
        self.description = description
        self.walkable = walkable
        self.creature = None


def make_street():
    """Create a new street tile."""
    return Tile('#', "a street", True)


def make_empty():
    """Create a new empty tile."""
    return Tile(' ', "open space", True)


def make_shield():
    """Create a new shield tile."""
    return Tile('~', "the shield", False)


def make_shield_generator():
    """Create a new shield generator tile."""
    return Tile('G', "the shield generator", False)
