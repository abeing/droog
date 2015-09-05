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

"""Droog Engine.

This module contains functions for resolving game-rules that either don't fit
in other classes or modules or would cause awkward external dependances for
those classes or modules."""

import logging
import random
import the
from . import actor

LOG = logging.getLogger(__name__)

# When determining the movement cost, diagonal and orthogonal squares do not
# cost the same.
DIAGONAL_COST = 3
ORTHOGONAL_COST = 2

# When determining action point cost of actions for high- or low- dexterity
# actors we apply a modifier, giving a bonus to high-dexterity actors and a
# penalty to low-dexterity actors.
APMOD_HIGHDEX = -1
APMOD_LOWDEX = 1
HIGHDEX_THRESHHOLD = 2
LOWDEX_THRESHHOLD = 2


def movement_cost(delta_y, delta_x):
    """Looks up the movement cost for a particular movement.

    Each diagonal movement costs 3 AP and each orthogonal movement costs 2 AP.
    """
    normal_y = abs(delta_y)
    normal_x = abs(delta_x)
    orthogonal_squares = abs(normal_y - normal_x)
    diaganol_squares = min(normal_y, normal_x)
    return orthogonal_squares * ORTHOGONAL_COST \
        + diaganol_squares * DIAGONAL_COST


def ap_mod(original_ap, dexterity):
    """Applies dexterity modifier to action point cost for one action."""
    modified_ap = original_ap
    if dexterity < LOWDEX_THRESHHOLD:
        modified_ap = original_ap + APMOD_LOWDEX
    if dexterity > HIGHDEX_THRESHHOLD:
        LOG.info("Applying high-dexterity bonus")
        modified_ap = original_ap + APMOD_HIGHDEX
    if modified_ap < 1:
        modified_ap = 1
    return modified_ap


# Attributes should be between 1 and 4, inclusive.
ATTRIBUTE_MAX = 4
ATTRIBUTE_MIN = 1


def is_valid_attribute(attribute):
    """Verifies if an attribute is in a valid range."""
    return ATTRIBUTE_MIN <= attribute <= ATTRIBUTE_MAX


class MonsterSpawner(actor.Actor):
    """Spawns new monsters into the game."""
    def __init__(self, world):
        self._world = world

    def act(self):
        LOG.info("Spawner tick.")
        return 100


class Generator(object):
    """Represents the end-game goal."""

    FULL_HEALTH = 3

    def __init__(self):
        """Construct a fresh generator with full health."""
        self.health = 3

    def deactivate(self):
        """Perform one step of deactivation."""
        verb = "continue"
        if self.health == self.FULL_HEALTH:
            verb = "begin"
        the.messages.add("You %s deactivating the shield generator." % verb)
        self.health -= 1
        return 8

    def active(self):
        return self.health != 0
