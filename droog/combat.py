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

BASE_TOHIT = 3

LOG = logging.getLogger(__name__)


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
            self.victim.end_reason = "killed by deadly disease"
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

    # We might be passed an empty attack in the case of an out-of-ammo weapon
    if not attack:
        return 0

    verb = random.choice(attack.verbs)
    if attack.range == 1:  # Melee attack
        attacker_bonus = attacker.strength
        defender_penalty = defender.strength
        ranged_penalty = 0
    else:  # Ranged attack
        attacker_bonus = attacker.dexterity
        defender_penalty = defender.dexterity
        ranged_penalty = attacker.loc.distance_to(defender.loc) / 10
    weapon_bonus = attack.attack_bonus
    attack_tohit = BASE_TOHIT + weapon_bonus + attacker_bonus \
        - ranged_penalty - defender_penalty
    attack_roll = random.randint(1, 6)
    LOG.info("Attack roll %r on tohit %r (3 + %r attacker bonus + %r weapon"
             " bonus - %r ranged penalty - %r defender penalty)", attack_roll,
             attack_tohit, attacker_bonus, weapon_bonus, ranged_penalty,
             defender_penalty)
    if attack_roll < attack_tohit:
        if defender.is_hero:
            the.messages.add("%s %s." %
                             (english.definite_creature(attacker),
                              english.conjugate_verb(attack, verb)))
        else:
            the.messages.add("%s %s %s." %
                             (english.definite_creature(attacker),
                              english.conjugate_verb(attacker, verb),
                              english.definite_creature(defender)))
        inflict_damage(defender, attack, attacker)
        return 2
    the.messages.add("%s missed." % (english.definite_creature(attacker)))
    return 2


def inflict_damage(victim, attack, attacker):
    """Inflicts damage onto a creature."""

    if random.randint(1, 4) <= victim.constitution:
        if victim.is_wounded:
            victim.end_reason = "killed by %s" % attacker
            kill(victim)
        else:
            wound(victim)

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


def kill(victim):
    """Kill the victim."""
    victim.is_dead = True
    the.messages.add("%s %s" % (english.definite_creature(victim),
                                english.conjugate_verb(victim, "die")))

def wound(victim):
    """Wound the victim."""
    victim.is_wounded = True
    the.messages.add("%s %s" % (english.definite_creature(victim),
                                english.conjugate_verb(victim, "wound")))
