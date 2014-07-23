import datetime
import logging
import Queue

log = logging.getLogger(__name__)

class Turn:
    """Tracks the current turn and in-game time."""

    def __init__(self):
        self.current_turn = 0
        self.SECONDS_PER_TURN = 6
        self._current_time = datetime.datetime(100, 1, 1, 7, 0, 0)
        self._queue = Queue.Queue()

    def next(self):
        """Advances to the turn."""
        self.current_turn += 1
        self._current_time += datetime.timedelta(0, self.SECONDS_PER_TURN)

    def current_time(self):
        """Return the current in-game clock.

        Each turn is some number of seconds.
        """
        return self._current_time.time().isoformat()

    def add_actor(self, actor):
        """Add a new actor to the end of the turn queue."""
        self._queue.put(actor)
        log.info("New actor in the turn queue: %r" % actor)
