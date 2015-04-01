import turn as turn_
import unittest


class EmptyTurnTestCase(unittest.TestCase):
    def runTest(self):
        """A default Turn tracker should contain a clock."""
        turn = turn_.Turn()
        for t in range(100):
            turn.next()
        self.assertEqual(turn.current_time(), '07:01:40', "We should have"
                         " advanced 100 seconds, to 07:01:40")


if __name__ == "__main__":
    unittest.main()
