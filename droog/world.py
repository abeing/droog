# -*- coding: UTF-8 -*-
import random
import logging
import math
import tile
import creature
import engine
import the


log = logging.getLogger(__name__)


class World(object):
    """Representation of the game world."""

    def __init__(self, height, width):
        """Creates a World of the specified width, height, number of roads and
        probability of intersection continuations.

        The world is a grid of streets with the hero in the center.
        """
        self.width = width
        self.height = height
        self.tiles = []

        self.hero_location = self._position_hero()
        for y in range(height):
            self.tiles.append(list())
            for x in range(width):
                self.tiles[y].append(tile.make_empty())
        self.spawn_monster('Z')
        self.spawn_monster('Z')
        self.spawn_monster('d')
        self.spawn_monster('d')
        self.spawn_monster('C')
        self.spawn_monster('C')

    def is_empty(self, y, x):
        """Returns True if the location is empty."""
        return self.tiles[y][x].walkable

    def is_walkable(self, y, x):
        """Returns True if the location can be traversed by walking."""
        if self.is_valid_location(y, x):
            if not self.tiles[y][x].walkable:
                return False
            if not self.tiles[y][x].creature is None:
                return False
            if self.hero_location == (y, x):
                return False
            return True
        return False

    def is_valid_location(self, y, x):
        return 0 <= y < self.height and 0 <= x < self.width

    def glyph_at(self, y, x):
        """Returns the world glyph and its color at the specified location.  If
        the location coordinates are out of bounds, returns a shield character.
        """
        if self.is_valid_location(y, x):
            return self.tiles[y][x].glyph
        else:
            return '~'

    def creature_at(self, y, x):
        """Returns the creature at the specified location or None if there is
        no creature at that location or if the location coordinates are out of
        bounds."""
        if self.hero_location == (y, x):
            return the.hero
        if self.is_valid_location(y, x):
            return self.tiles[y][x].creature
        else:
            return None

    def description_at(self, y, x):
        """Return a description of the location specified.

        The description of a map location is description of the first of the
        following elements at that location: monster, item, tile.

        If the location is invalid, the empty string is returned.
        """
        if self.is_valid_location(y, x):
            if (y, x) == self.hero_location:
                return "yourself"
            if self.tiles[y][x].creature:
                return engine.indefinite_creature(self.tiles[y][x].creature)
            else:
                return self.tiles[y][x].description
        return ""

    def move_creature(self, y, x, delta_y, delta_x):
        """Move a creature or hero at (y, x) by (delta_y, delta_x) and return
        the action point costs of the movement or zero if the movement was not
        possible.

        At the moment, only single-step movement is permitted as we do not have
        pathfinding implemented."""

        assert delta_y < 2
        assert delta_x < 2
        new_y = y + delta_y
        new_x = x + delta_x
        if self.is_walkable(new_y, new_x):
            moved_creature = self.creature_at(y, x)
            log.info('Moved creature %r from %r to %r', moved_creature.name,
                     (y, x), (new_y, new_x))
            moved_creature.loc = (new_y, new_x)
            self.tiles[y][x].creature = None
            self.tiles[new_y][new_x].creature = moved_creature
            return engine.movement_cost(delta_y, delta_x)
        return 0

    def move_hero(self, delta_y, delta_x):
        """Move the hero by (delta_y, delta_x)."""
        (old_y, old_x) = self.hero_location
        new_y = old_y + delta_y
        new_x = old_x + delta_x
        if self.is_walkable(new_y, new_x):
            log.info('Moved hero from %r to %r', (old_y, old_x),
                     (new_y, new_x))
            self.hero_location = (new_y, new_x)
            return engine.movement_cost(delta_y, delta_x)
        target = self.creature_at(new_y, new_x)
        if target:
            return the.hero.melee_attack(target)

        # If we have a shield generator, we begin to jurry rig it.
        if self.glyph_at(new_y, new_x) == 'G':
            return engine.deactivate_generator()
        return 0

    def _position_hero(self):
        """Calculates the location for the hero.

        The hero will start close to half way between the center and edge of
        the map, using a triangular distribution."""

        rand_dist = random.triangular(0, self.width / 2 - 1)
        rand_dir = random.uniform(0, 359)
        y = int(rand_dist * math.sin(rand_dir)) + self.height / 2
        x = int(rand_dist * math.cos(rand_dir)) + self.width / 2
        return (y, x)

    def _add_road(self, start_y, start_x, delta_y, delta_x, beta):
        """Adds a road to the map

        Starting at (start_y, start_x) and heading in a direction specified by
        delta_y and delta_x, draw a map until we reach the edge of the map.  If
        we run into another road, continue with probability beta, otherwise
        stop."""
        keep_going = True
        y = start_y
        x = start_x
        while self.is_valid_location(y, x) and keep_going:
            self.tiles[y][x] = tile.make_street()
            y += delta_y
            x += delta_x
            if 0 <= y < self.height and 0 <= x < self.width \
                    and self.tiles[y][x].glyph == '#':
                keep_going = random.uniform(0, 1) < beta

    def _log(self):
        """Dumps the world into a file called 'world.dump'"""
        with open("world.dump", "w") as dump_file:
            for y in range(self.height):
                for x in range(self.width):
                    dump_file.write(self.tiles[y][x].glyph)
                dump_file.write("\n")

    def random_empty_location(self, near=None, attempts=5, radius=10):
        """Creates a random location on the map, or a random location on the
        map near a specified location."""

        while attempts > 0:
            if near is None:
                y = int(random.uniform(0, self.height))
                x = int(random.uniform(0, self.width))
            else:
                (near_y, near_x) = near
                y = int(random.triangular(low=near_y - radius,
                                          high=near_y + radius))
                x = int(random.triangular(low=near_x - radius,
                                          high=near_x + radius))
            if self.is_valid_location(y, x) and \
               self.tiles[y][x].creature is None and self.tiles[y][x].walkable:
                return (y, x)
            attempts -= 1
        return None

    def teleport_hero(self, near):
        """Teleports the hero to a valid location near a specified location."""
        location = self.random_empty_location(near)
        self.hero_location = location

    def spawn_monster(self, monster_class='Z', near=None):
        """Spawns a monster on the map."""
        monster = None
        if monster_class == 'Z':
            monster = creature.Zombie()
        if monster_class == 'd':
            monster = creature.ZombieDog()
        if monster_class == 'C':
            monster = creature.Cop()

        location = self.random_empty_location(near)
        if location is None:
            return False
        if monster is not None:
            the.turn.add_actor(monster)
            (y, x) = location
            monster.loc = location
            self.tiles[y][x].creature = monster
            log.info('%r placed at (%r, %r)', monster, y, x)
            return True

    def remove_monster(self, monster):
        """Removes a monster from the map, for example when it dies."""
        (monster_y, monster_x) = monster.loc
        self.tiles[monster_y][monster_x].creature = None


