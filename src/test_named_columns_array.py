import unittest
import os
import numpy as np

from named_columns_array import NamedColumnsArray, NamedColumnsArrayBuilder
from named_columns_array import IdentificationData

class TestNamedArray(unittest.TestCase):

    def runTest(self):
        arr1 = NamedColumnsArray(np.array([[1, 10], [2, 20], [3, 30]]), ['a', 'b'])
        print(arr1.column_names)
        print(arr1[:])
        print(arr1[:, :])
        print(arr1[:, [0, 1]])
        print(arr1[:, :])
        print(arr1[:, ['a', 'b']])
        print(arr1[:, ['a', 'b']] + 1)
        print(arr1[:, ['a', 'b']] * 1.2)
        print(arr1[:, ['a', 'b']] / 1.2)
        print(arr1[:, ['b', 'a']])
        print(arr1[:, :])

class TestNamedArrayBuilder(unittest.TestCase):

    def runTest(self):
        builder = NamedColumnsArrayBuilder()
        builder.add_column('a', [1])
        print(builder.column_names)
        print(builder.data)
        
        builder.add_column('b', np.empty(10))
        print(builder.column_names)
        print(builder.data)

class TestIdentificationData(unittest.TestCase):

    def runTest(self):
        print("hej")
        inp = NamedColumnsArray(np.array([[1, 10], [2, 20], [3, 30]]), ['a', 'b'])
        out = NamedColumnsArray(np.array([[1, 10], [2, 20], [3, 30]]), ['a', 'b'])
        d = IdentificationData(inp, out)

        print("hej")
        print(d.input_data)
        print(d.output_data)
 

if __name__ == "__main__":
    unittest.main()
