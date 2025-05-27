import unittest
from unittest.mock import patch, MagicMock
import os
from .wf_file_data_processor import WFFileDataProcessor

class TestMethod_select_csv(unittest.TestCase):
    
    @patch("tkinter.filedialog.askopenfilename") # Link to parameter 1.
    def test_good_selection_with_default_dir(self, mock_askopenfilename):
        """
        Tests being called with the default directory (no parameters passed).
        Expects the method to return the file path of the selected CSV file.
        """

        # Setup -----------------------------------------------------------------------------------
        
        # Mock the askopenfilename method to return a test file path.
        mock_askopenfilename.return_value = "test.csv"

        # Execute ---------------------------------------------------------------------------------
        
        # Call the select_csv method to simulate selecting a file.
        result = WFFileDataProcessor.select_csv(self)

        # Analyze ---------------------------------------------------------------------------------
        
        # Check if the result is the expected file path.
        self.assertEqual(result, "test.csv")


    @patch("tkinter.filedialog.askopenfilename") # Link to parameter 1.
    def test_good_selection_with_custom_dir(self, mock_askopenfilename):
        """
        Tests being called with a custom initial directory being passed.
        Expects the method to return the file path of the selected CSV file.
        """
        
        # Setup -----------------------------------------------------------------------------------
        
        # Mock the askopenfilename method to return a test file path.
        mock_askopenfilename.return_value = "rando_dir/test.csv"
        custom_initial_dir = "/this/is/a/custom/starting/dir"

        # Execute ---------------------------------------------------------------------------------
        
        # Call the select_csv method to simulate selecting a file.
        result = WFFileDataProcessor.select_csv(self, default_dir=custom_initial_dir)

        # Analyze ---------------------------------------------------------------------------------
        self.assertEqual(result, "rando_dir/test.csv")
        mock_askopenfilename.assert_called_with(title='Select a file', typevariable='CSV files', initialdir='/this/is/a/custom/starting/dir', filetypes=[('CSV files', '*.csv')])


    @patch("tkinter.filedialog.askopenfilename") # Link to parameter 1.
    def test_cancelling_dialog_box(self, mock_askopenfilename):
        # Setup -----------------------------------------------------------------------------------
        
        # Mock the askopenfilename method to return a empty string (simulating cancellation).
        mock_askopenfilename.return_value = ""

        # Execute ---------------------------------------------------------------------------------
        
        # Call the select_csv method to simulate selecting a file.
        result = WFFileDataProcessor.select_csv(self)

        # Analyze ---------------------------------------------------------------------------------
        
        # Check if the result is the expected file path.
        self.assertEqual(result, "")

class TestMethod_load_csv_to_dataframe(unittest.TestCase):
    
    @patch("pandas.read_csv") # Link to parameter 1.
    def test_good_csv(self, mock_read_csv):
        """
        Tests being called with a valid csv file path.
        Expects the method to return a DataFrame containing the csv data.
        """
        
        # Setup -----------------------------------------------------------------------------------
        
        # Mock the read_csv method to return a test DataFrame.
        mock_read_csv.return_value = MagicMock()

        # Execute ---------------------------------------------------------------------------------
        
        # Call the load_csv_to_dataframe method to simulate loading a CSV file.
        result = WFFileDataProcessor.load_csv_to_dataframe(self, "test.csv")

        # Analyze ---------------------------------------------------------------------------------
        
        # Check if the result is the expected DataFrame.
        self.assertIsInstance(result, MagicMock)

    @patch("pandas.read_csv") # Link to parameter 1.
    def test_bad_csv(self, mock_read_csv):
        """
        Tests being called with an invalid csv file path.
        Expects the method to raise a RuntimeError.
        """
        
        # Setup -----------------------------------------------------------------------------------
        
        # Mock the read_csv method to raise an exception.
        mock_read_csv.side_effect = Exception("File not found")

        # Execute ---------------------------------------------------------------------------------
        
        # Call the load_csv_to_dataframe method to simulate loading a CSV file.
        with self.assertRaises(RuntimeError) as context:
            WFFileDataProcessor.load_csv_to_dataframe(self, "invalid.csv")

        # Analyze ---------------------------------------------------------------------------------
        
        # Check if the raised exception message is as expected.
        self.assertEqual(str(context.exception), "An error occurred while reading the csv: File not found")

    @patch("pandas.read_csv") # Link to parameter 1.
    def test_corrupted_csv_data(self, mock_read_csv):
        """
        Tests being called with a valid file path but corrupted data within the file.
        Expects the method to raise a RuntimeError due to parsing error.
        """
        # Setup -----------------------------------------------------------------------------------
        
        # Simulate pandas raising a ParserError for corrupted CSV data.
        mock_read_csv.side_effect = Exception("Error tokenizing data. C error: Expected 2 fields in line 3, saw 3")

        # Execute ---------------------------------------------------------------------------------

        # Call the load_csv_to_dataframe method to simulate loading a CSV file.
        # This should raise a RuntimeError due to the corrupted data.
        with self.assertRaises(RuntimeError) as context:
            WFFileDataProcessor.load_csv_to_dataframe(self, "corrupted.csv")
        
        # Analyze ---------------------------------------------------------------------------------

        self.assertIn("An error occurred while reading the csv: Error tokenizing data", str(context.exception))

if __name__ == "__main__":
    unittest.main()