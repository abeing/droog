import ui as _ui
import world as _world
import logging
import hero as _hero
import Queue

logging.basicConfig(filename="droog.log", level=logging.INFO)
log = logging.getLogger(__name__)


messages = Queue.Queue()
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

    messages.put("Welcome to Droog. This is a very long line and should extend"
                 " beyond the edge of the screen. This means that it will not"
                 " be displayed.")
    messages.put("This is a second message.")
    messages.put("This is the third and final message!")
    messages.put("This is the fourth and really final messages that should"
                 " make all of this scroll.")

    command = ' '
    while command != 'q':
        ui.draw_area(world)
        ui.draw_status(world)
        ui.draw_hero(hero)
        ui.draw_messages(messages)
        command = chr(ui.input())
        if command in movements:
            delta_y, delta_x = movements[command]
            move_hero(delta_y, delta_x)
