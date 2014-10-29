#!/usr/bin/python
import ui as _ui
import world as _world
import logging
import creature
import message
import turn
import sys
import functools

logging.basicConfig(filename="droog.log", level=logging.INFO)
log = logging.getLogger(__name__)


turn = turn.Turn()
hero = creature.make_hero("Snaugh")
world = _world.World(200, 200, turn, hero)
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


def hero_goes(ui):
    command = ui.input()
    if command in movements:
        delta_y, delta_x = movements[command]
        return world.move_hero(delta_y, delta_x)
    if command == '/':
        ui.look(world)
        return 0
    if command == '~':
        ui.wizard(world)
    if command == 'q':
        sys.exit(0)
    return 0


def main():
    with _ui.UI() as ui:

        message.add("Welcome to Droog.")

        hero.act_func = functools.partial(hero_goes, ui)
        turn.add_actor(hero)

        refresh(ui)
        while turn.next():
            refresh(ui)


if __name__ == "__main__":
    main()
