import ui as _ui
import world as _world
import logging
import creature
import Queue
import turn
import sys

logging.basicConfig(filename="droog.log", level=logging.INFO)
log = logging.getLogger(__name__)


messages = Queue.Queue()
world = _world.World(200, 200)
hero = creature.make_hero("Snaugh")
status = ""
turn = turn.Turn()


def move_hero(delta_y, delta_x):
    """Move the hero in the specified direction.

    Returns True if the movement was successful, false otherwise.
    """
    (old_hero_y, old_hero_x) = world.hero_location
    new_hero_y = old_hero_y + delta_y
    new_hero_x = old_hero_x + delta_x
    if world.is_walkable(new_hero_y, new_hero_x):
        world.hero_location = (new_hero_y, new_hero_x)
        log.info('Moved hero from %r to %r', (old_hero_y, old_hero_x),
                 (new_hero_y, new_hero_x))
        return True
    return False

movements = {'h': (0, -1),   # West
             'l': (0, 1),    # East
             'j': (1, 0),    # South
             'k': (-1, 0),   # North
             'y': (-1, -1),  # Northwest
             'u': (-1, 1),   # Northeast
             'b': (1, -1),   # Southwest
             'n': (1, 1),    # Southeast
             }

def movement_cost(delta_y, delta_x):
    if delta_y * delta_x == 0:
        return 1
    return 1.5

def refresh(ui):
    ui.draw_area(world)
    ui.draw_status(turn.current_time())
    ui.draw_hero(hero)
    ui.draw_messages(messages)


def hero_goes():
    command = chr(ui.input())
    if command in movements:
        delta_y, delta_x = movements[command]
        if move_hero(delta_y, delta_x):
            return movement_cost(delta_y, delta_x)
    if command == '/':
        ui.look(world)
        return 0
    if command == 'q':
        sys.exit(0)
    return 0

with _ui.UI() as ui:

    messages.put("Welcome to Droog.")

    hero.act_func = hero_goes
    turn.add_actor(hero)

    refresh(ui)
    while turn.next():
        refresh(ui)
