import curses

MAP_ROWS = 23
MAP_COLUMNS = 47

class Renderer:
    def __init__(self):
        """Initializes the rendering environment.
        
        Currently this initializes curses and creates the following curses 
        windows:
        
        -- map_window : 24 rows, 48 columns displays the map with the hero in 
                        the center
        """
        
        self.main_window = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.main_window.scrollok(1)

        
        self.map_window = curses.newwin(MAP_ROWS, MAP_COLUMNS+1, 0, 0)
        self.hero_x = MAP_COLUMNS/2
        self.hero_y = MAP_ROWS/2
        
        self.main_window.refresh()

    def shutdown(self):
        """Ends curses and restores the terminal state."""
        curses.nocbreak()
        curses.echo()
        curses.endwin()
    
    def map(self, map_):
        """Draws a Map onto the renderer's map window."""
        for y in range(map_.height):
            for x in range(map_.width):
                self.map_window.addch(y, x, ord(map_.tiles[y][x]))
        self.map_window.addch(self.hero_y, self.hero_x, ord('@'))
        self.map_window.move(self.hero_y, self.hero_x)
        self.map_window.refresh()
                
    def input(self):
        return self.main_window.getch()