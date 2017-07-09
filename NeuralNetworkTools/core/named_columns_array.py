import numpy as np

class NamedColumnsArray(np.ndarray):

    def __new__(cls, input_array, column_names=None):
        obj = np.asarray(input_array).view(cls)
        obj._column_names = column_names
        
        # Add default column names
        if not column_names:
            for i in range(input_array.shape()[1]):
                print(i)
            #obj._column_names = 
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self._column_names = getattr(obj, "_column_names", None)

    def __getitem__(self, idx):
        _idx = self._getindeces(idx)
        if isinstance(_idx, tuple):
            self._column_names = [self._column_names[i] for i in _idx[1]]
        return super(NamedColumnsArray, self).__getitem__(_idx)

    def __setitem__(self, idx, value):
        _idx = self._getindeces(idx)
        return super(NamedColumnsArray, self).__setitem__(_idx, value)

    def _getindeces(self, idx):
        # Check if columns are indexed
        if not isinstance(idx, tuple): return idx

        names = idx[1]
        if not self._is_list_of_strings(names): return idx
        return (idx[0], [self.column_names.index(name) for name in names])

    def _is_list_of_strings(self, obj):
        if isinstance(obj, list):
            return all(isinstance(elem, str) for elem in obj)
        return False

    @property 
    def column_names(self):
        return self._column_names

class NamedColumnsArrayBuilder():
        
    def __init__(self):
        self._column_names = []
        self._data = []

    @property
    def column_names(self):
        return self._column_names
    
    @property
    def data(self):
        return self._data

    def append_row(self, row):
        if not row:
            raise ValueError("Cannot add an empty row!")
        if not self.data:
            self._column_names = list(row.keys())

        self.data.append([])
        for col in self.column_names:
            self.data[-1].append(row[col])

    def build(self):
        return NamedColumnsArray(np.array(self.data, np.float64), self.column_names)
