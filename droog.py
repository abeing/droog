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

mainw.getch()
curses.endwin()
