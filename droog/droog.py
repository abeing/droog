#!/usr/bin/python
import ui as _ui
import world as _world
import logging
import hero as _hero
import message
import turn
import the

logging.basicConfig(filename="droog.log", level=logging.INFO)
log = logging.getLogger(__name__)

status = ""


def new_game(ui):
    the.turn = turn.Turn()
    the.hero = _hero.Hero("Snaugh", ui)
    the.turn.add_actor(the.hero)
    the.world = _world.World(200, 200, turn)


def refresh(ui):
    ui.draw_area(the.world)
    ui.draw_status(the.turn.current_time())
    ui.draw_hero(the.hero)
    ui.draw_messages()


def main():
    with _ui.UI() as ui:
        new_game(ui)
        message.add("Welcome to Droog.")
        refresh(ui)
        while the.turn.next():
            refresh(ui)


if __name__ == "__main__":
    main()
