"""Droog - Weapon

The weapon module defines various weapons available for use in Droog. This
includes natural weapons such as bites and punches.
"""


class Weapon(object):
    """A Weapon manages the combat-related aspects of attacks."""
    def __init__(self, name, verbs, attack_bonus, range=1,
                 special_damage=None):
        """Create a new weapon.

        name -- a string representing the name of the weapon
        verb -- a list of verbs that can be used to describe the use of this
                weapon
        range -- weapon range, in squares; 1 for melee
        attack_bonus -- more effective weapons are easier to hit with
        special_damage -- not yet implemented
        """
        self.name = name
        self.verbs = verbs
        self.attack_bonus = attack_bonus
        self.range = range
        self.special_damage = special_damage


def make_unarmed():
    """Factory function to create a punch natural weapon."""
    return Weapon("unarmed", ["punch", "kick"], 0)


def make_bite():
    """Factory function to create a bite natural weapon."""
    return Weapon("bite", ["bite", "chomp"], 0)
