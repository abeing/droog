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
turn = turn.Turn()
world = _world.World(200, 200, turn)
hero = creature.make_hero("Snaugh")
status = ""


def move_creature(creature_loc, delta_y, delta_x):
    """Move the hero in the specified direction.

    Returns a tuple of the new location if the movement was successful or an
    empty tuple if the movement failed for any reason.
    """
    (old_y, old_x) = creature_loc
    new_y = old_y + delta_y
    new_x = old_x + delta_x
    if world.is_walkable(new_y, new_x):
        log.info('Moved creature from %r to %r', (old_y, old_x),
                 (new_y, new_x))
        return (new_y, new_x)
    return ()

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
        new_loc = move_creature(world.hero_location, delta_y, delta_x)
        if len(new_loc) == 2:
            world.hero_location = new_loc
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
