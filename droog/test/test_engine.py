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

import mock
from .. import engine
from .. import the

the.world = mock.Mock()
the.hero = mock.Mock()


def test_generator_init():
    """Test that a freshly-created generator has three hit points."""
    generator = engine.Generator()
    assert generator.health == 3


def test_generator_deactivate():
    """Test that deactivating a generator three times results in a win."""
    generator = engine.Generator()
    generator.deactivate()
    assert generator.health == 2
    generator.deactivate()
    assert generator.health == 1
    generator.deactivate()
    assert generator.health == 0
    assert the.hero.is_dead
