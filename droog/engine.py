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
import actor
import creature
import item

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


def random_monster():
    """Return a random monster."""
    die_roll = random.randint(1, 6)
    if die_roll >= 6:
        return creature.Cop()
    elif die_roll >= 3:
        return creature.ZombieDog()
    else:
        return creature.Zombie()


# The maximum number of monsters allowed in the world.
MONSTER_CAP = 10
MONSTER_STARTING_COUNT = 6
MONSTER_RESPAWN_CHANCE = 20
MONSTER_RESPAWN_FREQUENCY = 100


class MonsterSpawner(actor.Actor):
    """Spawns new monsters into the game."""
    def __init__(self, world):
        self._world = world

    def populate(self):
        """Spawns the initial monsters into the game."""
        LOG.info("Creating initial monsters.")
        for _ in xrange(1, MONSTER_STARTING_COUNT):
            monster = random_monster()
            success = self._world.attempt_to_place_monster(monster)
            success_string = "Placed" if success else "Failed to place"
            LOG.info("%s starting %s in the world at %r.", success_string,
                     monster.name, monster.loc)

    def act(self):
        """On each MonsterSpawner tick, there is a chance to spawn a new
        monster into the world, so long as we are not above the monster cap."""
        LOG.info("Spawner ticl. There are %d of %d monsters.",
                 self._world.monster_count, MONSTER_CAP)
        if self._world.monster_count < MONSTER_CAP:
            spawn_roll = random.randint(1, 100)
            if spawn_roll < MONSTER_RESPAWN_CHANCE:
                monster = random_monster()
                success = self._world.attempt_to_place_monster(monster,
                                                               hidden=True)
                if success:
                    LOG.info("Spawned a new %s.", monster.name)
                else:
                    LOG.debug("Attempted to spawn %s but did not find a \
                              location for it.", monster.name)
            else:
                LOG.debug("Spawn roll failed. Rolled %d with %d chance.",
                          spawn_roll, MONSTER_RESPAWN_CHANCE)
        else:
            LOG.info("Not spawning due to cap.")
        return MONSTER_RESPAWN_FREQUENCY

# On average, per how many tiles will an item of loot spawn.
LOOT_SPARSENESS = 1000

loot_chance = [(4, item.make_knife),
               (2, item.make_pistol),
               (1, item.make_porter),
               (10, item.make_clip),
               (10, item.make_battery)]


class LootPlacer(object):
    """Places loot into the game."""
    def __init__(self):
        self.rarity_max = 0
        self.loot_table = []
        for rarity, factory in loot_chance:
            self.rarity_max += rarity
            self.loot_table.append((self.rarity_max, factory))
        LOG.info("Created loot table: %r", self.loot_table)

    def populate(self, world):
        """Place a random assortment of loot items into the world."""
        loot_count = world.size_in_tiles() / LOOT_SPARSENESS
        for item_id in xrange(loot_count):
            roll = random.randint(1, self.rarity_max)
            LOG.info("Loot item %d, rolled %d.", item_id, roll)
            for (target, factory) in self.loot_table:
                if roll < target:
                    loot_item = factory()
                    LOG.info("Created a %r", loot_item)
                    break

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
