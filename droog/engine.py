"""Droog Engine.

This module contains functions for resolving game-rules that either don't fit
in other classes or modules or would cause awkward external dependances for
those classes or modules."""

import logging
import random
import the

LOG = logging.getLogger(__name__)

# When determining the movement cost, diagonal and orthogonal squares do not
# cost the same.
DIAGONAL_COST = 3
ORTHOGONAL_COST = 2

# When determining action point cost of actions for high- or low- dexterity
# actors we apply a modifier, giving a bonus to high-dexterity actors and a
# penalty to low-dexterity actors.
APMOD_HIGHDEX = -1
APMOD_LOWDEX = 1
HIGHDEX_THRESHHOLD = 2
LOWDEX_THRESHHOLD = 2


def movement_cost(delta_y, delta_x):
    """Looks up the movement cost for a particular movement.

    Each diagonal movement costs 3 AP and each orthogonal movement costs 2 AP.
    """
    normal_y = abs(delta_y)
    normal_x = abs(delta_x)
    orthogonal_squares = abs(normal_y - normal_x)
    diaganol_squares = min(normal_y, normal_x)
    return orthogonal_squares * ORTHOGONAL_COST \
        + diaganol_squares * DIAGONAL_COST


def ap_mod(original_ap, dexterity):
    """Applies dexterity modifier to action point cost for one action."""
    modified_ap = original_ap
    if dexterity < LOWDEX_THRESHHOLD:
        modified_ap = original_ap + APMOD_LOWDEX
    if dexterity > HIGHDEX_THRESHHOLD:
        LOG.info("Applying high-dexterity bonus")
        modified_ap = original_ap + APMOD_HIGHDEX
    if modified_ap < 1:
        modified_ap = 1
    return modified_ap


def attack_bite(attacker, defender):
    """Performs a bite attack by the attacker onto the defender."""
    the.messages.add("%s bites %s." % (creature_or_you(attacker),
                                       creature_or_you(defender)))
    inflict_damage(defender)
    return 8


# Attributes should be between 1 and 4, inclusive.
ATTRIBUTE_MAX = 4
ATTRIBUTE_MIN = 1


def is_valid_attribute(attribute):
    """Verifies if an attribute is in a valid range."""
    return ATTRIBUTE_MIN <= attribute <= ATTRIBUTE_MAX


def inflict_damage(victim):
    """Inflicts damage onto a creature."""
    strength = victim.strength
    dexterity = victim.dexterity
    constitution = victim.constitution

    # In the must-die case:
    if strength == dexterity == constitution == 1:
        the.messages.add("You die.")
        victim.is_dead = True
        return

    damage = []

    assert strength > 0
    for _ in range(strength - 1):
        damage.append("strength")

    assert dexterity > 0
    for _ in range(dexterity - 1):
        damage.append("dexterity")

    assert constitution > 0
    for _ in range(constitution - 1):
        damage.append("constitution")

    damage = random.choice(damage)
    old_attribute = getattr(victim, damage)
    setattr(victim, damage, old_attribute - 1)
    LOG.info("Damaged %s's %s from %d to %d", victim, damage, old_attribute,
             old_attribute - 1)
    # TODO: special damage
    the.messages.add("%s %s is weakened." % (creatures_or_your(victim),
                                             damage))


def creature_or_you(who):
    """Returns either a creature's name or "you" if the creature is the hero.
    """
    name = "the " + who.name  # TODO: use indefinate article somtimes?
    if who.is_hero:
        name = "you"
    return name


def creatures_or_your(who):
    """Returns a possessive for either a creature by name or "your" if the
    creature is the hero."""
    name = who.name + "'s"
    if who.is_hero:
        name = "your"
    return name


def indefinite_creature(who):
    """Returns the indefinate referant to a creature."""
    name = who.name
    article = "a"
    if who.is_hero:
        name = "you"
    if who.initial_vowel:
        article = "an"
    return article + " " + name
