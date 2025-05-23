# This script provides a console menu for loading and unloading CSV files.
# It uses the WFConsole class for console interactions and the WFFileDataProcessor class for file operations.
# The script allows users to select a CSV file, load it into a DataFrame, and unload it.

import os
from wf_console import WFConsole
from wf_file_data_processor import WFFileDataProcessor

def csv_menu(starting_dir = None):

    # Check if starting_dir is None, and if so, set it to the current working directory.
    if starting_dir is None: starting_dir = os.getcwd()

    # Create instance of WFConsole.
    console = WFConsole()

    # Create instance of FileProcessor.
    file_processor = WFFileDataProcessor()

    # Initialize the CSV file path to None.
    csv_file_path = None

    # Initialize the DataFrame that will hold csv data to None.
    csv_df = None

    # Loop until the user chooses to exit.
    while True:

        # Clear the console.
        console.clear()

        # Prepend string to the menu.
        if not csv_file_path:
            prepend_str = "<BAD_TEXT>csv file not selected.</BAD_TEXT>"
            prepend_str += "\n<BAD_TEXT>no dataframe loaded.</BAD_TEXT>"
        if csv_file_path:
            prepend_str = f"<GOOD_TEXT>csv file selected:</GOOD_TEXT> <YELLOW>{csv_file_path}</YELLOW>"
            if csv_df is not None:
                prepend_str += f"\n<GOOD_TEXT>dataframe loaded:</GOOD_TEXT> <YELLOW>{csv_df.shape[0]} rows, {csv_df.shape[1]} columns</YELLOW>"
            else:
                prepend_str += "\n<BAD_TEXT>no dataframe loaded.</BAD_TEXT>"

        # Show the menu and get the user's selection (if there a a csv selected).
        selection_int, selection_text = console.integer_only_menu_with_validation('csv menu', ['load csv', 'unload csv', 'return'], prepend_str = prepend_str)

        # Determine what to do based on the user's selection.
        if selection_text == 'load csv':
            
            # Open a file dialog to select a CSV file.
            csv_file_path = file_processor.select_csv(starting_dir)

            if csv_file_path:
                try:
                    csv_df = file_processor.load_csv_to_dataframe(csv_file_path)
                except RuntimeError:
                    # If there was an error loading the CSV file, set csv_df to None.
                    csv_df = None
                    # Print the error message.
                    console.fancy_print(f"<BAD_TEXT>error loading csv: {csv_file_path}</BAD_TEXT>")
                    # Pause for user input.
                    console.press_enter_pause()
                

        # If the user selected 'clear selection', clear the selected CSV file path.
        if selection_text == 'unload csv':
            # Clear the selected CSV file path.
            csv_file_path = None
            csv_df = None
        
        # If the user selected 'return'.
        if selection_text == 'return': 
            return csv_file_path, csv_df

# If this script is run directly, call the csv_menu function.
if __name__ == "__main__":
    csv_menu()
