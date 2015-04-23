# Droog
# Copyright (C) 2015  Adam Miezianko
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""Droog - Tile

This module provides the Tile class representing map tiles and various factory
functions to create different types of tiles.
"""


class Tile(object):
    """Representation of a map tile."""
    def __init__(self, glyph, description, walkable, color=0):
        self.glyph = glyph
        self.color = color
        self.description = description
        self._walkable = walkable
        self.creature = None
        self.items = []
        self._seen = False
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

    @property
    def walkable(self):
        """Returns True if the tile can be traversed by walking."""
        return self._walkable and not self.creature

    @property
    def transparent(self):
        return self._walkable


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


def make_tree():
    """Create a tree tile."""
    return Tile('%', "a tree", False, color=2)


def make_wall():
    """Create a wall tile."""
    return Tile('#', "a wall", False)


def make_floor():
    """Create a floor tile."""
    return Tile(',', "a floor", True)
