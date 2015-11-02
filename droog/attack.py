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

"""Droog - Attack

The attack module defines various weapons available for use in Droog. This
includes natural weapons such as bites and punches.
"""


class Attack(object):
    """An Attack manages the combat-related aspects of attacks."""
    def __init__(self, name, verbs, attack_bonus, attack_range=1,
                 stun_chance=0, bleed_chance=0, disease_chance=0,
                 use_name=False):
        """Create a new Attack.

        name -- a string representing the name of the attack
        verb -- a list of verbs that can be used to describe the use of this
                attack
        range -- attack range, in squares; 1 for melee
        attack_bonus -- more effective weapons are easier to hit with
        use_name -- use the name of this attack in attack messages
        """
        self.name = name
        self.verbs = verbs
        self.attack_bonus = attack_bonus
        self.range = attack_range
        self.stun_chance = stun_chance
        self.bleed_chance = bleed_chance
        self.disease_chance = disease_chance
        self.use_name = use_name


def make_unarmed():
    """Factory function to create a punch natural attack."""
    return Attack("unarmed", ["punch", "kick"], 0, stun_chance=50,
                  bleed_chance=10)


def make_bite(effectiveness=35):
    """Factory function to create a bite natural attack."""
    return Attack("bite", ["bite", "chomp"], 1, bleed_chance=30,
                  disease_chance=effectiveness)


def make_knife():
    """Factory function to create a knife attack."""
    return Attack("knife", ["slash", "stab", "jab", "slice"], 2, use_name=True,
                  bleed_chance=50)


def make_pistol():
    """Make a pistol attack."""
    return Attack("pistol", ["shoot"], 3, bleed_chance=75, attack_range=10)
