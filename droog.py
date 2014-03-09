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

# center the hero
height, width = mainw.getmaxyx()
hero.x = width / 2
hero.y = height / 2

theMap = Map(height, width)

# draw the map
drawMap(theMap, mainw)

# draw the hero
mainw.addch(hero.y, hero.x, ord("@"))
mainw.move(hero.y, hero.x)

command = ' '

while command != ord('q'):
	command = mainw.getch()
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
	mainw.addch(old_hero_y, old_hero_x, ord(' '))
	mainw.addch(hero.y, hero.x, ord("@"))
	mainw.move(hero.y, hero.x)

curses.nocbreak()
curses.echo()
curses.endwin()
