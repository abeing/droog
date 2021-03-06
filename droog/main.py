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
import sys
import getopt
import logging
import ui as _ui
import world as _world
import hero as _hero
import message
import turn
import the
import english
from . import engine
from . import score

logging.basicConfig(filename="droog.log", level=logging.DEBUG)
LOG = logging.getLogger(__name__)

EMPTY_STATUS = ""


def new_game(ui_object, hero_name):
    """Creates a new game: the.turn, the.hero and the.world will be
    re-created."""
    the.turn = turn.Turn()
    the.hero = _hero.Hero(hero_name[:10], ui_object)
    the.turn.add_actor(the.hero)
    the.messages = message.Messages(turn=the.turn)
    the.world = _world.World(240, 240)
    the.world._log()
    monster_spawner = engine.MonsterSpawner(the.world)
    the.turn.add_actor(monster_spawner)
    monster_spawner.populate()
    loot_placer = engine.LootPlacer(the.world)
    loot_placer.populate()


def end_game(ui_object):
    """Display the ending, calculate the score and display to top scores."""
    if the.hero.is_dead:
        ui_object.draw_messages(the.messages)
        ui_object.input()
        ui_object.story_screen(english.FAILURE_STORY)
    elif not the.world.generator.active():
        ui_object.story_screen(english.SUCCESS_STORY)
    time_score = score.calculate_time_score(the.turn, not the.hero.is_dead)
    map_score = score.calculate_map_score(the.world)
    kill_score = score.calculate_kill_score(the.world.dead_monsters)
    victory_score = score.calculate_victory_score(not the.hero.is_dead)
    ui_object.score_screen(time_score, map_score, kill_score, victory_score)
    total_score = time_score + map_score + kill_score + victory_score
    high_scores = score.record_score(the.hero.name, the.hero.end_reason,
                                     total_score)
    ui_object.record_screen(high_scores)


def refresh(ui_object):
    """Redraw the entire screen."""
    ui_object.draw_area(the.world)
    ui_object.draw_status(time=the.turn.current_time())


def main(argv):
    """Bootstraps a new game and cleans up after the game."""
    hero_name = 'Snaugh'
    try:
        opts, args = getopt.getopt(argv, "n:")
    except getopt.GetoptError:
        print 'python -m droog.main'
        system.exit(2)
    for opt, arg in opts:
        if opt == '-n':
            hero_name = arg
    with _ui.Curses() as ui_object:
        new_game(ui_object, hero_name)
        selected_build = ui_object.character_creation(
            english.CREATION_STORY, _hero.attrib_choices(),
            _hero.weapon_choices(), _hero.gear_choices())
        if selected_build[0] == None:
            return
        the.hero.build(selected_build)
        the.messages.add("Welcome to Droog.")
        the.messages.add("Press ? for help.")
        refresh(ui_object)
        while the.world.generator.active() and not the.hero.is_dead:
            the.turn.next()
            refresh(ui_object)
        end_game(ui_object)

if __name__ == "__main__":
    main(sys.argv[1:])
