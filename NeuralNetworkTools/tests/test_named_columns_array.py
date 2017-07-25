import unittest
import os
import numpy as np
import sys

sys.path.append("/home/martin/github/NeuralNetworkTools")
from NeuralNetworkTools.core.named_columns_array import NamedColumnsArray, NamedColumnsArrayBuilder

class TestNamedArray(unittest.TestCase):
    
    def setUp(self):
        self.arr = np.array([[1, 10, 100], [2, 20, 200], [3, 30, 300]])
        self.default_named_arr = NamedColumnsArray(self.arr)
        self.named_arr = NamedColumnsArray(self.arr, ['a', 'b', 'c'])

    def test_creation_init(self):
        _ = NamedColumnsArray(self.arr, ['a', 'b', 'c'])

    def test_np_indexing(self):
        # Test indexing when default column names are used
        np.testing.assert_array_almost_equal(self.arr[:], self.default_named_arr[:])
        np.testing.assert_array_almost_equal(self.arr[:, [0]], self.default_named_arr[:, [0]])
        np.testing.assert_array_almost_equal(self.arr[:, 0:2], self.default_named_arr[:, 0:2])
        np.testing.assert_array_almost_equal(self.arr[0:2, 0:2], self.default_named_arr[0:2, 0:2])
   
        # Test indexing when default column names are used
        np.testing.assert_array_almost_equal(self.arr[:], self.named_arr[:])
        np.testing.assert_array_almost_equal(self.arr[:, 0], self.named_arr[:, 0])
        np.testing.assert_array_almost_equal(self.arr[:, 0:2], self.named_arr[:, 0:2])
        np.testing.assert_array_almost_equal(self.arr[0:2, 0:2], self.named_arr[0:2, 0:2])

    def test_named_indexing(self):
        # Test indexing when default column names are used
        np.testing.assert_array_almost_equal(self.arr[:, [0]], self.default_named_arr[:, ["column_0"]])
        np.testing.assert_array_almost_equal(self.arr[:, [0,1]], self.default_named_arr[:, ["column_0", "column_1"]])
        np.testing.assert_array_almost_equal(self.arr[0:2, [1, 0]], self.default_named_arr[0:2, ["column_1", "column_0"]])
   
        # Test indexing when default column names are used
        np.testing.assert_array_almost_equal(self.arr[:], self.named_arr[:])
        np.testing.assert_array_almost_equal(self.arr[:, [0]], self.named_arr[:, ['a']])
        np.testing.assert_array_almost_equal(self.arr[:, 0:2], self.named_arr[:, ['a', 'b']])
        np.testing.assert_array_almost_equal(self.arr[0:2, 0:2], self.named_arr[0:2, ['a', 'b']])
    
    def test_printing(self):
        print("before printing")
        print(self.named_arr)

class TestNamedArrayBuilder(unittest.TestCase):

    def runTest(self):
        builder = NamedColumnsArrayBuilder()
        builder.append_row({'a': 1, 'b': 2})
        builder.append_row({'b': 20, 'a': 10})

if __name__ == "__main__":
    unittest.main()
