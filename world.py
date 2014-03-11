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

        Then we select an existing line."""

        # We'll store the roads we create here.
        roads = []

        equator = int(random.triangular(low=0, high=self.height,
                                        mode=self.height / 2))
        for x in range(self.width):
            self.tiles[equator][x] = '#'
        roads.append(((equator, 0), (equator, self.width)))
        log.info('Equator road from %r to %r', (equator, 0),
                 (equator, self.width))

        meridian = int(random.triangular(low=0, high=self.width,
                                         mode=self.width / 2))
        for y in range(self.height):
            self.tiles[y][meridian] = '#'
        roads.append(((0, meridian), (self.height, meridian)))
        log.info('Meridian road from %r to %r', (0, meridian),
                 (self.height, meridian))

        for i in range(10):  # make ten additional roads for now
            ((begin_y, begin_x), (end_y, end_x)) = random.choice(roads)
            if (begin_y == end_y):  # We chose a horizontal road
                # bisect = random.range(begin_x, end_x)
                # direction = random.range(0, 2)
                log.info('Creating road %d horizontally', i)
            elif (begin_x == end_x):  # We chose a vertical road
                log.info('Creating road %d vertically', i)
            else:
                log.error('Road is neither horizontal nor vertical')
