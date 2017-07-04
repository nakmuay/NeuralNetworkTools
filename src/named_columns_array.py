import numpy as np
from collections import defaultdict

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

class IdentificationDataFromFileFactory():

    # static variables
    _header_delim = ':' 
    _data_delim = ',' 
    _input_prefix = "input" + _header_delim
    _output_prefix = "output" + _header_delim
    
    _name_format = "name" + _header_delim + "{0}"
    _num_samples_format = "number_of_samples" + _header_delim + "{0}"

    def __init__(self, reader):
        self._reader = reader
        self._input_data = defaultdict(list)
        self._output_data = defaultdict(list)

    def create(self):
        input_data = default_dict();

class IdentificationData():

    def __init__(self, input_data, output_data):
        self._input_data = input_data
        self._output_data = output_data

    @property
    def input_data(self):
        return self._input_data

    @property
    def input_names(self):
        return self._input_data.names

    @property
    def output_data(self):
        return self._output_data

    @property
    def output_names(self):
        return self._output_data.names

        
