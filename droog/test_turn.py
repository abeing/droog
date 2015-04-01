import turn as turn_
import unittest
import actor


class TestActor(actor.Actor):
    def act(self):
        """Does nothing."""
        return 10


class EmptyTurnTestCase(unittest.TestCase):
    def runTest(self):
        """A default Turn tracker should contain a clock."""
        turn = turn_.Turn()
        for t in range(100):
            turn.next()
        self.assertEqual(turn.current_time(), '07:01:40', "We should have"
                         " advanced 100 seconds, to 07:01:40")


class ManyActors(unittest.TestCase):
    def runTest(self):
        """Add a hundred TestActors and run through a thousand next()s"""
        turn = turn_.Turn()
        for _ in range(100):
            turn.add_actor(TestActor())
        for _ in range(1000):
            turn.next()

if __name__ == "__main__":
    unittest.main()
