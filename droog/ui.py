"""Droog User Interface."""
import curses
import logging
import sys
import message
import english

MINIMUM_WIDTH = 80
MINIMUM_HEIGHT = 24

HERO_COLUMNS = 18
MESSAGE_ROWS = 1
STATUS_ROWS = 1
STATUS_COLUMNS = 47

LOG = logging.getLogger(__name__)

"""Maps glyphs to color pair indicies."""
COLOR_MAP = {'Z': 3,
             'd': 3,
             'C': 6,
             '.': 2,
             '#': 0,
             '~': 4,
             'G': 6,
             ')': 5
             }


class Curses(object):
    """The UserInterface class manages the drawing to curses and input from the
    user."""

    movements = {'h': (0, -1),   # West
                 'l': (0, 1),    # East
                 'j': (1, 0),    # South
                 'k': (-1, 0),   # North
                 'y': (-1, -1),  # Northwest
                 'u': (-1, 1),   # Northeast
                 'b': (1, -1),   # Southwest
                 'n': (1, 1),    # Southeast
                 }

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

        # Our palette
        curses.start_color()
        LOG.info('Curses color support: %r', curses.has_colors())
        self.build_palette()

        # Our screen size
        height, width = self.main_window.getmaxyx()
        LOG.info('Main window has %r width and %r height', width, height)

        # Ensure that our screen size is at least the minimum required
        if width < MINIMUM_WIDTH or height < MINIMUM_HEIGHT:
            shutdown()
            print 'ERROR: Terminal window too small.'
            print 'Minimum width: %r' % MINIMUM_WIDTH
            print 'Minimum height: %r' % MINIMUM_HEIGHT
            sys.exit(1)

        # Calculate the area window size (it should be the biggest)
        self.area_width = width - HERO_COLUMNS - 1
        self.area_height = height - MESSAGE_ROWS - STATUS_ROWS - 1
        LOG.info('Area window has %r width and %r height', self.area_width,
                 self.area_height)

        # We make the area_window actually be one column larger than necessary
        # because curses will throw an error if we write to the
        # bottom-right-most character.
        self.area_window = self.main_window.subwin(self.area_height,
                                                   self.area_width + 1,
                                                   MESSAGE_ROWS + 1, 0)

        # Draw the border between the area window and the hero windows.
        for y in range(MESSAGE_ROWS, self.area_height + MESSAGE_ROWS + 1):
            self.main_window.addch(y, self.area_width, '|')

        self.hero_window = self.main_window.subwin(self.area_height,
                                                   HERO_COLUMNS,
                                                   MESSAGE_ROWS + 1,
                                                   self.area_width + 1)

        # Draw the border between the hero window and the message window,
        for x in range(0, width):
            self.main_window.addch(MESSAGE_ROWS, x, '-')
        self.main_window.addch(MESSAGE_ROWS, self.area_width, '+')

        self.message_window = self.main_window.subwin(MESSAGE_ROWS,
                                                      width,
                                                      0,
                                                      0)
        self.message_window.scrollok(True)

        self.status_line = self.main_window.subwin(STATUS_ROWS,
                                                   width,
                                                   self.area_height + 1 +
                                                   MESSAGE_ROWS, 0)
        self.status = ""

        # The hero will always be present in the center.
        self.hero_x_offset = self.area_width / 2
        self.hero_y_offset = self.area_height / 2

        # We need to refresh the main window at least once, even if we do all
        # updates through child windows.
        self.main_window.refresh()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        shutdown()

    def build_palette(self):
        """Builds the color palette for the user interface."""
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def glyph_color(self, glyph):
        """Looks up the color for a glyph and sets the specified color pair to
        be that color."""
        global COLOR_MAP
        if glyph in COLOR_MAP:
            return curses.color_pair(COLOR_MAP[glyph])
        return curses.color_pair(0)

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
                glyph = world.glyph_at(y, x)
                self.area_window.addstr(y - top, x - left,
                                        glyph, self.glyph_color(glyph))
                creature = world.creature_at(y, x)
                if creature is not None:
                    self.area_window.addstr(y - top, x - left,
                                            creature.glyph,
                                            self.glyph_color(creature.glyph))
                item = world.item_at(y, x)
                if item:
                    self.area_window.addstr(y - top, x - left,
                                            item.glyph,
                                            self.glyph_color(item.glyph))

        # The hero is drawn in the center last so we can always see him or
        # her. The curses is then placed on top of the hero for visual
        # distinction.
        self.area_window.addstr(self.hero_y_offset, self.hero_x_offset,
                                '@', curses.A_REVERSE)
        self.area_window.refresh()

    def draw_status(self, message=None, time=None):
        """Draw a status message.

        Generally this will be the time. Occasionally, we want to override the
        typical status message with a more persistant one, but we don't want to
        pause for user input. For that, we can persist a message over two
        updates instead.

        status_message -- a status message string
        persist -- ignore the next message

        """
        if time:
            self.status_line.addstr(0, 0, time)
        if message:
            self.status = message
        self.status_line.addstr(0, 10, self.status)
        self.status_line.clrtoeol()
        self.status_line.refresh()

    def draw_hero(self, hero):
        """Draws the hero information window. Does not draw the actual @
        symbol on the map; that is handled by draw_area."""
        self.hero_window.clear()
        stats = english.epithet(hero.strength, hero.dexterity,
                                hero.constitution)
        if stats:
            hero_line = hero.name + " the " + stats
        else:
            hero_line = hero.name
        hero_lines = english.wrap(hero_line, HERO_COLUMNS)
        index = 0
        for line in hero_lines:
            self.hero_window.addstr(index, 0, line)
            index += 1
        index = self.draw_conditions(hero, index)
        self.draw_inventory(hero.inventory, index + 1)
        self.hero_window.refresh()

    def draw_conditions(self, hero, index):
        """Draw the hero's conditions."""
        idx = index
        if hero.blood < 10:
            blood_meter = create_meter(hero.blood, 10)
            self.hero_window.addstr(idx, 2, blood_meter, curses.color_pair(1))
            idx += 1
        if hero.is_bleeding:
            self.hero_window.addstr(idx, 2, "Bleeding", curses.color_pair(1))
            idx += 1
        if hero.is_stunned:
            self.hero_window.addstr(idx, 2, "Stunned", curses.color_pair(1))
            idx += 1
        if hero.is_weakened:
            self.hero_window.addstr(idx, 2, "Weakened", curses.color_pair(3))
            idx += 1
        if hero.is_hobbled:
            self.hero_window.addstr(idx, 2, "Hobbled", curses.color_pair(3))
            idx += 1
        if hero.is_diseased:
            self.hero_window.addstr(idx, 2, "Diseased", curses.color_pair(3))
            idx += 1
        return idx

    def draw_inventory(self, inventory, index):
        """Draw the hero's inventory in the hero screen."""
        item_index = 0
        for item in inventory:
            self.hero_window.addstr(index, 0,
                                    '%s - %s' % (index_to_alpha(item_index),
                                                 item.name))
            self.hero_window.clrtoeol()
            index += 1
            item_index += 1
        for row in range(9 + index, HERO_COLUMNS):
            self.hero_window.move(row, 0)
            self.hero_window.clrtoeol()
        return index

    def draw_messages(self, messages):
        """Draws the most recent messages in the message log."""

        self.message_window.clear()
        height, width = self.message_window.getmaxyx()

        all_messages = ""
        while not messages.empty():
            all_messages += messages.get() + " "

        wrapped_messages = english.wrap(all_messages.strip(), width - 1)

        row = 0
        for line in wrapped_messages:
            self.message_window.addstr(row, 0, line)
            row += 1
            if row == height and line != wrapped_messages[-1]:
                self.main_window.addstr(row, 75, "MORE", curses.A_REVERSE)
                self.main_window.refresh()
                self.message_window.getch()
                self.message_window.scroll(1)
                self.main_window.addstr(row, 75, "----")
                row = height - 1

        self.message_window.refresh()
        # words = a_message.split()
        # for word in words:
        #     if self.message_column + len(word) > width:
        #         self.message_row += 1
        #         self.message_column = 0
        #     self.message_window.addstr(self.message_row,
        #                                self.message_column, word)
        #     self.message_column += len(word) + 1

    def look(self, world):
        """Enters look mode. Look mode allows the player to move the cursor
        around the map area with the cursor-movement keys. While looking, the
        status line updates with information about whatever is under the cursor
        at the time."""
        self.draw_status(message="Looking around (using the movement keys).")
        max_y, max_x = self.area_window.getmaxyx()
        y = self.hero_y_offset
        x = self.hero_x_offset
        curses.curs_set(1)
        self.area_window.move(y, x)
        self.area_window.refresh()

        (left, right, top, bottom) = self.map_bounds(world)

        command = self.input()
        while command in self.movements:
            delta_y, delta_x = self.movements[command]
            y += delta_y
            x += delta_x
            if y >= 0 and y < max_y and x >= 0 and x < max_x - 1:
                LOG.info("Highlighting %r, %r.", y, x)
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
            command = self.input()
        curses.curs_set(0)
        self.draw_status("Done looking around.")

    def input(self):
        """Returns when the user types a character on the keyboard."""
        self.status = ""
        return chr(self.main_window.getch())

    def drop(self, hero, world):
        """Drop an item."""
        self.draw_status(message="Drop what?")
        alpha = self.input()
        index = alpha_to_index(alpha)
        item = hero.inventory.pop(index)
        world.add_item(world.hero_location, item)

    def wizard(self, world):
        """Parses a wizard command."""
        self.draw_status(message="What doest thou want, wizard?")
        command = self.input()
        if command == 's':
            self.draw_status(message="Summon what?")
            monster = self.input()
            LOG.info("Spawning a %r near the hero.", monster)
            if not world.spawn_monster(monster, near=world.hero_location):
                self.draw_status("I know not how to spawn a %s, wizard." %
                                 monster)
        if command == 't':
            self.draw_status(message="Teleport where?")
            location = self.input()
            if location == 'g':
                world.teleport_hero(world.generator_location)

    def help(self):
        """Display the help screen."""
        # height, width = self.main_window.getmaxyx()
        LOG.info("creating help window width=%d, height=%d", self.area_width,
                 self.area_height)
        help_screen = curses.newwin(self.area_height, self.area_width,
                                    MESSAGE_ROWS + 1, 0)
        row = self.hero_y_offset
        col = self.hero_x_offset
        cmd_col = col - 22
        LOG.info("Drawing movement at (%d, %d)", row, col)
        help_screen.addstr(row - 4, col - 4, "Movement")
        help_screen.addstr(row - 3, col - 4, "--------")
        help_screen.addstr(row - 2, col - 4, " y  k  u")
        help_screen.addstr(row - 1, col - 4, "  \\ | /")
        help_screen.addstr(row, col - 4, " h--@--l ")
        help_screen.addstr(row + 1, col - 4, "  / | \\")
        help_screen.addstr(row + 2, col - 4, " b  j  n ")
        help_screen.addstr(row - 4, cmd_col, "Commands")
        help_screen.addstr(row - 3, cmd_col, "--------")
        help_screen.addstr(row - 2, cmd_col, "q quit")
        help_screen.addstr(row - 1, cmd_col, "? help")
        help_screen.addstr(row, cmd_col, "/ look")
        help_screen.addstr(row + 1, cmd_col, "d drop")
        help_screen.addstr(row + 2, cmd_col, "m message history")
        help_screen.addstr(row - 2, col + 6, "Bump into enemies with")
        help_screen.addstr(row - 1, col + 6, "the movement keys to")
        help_screen.addstr(row + 0, col + 6, "perform a melee attack.")
        help_screen.refresh()
        command = self.input()
        del help_screen
        self.redraw()

    def redraw(self):
        """Redraw the windows."""
        self.main_window.redrawwin()


def index_to_alpha(index):
    """Convert a list index into an alphabetic character."""
    return chr(index + 97)


def alpha_to_index(alpha):
    """Convert an alphabetic character into a list index."""
    return ord(alpha) - 97


def create_meter(value, maximum):
    """Create a string representing a proprtion of a value.

    A `value` number of asterisks fill a `maximum` number of empty spaces,
    bookended by square brackets.

    For example a strgeth of 2 out of 3 is represented as [** ]
    """
    LOG.debug("Creating a meter of %r out of %r.", value, maximum)
    ivalue = int(value)
    meter = "["
    for x in range(0, ivalue):
        meter += "*"
    for y in range(0, maximum - ivalue):
        meter += " "
    meter += "]"
    LOG.debug("Returning the meter as %r", meter)
    return meter


def shutdown():
    """Cleans up the curses environment. This is called if the Curses object
    ever goes out of scope or if the Curses object fails to initialize."""
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)
    curses.endwin()
