"""Droog - Message

The message module defines the Message class which is a queue of messages to
display in the user interface.
"""
import Queue
import logging
import english


LOG = logging.getLogger(__name__)


class Messages(object):
    """The Messages class allows various components to add messages to be
    displayed in the user interface. The user interface can then filter and
    format the messages."""

    def __init__(self):
        self._queue = Queue.Queue()

    def add(self, message, clean=True):
        """Add a message to the message queue.

        clean -- If true, process it for proper English form
        """
        if clean:
            message = english.make_sentence(message)
        if len(message) is not 0:
            LOG.info("Adding '%s' to the message queue.", message)
            self._queue.put(message)
        else:
            LOG.warning("Zero-length message not added to the message queue.")

    def empty(self):
        """True if the message queue is empty."""
        return self._queue.empty()

    def get(self):
        """Return the next message in the queue."""
        return self._queue.get()
