import logging
import random
import the
import engine
import english
import actor

# This is the threshold for a melee hit
MELEE_TOHIT = 4

log = logging.getLogger(__name__)


class BleedAction(actor.Actor):
    def __init__(self, victim):
        """Create a new bleed action, causing the victim to bleed."""
        self.victim = victim
        self.victim.is_bleeding = True

    def act(self):
        """Bleed."""
        if random.randint(0, 100) < self.victim.constitution * 20:
            self.victim.is_bleeding = False
            return self.DONE
        self.victim.blood -= 1
        # We don't check the victim is visible!
        the.messages.add("%s %s." % (english.definite_creature(self.victim),
                         english.conjugate_verb(self.victim, "bleed")))
        if self.victim.blood == 0:
            kill(victim)
        return 60


def attack(attacker, defender, attack):
    """Perform an attack by the attacker onto the defender using attack."""
    assert attack.range == 1  # We only support melee weapons at the moment.
    melee_attack(attacker, defender, attack)
    return 2


def melee_attack(attacker, defender, attack):
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
    attack -- an Attack object describing this attack method
    """
    log.info("Melee attack from %r to %r using %r", attacker, defender, attack)
    verb = random.choice(attack.verbs)
    attacker_bonus = max(attacker.strength, attacker.dexterity)
    defender_penalty = max(defender.strength, defender.dexterity)
    weapon_bonus = 0  # Fists only
    attack_roll = random.randint(1, 6)
    attack_magnitude = attack_roll + attacker_bonus + weapon_bonus - \
        defender_penalty
    log.info("Melee attack %r (%r die roll + %r attacker bonus + %r attack"
             " bonus - %r defender penalty)", attack_magnitude, attack_roll,
             attacker_bonus, weapon_bonus, defender_penalty)
    if attack_magnitude >= MELEE_TOHIT:
        the.messages.add("%s %s %s." % (english.definite_creature(attacker),
                         english.conjugate_verb(attacker, verb),
                         english.definite_creature(defender)))
        inflict_damage(defender, attack)
        return True

    # Determine "why" we missed.
    miss_reason = random.choice(["missed"] * 2 +
                                ["was dodged by"] * defender.dexterity +
                                ["was parried by"] * defender.strength)
    log.info("Melee attack %r %r", miss_reason, attack_magnitude)
    the.messages.add("%s %s %s %s" % (english.possessive(attacker), verb,
                     miss_reason, english.definite_creature(defender)))
    return False


def inflict_damage(victim, attack):
    """Inflicts damage onto a creature."""
    damage = random.choice(['str', 'dex', 'con'])

    if damage == 'str':
        if not victim.is_weakened:
            victim.is_weakened = True
            the.messages.add("%s %s weakened." % 
                             (english.definite_creature(victim),
                              english.conjugate_verb(victim, "be"))
                             )

    if damage == 'dex':
        if not victim.is_hobbled:
            victim.is_hobbled = True
            the.messages.add("%s %s hobbled." % 
                             (english.definite_creature(victim),
                              english.conjugate_verb(victim, "be"))
                             )

    if damage == 'con':
        if random.random() < attack.stun_chance and not victim.is_stunned:
            the.messages.add("%s %s %s." %
                             (english.definite_creature(victim),
                              english.conjugate_verb(victim, "be"), "stunned"))
            victim.is_stunned = True
            stun_time = 10 * (random.randint(2, 5) - victim.constitution)
            log.info("%s is stunned for %s ticks.", victim, stun_time)
            the.turn.delay_actor(victim, stun_time)
        if random.random() < attack.bleed_chance and not victim.is_bleeding:
            bleed = BleedAction(victim)
            the.turn.add_actor(bleed)


def kill(victim):
    """Kill the victim."""
    victim.is_dead = True
    the.messages.add("%s %s" % (english.definite_creature(victim),
                     english.conjugate_verb("die")))
