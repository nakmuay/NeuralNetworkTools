import unittest
import os
import numpy as np

from named_columns_array import NamedColumnsArray, NamedColumnsArrayBuilder
from named_columns_array import IdentificationData

class TestNamedArray(unittest.TestCase):

    def runTest(self):
        arr1 = NamedColumnsArray(np.array([[1, 10], [2, 20], [3, 30]]), ['a', 'b'])


class TestNamedArrayBuilder(unittest.TestCase):

    def runTest(self):
        builder = NamedColumnsArrayBuilder()
        builder.add_column('a', [1, 2])
        builder.add_column('b', np.empty(10))
        print(builder.column_names)
        print(builder.data)


class TestIdentificationData(unittest.TestCase):

    def runTest(self):
        inp = NamedColumnsArray(np.array([[1, 10], [2, 20], [3, 30]]), ['a', 'b'])
        out = NamedColumnsArray(np.array([[1, 10], [2, 20], [3, 30]]), ['a', 'b'])
        d = IdentificationData(inp, out)
        print(d.input_data)
        print(d.output_data)
 

if __name__ == "__main__":
    unittest.main()