def distance_between(y1, x1, y2, x2):
    """Computes the distance between two coordinates."""
    delta_y = abs(y2 - y1)
    delta_x = abs(x2 - x1)
    return math.sqrt(delta_y + delta_x)

def _add_shield_generator(a_world):
    """Places a shield generator in the center of the map."""
    y = a_world.height / 2
    x = a_world.width / 2
    a_world.tiles[y][x] = tile.make_shield_generator()
    a_world.generator_location = (y, x)

def _add_shield(a_world):
    """Creates the shield border around the navigable map."""

    for y in range(0, a_world.height):
        a_world.tiles[y][0] = tile.make_shield()
        a_world.tiles[y][a_world.width - 1] = tile.make_shield()

    for x in range(a_world.width):
        a_world.tiles[0][x] = tile.make_shield()
        a_world.tiles[a_world.height - 1][x] = tile.make_shield()


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
        if a_world.height > a_world.width:
            road_count = a_world.height / 10
        else:
            road_count = a_world.width / 10

    equator = int(random.triangular(low=0, high=a_world.height,
                                    mode=a_world.height / 2))
    a_world._add_road(equator, 0, 0, 1, 1.0)
    roads.append(((equator, 0), (equator, a_world.width - 1)))
    log.info('Equator road from %r to %r', (equator, 0),
             (equator, a_world.width))

    meridian = int(random.triangular(low=0, high=a_world.width,
                                     mode=a_world.width / 2))
    a_world._add_road(0, meridian, 1, 0, 1.0)
    roads.append(((0, meridian), (a_world.height - 1, meridian)))
    log.info('Meridian road from %r to %r', (0, meridian),
             (a_world.height, meridian))

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
            log.info('Creating road %d vertically from %r heading %d', i,
                     (begin_y, bisect), direction)
            if direction > -1:  # Going south.
                a_world._add_road(begin_y, bisect, 1, 0, beta)
            if direction < 1:  # Going north.
                a_world._add_road(begin_y, bisect, -1, 0, beta)
        elif begin_x == end_x:  # We chose a vertical road, we will make
                                  # a horizontal road
            bisect = random.randint(begin_y, end_y)
            log.info('Creating road %d horizontally from %r heading %d', i,
                     (bisect, begin_x), direction)
            if direction > -1:  # Going east.
                a_world._add_road(bisect, begin_x, 0, 1, beta)
            if direction < 1:  # Going west.
                a_world._add_road(bisect, begin_x, 0, -1, beta)
        else:
            log.error('Road is neither horizontal nor vertical')

    _add_shield_generator(a_world)
    _add_shield(a_world)
