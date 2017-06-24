import unittest
import os
import numpy as np

from named_array import NamedArray

class TestNamedArray(unittest.TestCase):

    def runTest(self):
        arr1 = NamedArray(np.array([[1, 10], [2, 20], [3, 30]]), ['a', 'b'])
        print(arr1)
        print(arr1.loc('a'))
        print(arr1.loc('b'))
        arr2 = NamedArray(np.array([[1, 10], [2, 20], [3, 30]]))
        print(arr2)
        print(arr2.iloc([0]))
        print(arr2.iloc([1]))

if __name__ == "__main__":
    unittest.main()
