"""Droog - Turn"""
import datetime
import logging
import sys
import actor
import Queue
import the

LOG = logging.getLogger(__name__)
SECONDS_PER_TURN = 1


class Clock(actor.Actor):
    """Tracks the current turn and in-game time."""

    def __init__(self):
        self.current_turn = 0
        self._current_time = datetime.datetime(100, 1, 1, 7, 0, 0)

    def current_time(self):
        """Return the current in-game clock.

        Each turn is some number of seconds.
        """
        return self._current_time.time().isoformat()

    def act(self):
        """When it is the clock's turn, it advances the time."""
        self.current_turn += 1
        self._current_time += datetime.timedelta(0, SECONDS_PER_TURN)
        LOG.info("Turn %r start. Time is %r", self.current_turn,
                 self.current_time())
        return 0.9  # This is so the clock always go last on a given tick.

    def __repr__(self):
        """The clock's string representation is useful for logging purposes."""
        return "the clock reading " + self.current_time()


class Turn(object):
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
            LOG.error("Turn queue should never be empty!")
            sys.exit(1)
        (_, an_actor) = self._queue.get()  # Ignoring priority
        LOG.info("It is time for %r to act.", an_actor)
        action_cost = an_actor.act()

        # check for death
        is_dead = getattr(an_actor, "is_dead", False)
        if not is_dead:
            next_tick = action_cost + self._clock.current_turn
            LOG.info("Requeueing actor %r at turn %r", an_actor,
                     next_tick)
            self._queue.put((next_tick, an_actor))
        else:
            LOG.info("Removing dead actor %r from turn queue.", an_actor)
            if getattr(an_actor, "is_hero", False):
                LOG.info("Removed hero, the game is over.")
                return False
            the.world.remove_monster(an_actor)
        return True

    def current_time(self):
        """Return the current in-game clock."""
        return self._clock.current_time()

    def add_actor(self, an_actor):
        """Add a new actor to the end of the turn queue."""
        self._queue.put((self._clock.current_turn, an_actor))
        LOG.info("New actor in the turn queue: %r", an_actor)
