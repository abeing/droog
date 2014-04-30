# -*- coding: UTF-8 -*-
import random
import logging
import math


log = logging.getLogger(__name__)


class World:
    def __init__(self, height, width, road_count=22, beta=0.5):
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
                self.tiles[y].append(' ')
        self._generate(road_count, beta)
        self._add_shield_generator()

    def isEmpty(self, y, x):
        """Returns True if the location is empty."""
        return self.tiles[y][x] == ' '

    def valid_location(self, y, x):
        return 0 <= y < self.height and 0 <= x < self.width

    def glyph_at(self, y, x):
        """Returns the world glyph at the specified location.  If the location
        coordinates are out of bounds, returns a blank."""
        if self.valid_location(y, x):
            return self.tiles[y][x]
        else:
            return ' '

    def _position_hero(self):
        """Calculates the location for the hero.

        The hero will start close to half way between the center and edge of
        the map, using a normal distribution."""

        rand_dist = random.normalvariate(self.width / 2, self.width / 8)
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
        while self.valid_location(y, x) and keep_going:
            self.tiles[y][x] = '#'
            y += delta_y
            x += delta_x
            if 0 <= y < self.height and 0 <= x < self.width \
                    and self.tiles[y][x] == '#':
                keep_going = random.uniform(0, 1) < beta

    def _generate(self, road_count=10, beta=0.5):
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

        equator = int(random.triangular(low=0, high=self.height,
                                        mode=self.height / 2))
        self._add_road(equator, 0, 0, 1, 1.0)
        roads.append(((equator, 0), (equator, self.width - 1)))
        log.info('Equator road from %r to %r', (equator, 0),
                 (equator, self.width))

        meridian = int(random.triangular(low=0, high=self.width,
                                         mode=self.width / 2))
        self._add_road(0, meridian, 1, 0, 1.0)
        roads.append(((0, meridian), (self.height - 1, meridian)))
        log.info('Meridian road from %r to %r', (0, meridian),
                 (self.height, meridian))

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
                    self._add_road(begin_y, bisect, 1, 0, beta)
                if direction < 1:  # Going north.
                    self._add_road(begin_y, bisect, -1, 0, beta)
            elif begin_x == end_x:  # We chose a vertical road, we will make
                                      # a horizontal road
                bisect = random.randint(begin_y, end_y)
                log.info('Creating road %d horizontally from %r heading %d', i,
                         (bisect, begin_x), direction)
                if direction > -1:  # Going east.
                    self._add_road(bisect, begin_x, 0, 1, beta)
                if direction < 1:  # Going west.
                    self._add_road(bisect, begin_x, 0, -1, beta)
            else:
                log.error('Road is neither horizontal nor vertical')
        self._log()

    def _log(self):
        with open("world.dump", "w") as dump_file:
            for y in range(self.height):
                for x in range(self.width):
                    dump_file.write(self.tiles[y][x])
                dump_file.write("\n")

    def _add_shield_generator(self):
        """Places a shield generator in the center of the map."""

        y = self.height / 2
        x = self.width / 2
        self.tiles[y][x] = "G"
