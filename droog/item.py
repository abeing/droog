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

"""Droog - Item

The item module defines the general Item class as well as individual items.
"""

import logging
from . import attack as attack_

LOG = logging.getLogger(__name__)


class Item(object):
    """The Item class represents an item that can be in the game world or
    in a creature's inventory."""
    def __init__(self, glyph, name, article='a', attack=None, ammo_capacity=0):
        """Create an item.

        glyph -- a single single character representation, for the map
        name -- a string representation, for the inventory
        initial_vowel -- when true, use 'an', not 'a' in sentences
        attack -- how this item is used as a weapon, or None if it cannot be
        ammo_capacity -- how many units of ammunition this item can store; new
          items start with full ammunition.
        """
        self.glyph = glyph
        self._name = name
        self._article = article
        self.attack = attack
        self.ammo_capacity = ammo_capacity
        self.ammo = ammo_capacity

    @property
    def name(self):
        """The name of this item, with appropriate article."""
        return "%s %s" % (self._article, self._name)

    def __repr__(self):
        """Return string representation."""
        return self.name


def make_knife():
    """Create a knife object."""
    knife_attack = attack_.make_knife()
    return Item(')', 'knife', attack=knife_attack)


def make_pistol():
    """Create a pistol item."""
    return Item(')', '9mm pistol', attack=attack_.make_pistol(),
                ammo_capacity=6)


def make_porter():
    """Create a porter item."""
    return Item('=', 'porter')


def make_battery():
    """Create a battery ite."""
    return Item('=', 'battery')


def make_clip():
    """Create a 9mm pistol clip."""
    return Item('=', '9mm clip')
