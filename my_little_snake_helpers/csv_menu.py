# This script provides a console menu for loading and unloading CSV files.
# It uses the WFConsole class for console interactions and the WFFileDataProcessor class for file operations.
# The script allows users to select a CSV file, load it into a DataFrame, and unload it.

import os
from wf_console import WFConsole
from wf_file_data_processor import WFFileDataProcessor

def _drop_columns_menu(df):
    
    # Create instance of WFConsole.
    console = WFConsole()

    # Define return string.
    return_str = "<MENU_NAV_ITEM>return</MENU_NAV_ITEM>"
    
    # Loop until the user chooses to return.
    while True:
        
        # Clear the console.
        console.clear()

        # Get a list of columns from the DataFrame.
        columns_list = list(df.columns)
        
        # Remove the 'return' column from the list.
        columns_list.append(return_str)

        prepend_str = f"select columns to drop\ndataframe shape:</GOOD> <DATA>{df.shape[0]} rows, {df.shape[1]} columns</DATA>"

        # List all the columns in the DataFrame.
        selection_int, selection_text = console.integer_only_menu_with_validation('drop columns', columns_list, prepend_str = prepend_str)

        if selection_text != return_str:
            # Drop the selected column from the DataFrame.
            df.drop(columns = [selection_text], inplace = True)

        # If the user selected 'return'.
        if selection_text == return_str: 
            return df

def csv_menu(starting_dir = None):

    # Check if starting_dir is None, and if so, set it to the current working directory.
    if starting_dir is None: starting_dir = os.getcwd()

    # Create instance of WFConsole.
    console = WFConsole()

    # Define return string.
    return_str = "<MENU_NAV_ITEM>return</MENU_NAV_ITEM>"

    # Create instance of FileProcessor.
    file_processor = WFFileDataProcessor()

    # Initialize the CSV file path to None.
    csv_file_path = None

    # Initialize the DataFrame that will hold csv data to None.
    csv_df = None

    # Loop until the user chooses to return.
    while True:

        # Clear the console.
        console.clear()

        # Prepend string to the menu.
        if not csv_file_path:
            prepend_str = "<BAD>csv file not selected.</BAD>"
            prepend_str += "\n<BAD>no dataframe loaded.</BAD>"
        if csv_file_path:
            prepend_str = f"<GOOD>csv file selected:</GOOD> <DATA>{csv_file_path}</DATA>"
            if csv_df is not None:
                prepend_str += f"\n<GOOD>dataframe loaded:</GOOD> <DATA>{csv_df.shape[0]} rows, {csv_df.shape[1]} columns</DATA>"
            else:
                prepend_str += "\n<BAD>no dataframe loaded.</BAD>"

        # Show the menu and get the user's selection (if there a a csv selected).
        if csv_df is not None: selection_int, selection_text = console.integer_only_menu_with_validation('csv menu', ['unload csv', 'view dataframe', 'drop columns', return_str], prepend_str = prepend_str)
        else: selection_int, selection_text = console.integer_only_menu_with_validation('csv menu', ['load csv', return_str], prepend_str = prepend_str)

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
                    console.fancy_print(f"<BAD>error loading csv: {csv_file_path}</BAD>")
                    # Pause for user input.
                    console.press_enter_pause()
                

        # If the user selected 'clear selection', clear the selected CSV file path.
        if selection_text == 'unload csv':
            # Clear the selected CSV file path.
            csv_file_path = None
            csv_df = None

        if selection_text == 'view dataframe':
            console.paginated_print(csv_df)

        # If the user selected 'drop columns', show the drop columns menu.
        if selection_text == 'drop columns':
            # Call the _drop_columns_menu function to drop columns from the DataFrame.
            csv_df = _drop_columns_menu(csv_df)

        # If the user selected 'return'.
        if selection_text == return_str: 
            return csv_file_path, csv_df

# If this script is run directly, call the csv_menu function.
if __name__ == "__main__":
    csv_menu()
