import actor
import unittest


class ActCheck(unittest.TestCase):
    def testActRaises(self):
        """Actor.act() should raise a NotImplementedError."""
        a = actor.Actor()
        self.assertRaises(NotImplementedError, a.act)


if __name__ == "__main__":
    unittest.main()
