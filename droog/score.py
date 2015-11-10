# -*- coding: UTF-8 -*-

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

"""Routines for calculating the hero's score at the end of the game."""

POINTS_PER_TURN = 1
MAX_TURN_POINTS = 25200


def calculate_time_score(turn, victorious):
    """Calculate the score portion based on elapsed time. In the case of a
    victory, shorter games are better. In the case of death, longer games are
    better."""
    if victorious:
        return MAX_TURN_POINTS - (turn.current_turn * POINTS_PER_TURN)
    else:
        return turn.current_turn * POINTS_PER_TURN


def calculate_map_score(world):
    """Calculate the score portion based on amount of the map explored."""
    seen_tiles = 0
    for rows in world.tiles:
        for tile in rows:
            if tile.seen:
                seen_tiles += 1
    return seen_tiles
