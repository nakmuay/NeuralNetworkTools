import unittest
import os
import numpy as np

from named_columns_array import NamedColumnsArray, NamedColumnsArrayBuilder

class TestNamedArray(unittest.TestCase):

    def runTest(self):
        arr1 = NamedColumnsArray(np.array([[1, 10], [2, 20], [3, 30]]), ['a', 'b'])


class TestNamedArrayBuilder(unittest.TestCase):

    def runTest(self):
        builder = NamedColumnsArrayBuilder()
        builder.append_row({'a': 1, 'b': 2})
        builder.append_row({'b': 20, 'a': 10})
        print(builder.column_names)
        print(builder.data)


if __name__ == "__main__":
    unittest.main()
