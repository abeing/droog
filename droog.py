import ui as _ui
import world as _world
import logging
import hero as _hero

logging.basicConfig(filename="droog.log", level=logging.INFO)
log = logging.getLogger(__name__)


world = _world.World(200, 200)
hero = _hero.Hero()


def move_hero(delta_y, delta_x):
    (old_hero_y, old_hero_x) = world.hero_location
    new_hero_y = old_hero_y + delta_y
    new_hero_x = old_hero_x + delta_x
    if world.is_walkable(new_hero_y, new_hero_x):
        world.hero_location = (new_hero_y, new_hero_x)
        log.info('Moved hero from %r to %r', (old_hero_y, old_hero_x),
                 (new_hero_y, new_hero_x))

movements = {'h': (0, -1),   # West
             'l': (0, 1),    # East
             'j': (1, 0),    # South
             'k': (-1, 0),   # North
             'y': (-1, -1),  # Northwest
             'u': (-1, 1),   # Northeast
             'b': (1, -1),   # Southwest
             'n': (1, 1),    # Southeast
             }


with _ui.UI() as ui:

    command = ' '
    while command != 'q':
        ui.draw_area(world)
        ui.draw_status(world)
        ui.draw_hero(hero)
        ui.draw_messages()
        command = chr(ui.input())
        if command in movements:
            delta_y, delta_x = movements[command]
            move_hero(delta_y, delta_x)
