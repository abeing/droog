import curses

AREA_ROWS = 23
AREA_COLUMNS = 47

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

        # We make the area_window actually be one column larger than necessary
        # because curses will throw an error if we write to the
        # bottom-right-most character.
        self.area_window = curses.newwin(AREA_ROWS, AREA_COLUMNS + 1, 0, 0)

        # The hero will always be present in the center.
        self.hero_x = AREA_COLUMNS/2
        self.hero_y = AREA_ROWS/2

        # We need to refresh the main window at least once, even if we do all
        # updates through child windows.
        self.main_window.refresh()

    def shutdown(self):
        """Ends curses and restores the terminal state."""
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def draw_area(self, world):
        """Draws an area of the world onto the renderer's area window."""
        for y in range(world.height):
            for x in range(world.width):
                self.area_window.addch(y, x, ord(world.tiles[y][x]))

        # The hero is drawn in the center last so we can always see him or
        # her. The curses is then placed on top of the hero for visual
        # distinction.
        self.area_window.addch(self.hero_y, self.hero_x, ord('@'))
        self.area_window.move(self.hero_y, self.hero_x)

        self.area_window.refresh()

    def input(self):
        """Returns when the user types a character on the keyboard."""
        return self.main_window.getch()
