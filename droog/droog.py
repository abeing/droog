#!/usr/bin/python
"""Droog - a present-perfect post-apocalyptic roguelike"""
import ui as _ui
import world as _world
import logging
import hero as _hero
import message
import turn
import the

logging.basicConfig(filename="droog.log", level=logging.INFO)
LOG = logging.getLogger(__name__)

EMPTY_STATUS = ""


def new_game(ui_object):
    """Creates a new game: the.turn, the.hero and the.world will be
    re-created."""
    the.turn = turn.Turn()
    the.hero = _hero.Hero("Snaugh", ui_object)
    the.turn.add_actor(the.hero)
    the.messages = message.Messages()
    the.world = _world.World(200, 200)
    _world.generate_city(the.world)


def refresh(ui_object):
    """Redraw the entire screen."""
    ui_object.draw_area(the.world)
    ui_object.draw_status(the.turn.current_time())
    ui_object.draw_hero(the.hero)
    ui_object.draw_messages(the.messages)


def main():
    """Bootstraps a new game and cleans up after the game."""
    with _ui.Curses() as ui_object:
        new_game(ui_object)
        the.messages.add("Welcome to Droog.")
        the.messages.add("Press ? for help.")
        refresh(ui_object)
        while the.turn.next():
            refresh(ui_object)
        refresh(ui_object)
        ui_object.input()


if __name__ == "__main__":
    main()
