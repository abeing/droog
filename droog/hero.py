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

"""Droog Hero class"""
import sys
from . import the
from . import combat
from . import creature
from . import item


class Hero(creature.Creature):
    """The Hero is an instance of a Creature with its act() method calling the
    user iterface to determine actions."""
    def __init__(self, name, user_interface):
        super(Hero, self).__init__('@', name)
        self.ui = user_interface
        self.is_hero = True
        self.weapon = item.make_pistol()
        self.inventory.append(item.make_pistol())
        self.msg = 0

    def __repr__(self):
        return "the hero %s" % self.name

    def act(self):
        super(Hero, self).act()
        self.ui.draw_hero(self)
        self.ui.draw_messages(the.messages)
        command = self.ui.input()
        if command in self.ui.movements:
            delta_y, delta_x = self.ui.movements[command]
            return the.world.move_hero(delta_y, delta_x)
        if command == '/':
            self.ui.look(the.world)
            return 0
        if command == 'd':
            self.ui.drop(self, the.world)
        if command == 'p':
            self.ui.pickup(self, the.world)
        if command == '~':
            self.ui.wizard(the.world)
        if command == 'm':
            self.ui.history(the.messages)
        if command == 'q':
            sys.exit(0)
        if command == '?':
            self.ui.help()
        return 0

    def melee_attack(self, target):
        """Performs a melee attack against the target."""
        return combat.attack(self, target, self.weapon.attack)

    def build(self, build):
        """Apply the character creation build.

        Build is a tuple of attribute name, weapon and items."""
        attrib_name, weapon, items = build
        if attrib_name == "strongest":
            self._strength = 3
        elif attrib_name == "nimblest":
            self._dexterity = 3
        elif attrib_name == "halest":
            self._constitution = 3


def attrib_choices():
    """Return a list of hero attribute options."""
    return ["strongest", "nimblest", "halest"]


def weapon_choices():
    """Return a list of hero weapon choices."""
    return ["rifle", "pistol", "knife"]


def gear_choices():
    """Return a list of hero gear choices."""
    return ["local porter", "battery", "grenades"]
