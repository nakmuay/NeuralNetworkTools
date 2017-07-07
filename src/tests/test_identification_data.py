import unittest
import os
import numpy as np

import src

class TestIdentificationDataDeserialization(unittest.TestCase):

    def setUp(self):
        self.test_data_path = "../test"
        self.data_filename = "simple_iddata.txt"

        # Create expected data
        self.expected_input_data = {"input_var_0": np.array([1.0, 2.0, 3.0, 4.0])}
        self.expected_output_data = {"output_var_0": np.array([0.2, 0.4, 0.6, 0.8])}

    @property
    def test_filepath(self):
        return os.path.join(self.test_data_path, self.data_filename)

    def runTest(self):
        # Read file
        with open(self.test_filepath) as f:
           actual = IdentificationData.from_file(f)
      
        # Compare input data
        self.assertIdDataAlmostEqual(actual.input_data, self.expected_input_data)
        
        # Compare output data
        self.assertIdDataAlmostEqual(actual.output_data, self.expected_output_data)

    def assertIdDataAlmostEqual(self, actual, expected):
        # Compare variable names
        self.assertEqual(actual.keys(), expected.keys())

        # Compare data
        for var in expected.keys():
            np.testing.assert_array_almost_equal(actual[var], expected[var])



"""
class TestSimpleIdentificationDataDeserialization(TestIdentificationDataDeserialization):

    def setUp(self):
        super(TestSimpleIdentificationDataDeserialization, self).setUp()
        self.data_filename = "proper_iddata.txt"
"""        

if __name__ == "__main__":
    unittest.main()
