import curses
import logging
import sys

MINIMUM_WIDTH = 80
MINIMUM_HEIGHT = 24

HERO_COLUMNS = 18
MESSAGE_ROWS = 3
STATUS_ROWS = 1
STATUS_COLUMNS = 47

log = logging.getLogger(__name__)


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

    def draw_area(self, world):
        """Draws an area of the world onto the renderer's area window."""
        (hero_y, hero_x) = world.hero_location
        left = hero_x - self.hero_x_offset
        right = hero_x + self.hero_x_offset
        top = hero_y - self.hero_y_offset
        bottom = hero_y + self.hero_y_offset
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

    def draw_status(self, world):
        """Draws the status information."""
        hero_y, hero_x = world.hero_location
        coordinates = "({0}, {1})".format(hero_y, hero_x)
        self.status_line.addstr(0, 0, coordinates)
        self.status_line.clrtoeol()
        self.status_line.refresh()

    def draw_hero(self, hero):
        """Draws the hero information window. Does not draw the actual @
        symbol on the map; that is handled by draw_area."""
        self.hero_window.addstr(0, 0, hero.name)
        self.hero_window.refresh()

    def draw_messages(self):
        """Draws the most recent messages in the message log."""
        self.message_window.addstr(0, 0, "This is the message window.")
        self.message_window.refresh()

    def refresh(self):
        pass

    def input(self):
        """Returns when the user types a character on the keyboard."""
        return self.main_window.getch()
