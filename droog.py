import curses

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

class Hero:
    pass

def drawMap(aMap, aWindow):
    for y in range(aMap.height - 1):
        for x in range(aMap.width - 1):
            aWindow.addch(y, x, ord(aMap.tiles[y][x]))

hero = Hero()

mainw = curses.initscr()
curses.noecho()
curses.cbreak()

# Create the map window
map_window = curses.newwin(24, 48, 0, 0)

# center the hero
height, width = map_window.getmaxyx()
hero.x = width / 2
hero.y = height / 2

theMap = Map(height, width)

# draw the map
drawMap(theMap, map_window)

# draw the hero
map_window.addch(hero.y, hero.x, ord("@"))
map_window.move(hero.y, hero.x)

command = ' '

while command != ord('q'):
    command = map_window.getch()
    old_hero_x, old_hero_y = hero.x, hero.y
    if command == ord('h'):
        hero.x -= 1
    elif command == ord('l'):
        hero.x += 1
    elif command == ord('j'):
        hero.y += 1
    elif command == ord('k'):
        hero.y -= 1
    elif command == ord('y'):
        hero.x -= 1
        hero.y -= 1
    elif command == ord('u'):
        hero.x += 1
        hero.y -= 1
    elif command == ord('b'):
        hero.x -= 1
        hero.y += 1
    elif command == ord('n'):
        hero.x += 1
        hero.y += 1
    
    if not theMap.isEmpty(hero.y, hero.x):
        hero.x = old_hero_x
        hero.y = old_hero_y
        
    # draw the hero
    map_window.addch(old_hero_y, old_hero_x, ord(' '))
    map_window.addch(hero.y, hero.x, ord("@"))
    map_window.move(hero.y, hero.x)

curses.nocbreak()
curses.echo()
curses.endwin()
