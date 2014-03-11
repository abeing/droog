import ui as _ui
import world as _world
import logging


logging.basicConfig(filename="droog.log", level=logging.INFO)


class Hero:
    pass

ui = _ui.UI()
world = _world.World(_ui.AREA_ROWS, _ui.AREA_COLUMNS)

# draw the map
ui.draw_area(world)

command = ' '

while command != ord('q'):
    command = ui.input()
#    old_hero_x, old_hero_y = hero.x, hero.y
#    if command == ord('h'):
#        hero.x -= 1
#    elif command == ord('l'):
#        hero.x += 1
#    elif command == ord('j'):
#        hero.y += 1
#    elif command == ord('k'):
#        hero.y -= 1
#    elif command == ord('y'):
#        hero.x -= 1
#        hero.y -= 1
#    elif command == ord('u'):
#        hero.x += 1
#        hero.y -= 1
#    elif command == ord('b'):
#        hero.x -= 1
#        hero.y += 1
#    elif command == ord('n'):
#        hero.x += 1
#        hero.y += 1

#    if not theMap.isEmpty(hero.y, hero.x):
#        hero.x = old_hero_x
#        hero.y = old_hero_y

    # draw the hero
#    map_window.addch(old_hero_y, old_hero_x, ord(' '))
#    map_window.addch(hero.y, hero.x, ord("@"))
#    map_window.move(hero.y, hero.x)

ui.shutdown()
