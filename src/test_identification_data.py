import unittest
import os
import numpy as np

from identification_data import IdentificationData

class TestIdentificationDataDeserialization(unittest.TestCase):

    def setUp(self):
        self.test_data_path = "../test"
        self.data_filename = "simple_iddata.txt"

        # Create expected data
        self.input_data = {"input_var_0": np.array([0.0, 1.0, 2.0, 3.0])}
        self.output_data = {"output_data": np.array([0.0, 0.1, 0.2, 0.4])}

    @property
    def test_filepath(self):
        return os.path.join(self.test_data_path, self.data_filename)

    def runTest(self):
        # Create expected data
        expected = IdentificationData(self.input_data, self.output_data, "simple_iddata")

        # Read file
        with open(self.test_filepath) as f:
           actual = IdentificationData.from_file(f)
      
        # Compare data
        self.assert_iddata_almost_equal(actual, expected)

    def assert_iddata_almost_equal(self, actual, expected):
        # Compare data
        np.testing.assert_array_almost_equal(actual.input_data["input_var_0"],
                                                expected.input_data["input_var_0"])



"""
class TestSimpleIdentificationDataDeserialization(TestIdentificationDataDeserialization):

    def setUp(self):
        super(TestSimpleIdentificationDataDeserialization, self).setUp()
        self.data_filename = "proper_iddata.txt"
"""        

if __name__ == "__main__":
    unittest.main()
