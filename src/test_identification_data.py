import unittest
import os

from identification_data import IdentificationData

class TestIdentificationDataDeserialization(unittest.TestCase):

    def setUp(self):
        self.input_filename = "proper_iddata.txt"
        self.input_path = "../test_data"

    @property
    def input_filepath(self):
        return os.path.join(self.input_path, self.input_filename)

    def runTest(self):
        with open(self.input_filepath) as f:
           dat = IdentificationData.from_file(f)
        assert 1 == 1

class TestSimpleIdentificationDataDeserialization(TestIdentificationDataDeserialization):

    def setUp(self):
        self.input_filename = "simple_iddata.txt"
        super(TestSimpleIdentificationDataDeserialization, self).setUp()

if __name__ == "__main__":
    unittest.main()
