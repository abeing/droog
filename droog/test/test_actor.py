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

from .. import actor
import unittest


class ActCheck(unittest.TestCase):
    """Actor interface unnit tests."""

    def test_act_raises(self):
        """Actor.act() should raise a NotImplementedError."""
        a = actor.Actor()
        self.assertRaises(NotImplementedError, a.act)


if __name__ == "__main__":
    unittest.main()
