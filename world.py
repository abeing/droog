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
                if y == 0 or y == height - 1:
                    self.tiles[y][x] = '#'
                elif x == 0 or x == width - 1:
                    self.tiles[y][x] = '#'

    def isEmpty(self, y, x):
        """Returns True if the location is empty."""
        if (self.tiles[y][x] == ' '):
            return True
        return False
