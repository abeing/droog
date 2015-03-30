"""Droog - Item

The item module defines the general Item class as well as individual items.
"""

import logging
import attack

log = logging.getLogger(__name__)


class Item(object):
    """The Item class represents an item that can be in the game world or
    in a creature's inventory."""
    def __init__(self, glyph, name, article='a', attack=None):
        """Create an item.

        glyph -- a single single character representation, for the map
        name -- a string representation, for the inventory
        initial_vowel -- when true, use 'an', not 'a' in sentences
        """
        self.glyph = glyph
        self._name = name
        self._article = article
        self.attack = attack

    @property
    def name(self):
        return "%s %s" % (self._article, self._name)


def make_knife():
    """Create a knife object."""
    knife_attack = attack.make_knife()
    return Item(')', 'knife', attack=knife_attack)
