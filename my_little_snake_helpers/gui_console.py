import curses  # For Windows, install windows-curses

class SimpleMenu:

    def __init__(self):
        self.menu_row_start = 3
        self.menu_col_start = 3
        self.menu_width = 10
        self.menu_height = 5
        self.menu_background_color_rgb = (0, 0, 1000)  # RGB tuple (0 to 1000).
        self.menu_window_color_rgb = (500, 500, 500)  # RGB tuple (0 to 1000).
        self.menu_text_color_rgb = (0, 0, 0)  # RGB tuple (0 to 1000).

        self.screen_rows, self.screen_cols = self.stdscr.getmaxyx()

    
    def menu(self, title: str, item_list: list[str], input_message: str ='enter selection: ', prepend_str: str = None, append_str: str = None):
        
        # Store parameters as instance variables.
        self.menu_title = title
        self.menu_item_list = item_list
        self.menu_input_message = input_message
        self.menu_prepend_str = prepend_str
        self.menu_append_str = append_str

        # Initialize curses and start the menu loop.
        curses.wrapper(self._menu_wrapped)

    def _menu_wrapped(self, stdscr):

        # Set up the curses environment.
        self._menu_setup(stdscr)
        
        # Start the menu loop.
        self._menu_loop()

    def _menu_setup(self, stdscr):
        self.stdscr = stdscr

        # Start color mode.
        curses.start_color()
        
        # Create color IDs.
        self.menu_background_color = 100
        self.menu_window_color = 101
        self.menu_text_color = 102
        
        # Initialize colors.
        curses.init_color(self.menu_background_color, *self.menu_background_color_rgb)
        curses.init_color(self.menu_window_color, *self.menu_window_color_rgb)
        curses.init_color(self.menu_text_color, *self.menu_text_color_rgb)
        
        # Create color pairs.
        curses.init_pair(200, self.menu_text_color, self.menu_window_color) # Window color pair.
        curses.init_pair(201, self.menu_text_color, self.menu_background_color) # Background color pair.
        
        # Set the background color for the entire window.
        stdscr.bkgd(' ', curses.color_pair(201))

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(True)
        self.stdscr.timeout(100)

    def _menu_loop(self):
        while True:
            self.stdscr.clear()
            #self.stdscr.addstr(self.menu_row_start, self.menu_col_start, "Hello world - Press 'q' to quit")
            self._draw_box()
            self.stdscr.refresh()

            key = self.stdscr.getch()
            if key == ord('q'):
                break

    def _draw_box(self):
        # Use color pair 200 (black on gray)
        box_attr = curses.color_pair(200)

        top = self.menu_row_start
        left = self.menu_col_start
        height = self.menu_height
        width = self.menu_width

        # Safety check
        if height < 2 or width < 2:
            return  # Can't draw a box with less than 2x2

        try:
            # Top border
            self.stdscr.addstr(top, left, '╔' + '═' * (width - 2) + '╗', box_attr)

            # Middle vertical bars
            for row in range(1, height - 1):
                if top + row >= curses.LINES:
                    break
                self.stdscr.addstr(top + row, left, '║', box_attr)
                self.stdscr.addstr(top + row, left + width - 1, '║', box_attr)
                # Fill the inside with spaces
                self.stdscr.addstr(top + row, left + 1, ' ' * (width - 2), box_attr)

            # Bottom border
            if top + height - 1 < curses.LINES:
                self.stdscr.addstr(top + height - 1, left, '╚' + '═' * (width - 2) + '╝', box_attr)

        except curses.error:
            # Prevent crash if drawing outside screen
            pass







if __name__ == "__main__":
    menu_list = ["Option 1", "Option 2", "Option 3"]
    gui = SimpleMenu()
    
    # Set menu parameters.
    gui.menu_col_start = 3
    gui.menu_row_start = 3
    gui.menu_width = 100
    gui.menu_height = 10

    gui.menu("main menu", menu_list)
