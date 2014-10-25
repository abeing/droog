import datetime
import logging
import sys
import Queue

log = logging.getLogger(__name__)

SECONDS_PER_TURN = 1
START_TIME = datetime.datetime(100, 1, 1, 7, 0, 0)

clock = {"turn": 0}
queue = Queue.PriorityQueue()


def current_time():
    current_time = START_TIME + \
        datetime.timedelta(0, SECONDS_PER_TURN * clock["turn"])
    return current_time.time().isoformat()


def clock_tick():
    clock["turn"] += 1
    return 0.9


def init():
    clock["act_func"] = clock_tick
    queue.put((0, clock))


def next():
    """Advances to the turn."""
    if queue.qsize() == 0:
        log.error("Turn queue should never be empty!")
        sys.exit(1)
    (priority, actor) = queue.get()
    log.info("It is time for %r to act." % actor)
    act_func = actor["act_func"]
    action_cost = act_func()
    next_tick = action_cost + clock["turn"]
    log.info("Requeueing actor %r at turn %r" % (actor, next_tick))
    queue.put((next_tick, actor))
    return True


def add_actor(actor):
    """Add a new actor to the end of the turn queue."""
    queue.put((clock["turn"], actor))
    log.info("New actor in the turn queue: %r" % actor)
