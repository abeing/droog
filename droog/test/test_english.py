import unittest
from .. import hero
from .. import english
from .. import creature


class EnglishTest(unittest.TestCase):
    def setUp(self):
        self.hero = hero.Hero("Test", None)
        self.bare_zombie = creature.Zombie(improvement='bare')
        self.str_zombie = creature.Zombie(improvement='str')
        self.dex_zombie = creature.Zombie(improvement='dex')
        self.con_zombie = creature.Zombie(improvement='con')
        self.dog = creature.ZombieDog()
        self.cop = creature.Cop()

    def test_definite_creature(self):
        """Test definite creature."""
        self.assertEqual("you", english.definite_creature(self.hero))
        self.assertEqual("the zombie",
                         english.definite_creature(self.bare_zombie))
        self.assertEqual("the strong zombie",
                         english.definite_creature(self.str_zombie))
        self.assertEqual("the nimble zombie",
                         english.definite_creature(self.dex_zombie))
        self.assertEqual("the hale zombie",
                         english.definite_creature(self.con_zombie))
        self.assertEqual("the zombie dog", english.definite_creature(self.dog))
        self.assertEqual("the cop", english.definite_creature(self.cop))

    def test_possessive(self):
        """Test possessive."""
        self.assertEqual("your", english.possessive(self.hero))
        self.assertEqual("the zombie's",
                         english.possessive(self.bare_zombie))
        self.assertEqual("the strong zombie's",
                         english.possessive(self.str_zombie))
        self.assertEqual("the nimble zombie's",
                         english.possessive(self.dex_zombie))
        self.assertEqual("the hale zombie's",
                         english.possessive(self.con_zombie))
        self.assertEqual("the zombie dog's", english.possessive(self.dog))
        self.assertEqual("the cop's", english.possessive(self.cop))

    def test_indefinite_creature(self):
        """Test indefinite creature."""
        self.assertEqual("you", english.indefinite_creature(self.hero))
        self.assertEqual("a zombie",
                         english.indefinite_creature(self.bare_zombie))
        self.assertEqual("a strong zombie",
                         english.indefinite_creature(self.str_zombie))
        self.assertEqual("a nimble zombie",
                         english.indefinite_creature(self.dex_zombie))
        self.assertEqual("a hale zombie",
                         english.indefinite_creature(self.con_zombie))
        self.assertEqual("a zombie dog", english.indefinite_creature(self.dog))
        self.assertEqual("a cop", english.indefinite_creature(self.cop))


class ConjugationTest(unittest.TestCase):
    def setUp(self):
        self.second = hero.Hero("Test", None)
        self.third = creature.Zombie()

    def test_no_subject(self):
        """Test missing actor."""
        self.assertEqual("is", english.conjugate_verb(None, "be"))

    def test_unknown_verb(self):
        """Test an unknown verb"""
        self.assertEqual("bounce",
                         english.conjugate_verb(self.second, "bounce"))
        self.assertEqual("slithers",
                         english.conjugate_verb(self.third, "slither"))

    def test_irregular(self):
        """Test an irregular verb, such as 'to be'"""
        self.assertEqual("are", english.conjugate_verb(self.second, "be"))
        self.assertEqual("is", english.conjugate_verb(self.third, "be"))


class AttributeTest(unittest.TestCase):
    def test_doc(self):
        self.assertIsNotNone(english.strength.__doc__)

    def test_zero(self):
        self.assertRaises(ValueError, english.strength, 0)
        self.assertRaises(ValueError, english.dexterity, 0)
        self.assertRaises(ValueError, english.constitution, 0)

    def test_five(self):
        """Test attributes of five, which is out of range."""
        self.assertRaises(ValueError, english.strength, 5)
        self.assertRaises(ValueError, english.dexterity, 5)
        self.assertRaises(ValueError, english.constitution, 5)

    def test_two(self):
        """Test attributes of 2, which are 'normal' and should all have empty
        strings."""
        self.assertEqual("", english.strength(2))
        self.assertEqual("", english.dexterity(2))
        self.assertEqual("", english.constitution(2))

    def test_strings(self):
        """Test attributes of 1, 3, and 4, all of which should have text
        descriptions."""
        self.assertEqual("weak", english.strength(1))
        self.assertEqual("nimble", english.dexterity(3))
        self.assertEqual("Panacean", english.constitution(4))


