import numpy as np

class NamedColumnsArray(np.ndarray):

    def __new__(cls, input_array, column_names=None):
        obj = np.asarray(input_array).view(cls)
        obj._column_names = column_names
        obj._column_names_idx = dict((idx, key) for key, idx in enumerate(column_names))
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self._column_names = getattr(obj, "_column_names", None)
        self._column_names_idx = getattr(obj, "_column_names_idx", None)

    def __getitem__(self, idx):
        _idx = self._getindeces(idx)
        return super(NamedColumnsArray, self).__getitem__(_idx)

    def __setitem__(self, idx, value):
        _idx = self._getindeces(idx)
        return super(NamedColumnsArray, self).__setitem__(_idx, value)

    def _getindeces(self, idx):
        # Check if columns are indexed
        if not isinstance(idx, tuple): return idx

        names = idx[1]
        if not self._is_list_of_strings(names): return idx
        return (idx[0], [self._column_names_idx[name] for name in names])

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
            self._column_names = row.keys()

        self.data.append([])
        for col in self.column_names:
            self.data[-1].append(row[col])

    def build(self):
        return NamedColumnsArray(np.array(self.data, np.float64), self.column_names)
