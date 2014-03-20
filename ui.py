import curses

AREA_ROWS = 23
AREA_COLUMNS = 47
STATUS_ROWS = 1
STATUS_COLUMNS = 47


class UI:
    def __init__(self):
        """Initializes the rendering environment.

        Currently this initializes curses and creates the following curses
        windows:

        -- area_window : 23 rows, 47 columns displays the map with the hero in
                         the center
        """

        self.main_window = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        # We make the area_window actually be one column larger than necessary
        # because curses will throw an error if we write to the
        # bottom-right-most character.
        self.area_window = self.main_window.subwin(AREA_ROWS, AREA_COLUMNS + 1,
                                                   0, 0)
        self.status_line = self.main_window.subwin(STATUS_ROWS,
                                                   STATUS_COLUMNS + 1,
                                                   AREA_ROWS, 0)

        # The hero will always be present in the center.
        self.hero_x_offset = AREA_COLUMNS / 2
        self.hero_y_offset = AREA_ROWS / 2

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

    def refresh(self):
        pass

    def input(self):
        """Returns when the user types a character on the keyboard."""
        return self.main_window.getch()
