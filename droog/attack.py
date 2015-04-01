"""Droog - Attack

The attack module defines various weapons available for use in Droog. This
includes natural weapons such as bites and punches.
"""


class Attack(object):
    """An Attack manages the combat-related aspects of attacks."""
    def __init__(self, name, verbs, attack_bonus, range=1,
                 stun_chance=0, use_name=False):
        """Create a new Attack.

        name -- a string representing the name of the attack
        verb -- a list of verbs that can be used to describe the use of this
                attack
        range -- attack range, in squares; 1 for melee
        attack_bonus -- more effective weapons are easier to hit with
        special_damage -- not yet implemented
        use_name -- use the name of this attack in attack messages
        """
        self.name = name
        self.verbs = verbs
        self.attack_bonus = attack_bonus
        self.range = range
        self.stun_chance = stun_chance
        self.use_name = use_name


def make_unarmed():
    """Factory function to create a punch natural attack."""
    return Attack("unarmed", ["punch", "kick"], 0, stun_chance=50)


def make_bite():
    """Factory function to create a bite natural attack."""
    return Attack("bite", ["bite", "chomp"], 1)


def make_knife():
    """Factory function to create a knife attack."""
    return Attack("knife", ["slash", "stab", "jab", "slice"], 2, use_name=True)
