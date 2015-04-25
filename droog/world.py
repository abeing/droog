# -*- coding: UTF-8 -*-

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

"""The Droog module for handling the world.

Location -- A class for value objects storing coordinates in the world.
World -- A class for reference objects of the World itself.
"""

import random
import logging
import math
from . import tile
from . import engine
from . import english
from . import the

LOG = logging.getLogger(__name__)

TREE_CHANCE = 0.05
ROAD_GRID_SIZE = 24
ROAD_CHANCE = 0.5
BUILDING_CHANCE = 0.42
WALL_BREAK_CHANCE = 0.12

mult = [[1, 0, 0, -1, -1, 0, 0, 1],
        [0, 1, -1, 0, 0, -1, 1, 0],
        [0, 1, 1, 0, 0, -1, -1, 0],
        [1, 0, 0, 1, -1, 0, 0, -1]]


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

    def delta_to(self, other_loc):
        """Return a delta between the other_loc and this one."""
        if other_loc.row == self.row:
            delta_row = 0
        else:
            delta_row = 1 if (other_loc.row - self.row > 0) else -1
        if other_loc.col == self.col:
            delta_col = 0
        else:
            delta_col = 1 if (other_loc.col - self.col > 0) else -1
        return Location(delta_row, delta_col)

    def __repr__(self):
        """Return string representation."""
        return "(%r, %r)" % (self.row, self.col)

    def __eq__(self, other):
        """Return True if these have the same value."""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        """Return True if these do not have the same value."""
        return not self.__eq__(other)


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
        assert rows > 20
        assert cols > 20
        self.cols = cols
        self.rows = rows
        self.tiles = []
        self.generator = engine.Generator()
        self.generator_location = None
        # The junction grid used to make this map, for logging and debugging.
        self._junction_grid = None

        for row in range(rows):
            self.tiles.append(list())
            for _ in range(cols):
                self.tiles[row].append(tile.make_empty())
        self.hero_location = self._position_hero()
        self.cell(self.hero_location).creature = the.hero
        self._generate()
        self.do_fov()

    def is_empty(self, loc):
        """Returns True if the location is empty."""
        return self.cell(loc).transparent

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
            return self.item_description_at(loc)
        else:
            return self.cell(loc).description

    def item_description_at(self, loc):
        """Return a description of the items at a location."""
        items_msg = ""
        items = self.cell(loc).items
        if items:
            items_msg = "%s" % items[0].name
            if len(items) > 1:
                items_msg += " amongst other things."
            else:
                items_msg += "."
        return items_msg

    def move_creature(self, from_loc, delta):
        """Move a creature or hero at (y, x) by (delta_y, delta_x) and return
        the action point costs of the movement or zero if the movement was not
        possible.

        At the moment, only single-step movement is permitted as we do not have
        pathfinding implemented."""

        assert delta.row < 2
        assert delta.col < 2
        to_loc = from_loc.offset(delta.row, delta.col)
        if self.cell(to_loc).walkable:
            moved_creature = self.cell(from_loc).creature
            LOG.info('Moved creature %r from %r to %r', moved_creature.name,
                     from_loc, to_loc)
            moved_creature.loc = to_loc
            self.cell(from_loc).creature = None
            self.cell(to_loc).creature = moved_creature
            return engine.movement_cost(delta.row, delta.col)
        return 0

    def change_hero_loc(self, new_loc):
        """Change the hero location."""
        old_loc = self.hero_location
        self.hero_location = new_loc
        self.cell(old_loc).creature = None
        self.cell(new_loc).creature = the.hero
        self.do_fov()

    def move_hero(self, delta_y, delta_x):
        """Move the hero by (delta_y, delta_x)."""
        old_loc = self.hero_location
        new_loc = self.hero_location.offset(delta_y, delta_x)
        if self.cell(new_loc).walkable:
            LOG.info('Moved hero from %r to %r', old_loc, new_loc)
            self.change_hero_loc(new_loc)
            # If there are items in the new location, report about them in the
            # message LOG.
            items_msg = self.item_description_at(new_loc)
            if items_msg:
                the.messages.add("You see here %s" % items_msg)
            return engine.movement_cost(delta_y, delta_x)
        target = self.cell(new_loc).creature
        if target:
            return the.hero.melee_attack(target)

        # If we have a shield generator, we begin to jurry rig it.
        if self.glyph_at(new_loc) == 'G':
            return self.generator.deactivate()
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
            for row in self._junction_grid:
                dump_file.write("%r" % row)
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
        new_loc = self.random_empty_location(near)
        self.change_hero_loc(new_loc)

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

    def get_item(self, loc):
        """Get an item from the world."""
        assert self.is_valid_location(loc)
        item = None
        if self.cell(loc).items:
            item = self.cell(loc).items.pop()
        return item

    def set_lit(self, loc):
        """Set the cell at loc as visible."""
        self.cell(loc).seen = True

    def _cast_light(self, cx, cy, row, start, end, radius, xx, xy, yx, yy):
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
                                             radius, xx, xy, yx, yy)
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
        for octant in range(8):
            self._cast_light(self.hero_location.col, self.hero_location.row,
                             1, 1.0, 0.0, 10,
                             mult[0][octant], mult[1][octant],
                             mult[2][octant], mult[3][octant])

    def _generate(self):
        """Generate the world map.

        This function builds the world in several stages.

        1) Generate grasses, bushes and trees.
        2) Generate the road grid.
        3) Build the fortress.
        4) Build the other buildings and a lake.
        """
        self._generate_vegetation()
        self._generate_roads()
        self._generate_computer()
        self._generate_shield()
        self._generate_buildings()

    def _generate_vegetation(self):
        """Fill the map with vegeation."""
        for row in xrange(0, self.rows):
            for col in xrange(0, self.cols):
                if TREE_CHANCE > random.random():
                    self.tiles[row][col] = tile.make_tree()
                else:
                    self.tiles[row][col] = tile.make_empty()

    def _generate_roads(self):
        """Fill the map with a grid of roads."""
        junction_grid = _create_junction_grid(self.rows, self.cols,
                                              ROAD_GRID_SIZE)
        self._junction_grid = junction_grid  # for dumping purposes
        prev_road_row = 0
        road_row = ROAD_GRID_SIZE
        prev_road_col = 0
        road_col = ROAD_GRID_SIZE

        for junction_row in junction_grid:
            for junction in junction_row:
                LOG.debug("Drawing junction %r", junction)
                if junction[0]:  # North road
                    LOG.debug("Drawing north road from row %d to row %d in "
                              "col %d", prev_road_row, road_row, road_col)
                    extended_prev_road_row = prev_road_row - 3
                    if extended_prev_road_row < 0:
                        extended_prev_road_row = 0
                    for row in xrange(extended_prev_road_row, road_row):
                        if self.tiles[row][road_col - 5].glyph != '*':
                            self.tiles[row][road_col - 5] = tile.make_empty()
                        if self.tiles[row][road_col - 4].glyph != '*':
                            self.tiles[row][road_col - 4] = tile.make_empty()
                        self.tiles[row][road_col - 3] = tile.make_street()
                        self.tiles[row][road_col - 2] = tile.make_street()
                        self.tiles[row][road_col - 1] = tile.make_street()
                        if road_col < self.cols - 1 \
                                and self.tiles[row][road_col].glyph != '*':
                            self.tiles[row][road_col + 0] = tile.make_empty()
                        if road_col < self.cols - 2 \
                                and self.tiles[row][road_col + 1].glyph != '*':
                            self.tiles[row][road_col + 1] = tile.make_empty()
                if junction[3]:  # West road
                    LOG.debug("Drawing west road from col %d to col %d in "
                              "row %d", prev_road_col, road_col, road_row)
                    for col in xrange(prev_road_col, road_col):
                        if self.tiles[road_row - 5][col].glyph != '*':
                            self.tiles[road_row - 5][col] = tile.make_empty()
                        if self.tiles[road_row - 4][col].glyph != '*':
                            self.tiles[road_row - 4][col] = tile.make_empty()
                        self.tiles[road_row - 3][col] = tile.make_street()
                        self.tiles[road_row - 2][col] = tile.make_street()
                        self.tiles[road_row - 1][col] = tile.make_street()
                        if road_row < self.rows - 1 \
                                and self.tiles[road_row][col].glyph != '*':
                            self.tiles[road_row][col] = tile.make_empty()
                        if road_row < self.rows - 2 \
                                and self.tiles[road_row + 1][col].glyph != '*':
                            self.tiles[road_row + 1][col] = tile.make_empty()
                prev_road_col = road_col
                road_col += ROAD_GRID_SIZE
                if road_col >= self.cols:
                    road_col = self.cols
            prev_road_row = road_row
            road_row += ROAD_GRID_SIZE
            if road_row >= self.rows:
                road_row = self.rows
            prev_road_col = 0
            road_col = ROAD_GRID_SIZE

        road_row = ROAD_GRID_SIZE
        road_col = ROAD_GRID_SIZE
        for junction_row in junction_grid:
            for junction in junction_row:
                if not junction[0] and not junction[3]:
                    self.tiles[road_row - 3][road_col - 3] = tile.make_empty()
                if not junction[2] and not junction[3]:
                    self.tiles[road_row - 1][road_col - 3] = tile.make_empty()
                if not junction[1] and not junction[2]:
                    self.tiles[road_row - 1][road_col - 1] = tile.make_empty()
                if not junction[0] and not junction[1]:
                    self.tiles[road_row - 3][road_col - 1] = tile.make_empty()
                road_col += ROAD_GRID_SIZE
                if road_col >= self.cols:
                    road_col = self.cols
            road_col = ROAD_GRID_SIZE
            road_row += ROAD_GRID_SIZE
            if road_row >= self.rows:
                road_row = self.rows

    def _generate_computer(self):
        """Places a shield generator in the center of the map."""
        row = self.rows / 2
        col = self.cols / 2
        self.generator_location = Location(row, col)
        self.tiles[row][col] = tile.make_shield_generator()

    def _generate_shield(self):
        """Creates the shield border around the navigable map."""

        for row in range(0, self.rows):
            self.tiles[row][0] = tile.make_shield()
            self.tiles[row][self.cols - 1] = tile.make_shield()

        for col in range(self.cols):
            self.tiles[0][col] = tile.make_shield()
            self.tiles[self.rows - 1][col] = tile.make_shield()

    def _generate_buildings(self):
        """Create buildings in some blocks."""
        cell_begin_row = 0
        cell_end_row = ROAD_GRID_SIZE
        cell_begin_col = 0
        cell_end_col = ROAD_GRID_SIZE

        while cell_end_row < self.rows:
            while cell_end_col < self.cols:
                if random.random() < BUILDING_CHANCE:
                    begin = Location(cell_begin_row, cell_begin_col)
                    end = Location(cell_end_row, cell_end_col)
                    self._generate_building(begin, end)
                cell_begin_col = cell_end_col
                cell_end_col += ROAD_GRID_SIZE
            cell_begin_row = cell_end_row
            cell_end_row += ROAD_GRID_SIZE
            cell_begin_col = 0
            cell_end_col = ROAD_GRID_SIZE

    def _generate_building(self, begin, end):
        """Create a building at the sepcified site."""
        LOG.debug("Generating a building between %r and %r.", begin, end)
        top = begin.row + random.randint(3, ROAD_GRID_SIZE / 3)
        bottom = end.row - random.randint(6, ROAD_GRID_SIZE / 3)
        left = begin.col + random.randint(3, ROAD_GRID_SIZE / 3)
        right = end.col - random.randint(6, ROAD_GRID_SIZE / 3)
        for row in xrange(top, bottom + 1):
            for col in xrange(left, right + 1):
                if row == top or row == bottom or col == left or col == right:
                    if WALL_BREAK_CHANCE < random.random():
                        self.tiles[row][col] = tile.make_wall()
                else:
                    self.tiles[row][col] = tile.make_floor()


