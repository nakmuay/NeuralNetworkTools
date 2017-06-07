import unittest
import os

from identification_data import IdentificationData

class TestIdentificationDataDeserialization(unittest.TestCase):

    def setUp(self):
        self.test_data_path = "../test_data"

class TestSimpleIdentificationDataDeserialization(TestIdentificationDataDeserialization):

    def runTest(self):
        filename = os.path.join(self.test_data_path, "proper_identification_data.txt")
        print(filename)
        with open(filename) as f:
           dat = IdentificationData.from_file(f)
        assert 1 == 1


if __name__ == "__main__":
    unittest.main()
