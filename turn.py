import datetime
import logging
import collections
import sys
import actor

log = logging.getLogger(__name__)


class Clock(actor.Actor):
    """Tracks the current turn and in-game time."""

    def __init__(self):
        self.current_turn = 0
        self.SECONDS_PER_TURN = 1
        self._current_time = datetime.datetime(100, 1, 1, 7, 0, 0)
        self.ap = 0
        self.ap_max = 0

    def current_time(self):
        """Return the current in-game clock.

        Each turn is some number of seconds.
        """
        return self._current_time.time().isoformat()

    def act(self):
        """When it is the clock's turn, it advances the time."""
        self.current_turn += 1
        self._current_time += datetime.timedelta(0, self.SECONDS_PER_TURN)
        log.info("Turn %r start. Time is %r", self.current_turn,
                 self.current_time())
        return 0

    def __repr__(self):
        """The clock's string representation is useful for logging purposes."""
        return "the clock reading " + self.current_time()


class Turn:
    """Tracks the current turn and in-game time."""

    def __init__(self):
        """Creates the turn actor queue and adds the clock to it.

        After initialization, the turn actor queue only has one actor: the
        clock. This means that the first actor of the first turn will be the
        clock and time will advance. We could start the clock earlier than the
        desired game start-time, or implement a no-op tick for the first tick,
        but for now we'll delibrately leave it as is.
        """
        self._queue = collections.deque()
        self._clock = Clock()
        self.add_actor(self._clock)

    def next(self):
        """Advances to the turn."""
        if len(self._queue) == 0:
            log.error("Turn queue should never be empty!")
            sys.exit(1)
        actor = self._queue.popleft()
        log.info("It is time for %r to act." % actor)
        actor.act()
        self._queue.append(actor)
        return True

    def current_time(self):
        """Return the current in-game clock."""
        return self._clock.current_time()

    def add_actor(self, actor):
        """Add a new actor to the end of the turn queue."""
        self._queue.append(actor)
        log.info("New actor in the turn queue: %r" % actor)
