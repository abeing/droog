#!/usr/bin/python

# Droog
# Copyright (C) 2015  Adam Miezianko
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""Droog - a present-perfect post-apocalyptic roguelike"""
import ui as _ui
import world as _world
import logging
import hero as _hero
import message
import turn
import the
import english
from engine import MonsterSpawner

logging.basicConfig(filename="droog.log", level=logging.DEBUG)
LOG = logging.getLogger(__name__)

EMPTY_STATUS = ""


def new_game(ui_object):
    """Creates a new game: the.turn, the.hero and the.world will be
    re-created."""
    the.turn = turn.Turn()
    the.hero = _hero.Hero("Snaugh", ui_object)
    the.turn.add_actor(the.hero)
    the.messages = message.Messages(turn=the.turn)
    the.world = _world.World(240, 240)
    the.world._log()
    spawner = MonsterSpawner(the.world)
    the.turn.add_actor(spawner)


def refresh(ui_object):
    """Redraw the entire screen."""
    ui_object.draw_area(the.world)
    ui_object.draw_status(time=the.turn.current_time())


def main():
    """Bootstraps a new game and cleans up after the game."""
    with _ui.Curses() as ui_object:
        new_game(ui_object)
        selected_build = ui_object.character_creation(
            english.CREATION_STORY, _hero.attrib_choices(),
            _hero.weapon_choices(), _hero.gear_choices())
        the.hero.build(selected_build)
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
