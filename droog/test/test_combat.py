import unittest
import creature
import combat
import mock
import the
import attack
import logging

logging.basicConfig(filename="unittest.log", level=logging.INFO)
the.messages = mock.Mock()
the.turn = mock.Mock()


class MeleeTestCase(unittest.TestCase):
    """Tests for melee attacks."""

    def setUp(self):
        """Create test fixtures."""
        self.attacker = creature.Zombie()
        self.defender = creature.Zombie()
        # A test attack that always hits.
        self.attack = attack.Attack("test", ["test"], 100)

    def test_action(self):
        """Melee attacks all cost 2 AP."""
        self.assertEquals(2, combat.attack(self.attacker, self.defender,
                                           self.attack))


class DamageTestCase(unittest.TestCase):
    """Tests for damage."""

    def setUp(self):
        """Create test fixtures."""
        self.attacker = creature.Zombie()
        self.defender = creature.Zombie()

    def test_no_status(self):
        """Test that an attack with all zero chances results in no status."""
        none_attack = attack.Attack("test", ["test"], 100)
        combat.attack(self.attacker, self.defender, none_attack)
        self.assertEquals(0, condition_count(self.defender))

    def test_stunned(self):
        """Test an attack that is guaranteed to stun the defender."""
        stun_attack = attack.Attack("test", ["test"], 100, stun_chance=100)
        combat.attack(self.attacker, self.defender, stun_attack)
        self.assertEquals(1, condition_count(self.defender))
        self.assertTrue(self.defender.is_stunned)

    def test_bleeding(self):
        """Test an attack that is guaranteed to make the defender bleed."""
        bleed_attack = attack.Attack("bleed", ["bleed"], 100, bleed_chance=100)
        combat.attack(self.attacker, self.defender, bleed_attack)
        self.assertEquals(1, condition_count(self.defender))
        self.assertTrue(self.defender.is_bleeding)

    def test_weakened(self):
        """Test an attack that is guaranteed to make the defender weakened."""
        weakened_attack = attack.Attack("weakened", ["weakened"], 100,
                                        weaken_chance=100)


def condition_count(creature):
    """Count the number of conditions set on the creature."""
    count = creature.is_hobbled + creature.is_weakened + creature.is_bleeding \
        + creature.is_stunned + creature.is_diseased
    return count

if __name__ == "__main__":
    unittest.main()
