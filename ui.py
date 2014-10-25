import curses
import logging
import sys
import message

MINIMUM_WIDTH = 80
MINIMUM_HEIGHT = 24

HERO_COLUMNS = 18
MESSAGE_ROWS = 3
STATUS_ROWS = 1
STATUS_COLUMNS = 47

log = logging.getLogger(__name__)

movements = {'h': (0, -1),   # West
             'l': (0, 1),    # East
             'j': (1, 0),    # South
             'k': (-1, 0),   # North
             'y': (-1, -1),  # Northwest
             'u': (-1, 1),   # Northeast
             'b': (1, -1),   # Southwest
             'n': (1, 1),    # Southeast
             }


class UI:
    def __init__(self):
        """Initializes the rendering environment.

        Currently this initializes curses and creates the following curses
        windows and borders around them:

        -- area_window : 23 rows, 47 columns displays the map with the hero in
                         the center
        -- hero_window : 10 rows, 30 columns displays the hero information
        -- message_window : 3 rows, full width, displays messages
        """

        self.main_window = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        # Our screen size
        height, width = self.main_window.getmaxyx()
        log.info('Main window has %r width and %r height', width, height)

        # Ensure that our screen size is at least the minimum required
        if width < MINIMUM_WIDTH or height < MINIMUM_HEIGHT:
            self.shutdown()
            print 'ERROR: Terminal window too small.'
            print 'Minimum width: %r' % MINIMUM_WIDTH
            print 'Minimum height: %r' % MINIMUM_HEIGHT
            sys.exit(1)

        # Calculate the area window size (it should be the biggest)
        self.area_width = width - HERO_COLUMNS - 1
        self.area_height = height - MESSAGE_ROWS - STATUS_ROWS - 1
        log.info('Area window has %r width and %r height', self.area_width,
                 self.area_height)

        # We make the area_window actually be one column larger than necessary
        # because curses will throw an error if we write to the
        # bottom-right-most character.
        self.area_window = self.main_window.subwin(self.area_height,
                                                   self.area_width + 1,
                                                   4, 0)

        # Draw the border between the area window and the hero windows.
        for y in range(MESSAGE_ROWS, self.area_height + MESSAGE_ROWS + 1):
            self.main_window.addch(y, self.area_width, '|')

        self.hero_window = self.main_window.subwin(self.area_height,
                                                   HERO_COLUMNS,
                                                   MESSAGE_ROWS + 1,
                                                   self.area_width + 1)

        # Draw the border between the hero window and the message window,
        for x in range(0, width):
            self.main_window.addch(3, x, '-')
        self.main_window.addch(3, self.area_width, '+')

        self.message_window = self.main_window.subwin(MESSAGE_ROWS,
                                                      width,
                                                      0,
                                                      0)
        self.message_window.scrollok(True)
        self.message_column = 0
        self.message_row = 0

        self.status_line = self.main_window.subwin(STATUS_ROWS,
                                                   width,
                                                   self.area_height + 1
                                                   + MESSAGE_ROWS, 0)

        # The hero will always be present in the center.
        self.hero_x_offset = self.area_width / 2
        self.hero_y_offset = self.area_height / 2

        # We need to refresh the main window at least once, even if we do all
        # updates through child windows.
        self.main_window.refresh()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()

    def shutdown(self):
        """Ends curses and restores the terminal state."""
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()

    def map_bounds(self, world):
        """Calculate world coordinates visible in the UI area.

        Return the left and right limit of the x-axis and top and bottom
        limit of the y-axis of the world-coordinates visible in the area
        window.

        The coorindates are returned as a tuple of (left, right, top, bottom).

        The calculation is based on the hero's location.
        """
        (hero_y, hero_x) = world.hero_location
        left = hero_x - self.hero_x_offset
        right = hero_x + self.hero_x_offset
        top = hero_y - self.hero_y_offset
        bottom = hero_y + self.hero_y_offset
        return (left, right, top, bottom)

    def create_meter(self, value, maximum):
        """Create a string representing a proprtion of a value.

        A `value` number of asterisks fill a `maximum` number of empty spaces,
        bookended by square brackets.

        For example a strgeth of 2 out of 3 is represented as [** ]
        """
        log.debug("Creating a meter of %r out of %r." % (value, maximum))
        ivalue = int(value)
        meter = "["
        for x in range(0, ivalue):
            meter += "*"
        for y in range(0, maximum - ivalue):
            meter += " "
        meter += "]"
        log.debug("Returning the meter as %r" % meter)
        return meter

    def draw_area(self, world):
        """Draws an area of the world onto the renderer's area window."""
        (left, right, top, bottom) = self.map_bounds(world)

        # If the area is an odd height and/or width we want to add one to the
        # bottom and/or right to prevent a gutter of undrawn map.
        if not self.area_width % 2 == 0:
            right += 1
        if not self.area_height % 2 == 0:
            bottom += 1

        for y in range(top, bottom):
            for x in range(left, right):
                self.area_window.addstr(y - top, x - left,
                                        world.glyph_at(y, x))
                creature = world.creature_at(y, x)
                if creature is not None:
                    self.area_window.addstr(y - top, x - left,
                                            creature.glyph)

        # The hero is drawn in the center last so we can always see him or
        # her. The curses is then placed on top of the hero for visual
        # distinction.
        self.area_window.addstr(self.hero_y_offset, self.hero_x_offset,
                                '@', curses.A_REVERSE)
        self.area_window.refresh()

    def draw_status(self, message):
        """Draws the status message, if any."""
        self.status_line.addstr(0, 0, message)
        self.status_line.clrtoeol()
        self.status_line.refresh()

    def draw_hero(self, hero):
        """Draws the hero information window. Does not draw the actual @
        symbol on the map; that is handled by draw_area."""
        self.hero_window.addstr(0, 0, hero.name)
        strength_meter = self.create_meter(hero.str, 3)
        dexterity_meter = self.create_meter(hero.dex, 3)
        constitution_meter = self.create_meter(hero.con, 3)
        self.hero_window.addstr(1, 2, "Str %s" % strength_meter)
        self.hero_window.addstr(2, 2, "Dex %s" % dexterity_meter)
        self.hero_window.addstr(3, 2, "Con %s" % constitution_meter)
        self.hero_window.addstr(9, 0, "Equipped:")
        self.hero_window.addstr(10, 1, "Knife")
        self.hero_window.addstr(11, 0, "Inventory:")
        self.hero_window.addstr(12, 1, "9mm pistol (6)")
        self.hero_window.addstr(13, 1, "2 pistol clips")
        self.hero_window.refresh()

    def draw_messages(self):
        """Draws the most recent messages in the message log."""

        height, width = self.message_window.getmaxyx()

        while not message.messages.empty():
            a_message = message.messages.get()
            words = a_message.split()
            for word in words:
                log.info("line %r col %r", self.message_row,
                         self.message_column)
                if (self.message_column + len(word) > width):
                    self.message_row += 1
                    self.message_column = 0
                if self.message_row == height:
                    self.main_window.addstr(self.message_row, 75, "MORE",
                                            curses.A_REVERSE)
                    self.main_window.refresh()
                    self.message_window.getch()
                    self.message_window.scroll(1)
                    self.main_window.addstr(self.message_row, 75, "----")
                    self.message_row = height - 1
                self.message_window.addstr(self.message_row,
                                           self.message_column, word)
                self.message_column += len(word) + 1
        self.message_window.refresh()

    def look(self, world):
        """Enters look mode. Look mode allows the player to move the cursor
        around the map area with the cursor-movement keys. While looking, the
        status line updates with information about whatever is under the cursor
        at the time."""
        self.draw_status("Looking around (using the movement keys).")
        max_y, max_x = self.area_window.getmaxyx()
        y = self.hero_y_offset
        x = self.hero_x_offset
        curses.curs_set(1)
        self.area_window.move(y, x)
        self.area_window.refresh()

        (left, right, top, bottom) = self.map_bounds(world)

        command = chr(self.input())
        while command in movements:
            delta_y, delta_x = movements[command]
            y += delta_y
            x += delta_x
            if y >= 0 and y < max_y and x >= 0 and x < max_x - 1:
                log.info("Highlighting %r, %r.", y, x)
                description = world.description_at(y + top,
                                                   x + left)
                self.draw_status("You see here %s." % description)
                self.area_window.move(y, x)
                self.area_window.refresh()
            else:
                y -= delta_y
                x -= delta_x
                self.draw_status("You cannot see further.")
                self.area_window.move(y, x)
                self.area_window.refresh()
            command = chr(self.input())
        curses.curs_set(0)
        self.draw_status("Done looking around.")

    def refresh(self):
        pass

    def input(self):
        """Returns when the user types a character on the keyboard."""
        return self.main_window.getch()
