import unittest
import message
import english


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
        message = "This is a test message."
        self.sut.add(message)
        self.assertFalse(self.sut.empty())
        got_message = self.sut.get()
        self.assertEquals(message, got_message)
        self.assertTrue(self.sut.empty())

    def test_make_sentence(self):
        """Messages should be well-formed sentences."""
        message = "clean me up"
        clean_message = english.make_sentence(message)
        self.sut.add(message)
        got_message = self.sut.get()
        self.assertEquals(got_message, clean_message)

    def test_no_make_sentence(self):
        """When we specify not to clean up messages, we shouldn't."""
        message = "don't clean this one up"
        self.sut.add(message, clean=False)
        got_message = self.sut.get()
        self.assertEquals(got_message, message)
