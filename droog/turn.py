import datetime
import logging
import sys
import actor
import Queue

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
        return 0.9  # This is so the clock always go last on a given tick.

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
        self._queue = Queue.PriorityQueue()
        self._clock = Clock()
        self.add_actor(self._clock)

    def next(self):
        """Advances to the turn."""
        if self._queue.qsize() == 0:
            log.error("Turn queue should never be empty!")
            sys.exit(1)
        (priority, actor) = self._queue.get()
        log.info("It is time for %r to act." % actor)
        action_cost = actor.act()
        next_tick = action_cost + self._clock.current_turn
        log.info("Requeueing actor %r at turn %r" % (actor,
                 next_tick))
        self._queue.put((next_tick, actor))
        return True

    def current_time(self):
        """Return the current in-game clock."""
        return self._clock.current_time()

    def add_actor(self, actor):
        """Add a new actor to the end of the turn queue."""
        self._queue.put((self._clock.current_turn, actor))
        log.info("New actor in the turn queue: %r" % actor)
