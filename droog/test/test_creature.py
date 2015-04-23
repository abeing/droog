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


class ActCheck(unittest.TestCase):
    def setUp(self):
        self.c = creature.Creature('Z', "zombie", 2, 2, 2)

    def testActRaises(self):
        """Actor.act() should raise a NotImplementedError."""
        self.c.is_stunned = True
        self.c.act()
        self.assertFalse(self.c.is_stunned)


class NameCheck(unittest.TestCase):
    def setUp(self):
        self.c = creature.Creature('Z', "zombie", 2, 2, 2)

    def testZombieName(self):
        """Zombie name should include indefinite article."""
        self.assertEqual("zombie", str(self.c))


class ConstructionCheck(unittest.TestCase):
    def testLongGlyph(self):
        """Creature glyphs should be on character long."""
        self.assertRaises(AssertionError, creature.Creature, 'ZZ', 'zombie',
                          False, 2, 2, 2)

    def testStrMin(self):
        """Creature strength should be at least 1."""
        self.assertRaises(AssertionError, creature.Creature, 'Z', 'zombie',
                          False, 0, 2, 2)

    def testStrMax(self):
        """Creature strength should be at most 4."""
        self.assertRaises(AssertionError, creature.Creature, 'Z', 'zombie',
                          False, 5, 2, 2)

    def testDexMin(self):
        """Creature Dexterity should be at least 1."""
        self.assertRaises(AssertionError, creature.Creature, 'Z', 'zombie',
                          False, 0, 2, 2)

    def testDexMax(self):
        """Creature constitution should be at most 4."""
        self.assertRaises(AssertionError, creature.Creature, 'Z', 'zombie',
                          False, 5, 2, 2)

    def testConMin(self):
        """Creature constitution should be at least 1."""
        self.assertRaises(AssertionError, creature.Creature, 'Z', 'zombie',
                          False, 0, 2, 2)

    def testConMax(self):
        """Creature constitution should be at least 4."""
        self.assertRaises(AssertionError, creature.Creature, 'Z', 'zombie',
                          False, 5, 2, 2)

if __name__ == "__main__":
    unittest.main()
