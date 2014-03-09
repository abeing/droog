import curses

class Hero:
	pass

hero = Hero()


mainw = curses.initscr()
curses.noecho()
curses.cbreak()

# center the hero
height, width = mainw.getmaxyx()
hero.x = width / 2
hero.y = height / 2

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
	# draw the hero
	mainw.addch(old_hero_y, old_hero_x, ord(' '))
	mainw.addch(hero.y, hero.x, ord("@"))
	mainw.move(hero.y, hero.x)

curses.endwin()
