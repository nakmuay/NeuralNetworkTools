import numpy as np

class NamedColumnsArray():

    def __init__(self, input_array, column_names=None):
        self._data = np.asarray(input_array)
        self._column_names = column_names
        
        # Add default column names
        _column_names = []
        if not column_names:
            for i in range(input_array.shape[1]):
                _column_names.append("column_{0}".format(i))
            self._column_names = _column_names

    def __getitem__(self, idx):
        _idx = self._getindeces(idx)
        _column_names = self.column_names 
        if isinstance(_idx, tuple):
            if isinstance(_idx[1], list):
                _column_names = [self.column_names[i] for i in _idx[1]]
            else:
                _column_names = self._column_names[_idx[1]]
        return NamedColumnsArray(self._data[_idx], _column_names)

    def __setitem__(self, idx, value):
        _idx = self._getindeces(idx)
        self._data[_idx] = value

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

    def __str__(self):
        array_str = self._data.__str__()
        return "{0}\n{1}".format(self.column_names, array_str)

    @property 
    def column_names(self):
        return self._column_names

    @property 
    def data(self):
        return self._data

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
