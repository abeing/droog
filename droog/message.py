"""Droog - Message

The message module defines the Message class which is a queue of messages to
display in the user interface.
"""
import Queue
import logging


LOG = logging.getLogger(__name__)


class Messages(object):
    """The Messages class allows various components to add messages to be
    displayed in the user interface. The user interface can then filter and
    format the messages."""

    def __init__(self):
        self._queue = Queue.Queue()

    def add(self, message):
        """Add a message to the message queue. Each message should be one
        sentence. The first word will be capitalized (if not already) and the
        sentence will end with a period (if not already)."""
        if len(message) is not 0:
            message = message.capitalize()
            if message[-1] is not ".":
                message = message + "."
                LOG.info("Appending period to non-period-terminated message")
            LOG.info("Adding %s to the message queue.", message)
            self._queue.put(message)
        else:
            LOG.warning("Zero-length message not added to the message queue.")

    def empty(self):
        """True if the message queue is empty."""
        return self._queue.empty()

    def get(self):
        """Return the next message in the queue."""
        return self._queue.get()
