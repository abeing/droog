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
        if (self.tiles[y][x] == ' '):
            return True
        return False

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
        for x in range(self.width):
            self.tiles[equator][x] = '#'
        roads.append(((equator, 0), (equator, self.width - 1)))
        log.info('Equator road from %r to %r', (equator, 0),
                 (equator, self.width))

        meridian = int(random.triangular(low=0, high=self.width,
                                         mode=self.width / 2))
        for y in range(self.height):
            self.tiles[y][meridian] = '#'
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
            if (begin_y == end_y):  # We chose a horizontal road, we will make
                                    # a vertical road
                bisect = random.randint(begin_x, end_x)
                log.info('Creating road %d horizontally from %r heading %d', i,
                         (begin_y, bisect), direction)
                y = begin_y
                x = bisect
                if (direction > -1):  # Going south.
                    keep_going = True
                    while y < self.height and keep_going:
                        self.tiles[y][x] = '#'
                        y += 1
                        if y < self.height and self.tiles[y][x] == '#':
                            keep_going = random.uniform(0, 1) < beta
                y = begin_y  # Reset y for the both-direction case.
                if (direction < 1):  # Going north.
                    keep_going = True
                    while y >= 0 and keep_going:
                        self.tiles[y][x] = '#'
                        y -= 1
                        if y >= 0 and self.tiles[y][x] == '#':
                            keep_going = random.uniform(0, 1) < beta
            elif (begin_x == end_x):  # We chose a vertical road, we will make
                                      # a horizontal road
                bisect = random.randint(begin_y, end_y)
                log.info('Creating road %d vertically from %r heading %d', i,
                         (bisect, begin_x), direction)
                y = bisect
                x = begin_x
                if (direction > -1):  # Going east.
                    keep_going = True
                    while x < self.width and keep_going:
                        self.tiles[y][x] = '#'
                        x += 1
                        if x < self.width and self.tiles[y][x] == '#':
                            keep_going = random.uniform(0, 1) < beta
                x = begin_x
                if (direction < 1):  # Going west.
                    keep_going = True
                    while x >= 0 and keep_going:
                        self.tiles[y][x] = '#'
                        x -= 1
                        if x >= 0 and self.tiles[y][x] == '#':
                            keep_going = random.uniform(0, 1) < beta
            else:
                log.error('Road is neither horizontal nor vertical')
