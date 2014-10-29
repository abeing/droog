import actor
import unittest


class ActCheck(unittest.TestCase):
    def testActReturns(self):
        """Actor.act() should return a nonnegative integer."""
        a = actor.Actor()
        result = a.act()
        self.assertGreaterEqual(result, 0)

if __name__ == "__main__":
    unittest.main()