class EpithetTest(unittest.TestCase):
    def test_normals(self):
        """Test all twos."""
        self.assertEqual("", english.epithet(2, 2, 2))

    def test_one(self):
        """Test one good attribute."""
        self.assertEqual("strong", english.epithet(3, 2, 2))
        self.assertEqual("nimble", english.epithet(2, 3, 2))
        self.assertEqual("Panacean", english.epithet(2, 2, 4))
        self.assertEqual("sickly", english.epithet(2, 2, 1))
        self.assertEqual("clumsy", english.epithet(2, 1, 2))
        self.assertEqual("weak", english.epithet(1, 2, 2))

    def test_two_same(self):
        """Test two good or two bad."""
        self.assertEqual("strong and nimble", english.epithet(3, 3, 2))
        self.assertEqual("clumsy and sickly", english.epithet(2, 1, 1))

    def test_three_same(self):
        """Test three good or three bad."""
        self.assertEqual("strong, Hermesian, and hale",
                         english.epithet(3, 4, 3))
        self.assertEqual("weak, clumsy, and sickly",
                         english.epithet(1, 1, 1))

    def test_one_each(self):
        """Test one good and one bad."""
        self.assertEqual("strong but sickly", english.epithet(3, 2, 1, 'but'))
        self.assertEqual("Panacean yet weak", english.epithet(1, 2, 4, 'yet'))

    def test_two_and_one(self):
        """Test two good one bad or one good two bad."""
        self.assertEqual("strong and nimble but sickly",
                         english.epithet(3, 3, 1, 'but'))
        self.assertEqual("nimble and hale yet weak",
                         english.epithet(1, 3, 3, 'yet'))


class WrapTestCase(unittest.TestCase):
    def test_empty(self):
        """Test an empty string."""
        self.assertEqual([""], english.wrap("", 23))

    def test_none(self):
        """Test a null string."""
        self.assertEqual([""], english.wrap(None, 23))

    def test_one_short(self):
        """Test one short word."""
        self.assertEqual(["short"], english.wrap("short", 23))

    def test_two_short(self):
        """Test two words shorter than the line."""
        self.assertEqual(["short again"], english.wrap("short again", 23))

    def test_two_lines(self):
        """Test two lines."""
        self.assertEqual(["shorter", "again"],
                         english.wrap("shorter again", 9))

    def test_word_too_long(self):
        """Test a word that is longer than the line."""
        self.assertEqual(["longerword", "second", "line"],
                         english.wrap("longerword second line", 8))

    def test_hero(self):
        self.assertEqual(["Snaugh the strong,", "nimble, and hale."],
                         english.wrap("Snaugh the strong, nimble, and hale.", 
                                      18))


class SentenceTestCase(unittest.TestCase):
    def test_none(self):
        """Test the None case."""
        self.assertEqual("", english.make_sentence(None))

    def test_empty(self):
        """Test the empty string case."""
        self.assertEqual("", english.make_sentence(""))

    def test_strip(self):
        """Test that strings are stripped."""
        self.assertEqual("", english.make_sentence(" "))

    def test_sentence(self):
        """Test some typical sentences."""
        self.assertEqual("Adam.", english.make_sentence("adam"))
        self.assertEqual("This sucks.", english.make_sentence("this sucks"))

    def test_capital(self):
        """Test some already-capitalized sentences."""
        self.assertEqual("Audelyn.", english.make_sentence("Audelyn"))
        self.assertEqual("It's time.", english.make_sentence("It's time"))

    def test_punctuation(self):
        """Test some already punctuated strings."""
        self.assertEqual("No way!", english.make_sentence("No way!"))
        self.assertEqual("Do we?", english.make_sentence("do we?"))
        self.assertEqual("This sentence is well-formed.",
                         english.make_sentence("This sentence is well-formed.")
                         )

if __name__ == "__main__":
    unittest.main()
