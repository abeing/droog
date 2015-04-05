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

    def __init__(self, turn=None, history_size=100):
        self._queue = Queue.Queue()
        self.history = []
        self._history_size = history_size
        self._turn = turn

    def add(self, message, clean=True):
        """Add a message to the message queue.

        clean -- If true, process it for proper English form
        """
        if clean:
            message = english.make_sentence(message)
        if len(message) is not 0:
            LOG.info("Adding '%s' to the message queue.", message)
            time = self._turn.current_time() if self._turn else ""
            self._queue.put((message, time))
        else:
            LOG.warning("Zero-length message not added to the message queue.")

    def empty(self):
        """True if the message queue is empty."""
        return self._queue.empty()

    def get(self):
        """Return the next message in the queue."""
        message, time = self._queue.get()
        if self._history_size > 0 and len(self.history) >= self._history_size:
            self.history.pop(0)
        self.history.append((message, time))
        return message

    def get_history(self, index, time=True):
        """Get an (optionally time-stamped) message from the history."""
        if index > len(self.history):
            return ""
        text, time = self.history[index]
        if time:
            return "%s %s" % (time, text)
        return text