def _generate_random_junction(north, south, east, west):
    """Generate random junction given which roads much or must not exist.
    For north, south, east, and west True means road must exist, False means
    road must not exist, and None means either is okay.
    """
    result = [north, south, east, west]
    free_roads = []
    for index in xrange(4):
        if result[index] is None:
            free_roads.append(index)
    free_road_count = len(free_roads)
    fill_road_count = 0
    for _ in xrange(free_road_count):
        fill_road_count += random.random() < ROAD_CHANCE
    while fill_road_count > 0:
        fill_road = random.choice(free_roads)
        result[fill_road] = True
        free_roads.remove(fill_road)
        fill_road_count -= 1
    road_count = 0
    for road in result:
        if road is True:
            road_count += 1
    if road_count == 1:
        fill_road = random.choice(free_roads)
        free_roads.remove(fill_road)
        result[fill_road] = True
    while free_roads:
        fill_road = free_roads.pop()
        result[fill_road] = False
    return result


def _log_junction_grid(grid):
    """Writes the junction grid out to the log."""
    LOG.debug("Junction grid")
    for row in grid:
        LOG.debug(row)


def _create_junction_grid(map_rows, map_cols, cell_size):
    """Create a grid of valid road intersations."""
    assert cell_size < map_rows
    assert cell_size < map_cols
    junction_grid = []
    rows = map_rows / cell_size
    cols = map_cols / cell_size

    LOG.debug("Creating junction grid of size %d rows by %d columns. cell"
              " size is %d", rows, cols, cell_size)

    for row in xrange(0, rows):
        junction_grid.append([])
        for col in xrange(0, cols):
            north = junction_grid[row - 1][col][2] if row > 0 else None
            west = junction_grid[row][col - 1][1] if col > 0 else None
            junction = _generate_random_junction(north, None, None, west)
            junction_grid[row].append(junction)
    return junction_grid


