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

import logging
import random
from . import the
from . import english
from . import actor

# This is the threshold for a melee hit
MELEE_TOHIT = 4
RANGED_TOHIT = 5

LOG = logging.getLogger(__name__)


class BleedAction(actor.Actor):
    """Actor to apply bleeding condition to creatures."""
    def __init__(self, victim, magnitude):
        """Create a new bleed action, causing the victim to bleed."""
        self.victim = victim
        self.victim.is_bleeding = True
        self.magnitude = magnitude

    def act(self):
        """Bleed."""
        self.victim.blood -= 1
        if self.victim.blood <= 0:
            the.messages.add("%s bled out." %
                             (english.definite_creature(self.victim)))
            kill(self.victim)
            return self.DONE
        # We don't check the victim is visible!
        victim_english = english.definite_creature(self.victim)
        if random.randint(0, self.magnitude) > self.victim.constitution * 20:
            self.victim.is_bleeding = False
            the.messages.add("%s %s bleeding." %
                             (victim_english,
                              english.conjugate_verb(self.victim, "stop")))
            return self.DONE
        else:
            the.messages.add("%s %s." %
                             (victim_english,
                              english.conjugate_verb(self.victim, "bleed")))
        return 60


class DiseaseAction(actor.Actor):
    """Actor that applies diseased condition on creatures."""
    def __init__(self, victim):
        """Create a new disease action, causing the victim to die
        eventually."""
        self.victim = victim
        self.progress = 2

    PROGRESS = ["near death from illness", "quite ill", "feverish"]

    def act(self):
        if self.victim.is_diseased:
            return self.DONE
        if self.progress == 0:
            kill(self.victim)
            return self.DONE
        self.victim.is_diseased = True
        the.messages.add("%s %s %s." %
                         (english.definite_creature(self.victim),
                          english.conjugate_verb(self.victim, "_disease"),
                          self.PROGRESS[self.progress]))
        self.progress -= 1
        return 3600 * self.victim.constitution


def attack(attacker, defender, attack):
    """Perform a melee attack.

    - Melee offense is the higher of the attacker's strength and dexterity.
    - Melee defense is the higher of the defender's strength and dexterity.
    - Attacker rolls 1d6 + weapon offense + melee offense - melee defense
    - On a 4 or higher, apply damage

    attacker -- the higher of their strength and dexterity is used
    defender -- at the moment, this is ignored
    attack -- an Attack object describing this attack method
    """
    LOG.info("Melee attack from %r to %r using %r", attacker, defender, attack)
    verb = random.choice(attack.verbs)
    if attack.range == 1:  # Melee attack
        tohit = MELEE_TOHIT
        attacker_bonus = max(attacker.strength, attacker.dexterity)
        defender_penalty = max(defender.strength, defender.dexterity)
    else:  # Ranged attack
        tohit = RANGED_TOHIT
        attacker_bonus = attacker.dexterity
        defender_penalty = attacker.loc.distance_to(defender.loc) / 10
    weapon_bonus = attack.attack_bonus
    attack_roll = random.randint(1, 6)
    attack_magnitude = attack_roll + attacker_bonus + weapon_bonus - \
        defender_penalty
    LOG.info("Attack %r (%r die roll + %r attacker bonus + %r attack"
             " bonus - %r defender penalty)", attack_magnitude, attack_roll,
             attacker_bonus, weapon_bonus, defender_penalty)
    if attack_magnitude >= tohit:
        if defender.is_hero:
            the.messages.add("%s %s." %
                             (english.definite_creature(attacker),
                              english.conjugate_verb(attack, verb)))
        else:
            the.messages.add("%s %s %s." %
                             (english.definite_creature(attacker),
                              english.conjugate_verb(attacker, verb),
                              english.definite_creature(defender)))
        inflict_damage(defender, attack)
        return True

    LOG.info("Attack missed with %r", attack_magnitude)
    the.messages.add("%s missed." % (english.definite_creature(attacker)))
    return 2


def inflict_damage(victim, attack):
    """Inflicts damage onto a creature."""

    if random.random() < attack.weaken_chance and not victim.is_weakened:
        victim.is_weakened = True
        the.messages.add("%s %s weakened." %
                         (english.definite_creature(victim),
                          english.conjugate_verb(victim, "be")))

    if random.random() < attack.hobble_chance and not victim.is_hobbled:
        victim.is_hobbled = True
        the.messages.add("%s %s hobbled." %
                         (english.definite_creature(victim),
                          english.conjugate_verb(victim, "be")))

    if random.random() < attack.stun_chance and not victim.is_stunned:
        the.messages.add("%s %s %s." %
                         (english.definite_creature(victim),
                          english.conjugate_verb(victim, "be"), "stunned"))
        victim.is_stunned = True
        stun_time = 10 * (random.randint(2, 5) - victim.constitution)
        LOG.info("%s is stunned for %s ticks.", victim, stun_time)
        the.turn.delay_actor(victim, stun_time)

    if random.random() < attack.disease_chance and not victim.is_diseased:
        disease = DiseaseAction(victim)
        the.turn.add_actor(disease, 600)

    if random.random() < attack.bleed_chance:
        if victim.is_bleeding:
            victim.blood -= 1
        else:
            bleed = BleedAction(victim, attack.bleed_chance)
            the.turn.add_actor(bleed)


def kill(victim):
    """Kill the victim."""
    victim.is_dead = True
    the.messages.add("%s %s" % (english.definite_creature(victim),
                                english.conjugate_verb(victim, "die")))
