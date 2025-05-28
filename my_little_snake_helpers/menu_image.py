# When running this script directly, use launch.json to run as a module or use `python -m my_little_snake_helpers.menu_image`.

# This script provides a console menu for loading and unloading image files.
# It uses the Console class for console interactions and the FileDataProcessor class for file operations.
# The script allows users to select a image file, load it into a Numpy array, and perform operations like viewing the image.
import os
import numpy as np
from .console import Console
from .file_data_processor import FileDataProcessor

class MenuImage:

    def show_menu(self, starting_dir = None):

        # Check if starting_dir is None, and if so, set it to the current working directory.
        if starting_dir is None: starting_dir = os.getcwd()

        # Create instance of Console.
        console = Console()

        # Define return string.
        return_str = "<MENU_NAV_ITEM>return</MENU_NAV_ITEM>"

        # Create instance of FileProcessor.
        file_processor = FileDataProcessor()

        # Initialize the image file path to None.
        image_file_path = None

        # Initialize the numpy array to None.
        image_array = None

        # Loop until the user chooses to return.
        while True:

            # Clear the console.
            console.clear()

            # Prepend string to the menu.
            if not image_file_path:
                prepend_str = "<BAD>image file not selected.</BAD>"
            if image_file_path:
                prepend_str = f"<GOOD>image file selected:</GOOD> <DATA>{image_file_path}</DATA>"

            # Show the menu and get the user's selection (if there a a image selected).
            if image_array is not None: selection_int, selection_text = console.integer_only_menu_with_validation('image menu', ['unload image', 'view image', return_str], prepend_str = prepend_str)
            else: selection_int, selection_text = console.integer_only_menu_with_validation('image menu', ['load image', return_str], prepend_str = prepend_str)

            # Determine what to do based on the user's selection.
            if selection_text == 'load image':
                
                # Open a file dialog to select a image file.
                image_file_path = file_processor.select_image(starting_dir)

                if image_file_path:
                    try:
                        image_array = file_processor.load_image_to_array(image_file_path)
                    except RuntimeError:
                        # If there was an error loading the image file, set image_array to None.
                        image_array = None
                        # Print the error message.
                        console.fancy_print(f"<BAD>error loading image: {image_file_path}</BAD>")
                        # Pause for user input.
                        console.press_enter_pause()
                    

            # If the user selected 'clear image', clear the selected image file path.
            if selection_text == 'unload image':
                # Clear the selected image file path.
                image_file_path = None
                image_array = None

            if selection_text == 'view image':
                FileDataProcessor.view_image(image_file_path)

            # If the user selected 'return'.
            if selection_text == return_str: 
                return image_file_path, image_array

# If this script is run directly, call the show_menu function.
if __name__ == "__main__":
    
    # Create an instance of MenuImage.
    image_menu = MenuImage()
    
    # Show the image menu and get the selected file path and numpy data.
    file_path, numpy_array = image_menu.show_menu()