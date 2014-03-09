class Map:
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.tiles = []
        for y in range(height):
            self.tiles.append(list())
            for x in range(width):
                self.tiles[y].append(' ')
                if y == 0 or y == height - 2:
                    self.tiles[y][x] = '#'
                elif x == 0 or x == width - 2:
                    self.tiles[y][x] = '#'

    def isEmpty(self, y, x):
        if (self.tiles[y][x] == ' '):
            return True
        return False