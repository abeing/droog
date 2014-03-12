# -*- coding: UTF-8 -*-
import random
import logging


log = logging.getLogger(__name__)


class World:
    def __init__(self, height, width):
        """Creates a World of the specified width and height.

        Currently the world is a large box.
        """
        self.width = width
        self.height = height
        self.tiles = []
        for y in range(height):
            self.tiles.append(list())
            for x in range(width):
                self.tiles[y].append(' ')
        self._generate()

    def isEmpty(self, y, x):
        """Returns True if the location is empty."""
        return self.tiles[y][x] == ' '

    def _add_road(self, start_y, start_x, delta_y, delta_x, beta):
        """Adds a road to the map

        Starting at (start_y, start_x) and heading in a direction specified by
        delta_y and delta_x, draw a map until we reach the edge of the map.  If
        we run into another road, continue with probability beta, otherwise
        stop."""
        keep_going = True
        y = start_y
        x = start_x
        while 0 <= y < self.height and 0 <= x < self.width and keep_going:
            self.tiles[y][x] = '#'
            y += delta_y
            x += delta_x
            if 0 <= y < self.height and 0 <= x < self.width \
                    and self.tiles[y][x] == '#':
                keep_going = random.uniform(0, 1) < beta

    def _generate(self):
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

        # Number of roads beyond the equator and meridian to create.
        road_count = 3

        # Probability that new roads crossing existing roads continue.
        beta = 0.5

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
