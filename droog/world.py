# -*- coding: UTF-8 -*-

"""The Droog module for handling the world.

Location -- A class for value objects storing coordinates in the world.
World -- A class for reference objects of the World itself.
"""

# The MIT License (MIT)
#
# Copyright (c) 2015 Adam Miezianko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import random
import logging
import math
from . import tile
from . import engine
from . import english
from . import the

LOG = logging.getLogger(__name__)

mult = [
                [1,  0,  0, -1, -1,  0,  0,  1],
                [0,  1, -1,  0,  0, -1,  1,  0],
                [0,  1,  1,  0,  0, -1, -1,  0],
                [1,  0,  0,  1, -1,  0,  0, -1]
            ]

class Location(object):
    """The Location class represents a position on a grid."""
    def __init__(self, row, col):
        """Construct a new location."""
        self.row = row
        self.col = col

    def offset(self, delta_row, delta_col):
        """Offset the location by a given number of rows and columns."""
        return Location(self.row + delta_row, self.col + delta_col)

    def distance_to(self, other_loc):
        """Return the distance between another location and this one."""
        delta_row = abs(other_loc.row - self.row)
        delta_col = abs(other_loc.col - self.col)
        return math.sqrt(delta_row * delta_row + delta_col * delta_col)

    def delta_to(self, other_loc, steps=1):
        """Return a delta between the other_loc and this one."""
        delta_row = steps if (other_loc.row - self.row > 0) else -steps
        delta_col = steps if (other_loc.col - self.col > 0) else -steps
        return Location(delta_row, delta_col)

    def __repr__(self):
        """Return string representation."""
        return "(%r, %r)" % (self.row, self.col)


def random_delta():
    """Return a random delta."""
    return Location(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))


