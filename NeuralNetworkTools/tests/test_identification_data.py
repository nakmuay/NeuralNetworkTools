import unittest
import os
import numpy as np
import sys

sys.path.append("/home/martin/github/NeuralNetworkTools")
from NeuralNetworkTools.tests import *
from NeuralNetworkTools.core import *
from NeuralNetworkTools.io import *

class TestIdentificationDataDeserialization(unittest.TestCase):

    def setUp(self):
        self.test_data_path = "data"
       
    @property
    def test_filepath(self):
        return os.path.join(self.test_data_path, self.data_filename)
    
    def test_simple_iddata(self):
        self.data_filename = "simple_iddata.txt"

        # Create expected data
        self.expected_input_data = {"input_var_0": np.array([[1.0], [2.0], [3.0], [4.0]])}
        self.expected_output_data = {"output_var_0": np.array([[0.2], [0.4], [0.6], [0.8]])}
        self.perform_test()
    
    def test_multiple_input_output_iddata(self):
        self.data_filename = "multiple_input_output_iddata.txt"

        # Create expected data
        self.expected_input_data = {"input_var_0": np.array([[1.0], [2.0], [3.0], [4.0]]), \
                                    "input_var_1": np.array([[10.0], [20.0], [30.0], [40.0]])}
        self.expected_output_data = {"output_var_0": np.array([[0.2], [0.4], [0.6], [0.8]]), \
                                    "output_var_1": np.array([[0.22], [0.44], [0.66], [0.88]])}
        self.perform_test()

    def perform_test(self):
        # Read file
        actual = from_file(self.test_filepath)
      
        # Compare input data
        self.assert_iddata_almost_equal(actual.input_data, self.expected_input_data)
        
        # Compare output data
        self.assert_iddata_almost_equal(actual.output_data, self.expected_output_data)

    def assert_iddata_almost_equal(self, actual, expected):
        # Compare variable names
        self.assertEqual(actual.column_names, list(expected.keys()))

        # Compare data
        for k in expected.keys():
            np.testing.assert_array_almost_equal(actual[:, [k]].data, expected[k])

class TestIdentificationDataIndexing(unittest.TestCase):

    def setUp(self):
        input_data = NamedColumnsArray(np.array([[1.0, 1.1], [2.0, 2.2], [3.0, 3.3]]), ["input_1", "input_2"])
        output_data = NamedColumnsArray(np.array([[10.0, 10.1], [20.0, 20.2], [30.0, 30.3]]), ["output_1", "output_2"])
        self.data = IdentificationData(input_data, output_data) 

    def test_row_indexing(self):
        iddata = self.data[:, ["input_2", "input_1"], ["output_2"]]
        print(iddata.input_data)
        print(iddata.output_data)
        print()

        """
        iddata = self.data[:, [0]]
        print(iddata.input_data.column_names)
        print(iddata.input_data)
        print(iddata.output_data.column_names)
        print(iddata.output_data)
        print()

        iddata = self.data[:, [0], [1]]
        print(iddata.input_data.column_names)
        print(iddata.input_data)
        print(iddata.output_data.column_names)
        print(iddata.output_data)
        print()
       
        iddata = self.data[0:2, [0], [1]]
        print(iddata.input_data.column_names)
        print(iddata.input_data)
        print(iddata.output_data.column_names)
        print(iddata.output_data)
        print()

        iddata = self.data[[0], ...]
        print(iddata.input_data.column_names)
        print(iddata.input_data[:])
        print(iddata.output_data.column_names)
        print(iddata.output_data)
        print()

        iddata = self.data[..., [0]]
        print(iddata.input_data.column_names)
        print(iddata.input_data[:])
        print(iddata.output_data.column_names)
        print(iddata.output_data)
        print()
        """

    def test_iter(self):
        print("first iter")
        for d in self.data:
            print(d.input_data)
            print(d.output_data)

        print("second iter")
        for d in self.data:
            print(d.input_data)
            print(d.output_data)

if __name__ == "__main__":
    unittest.main()
