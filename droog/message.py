"""Droog - Message

The message module defines the Message class which is a queue of messages to
display in the user interface.
"""
import Queue


class Messages(object):
    """The Messages class allows various components to add messages to be
    displayed in the user interface. The user interface can then filter and
    format the messages."""

    def __init__(self):
        self._queue = Queue.Queue()

    def add(self, message):
        """Add a message to the message queue."""
        self._queue.put(message)

    def empty(self):
        """True if the message queue is empty."""
        return self._queue.empty()

    def get(self):
        """Return the next message in the queue."""
        return self._queue.get()
