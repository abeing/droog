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

"""Unit tests for the score module."""

import mock
from .. import score


def test_zero_time():
    """Calculating the time score on turn 0 should give no score."""
    turn = mock.Mock()
    turn.current_turn = 0
    time_score = score.calculate_time_score(turn, False)
    assert time_score == 0


def test_zero_time_victory():
    """A victory on turn zero should give the maximum score allowed for time.
    """
    turn = mock.Mock()
    turn.current_turn = 0
    time_score = score.calculate_time_score(turn, True)
    assert time_score == 25200
