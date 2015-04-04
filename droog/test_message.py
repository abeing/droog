import unittest
import message


class QueueTest(unittest.TestCase):
    """Test the queue functionality itself."""

    def setUp(self):
        self.sut = message.Messages()

    def test_empty(self):
        """Test that an empty queue reports it is empty."""
        self.assertTrue(self.sut.empty(), "A new queue should be empty.")

    def test_add_remove(self):
        """Adding and removing a message should result in the same message and
        an empty queue."""
        message = "test message"
        self.sut.add(message)
        self.assertFalse(self.sut.empty())
        got_message = self.sut.get()
        # TODO: self.assertEquals(message, got_message)
        self.assertTrue(self.sut.empty())
