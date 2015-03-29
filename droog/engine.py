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
    melee_attack(attacker, defender, 'bite')
    return 2


def attack_punch(attacker, defender):
    """Performs a punch attack by the attacker onto the defener."""
    melee_attack(attacker, defender, 'punch')
    return 2


# Attributes should be between 1 and 4, inclusive.
ATTRIBUTE_MAX = 4
ATTRIBUTE_MIN = 1


def is_valid_attribute(attribute):
    """Verifies if an attribute is in a valid range."""
    return ATTRIBUTE_MIN <= attribute <= ATTRIBUTE_MAX

# This is the threshold for a melee hit
MELEE_TOHIT = 4


def melee_attack(attacker, defender, weapon='punch'):
    """Perform a melee attack.

    - Melee offense is the higher of the attacker's strength and dexterity.
    - Melee defense is the higher of the defender's strength and dexterity.
    - Attacker rolls 1d6 + weapon offense + melee offense - melee defense
    - On a 4 or higher, randomly determine one of the defenders stats, then:
      - For strength, apply weakened condition
      - For dexterity, apply hobbled condition
      - For constitution, apply the weapon's special damage
    - On a 3 or less, determine a miss reason by adding to a list:
      - One "dodge" for each dexterity point the defender has.
      - One "parry" for each strength point the defender has.
      - Two "miss"
      - Choosing one of those.

    attacker -- the higher of their strength and dexterity is used
    defender -- at the moment, this is ignored
    weapon -- at the moment, this is a string describing the attack
    """
    LOG.info("Melee attack from %r to %r using %r", attacker, defender, weapon)
    attacker_bonus = max(attacker.strength, attacker.dexterity)
    defender_penalty = max(defender.strength, defender.dexterity)
    weapon_bonus = 0  # Fists only
    attack_roll = random.randint(1, 6)
    attack_magnitude = attack_roll + attacker_bonus + weapon_bonus - \
        defender_penalty
    LOG.info("Melee attack %r (%r die roll + %r attacker bonus + %r weapon"
             " bonus - %r defender penalty)", attack_magnitude, attack_roll,
             attacker_bonus, weapon_bonus, defender_penalty)
    if attack_magnitude >= MELEE_TOHIT:
        the.messages.add("%s %s %s." % (definite_creature(attacker),
                         conjugate_verb(attacker, weapon),
                         definite_creature(defender)))
        inflict_damage(defender)
        return True

    # Determine "why" we missed.
    miss_reason = random.choice(["missed"] * 2 +
                                ["was dodged by"] * defender.dexterity +
                                ["was parried by"] * defender.strength)
    LOG.info("Melee attack %r %r", miss_reason, attack_magnitude)
    the.messages.add("%s %s %s %s" % (possessive(attacker), weapon,
                     miss_reason, definite_creature(defender)))
    return False


def inflict_damage(victim):
    """Inflicts damage onto a creature."""
    strength = victim.strength
    dexterity = victim.dexterity
    constitution = victim.constitution

    # In the must-die case:
    if strength == dexterity == constitution == 1:
        if victim.is_hero:
            the.messages.add("You die.")
        else:
            the.messages.add("%s dies." % definite_creature(victim))
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
    the.messages.add("%s %s is weakened." % (possessive(victim),
                                             damage))


def definite_creature(who):
    """Returns either a creature's name or "you" if the creature is the hero.
    """
    name = "the " + who.name
    if who.is_hero:
        name = "you"
    return name


def possessive(who):
    """Returns a possessive for either a creature by name or "your" if the
    creature is the hero."""
    name = "the %s's" % who.name
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

CONJUGATIONS = {'bite': ("bite", "bites"),
                'punch': ("punch", "punches")}


def conjugate_verb(subject, verb):
    """Returns the conjugation of the verb for a given subject.

    The verb should be provided in the infinitive.
    """
    global CONJUGATIONS
    if verb not in CONJUGATIONS:
        return verb
    if subject.is_hero:
        return CONJUGATIONS[verb][0]
    else:
        return CONJUGATIONS[verb][1]


# Shield generator stats
generator_health = 3
generator_full = 3


def deactivate_generator():
    """Performs one turn worth of deactivation of the generator."""
    verb = "continue"
    global generator_health
    if generator_health == generator_full:
        verb = "begin"
        the.messages.add("A defender materializes nearby.")
        the.world.spawn_monster('z', near=the.world.hero_location)
    the.messages.add("You %s deactivating the shield generator." % verb)
    generator_health -= 1
    if generator_health == 0:
        the.messages.add("You win!")
        the.hero.is_dead = True
    return 8
