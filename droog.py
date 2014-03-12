import ui as _ui
import world as _world
import logging


logging.basicConfig(filename="droog.log", level=logging.INFO)


class Hero:
    pass

ui = _ui.UI()
world = _world.World(200, 200)

# draw the map
ui.draw_area(world)

command = ' '


def move_hero(delta_y, delta_x):
    (old_hero_y, old_hero_x) = world.hero_location
    new_hero_y = old_hero_y + delta_y
    new_hero_x = old_hero_x + delta_x
    if world.valid_location(new_hero_y, new_hero_x):
        world.hero_location = (new_hero_y, new_hero_x)


while command != ord('q'):
    ui.draw_area(world)
    command = ui.input()
    if command == ord('h'):
        move_hero(0, -1)
    elif command == ord('l'):
        move_hero(0, 1)
    elif command == ord('j'):
        move_hero(1, 0)
    elif command == ord('k'):
        move_hero(-1, 0)
    elif command == ord('y'):
        move_hero(-1, -1)
    elif command == ord('u'):
        move_hero(-1, 1)
    elif command == ord('b'):
        move_hero(1, -1)
    elif command == ord('n'):
        move_hero(1, 1)

ui.shutdown()
