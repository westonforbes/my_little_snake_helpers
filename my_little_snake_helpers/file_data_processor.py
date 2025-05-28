import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
    
class FileDataProcessor():

    """
    This class contains methods for file processing.
    """

    def __init__(self):
        """
        Initialize the file_processing class.
        """
        pass

    def view_image(filepath):
        """Launch an image viewer for the given image filepath."""
        try:
            image = Image.open(filepath)
            plt.imshow(image)
            plt.axis('off')  # Hide axes
            plt.title(f"Viewing: {filepath}")
            plt.show()
        except Exception as e:
            print(f"Error loading image: {e}")

    def select_image(self, default_dir:str = None) -> str:
        """
        Opens a file dialog to select an image file and returns the file path.

        Returns:
            str: The path to the selected file.
        """

        if default_dir is None:
            # If no default directory is provided, use the current working directory.
            default_dir = os.getcwd()

        # Hide the main root window.
        root = tk.Tk()
        root.withdraw()

        # Launch the file picker.
        file_path = filedialog.askopenfilename(title = "Select a file", initialdir = default_dir, filetypes = [("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

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
    
    def select_csv(self, default_dir:str = None) -> str:
        """
        Opens a file dialog to select a CSV file and returns the file path.

        Returns:
            str: The path to the selected file.
        """

        if default_dir is None:
            # If no default directory is provided, use the current working directory.
            default_dir = os.getcwd()

        # Hide the main root window.
        root = tk.Tk()
        root.withdraw()

        # Launch the file picker.
        file_path = filedialog.askopenfilename(title = "Select a file", typevariable = "CSV files", initialdir = default_dir, filetypes = [("CSV files", "*.csv")])

        # Destroy the Tkinter root window to avoid resource leaks.
        root.destroy()

        return file_path
    
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