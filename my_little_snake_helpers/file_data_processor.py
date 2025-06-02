import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

class FileDataProcessor():
    """
    This class contains methods for file processing, including file dialogs,
    image viewing, and data loading utilities.
    """

    def __init__(self):
        """
        Initialize the FileDataProcessor class.
        Currently, no initialization logic is required.
        """
        pass

    def view_image(self, filepath):
        """
        Launch an image viewer for the given image filepath.

        Parameters:
            filepath (str): The path to the image file to display.

        Displays the image using matplotlib. If the image cannot be loaded,
        prints an error message.
        """
        try:
            image = Image.open(filepath)
            plt.imshow(image)
            plt.axis('off')  # Hide axes for a cleaner view
            plt.title(f"Viewing: {filepath}")
            plt.show()
        except Exception as e:
            print(f"Error loading image: {e}")

    def save_file(self, default_dir: str = None, default_filename: str = "", filetypes = ("All files", "*.*")) -> str:
        """
        Opens a Save As file dialog and returns the selected file path.

        Parameters:
            default_dir (str): The directory to open the dialog in. If None, uses the current working directory.
            default_filename (str): The default filename to display in the dialog.
            filetypes (tuple): A tuple of file types to filter the files shown in the dialog.

        Returns:
            str: The path to the file to save, or an empty string if cancelled.
        """
        if default_dir is None:
            default_dir = os.getcwd()

        # Create a hidden root window for the dialog
        root = tk.Tk()
        root.withdraw()

        # Open the Save As dialog
        file_path = filedialog.asksaveasfilename(
            title="Save file as",
            initialdir=default_dir,
            initialfile=default_filename,
            filetypes=[filetypes]
        )

        # Destroy the root window to free resources
        root.destroy()

        return file_path

    def open_directory(self, default_dir: str = None) -> str:
        """
        Opens a dialog to select a directory and returns the directory path.

        Parameters:
            default_dir (str): The directory to open the dialog in. If None, uses the current working directory.

        Returns:
            str: The path to the selected directory, or an empty string if cancelled.
        """
        if default_dir is None:
            default_dir = os.getcwd()

        # Create a hidden root window for the dialog
        root = tk.Tk()
        root.withdraw()

        # Open the directory selection dialog
        directory_path = filedialog.askdirectory(title="Select a directory", initialdir=default_dir)

        # Destroy the root window to free resources
        root.destroy()

        return directory_path

    def open_file(self, default_dir:str = None, filetypes = ("All files", "*.*")) -> str:
        """
        Opens a file dialog to select a file and returns the file path.

        Parameters:
            default_dir (str): The directory to open the file dialog in. If None, uses the current working directory.
            filetypes (tuple): A tuple of file types to filter the files shown in the dialog.
                Example: ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")      

        Returns:
            str: The path to the selected file, or an empty string if cancelled.
        """
        if default_dir is None:
            # If no default directory is provided, use the current working directory.
            default_dir = os.getcwd()

        # Hide the main root window.
        root = tk.Tk()
        root.withdraw()

        # Launch the file picker dialog.
        file_path = filedialog.askopenfilename(
            title="Select a file",
            initialdir=default_dir,
            filetypes=[filetypes]
        )

        # Destroy the Tkinter root window to avoid resource leaks.
        root.destroy()

        return file_path

    def load_image_to_array(self, filepath):
        """
        Loads an image file into a numpy array.

        Parameters:
            filepath (str): The path to the image file.

        Returns:
            np.ndarray: Numpy array containing the image data.

        Raises:
            RuntimeError: If there is an error reading the image file.
        """
        try:
            # Open the image file using PIL and convert it to a numpy array.
            img = Image.open(filepath)
            img_array = np.array(img)
            return img_array
        except Exception as e:
            raise RuntimeError(f"an error occurred while reading the image: {e}")

    def load_csv_to_dataframe(self, filepath):
        """
        Loads a CSV file into a pandas DataFrame.

        Parameters:
            filepath (str): The path to the CSV file.

        Returns:
            pd.DataFrame: DataFrame containing the CSV data.

        Raises:
            RuntimeError: If there is an error reading the CSV file.
        """
        try:
            df = pd.read_csv(filepath)
            return df
        except Exception as e:
            raise RuntimeError(f"An error occurred while reading the csv: {e}")

    def remove_keys_from_json(self, data, keys_to_remove):
        """
        Removes specified keys from each dictionary in a list.

        Parameters:
        - data: list of dictionaries (JSON-like)
        - keys_to_remove: list of keys to be removed from each dictionary

        Returns:
        - The cleaned list of dictionaries
        """
        for item in data:
            for key in keys_to_remove:
                item.pop(key, None)  # Safely remove key if it exists.
        return data

if __name__ == "__main__":
    try:
        from .console import Console
    except:
        from my_little_snake_helpers.console import Console
    
    console = Console()
    processor = FileDataProcessor()

    while True:
        integer_selection, text_selection = console.integer_only_menu_with_validation("Demo different features",["open file", "open folder", "save file as", "exit"])
        if text_selection == "open file": processor.open_file()
        if text_selection == "open folder": processor.open_directory()
        if text_selection == "save file as": processor.save_file()
        if text_selection == "exit": break
        text_selection = None