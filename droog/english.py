
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
                'punch': ("punch", "punches"),
                'chomp': ("chomp", "chomps"),
                'kick': ("kick", "kicks"),
                'slash': ("slash", "slashes"),
                'stab': ("stab", "stabs"),
                'jab': ("jab", "jabs"),
                'slice': ("slice", "slices"),
                'be': ("are", "is"),
                'bleed': ("bleed", "bleeds"),
                'die': ("die", "dies"),
                'stop': ("stop", "stops")}


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
