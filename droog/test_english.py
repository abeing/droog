import unittest
import hero
import english
import creature


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

if __name__ == "__main__":
    unittest.main()
