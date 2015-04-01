import turn as turn_
import unittest
import actor
import logging

logging.basicConfig()


class TestActor(actor.Actor):
    def __init__(self, name):
        """The test actor counts how many times it's gone."""
        self.count = 0
        self.name = name

    def act(self):
        """Inrecement act count for 10 AP."""
        self.count += 1
        return 10


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
        for _ in range(100):
            self.turn.next()
        self.assertEqual(self.odd.count, 50, "Odd actor should have acted 50"
                         " times.")
        self.assertEqual(self.even.count, 50, "Even actor should have acted"
                         " 50 times.")

if __name__ == "__main__":
    unittest.main()
