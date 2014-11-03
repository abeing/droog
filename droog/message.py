"""The messages module provides an interface for other modules to add messages
to a queue which the user interface will display."""

import Queue

MESSAGES = Queue.Queue()


def add(message):
    """Add a message to the message queue."""
    MESSAGES.put(message)
