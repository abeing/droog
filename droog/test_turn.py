import turn as turn_
import unittest
import actor
import logging

logging.basicConfig()


class TestActor(actor.Actor):
    def __init__(self, name, increment=10):
        """The test actor counts how many times it's gone."""
        self.count = 0
        self.name = name
        self.increment = increment

    def act(self):
        """Inrecement act count for 10 AP."""
        self.count += 1
        return self.increment


class ClockTurnTestCase(unittest.TestCase):
    def runTest(self):
        """A default Turn tracker should contain a clock."""
        turn = turn_.Turn()
        turn.add_actor(TestActor("clock"))
        for t in range(100):
            turn.next()
        self.assertEqual(turn.current_time(), '07:01:40', "We should have"
                         " advanced 100 seconds, to 07:01:40")


class ManyActors(unittest.TestCase):
    def runTest(self):
        """Add a hundred TestActors and run through a thousand next()s"""
        turn = turn_.Turn()
        for _ in range(100):
            turn.add_actor(TestActor(""))
        for _ in range(1000):
            turn.next()


class OrderActors(unittest.TestCase):

    def setUp(self):
        self.turn = turn_.Turn()
        self.odd = TestActor("odd")
        self.even = TestActor("even")
        self.turn.add_actor(self.odd)
        self.turn.add_actor(self.even)

    def testEven(self):
        """Add two actors and iterate through 100 turns. Each should act 50
        times."""
        for _ in range(100):
            self.turn.next()
        self.assertEqual(self.odd.count, 50, "Odd actor should have acted 50"
                         " times.")
        self.assertEqual(self.even.count, 50, "Even actor should have acted"
                         " 50 times.")

    def testOdd(self):
        """Add two actors and iterate through 99 turns. The first actor should
        act once more than the second."""
        for _ in range(99):
            self.turn.next()
        self.assertEqual(self.odd.count, 50, "Odd actor should have acted 50"
                         " times.")
        self.assertEqual(self.even.count, 49, "Even actor should have acted"
                         " 50 times.")


class ActionCostTest(unittest.TestCase):

    def setUp(self):
        self.turn = turn_.Turn()
        self.fast_actor = TestActor("fast", 1)
        self.slow_actor = TestActor("slow", 100)

    def testFast(self):
        """The fast actor should act 99 times to the slow actor's one time."""
        self.turn.add_actor(self.slow_actor)
        self.turn.add_actor(self.fast_actor)
        for _ in range(100):
            self.turn.next()
        self.assertEqual(self.fast_actor.count, 99,
                         "Fast actor should have acted 99 times.")
        self.assertEqual(self.slow_actor.count, 1,
                         "Slow actor should have acted 1 time.")

if __name__ == "__main__":
    unittest.main()
