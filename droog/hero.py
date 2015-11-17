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
from . import attack
from . import actor


class Hero(creature.Creature):
    """The Hero is an instance of a Creature with its act() method calling the
    user iterface to determine actions."""
    def __init__(self, name, user_interface):
        super(Hero, self).__init__('@', name)
        self.ui = user_interface
        self.is_hero = True
        self.msg = 0
        self.weapon = attack.make_unarmed()

    def __repr__(self):
        return "the hero %s" % self.name

    def act(self):
        super(Hero, self).act()
        self.ui.draw_hero(self, the.world)
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
        if command == 'f':
            return self.ranged_attack()
        if command == 'r':
            if self.weapon.ammo_capacity == self.weapon.ammo:
                the.messages.add("Your magazine is already full.")
                return 0
            if not self.weapon.reload(self.inventory):
                the.messages.add("You do not have suitable ammo.")
        if command == 'q':
            self.is_dead = True
            self.end_reason = "commited suicide"
            the.messages.add("You commit suicide!")
            return actor.Actor.DONE
        if command == '?':
            self.ui.help()
        return 0

    def melee_attack(self, target):
        """Performs a melee attack against the target."""
        ap_cost = combat.attack(self, target, self.weapon.attack)
        return ap_cost

    def ranged_attack(self):
        """Perform a ranged attack against a target."""
        if self.weapon.ammo_capacity and not self.weapon.ammo:
            the.messages.add("Your weapon is out of ammo!")
            return 0
        target = self.ui.target(self, the.world)
        if target:
            ap_cost = combat.attack(self, target, self.weapon.attack)
            return ap_cost

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
        self.inventory.append(weapon)
        self.weapon = weapon
        self.inventory.extend(items)


def attrib_choices():
    """Return a list of hero attribute options."""
    return ["strongest", "nimblest", "halest"]


def weapon_choices():
    """Return a list of hero weapon choices."""
    return [item.make_pistol(), item.make_knife()]


def gear_choices():
    """Return a list of hero gear choices."""
    return [item.make_porter(), item.make_battery(), item.make_clip()]
