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

import droog.turn as turn_
import unittest
from .. import actor
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


class DelayActorTest(unittest.TestCase):

    def setUp(self):
        self.turn = turn_.Turn()
        self.delayed_actor = TestActor("delayed", 10)
        self.other_actor = TestActor("other", 10)

    def testDelay(self):
        """Dealying an actor should allow the other actor to act."""
        self.turn.add_actor(self.delayed_actor)
        self.turn.add_actor(self.other_actor)
        self.turn.delay_actor(self.delayed_actor, 20)
        self.turn.next()
        self.assertEqual(self.delayed_actor.count, 0,
                         "Delayed actor should not have acted.")
        self.assertEqual(self.other_actor.count, 1,
                         "Other actor should have acted first.")

if __name__ == "__main__":
    unittest.main()
