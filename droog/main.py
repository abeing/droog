#!/usr/bin/python
"""Droog - a present-perfect post-apocalyptic roguelike"""
import ui as _ui
import world as _world
import logging
import hero as _hero
import message
import creature
import turn
import the
import english

logging.basicConfig(filename="droog.log", level=logging.INFO)
LOG = logging.getLogger(__name__)

EMPTY_STATUS = ""


def new_game(ui_object):
    """Creates a new game: the.turn, the.hero and the.world will be
    re-created."""
    the.turn = turn.Turn()
    the.hero = _hero.Hero("Snaugh", ui_object)
    the.turn.add_actor(the.hero)
    the.messages = message.Messages(turn=the.turn)
    the.world = _world.World(200, 200)
    _world.generate_city(the.world)
    the.world.spawn_monster(creature.Zombie())
    the.world.spawn_monster(creature.Zombie())
    the.world.spawn_monster(creature.ZombieDog())
    the.world.spawn_monster(creature.ZombieDog())
    the.world.spawn_monster(creature.Cop())
    the.world.spawn_monster(creature.Cop())


def refresh(ui_object):
    """Redraw the entire screen."""
    ui_object.draw_area(the.world)
    ui_object.draw_status(time=the.turn.current_time())


def main():
    """Bootstraps a new game and cleans up after the game."""
    with _ui.Curses() as ui_object:
        new_game(ui_object)
        ui_object.character_creation(english.CREATION_STORY,
                                     _hero.attrib_choices(),
                                     _hero.weapon_choices(),
                                    _hero.gear_choices())
        the.messages.add("Welcome to Droog.")
        the.messages.add("Press ? for help.")
        refresh(ui_object)
        while the.world.generator.active() and not the.hero.is_dead:
            the.turn.next()
            refresh(ui_object)
        if the.hero.is_dead:
            ui_object.story_screen(english.FAILURE_STORY)
        elif not the.world.generator.active():
            ui_object.story_screen(english.SUCCESS_STORY)


if __name__ == "__main__":
    main()
