"""Droog - Tile

This module provides the Tile class representing map tiles and various factory
functions to create different types of tiles.
"""


class Tile(object):
    """Representation of a map tile."""
    def __init__(self, glyph, description, walkable):
        self.glyph = glyph
        self.description = description
        self.walkable = walkable
        self.creature = None
        self.items = []
        self._seen = 0
        self.was_seen = False

    @property
    def seen(self):
        """Seen property getter, to support setter behavior."""
        return self._seen

    @seen.setter
    def seen(self, seen):
        """Set this tile to currently being seen, which also will set its
        was_seen for fog of war purposes."""
        self._seen = seen
        if seen:
            self.was_seen = True


def make_street():
    """Factory function to create a street tile."""
    return Tile('*', "a street", True)


def make_empty():
    """Factory function to create an empty tile."""
    return Tile('.', "open space", True)


def make_shield():
    """Factory function to create a shield tile."""
    return Tile('~', "the shield", False)


def make_shield_generator():
    """Factory function to create a shield generator tile."""
    return Tile('G', "the shield generator", False)
