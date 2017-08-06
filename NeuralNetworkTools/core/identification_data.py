import csv
import sys
import numpy as np
import pandas as pd

sys.path.append("/home/martin/github/NeuralNetworkTools")
from NeuralNetworkTools.core.named_columns_array import NamedColumnsArray, NamedColumnsArrayBuilder

class IdentificationData():

    def __init__(self, input_data=None, output_data=None, input_column_names=None, output_column_names=None):
        self._validate_init_input(input_data, output_data, input_column_names, output_column_names)

        self._input_data = pd.DataFrame(input_data, columns=input_column_names)
        self._output_data = pd.DataFrame(output_data, columns=output_column_names)
        self._iter_counter = 0

    @property
    def input_data(self):
        return self._input_data.values

    @property
    def input_column_names(self):
        return self._input_data.columns.values

    @property
    def output_data(self):
        return self._output_data.values

    @property
    def output_column_names(self):
        return self._output_data.columns.values

    @property
    def shape(self):
        num_rows = 0
        if self.input_data.size != 0:
            num_rows,num_input_cols = self.input_data.shape
        if self.output_data.size != 0:
            num_rows,num_output_cols = self.output_data.shape
        return (num_rows, num_input_cols, num_output_cols)

    def _validate_init_input(self, input_data, output_data, input_column_names, output_column_names):
        pass

    def __getitem__(self, key):
        if isinstance(key, tuple):
            key_dim = len(key)
            if key_dim == 2:
                input_data = self._input_data.iloc[key[0], key[1]]
                output_data = self._output_data.iloc[key[0]]
            elif key_dim == 3:
                input_data = self._input_data.iloc[key[0], key[1]]
                output_data = self._output_data.iloc[key[0], key[2]]
            else:
                raise IndexError("Indexing using more that three dimensions is an error.")
        else:
            input_data = self._input_data.iloc[key]
            output_data = self._output_data.iloc[key]
        
        return IdentificationData(input_data, output_data)

    def __iter__(self):
        # Reset iteration counter 
        self._reset_iter_counter()
        return self

    def __next__(self):
        if self._iter_counter > self.shape[0]-1:
            raise StopIteration
        else:
            self._iter_counter += 1
            return IdentificationData(self._input_data.iloc[[self._iter_counter-1], :], \
                                        self._output_data.iloc[[self._iter_counter-1], :])

    def _reset_iter_counter(self):
        self._iter_counter = 0
