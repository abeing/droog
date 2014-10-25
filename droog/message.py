import Queue

messages = Queue.Queue()


def add(message):
    """Add a message to the message queue."""
    messages.put(message)
