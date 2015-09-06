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

import unittest
from .. import creature


class CreatureChecks(unittest.TestCase):
    """Unit tests for creatures."""

    def setUp(self):
        self.sut = creature.Creature('Z', "zombie")

    def test_act_raises(self):
        """Actor.act() should raise a NotImplementedError."""
        self.sut.is_stunned = True
        self.sut.act()
        self.assertFalse(self.sut.is_stunned)

    def test_zombie_name(self):
        """Zombie name should include indefinite article."""
        self.assertEqual("zombie", str(self.sut))

    def test_long_glyph(self):
        """Creature glyphs should be on character long."""
        self.assertRaises(AssertionError, creature.Creature, 'ZZ', 'zombie',
                          False)

if __name__ == "__main__":
    unittest.main()
