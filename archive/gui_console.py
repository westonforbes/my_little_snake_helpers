import curses  # For Windows, install windows-curses

"""⚠️ This class is under development and not intended for production use. It still has potential but it still has lots to go. Mothballed for now. ⚠️"""
class SimpleMenu:

    def __init__(self):

        self.menu_background_color_rgb = (0, 0, 1000)  # RGB tuple (0 to 1000).
        self.menu_window_color_rgb = (500, 500, 500)  # RGB tuple (0 to 1000).
        self.menu_text_color_rgb = (0, 0, 0)  # RGB tuple (0 to 1000).
        self.error_rgb = (1000, 0, 0)  # RGB tuple (0 to 1000).

        self.menu_properties = {
            'title': None,
            'item_list': [],
            'input_message': 'enter selection: ',
            'prepend_str': None,
            'append_str': None
        }

        self.menu_dims = {
            'width': 50,
            'height': 10,
            'x_left': None,
            'y_top': None
        }

        self.screen_dims = {
            'x_max': None, 
            'y_max': None,
            'x_center': None,
            'y_center': None
            }
        
    
    def menu(self, title: str, item_list: list[str], input_message: str ='enter selection: ', prepend_str: str = None, append_str: str = None):
        
        # Store parameters as instance variables.
        self.menu_properties['title'] = title
        self.menu_properties['item_list'] = item_list
        self.menu_properties['input_message'] = input_message
        self.menu_properties['prepend_str'] = prepend_str
        self.menu_properties['append_str'] = append_str

        # Initialize curses and start the menu loop.
        curses.wrapper(self._menu_wrapped)

    def _menu_wrapped(self, stdscr):

        # Set up the curses environment.
        self._menu_setup(stdscr)
        
        # Start the menu loop.
        self._menu_loop(stdscr)

    def _menu_setup(self, stdscr):
        self.stdscr = stdscr

        # Start color mode.
        curses.start_color()
        
        # Create color IDs.
        self.menu_background_color = 100
        self.menu_window_color = 101
        self.menu_text_color = 102
        self.error_color = 103
        
        # Initialize colors.
        curses.init_color(self.menu_background_color, *self.menu_background_color_rgb)
        curses.init_color(self.menu_window_color, *self.menu_window_color_rgb)
        curses.init_color(self.menu_text_color, *self.menu_text_color_rgb)
        curses.init_color(self.error_color, *self.error_rgb)
        
        # Create color pairs.
        curses.init_pair(200, self.menu_text_color, self.menu_window_color) # Window color pair.
        curses.init_pair(201, self.menu_text_color, self.menu_background_color) # Background color pair.
        curses.init_pair(202, self.menu_text_color, self.error_color) # Error color pair.
        
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(True)
        self.stdscr.timeout(100)

    def _menu_loop(self, stdscr):
        while True:
            try:
                # Clear the screen and recalculate dimensions.
                self.stdscr.clear()
                self._calculate_centering_data()
                
                # Set the background color back to healthy color.
                stdscr.bkgd(' ', curses.color_pair(201))

                # Draw the menu box.
                self._draw_box()

                # Draw the title.
                self._draw_title()

                # Create a render position for the following lines.
                render_coordinates = (self.menu_dims['x_left'] + 3, self.menu_dims['y_top'] + 1)

                # If there is a prepend string, render it.
                if self.menu_properties['prepend_str']:
                    self.stdscr.addstr(render_coordinates[1], render_coordinates[0], self.menu_properties['prepend_str'], curses.color_pair(200))
                    render_coordinates = (render_coordinates[0], render_coordinates[1] + 1)

                # Render the item list.
                for index, item in enumerate(self.menu_properties['item_list']):
                    if render_coordinates[1] >= self.screen_dims['y_max']:
                        break
                    self.stdscr.addstr(render_coordinates[1], render_coordinates[0], f"{index + 1}. {item}", curses.color_pair(200))
                    render_coordinates = (render_coordinates[0], render_coordinates[1] + 1)

                # If there is a append string, render it.
                if self.menu_properties['append_str']:
                    self.stdscr.addstr(render_coordinates[1], render_coordinates[0], self.menu_properties['append_str'], curses.color_pair(200))
                    render_coordinates = (render_coordinates[0], render_coordinates[1] + 1)

                self.stdscr.refresh()

                key = self.stdscr.getch()
                if key == ord('q'):
                    break
            except Exception as e:
                self._display_render_error(stdscr, str(e))
                
    def _draw_title(self):
        # Calculate the position for the title.
        title = self.menu_properties['title']
        if title:
            title = " " + title + " "
            title_offset = self.menu_dims['x_left'] + (self.menu_dims['width'] // 2) - (len(title) // 2)
            self.stdscr.addstr(self.menu_dims['y_top'], title_offset, title, curses.color_pair(200))

    def _draw_box(self) -> bool:
        
        # Use color pair 200 (black on gray).
        box_attr = curses.color_pair(200)

        top = self.menu_dims['y_top']
        left = self.menu_dims['x_left']
        height = self.menu_dims['height']
        width = self.menu_dims['width']

        # Safety check.
        if height < 2 or width < 2:
            raise ValueError("Box dimensions must be at least 2x2.")
        if height + 2 > self.screen_dims['y_max'] or width + 2 > self.screen_dims['x_max']:
            raise ValueError("Box dimensions exceed screen size.")

        try:
            # Top border.
            self.stdscr.addstr(top, left, '╔' + '═' * (width - 2) + '╗', box_attr)

            # Middle vertical bars.
            for row in range(1, height - 1):
                if top + row >= self.screen_dims['y_max']:
                    break
                self.stdscr.addstr(top + row, left, '║', box_attr)
                self.stdscr.addstr(top + row, left + width - 1, '║', box_attr)
                
                # Fill the inside with spaces.
                self.stdscr.addstr(top + row, left + 1, ' ' * (width - 2), box_attr)

            # Bottom border.
            if top + height - 1 < self.screen_dims['y_max']:
                self.stdscr.addstr(top + height - 1, left, '╚' + '═' * (width - 2) + '╝', box_attr)

        except curses.error:
            # Prevent crash if drawing outside screen.
            pass

    def _calculate_centering_data(self):
        """Calculate the screen size and center position."""
        
        # Get the size of the screen.
        self.screen_dims['y_max'], self.screen_dims['x_max'] = self.stdscr.getmaxyx()
        
        # Figure out the center of the screen.
        self.screen_dims['x_center'] = self.screen_dims['x_max'] // 2
        self.screen_dims['y_center'] = self.screen_dims['y_max'] // 2

        # Calculate where the upper left corner of the menu should be.
        half_x = self.menu_dims['width'] // 2
        half_y = self.menu_dims['height'] // 2
        self.menu_dims['x_left'] = self.screen_dims['x_center'] - half_x
        self.menu_dims['y_top'] = self.screen_dims['y_center'] - half_y 

    def _display_render_error(self, stdscr, error_message: str):
        """Display an error message in the menu."""
        self.stdscr.clear()
        # Set the background color back to healthy color.
        stdscr.bkgd(' ', curses.color_pair(202))
        self.stdscr.addstr(0, 0, f"Error: {error_message}", curses.color_pair(202))
        self.stdscr.refresh()
        self.stdscr.getch()


if __name__ == "__main__":
    menu_list = ["Option 1", "Option 2", "Option 3"]
    gui = SimpleMenu()
    
    gui.menu("main menu", menu_list, "enter selection: ", prepend_str="This is a menu.", append_str=" APPEND STRING")