class World(object):
    """Representation of the game world."""

    def __init__(self, rows, cols):
        """Creates a World of the specified width, height, number of roads and
        probability of intersection continuations.

        The world is a grid of streets with the hero in the center.
        """
        self.cols = cols
        self.rows = rows
        self.tiles = []

        for row in range(rows):
            self.tiles.append(list())
            for _ in range(cols):
                self.tiles[row].append(tile.make_empty())
        self.hero_location = self._position_hero()
        self.do_fov()

    def is_walkable(self, loc):
        """Returns True if the location can be traversed by walking."""
        if not self.tiles[loc.row][loc.col].walkable:
            return False
        if not self.tiles[loc.row][loc.col].creature is None:
            return False
        if self.hero_location == loc:
            return False
        return True

    def is_empty(self, loc):
        """Returns True if the location is empty."""
        return self.cell(loc).walkable

    def is_valid_location(self, loc):
        """Return true if this location is in the world bounds."""
        return 0 <= loc.row < self.rows and 0 <= loc.col < self.cols

    def cell(self, loc):
        """Return the tile at the location."""
        return self.tiles[loc.row][loc.col]

    def glyph_at(self, loc):
        """Returns the world glyph and its color at the specified location.  If
        the location coordinates are out of bounds, returns a shield character.
        """
        if loc == self.hero_location:
            return '@'
        cell = self.cell(loc)
        if cell.creature:
            return cell.creature.glyph
        if cell.items:
            return cell.items[0].glyph
        return cell.glyph

    def creature_at(self, loc):
        """Returns the creature at the specified location or None if there is
        no creature at that location or if the location coordinates are out of
        bounds."""
        if self.hero_location == loc:
            return the.hero
        return self.cell(loc).creature

    def item_at(self, loc):
        """Return the top item at the specified location."""
        items = self.items_at(loc)
        if items:
            return items[0]
        return None

    def items_at(self, loc):
        """Return all the items at the specified location."""
        if self.tiles[loc.row][loc.col].items:
            return self.tiles[loc.row][loc.col].items

    def description_at(self, loc):
        """Return a description of the location specified.

        The description of a map location is description of the first of the
        following elements at that location: monster, item, tile.

        If the location is invalid, the empty string is returned.
        """
        if loc == self.hero_location:
            return "yourself"
        if self.cell(loc).creature:
            return english.indefinite_creature(self.cell(loc).creature)
        if self.cell(loc).items:
            return self.cell(loc).items[0].name
        else:
            return self.cell(loc).description

    def move_creature(self, from_loc, delta):
        """Move a creature or hero at (y, x) by (delta_y, delta_x) and return
        the action point costs of the movement or zero if the movement was not
        possible.

        At the moment, only single-step movement is permitted as we do not have
        pathfinding implemented."""

        assert delta.row < 2
        assert delta.col < 2
        to_loc = from_loc.offset(delta.row, delta.col)
        if self.is_walkable(to_loc):
            moved_creature = self.creature_at(from_loc)
            LOG.info('Moved creature %r from %r to %r', moved_creature.name,
                     from_loc, to_loc)
            moved_creature.loc = to_loc
            self.cell(from_loc).creature = None
            self.cell(to_loc).creature = moved_creature
            return engine.movement_cost(delta.row, delta.col)
        return 0

    def move_hero(self, delta_y, delta_x):
        """Move the hero by (delta_y, delta_x)."""
        old_loc = self.hero_location
        new_loc = self.hero_location.offset(delta_y, delta_x)
        if self.is_walkable(new_loc):
            LOG.info('Moved hero from %r to %r', old_loc, new_loc)
            self.hero_location = new_loc
            # If there are items in the new location, report about them in the
            # message LOG.
            items = self.items_at(new_loc)
            if items and len(items) == 1:
                the.messages.add("You see here %s." % items[0].name)
            elif items and len(items) > 1:
                items_msg = "You see here %s" % items[0].name
                for item in items[1:]:
                    items_msg += ", " + item.name
                items_msg += "."
                the.messages.add(items_msg)
            self.do_fov()
            return engine.movement_cost(delta_y, delta_x)
        target = self.creature_at(new_loc)
        if target:
            return the.hero.melee_attack(target)

        # If we have a shield generator, we begin to jurry rig it.
        if self.glyph_at(new_loc) == 'G':
            return engine.deactivate_generator()
        return 0

    def _position_hero(self):
        """Calculates the location for the hero.

        The hero will start close to half way between the center and edge of
        the map, using a triangular distribution."""

        rand_dist = random.triangular(0, self.cols / 2 - 1)
        rand_dir = random.uniform(0, 359)
        row = int(rand_dist * math.sin(rand_dir)) + self.rows / 2
        col = int(rand_dist * math.cos(rand_dir)) + self.cols / 2
        return Location(row, col)

    def add_road(self, start_loc, delta_y, delta_x, beta):
        """Adds a road to the map

        Starting at (start_y, start_x) and heading in a direction specified by
        delta_y and delta_x, draw a map until we reach the edge of the map.  If
        we run into another road, continue with probability beta, otherwise
        stop."""
        assert delta_y * delta_x == 0, 'We only support orthogonal roads.'
        keep_going = True
        road_loc = start_loc
        while self.is_valid_location(road_loc) and keep_going:
            self.tiles[road_loc.row][road_loc.col] = tile.make_street()
            road_loc = road_loc.offset(delta_y, delta_x)
            if self.is_valid_location(road_loc) \
                    and self.cell(road_loc).glyph == '#':
                keep_going = random.uniform(0, 1) < beta

    def _log(self):
        """Dumps the world into a file called 'world.dump'"""
        with open("world.dump", "w") as dump_file:
            for row in range(self.rows):
                for col in range(self.cols):
                    dump_file.write(self.cell(Location(row, col)).glyph)
                dump_file.write("\n")

    def random_empty_location(self, near=None, attempts=5, radius=10):
        """Creates a random location on the map, or a random location on the
        map near a specified location."""

        while attempts > 0:
            if near is None:
                row = int(random.uniform(0, self.rows))
                col = int(random.uniform(0, self.cols))
            else:
                row = int(random.triangular(low=near.row - radius,
                                            high=near.row + radius))
                col = int(random.triangular(low=near.col - radius,
                                            high=near.col + radius))
            loc = Location(row, col)
            if self.is_valid_location(loc) and \
               self.cell(loc).creature is None and self.cell(loc).walkable:
                return loc
            attempts -= 1
        return None

    def teleport_hero(self, near):
        """Teleports the hero to a valid location near a specified location."""
        location = self.random_empty_location(near)
        self.hero_location = location

    def spawn_monster(self, monster, near=None):
        """Spawns a monster on the map."""
        assert monster
        location = self.random_empty_location(near)
        if location is None:
            return False
        if monster is not None:
            the.turn.add_actor(monster)
            monster.loc = location
            self.cell(location).creature = monster
            LOG.info('%r placed at %r', monster, location)
            return True

    def remove_monster(self, monster):
        """Removes a monster from the map, for example when it dies."""
        (monster_y, monster_x) = monster.loc
        self.tiles[monster_y][monster_x].creature = None

    def add_item(self, loc, item):
        """Add an item to a location."""
        assert self.is_valid_location(loc)
        self.cell(loc).items.append(item)

    def set_lit(self, loc):
        self.cell(loc).seen = True

    def _cast_light(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        "Recursive lightcasting function"
        if start < end:
            return
        radius_squared = radius*radius
        for j in range(row, radius+1):
            dx, dy = -j-1, -j
            blocked = False
            while dx <= 0:
                dx += 1
                # Translate the dx, dy coordinates into map coordinates:
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering:
                l_slope, r_slope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
                loc = Location(Y, X)
                if not self.is_valid_location(loc):
                    return
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # Our light beam is touching this square; light it:
                    
                    if dx*dx + dy*dy < radius_squared:
                        self.set_lit(loc)
                    if blocked:
                        # we're scanning a row of blocked squares:
                        if not self.is_empty(loc):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if not self.is_empty(loc) and j < radius:
                            # This is a blocking square, start a child scan:
                            blocked = True
                            self._cast_light(cx, cy, j+1, start, l_slope,
                                             radius, xx, xy, yx, yy, id+1)
                            new_start = r_slope
            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break

    def reset_fov(self):
        """Reset the field of view data for the map."""
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                self.tiles[row][col].seen = False

    def do_fov(self):
        "Calculate lit squares from the given location and radius"
        self.reset_fov()
        for oct in range(8):
            # TODO: Update the radius.
            self._cast_light(self.hero_location.col, self.hero_location.row,
                             1, 1.0, 0.0, 10,
                             mult[0][oct], mult[1][oct],
                             mult[2][oct], mult[3][oct], 0)


def _add_shield_generator(a_world):
    """Places a shield generator in the center of the map."""
    row = a_world.rows / 2
    col = a_world.cols / 2
    a_world.generator_location = Location(row, col)
    a_world.tiles[row][col] = tile.make_shield_generator()


def _add_shield(a_world):
    """Creates the shield border around the navigable map."""

    for row in range(0, a_world.rows):
        a_world.tiles[row][0] = tile.make_shield()
        a_world.tiles[row][a_world.cols - 1] = tile.make_shield()

    for col in range(a_world.cols):
        a_world.tiles[0][col] = tile.make_shield()
        a_world.tiles[a_world.rows - 1][col] = tile.make_shield()


def generate_city(a_world, road_count=10, beta=0.5):
    """Generates a city map.

    We first draw a horizontal road somewhere near the equator of the map,
    choosing the latitude using a triangular distribution with a mode of
    the equator.

    Then we draw a vertical road somewhere near the prime meridian of the
    map, choosing the longitude using a triangular distribution with a
    mode of the prime meridian.

    Then we select an existing road, an existing point along it, and then
    draw a road in one, the other or both directions from it. We draw until
    we reach another road or the edge of the world. If we reach a road,
    we will continue with probability ß."""

    # We'll store the roads we create here.
    roads = []

    if road_count == 0:
        if a_world.rows > a_world.cols:
            road_count = a_world.rows / 10
        else:
            road_count = a_world.cols / 10

    equator = int(random.triangular(low=0, high=a_world.rows,
                                    mode=a_world.rows / 2))
    a_world.add_road(Location(equator, 0), 0, 1, 1.0)
    roads.append(((equator, 0), (equator, a_world.cols - 1)))
    LOG.info('Equator road from %r to %r', (equator, 0),
             (equator, a_world.cols))

    meridian = int(random.triangular(low=0, high=a_world.cols,
                                     mode=a_world.cols / 2))
    a_world.add_road(Location(0, meridian), 1, 0, 1.0)
    roads.append(((0, meridian), (a_world.rows - 1, meridian)))
    LOG.info('Meridian road from %r to %r', (0, meridian),
             (a_world.rows, meridian))

    for i in range(road_count):
        ((begin_y, begin_x), (end_y, end_x)) = random.choice(roads)
        # Choose a direction. Positive is south in the vertical case and
        # east in the horizontal case. Negative is north in the vertical
        # case and west in the horizontal case. Zero is both directions in
        # either case.
        direction = random.randint(-1, 1)
        if begin_y == end_y:  # We chose a horizontal road, we will make
                                # a vertical road
            bisect = random.randint(begin_x, end_x)
            LOG.info('Creating road %d vertically from %r heading %d', i,
                     (begin_y, bisect), direction)
            if direction > -1:  # Going south.
                a_world.add_road(Location(begin_y, bisect), 1, 0, beta)
            if direction < 1:  # Going north.
                a_world.add_road(Location(begin_y, bisect), -1, 0, beta)
        elif begin_x == end_x:  # We chose a vertical road, we will make
                                    # a horizontal road
            bisect = random.randint(begin_y, end_y)
            LOG.info('Creating road %d horizontally from %r heading %d', i,
                     (bisect, begin_x), direction)
            if direction > -1:  # Going east.
                a_world.add_road(Location(bisect, begin_x), 0, 1, beta)
            if direction < 1:  # Going west.
                a_world.add_road(Location(bisect, begin_x), 0, -1, beta)
        else:
            LOG.error('Road is neither horizontal nor vertical')

    _add_shield_generator(a_world)
    _add_shield(a_world)
    a_world.do_fov()

