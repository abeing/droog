import engine
import random


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
    if who.is_hero:
        return "you"
    name = who.name
    article = "a"
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
                'stop': ("stop", "stops"),
                '_disease': ("feel", "looks")}


def conjugate_verb(subject, verb):
    """Returns the conjugation of the verb for a given subject.

    The verb should be provided in the infinitive.
    """
    global CONJUGATIONS
    if getattr(subject, 'is_hero', False):
        if verb not in CONJUGATIONS:
            return verb
        else:
            return CONJUGATIONS[verb][0]
    else:
        if verb not in CONJUGATIONS:
            return verb + 's'
        else:
            return CONJUGATIONS[verb][1]

ATTRIBUTE_DESCRIPTION = {
                         'str': ["", "weak", "", "strong", "Herculean"],
                         'dex': ["", "clumsy", "", "nimble", "Hermesian"],
                         'con': ["", "sickly", "", "hale", "Panacean"],
                        }


def _lookup_attribute(attribute, value):
    """Provide the English description for a particular attribute.
    attribute -- One of 'str', 'dex', or 'con'.
    value -- An integer between 1 and 4, inclusive.
    """
    if not engine.is_valid_attribute(value):
        raise ValueError("%s is not in valid range [1-4] for English "
                         "conversion")
    return ATTRIBUTE_DESCRIPTION[attribute][value]


def strength(str):
    """Provide English description for a particular stregth score."""
    return _lookup_attribute('str', str)


def dexterity(dex):
    """Provide English description for a particular dexterity score."""
    return _lookup_attribute('dex', dex)


def constitution(con):
    """Provide English description for a particular constitution score."""
    return _lookup_attribute('con', con)


def _make_list(words, conjunction, no_space=False):
    """Make an english, comma separated list of words.
    words -- the list of words to process
    conjunction -- the word used at the end of the list (e.g. and, or)
    no_space -- if True, don't put a space before the conjunction
    """
    if not no_space:
        conjunction = " %s" % (conjunction)
    if len(words) == 0:
        return ""
    elif len(words) == 1:
        return words[0]
    elif len(words) == 2:
        return "%s%s %s" % (words[0], conjunction, words[1])
    elif len(words) == 3:
        # Note the oxford comma between the firs two terms here.
        return "%s,%s %s" % (_make_list(words[:-1], ',', no_space=True), 
                             conjunction, words[-1])


def epithet(str, dex, con, conjunction=None):
    """Create an epithet string for the specified attributes.

    [Good] {but, yet} [Bad]

    where [Good] and [Bad] are (possibly empty) lists of attributes of the form

    Good1
    Good1 and Good2
    Good1, Good2, and Good3

    conjunction -- if None can be one of many, otherwise the one specified
    """

    if not conjunction:
        conjunction = random.choice(["but", "yet"])

    good_attribs = []
    bad_attribs = []
    if str > 2:
        good_attribs.append(strength(str))
    elif str < 2:
        bad_attribs.append(strength(str))
    if dex > 2:
        good_attribs.append(dexterity(dex))
    elif dex < 2:
        bad_attribs.append(dexterity(dex))
    if con > 2:
        good_attribs.append(constitution(con))
    elif con < 2:
        bad_attribs.append(constitution(con))

    if len(good_attribs) + len(bad_attribs) == 0:
        return ""
    elif len(good_attribs) > 0 and len(bad_attribs) > 0:
        return _make_list([_make_list(good_attribs, "and"),
                           _make_list(bad_attribs, "and")], conjunction)
    elif len(good_attribs) > 0:
        return _make_list(good_attribs, "and")
    elif len(bad_attribs) > 0:
        return _make_list(bad_attribs, "and")
    else:
        raise RuntimeError


def wrap(string, width):
    """Wrap a string to a certain width, returning a list of wrapped strings.
    """
    if not string or string == "":
        return [""]

    wrapped = []
    pos = 0
    line = ""

    words = string.split()
    for word in words:
        if pos + len(word) > width:
            if not pos == 0:
                wrapped.append(line)
                line = ""
                pos = 0
        if line:
            line += " " + word
        else:
            line = word
        pos += len(word) + 1
    wrapped.append(line)

    return wrapped
