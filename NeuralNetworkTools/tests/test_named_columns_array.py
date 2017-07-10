import unittest
import os
import numpy as np
import sys

sys.path.append("/home/martin/github/NeuralNetworkTools")
from NeuralNetworkTools.core.named_columns_array import NamedColumnsArray, NamedColumnsArrayBuilder

class TestNamedArray(unittest.TestCase):
    
    def setUp(self):
        self.arr = np.array([[1, 10], [2, 20], [3, 30]])
        self.default_named_arr = NamedColumnsArray(self.arr)
        self.named_arr = NamedColumnsArray(self.arr, ['a', 'b'])

    def test_np_indexing(self):
        # Test access without indexing
        np.testing.assert_array_almost_equal(self.arr, self.named_arr.data)
        np.testing.assert_array_almost_equal(self.arr, self.default_named_arr.data)
        
        # Test indexing when default column names are used
        np.testing.assert_array_almost_equal(self.arr[:], self.default_named_arr[:].data)
        np.testing.assert_array_almost_equal(self.arr[:, 0], self.default_named_arr[:, 0].data)
        np.testing.assert_array_almost_equal(self.arr[:, 0:2], self.default_named_arr[:, 0:2].data)
        np.testing.assert_array_almost_equal(self.arr[0:2, 0:2], self.default_named_arr[0:2, 0:2].data)
   
        # Test indexing when default column names are used
        np.testing.assert_array_almost_equal(self.arr[:], self.named_arr[:].data)
        np.testing.assert_array_almost_equal(self.arr[:, 0], self.named_arr[:, 0].data)
        np.testing.assert_array_almost_equal(self.arr[:, 0:2], self.named_arr[:, 0:2].data)
        np.testing.assert_array_almost_equal(self.arr[0:2, 0:2], self.named_arr[0:2, 0:2].data)

    def test_named_indexing(self):
        # Test indexing when default column names are used
        np.testing.assert_array_almost_equal(self.arr[:, [0]], self.default_named_arr[:, ["column_0"]].data)
        np.testing.assert_array_almost_equal(self.arr[:, [0,1]], self.default_named_arr[:, ["column_0", "column_1"]].data)
        np.testing.assert_array_almost_equal(self.arr[0:2, [1, 0]], self.default_named_arr[0:2, ["column_1", "column_0"]].data)
   
        # Test indexing when default column names are used
        np.testing.assert_array_almost_equal(self.arr[:], self.named_arr[:].data)
        np.testing.assert_array_almost_equal(self.arr[:, [0]], self.named_arr[:, ['a']].data)
        np.testing.assert_array_almost_equal(self.arr[:, 0:2], self.named_arr[:, ['a', 'b']].data)
        np.testing.assert_array_almost_equal(self.arr[0:2, 0:2], self.named_arr[0:2, ['a', 'b']].data)

"""
class TestNamedArrayBuilder(unittest.TestCase):

    def runTest(self):
        builder = NamedColumnsArrayBuilder()
        builder.append_row({'a': 1, 'b': 2})
        builder.append_row({'b': 20, 'a': 10})
        print(builder.column_names)
        print(builder.data)
"""

if __name__ == "__main__":
    unittest.main()
