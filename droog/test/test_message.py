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

import unittest
from .. import message
from .. import english
from .. import turn


class QueueTest(unittest.TestCase):
    """Test the queue functionality itself."""

    def setUp(self):
        self.sut = message.Messages()

    def test_empty(self):
        """Test that an empty queue reports it is empty."""
        self.assertTrue(self.sut.empty(), "A new queue should be empty.")

    def test_add_remove(self):
        """Adding and removing a message should result in the same message and
        an empty queue."""
        message = "This is a test message."
        self.sut.add(message)
        self.assertFalse(self.sut.empty())
        got_message = self.sut.get()
        self.assertEquals(message, got_message)
        self.assertTrue(self.sut.empty())

    def test_make_sentence(self):
        """Messages should be well-formed sentences."""
        message = "clean me up"
        clean_message = english.make_sentence(message)
        self.sut.add(message)
        got_message = self.sut.get()
        self.assertEquals(got_message, clean_message)

    def test_no_make_sentence(self):
        """When we specify not to clean up messages, we shouldn't."""
        message = "don't clean this one up"
        self.sut.add(message, clean=False)
        got_message = self.sut.get()
        self.assertEquals(got_message, message)

    def test_timestamps(self):
        """We should be able to provide a Turn for timestamps."""
        clock = turn.Turn()
        sut = message.Messages(turn=clock)


class HistoryTestCase(unittest.TestCase):
    """TestCases for the message log."""

    def setUp(self):
        self.history_size = 10
        self.sut = message.Messages(history_size=10)

    def test_history_add(self):
        """Test that messages are added to the history when removed from the
        queue."""
        self.sut.add("One")
        self.assertEquals(0, len(self.sut.history))
        self.sut.get()
        self.assertEquals(1, len(self.sut.history))

    def test_history_cap(self):
        """Test that only the maximum number of messages are stored."""
        for x in range(self.history_size + 1):
            self.sut.add("Message %d" % (x))
            self.sut.get()
        self.assertEquals(10, len(self.sut.history))
        self.assertEquals("Message 1.", self.sut.get_history(0, time=False))

    def test_no_history(self):
        """Test that a history_size of zero provides no history."""
        sut = message.Messages(history_size=0)
        sut.add("One")
        self.assertEquals(0, len(sut.history))
        sut.get()
        self.assertEquals(1, len(sut.history))

    def test_get_history(self):
        """Test that getting a non-existant history message returns an empty
        string."""
        self.assertEquals("", self.sut.get_history(100))
