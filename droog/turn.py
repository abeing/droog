# Droog
# Copyright (C) 2015  Adam Miezianko
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""Droog - Turn"""
import datetime
import logging
import sys
import the
import heapq

LOG = logging.getLogger(__name__)
SECONDS_PER_TURN = 1


class PriorityQueue(object):
    """PriorityQueue implementation that can reorder elements."""

    def __init__(self):
        self._heap = []
        self._entries = {}
        self._REMOVED = None
        self._count = 0

    def get(self):
        """Get the next actor in the queue."""
        while self._heap:
            tick, count, actor = heapq.heappop(self._heap)
            if actor is not self._REMOVED:
                del self._entries[actor]
                return actor
        raise KeyError('Get from an empty priority queue.')

    def put(self, actor, tick=0):
        """Add actor to the queue at the specified tick."""
        if actor in self._entries:
            self._remove(actor)
        self._count += 1
        entry = [tick, self._count, actor]
        self._entries[actor] = entry
        heapq.heappush(self._heap, entry)

    def _remove(self, actor):
        """Mark an entry in the queue as removed."""
        entry = self._entries.pop(actor)
        entry[-1] = self._REMOVED

    def when(self, actor):
        """Return the tick count of an actor, or 0 if not found."""
        return self._entries[actor][1]


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
        self._queue = PriorityQueue()
        self._current_turn = 0
        self._current_time = datetime.datetime(100, 1, 1, 7, 0, 0)  # 07:00:00

    def next(self):
        """Advances to the turn."""

        self._current_turn += 1
        self._current_time += datetime.timedelta(seconds=SECONDS_PER_TURN)

        actor = self._queue.get()  # Ignoring priority
        LOG.info("It is time for %r to act.", actor)

        # check for death
        is_dead = getattr(actor, "is_dead", False)
        if not is_dead:
            action_cost = 0
            while action_cost == 0:
                action_cost = actor.act()
                if action_cost == 0:
                    LOG.info("Actor %r did nothing; goes again.", actor)
            if action_cost == actor.DONE:
                LOG.info("Actor %r is done, not requeueing.", actor)
                return True
            next_tick = action_cost + self._current_turn
            LOG.info("Requeueing actor %r at turn %r", actor, next_tick)
            self._queue.put(actor, next_tick)
        else:
            LOG.info("Removing dead actor %r from turn queue.", actor)
            if getattr(actor, "is_hero", False):
                LOG.info("Removed hero, the game is over.")
                return False
            the.world.remove_monster(actor)
        return True

    def current_time(self):
        """Return the current in-game clock."""
        return self._current_time.time().isoformat()

    def add_actor(self, actor, future=0):
        """Add a new actor to the end of the turn queue."""
        assert future >= 0
        self._queue.put(actor, self._current_turn + future)
        LOG.info("New actor in the turn queue: %r", actor)

    def delay_actor(self, actor, delta):
        """Add a delay to an actor."""
        tick = self._queue.when(actor)
        self._queue.put(actor, tick + delta)
