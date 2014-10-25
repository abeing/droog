import ui as _ui
import world as _world
import logging
import creature
import message
import turn
import sys

logging.basicConfig(filename="droog.log", level=logging.INFO)
log = logging.getLogger(__name__)


turn = turn.Turn()
world = _world.World(200, 200, turn)
hero = creature.make_hero("Snaugh")
status = ""


movements = {'h': (0, -1),   # West
             'l': (0, 1),    # East
             'j': (1, 0),    # South
             'k': (-1, 0),   # North
             'y': (-1, -1),  # Northwest
             'u': (-1, 1),   # Northeast
             'b': (1, -1),   # Southwest
             'n': (1, 1),    # Southeast
             }


def refresh(ui):
    ui.draw_area(world)
    ui.draw_status(turn.current_time())
    ui.draw_hero(hero)
    ui.draw_messages()


def hero_goes():
    command = chr(ui.input())
    if command in movements:
        delta_y, delta_x = movements[command]
        return world.move_hero(delta_y, delta_x)
    if command == '/':
        ui.look(world)
        return 0
    if command == 'q':
        sys.exit(0)
    return 0

with _ui.UI() as ui:

    message.add("Welcome to Droog.")

    hero.act_func = hero_goes
    turn.add_actor(hero)

    refresh(ui)
    while turn.next():
        refresh(ui)
