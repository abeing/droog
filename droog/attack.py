"""Droog - Attack

The attack module defines various weapons available for use in Droog. This
includes natural weapons such as bites and punches.
"""


class Attack(object):
    """An Attack manages the combat-related aspects of attacks."""
    def __init__(self, name, verbs, attack_bonus, range=1,
                 hobble_chance=0, weaken_chance=0, stun_chance=0,
                 bleed_chance=0, disease_chance=0, use_name=False):
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
        self.hobble_chance = hobble_chance
        self.weaken_chance = weaken_chance
        self.stun_chance = stun_chance
        self.bleed_chance = bleed_chance
        self.disease_chance = disease_chance
        self.use_name = use_name


def make_unarmed():
    """Factory function to create a punch natural attack."""
    return Attack("unarmed", ["punch", "kick"], 0, hobble_chance=25,
                  weaken_chance=25, stun_chance=50, bleed_chance=10)


def make_bite(effectiveness=35):
    """Factory function to create a bite natural attack."""
    return Attack("bite", ["bite", "chomp"], 1, hobble_chance=25,
                  weaken_chance=25, bleed_chance=30,
                  disease_chance=effectiveness)


def make_knife():
    """Factory function to create a knife attack."""
    return Attack("knife", ["slash", "stab", "jab", "slice"], 2, use_name=True,
                  bleed_chance=50, hobble_chance=25, weaken_chance=25)
