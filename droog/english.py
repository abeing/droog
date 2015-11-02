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

import textwrap
import random
import engine

# Attribute descriptions in lookup order from 0 to 4.
ATTRIBUTE_DESCRIPTION = {'str': ["", "weak", "", "strong", "Herculean"],
                         'dex': ["", "clumsy", "", "nimble", "Hermesian"],
                         'con': ["", "sickly", "", "hale", "Panacean"]}

# Verb conjugations, in the form:
#   infinitive: (second_person_singular, third_person_singular)
# Underscores are used to denote special-purpose verbs, where the second person
# might use a differnt verb than the third person (e.g. you feel, it looks).
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
                'wound': ("are wounded", "is wounded"),
                '_disease': ("feel", "looks")}

# Punctuation that is considered approprate to end a sentence with.
TERMINAL_PUNCTUATION = ['.', '?', '!']

CREATION_STORY = \
 [["Commander Splinter stands before you, pacing the room as he briefs you on"
   " your ultimate mission. 'As you know, our Orbital Sephiroth strike was"
   " unable to take out the Mother. The whole town is awash in cabalistic"
   " mana, so we put a Netzach Shield around the perimiter. The trouble is,"
   " we only have one working Personal Netzach Shield.'"],
  ["He looks at you with a grim expression, sighs, and continues. 'That's"
   " where you come in. You are our ", "{attrib}", ". We need you to go in"
   "there with boots on the ground and finish the job. Our supplies are low,"
   " so you'll have our last Sephiroth grenade, the PNS, ", "{weapon}",
   "{gear}", "{gear}", "{gear}", ".'"],
  ["'We'll drop the Netzach wall for a second and teleport you in. Godspeed.'"
   " He gives you a firm solute."]]


FAILURE_STORY = ["""Commander Splinter stared at dart gun the Cop Mark III was
aiming at him. He felt a sharp pain in his chest and looked down. The dart
buried deep in his heart filled him with dread which quickly melted into a
powerful hunger for brains. Seeing no brains, bolted into the street.""", """So
many humans with brains intact were streaming out into the streets he didn't
know where to start. He grabbed a young woman and pushed her onto her kneees.
With powerful fists he bludgeoned her skull until he could see glistening grey
matter. He stopped his inhuman violence and reached his fingers between skull
shards and extracted a small handful of brains. He tasted the soft, gooey
delicacy and savored it briefly before he felt his entire nervous system erupt
with pleasure. He fell upon the young woman's remaining brain like a starving
man.""", """He was just one zombie in an entire zombie army that made quick
work of humanity."""]

SUCCESS_STORY = ["""The computer display blinks and spews cryptic messages
on a bright blue screen. You sigh, your mission is a success.""", """All over
the world, bots shut down and become empty husks. Humans emerge from their
hiding places and begin to destroy all of the contaminated crops and processed
foods.""", """Over time, human civilization rebuilds itself. You have saved
humanity. Your name goes down as one of the most remembered in all of history.
Even though your body succumbs to radiation sickness, you have achieved
immortality."""]


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


def conjugate_verb(subject, verb):
    """Returns the conjugation of the verb for a given subject.

    The verb should be provided in the infinitive.
    """
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


def partial_wrap(string, width):
    """Wrap a string to width but return the remaining unwrapped string too."""
    first_line = textwrap.wrap(string, width)
    rest_lines = string[len(first_line[0])+1:]
    return first_line[0], rest_lines


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


def make_sentence(string):
    """Convert a string into a well-formed sentence.

    - The first character will be capitalized (if not already).
    - If the last character is not punctuation, a period will be added.
    """
    if not string:
        return ""
    string = string.strip()
    if len(string) is not 0:
        string = string.capitalize()
        if string[-1] not in TERMINAL_PUNCTUATION:
            string = string + "."
    return string
