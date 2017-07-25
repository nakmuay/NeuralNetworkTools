import numpy as np

class NamedColumnsArray(np.ndarray):

    def __new__(cls, arr, column_names=None):
        obj = np.asarray(arr).view(cls)

        # Handle column names
        #NamedColumnsArray._validate_new_inputs(arr, column_names)
        if column_names:
            column_names_ = column_names
        else:
            # Add default column names
            column_names_ = ["column_{0}".format(i) for i in range(arr.shape[1])]
        obj._column_names = column_names_

        return obj

    @classmethod
    def _validate_new_inputs(self, arr, column_names):
        # If no column_names were supplied we do not need to validate them
        if not column_names: return

        if len(column_names) != arr.shape[1]:
            raise ValueError("Dimension mismatch. Number of columns in array must equal the number of column names.")

    def __array_finalize__(self, obj):
        if obj is None: return
        self._column_names = getattr(obj, "_column_names", None)
    
    def __getitem__(self, idx):
        idx_ = self._getindeces(idx)
        arr = super(NamedColumnsArray, self).__getitem__(idx_)
        column_names = self._get_column_names_from_indeces(idx_)
        return NamedColumnsArray(arr, column_names)

    def _get_column_names_from_indeces(self, idx):
        column_names = self._column_names
        if isinstance(idx, tuple):
            # Note that this code will fail if Ellipsis indexing is used since column_names cannot be indexed using Ellipsis objects.
            if isinstance(idx[1], list):
                column_names = [self._column_names[i] for i in idx[1]]
            else:
                column_names = self._column_names[idx[1]]
        return column_names 

    def _getindeces(self, keys):
        # Check if columns are indexed
        if isinstance(keys, tuple):
            if self._is_list_of_strings(keys[1]):
                return (keys[0], [self.column_names.index(key) for key in keys[1]])
            else:
                return keys
        else:
            return keys

    def _is_list_of_strings(self, obj):
        if isinstance(obj, list):
            return all(isinstance(elem, str) for elem in obj)
        return False
   
    @property 
    def column_names(self):
        return self._column_names

    def __str__(self):
        array_str = super(NamedColumnsArray, self).__str__()
        return "{0}\n{1}".format(self.column_names, array_str)

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
