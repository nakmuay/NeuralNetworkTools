import numpy as np
import csv
import sys

sys.path.append("/home/martin/github/NeuralNetworkTools")
from NeuralNetworkTools.core.named_columns_array import NamedColumnsArray, NamedColumnsArrayBuilder

class IdentificationData():

    def __init__(self, input_data, output_data):
        self._input_data = input_data
        self._output_data = output_data
        self._iter_counter = 0

    @property
    def input_data(self):
        return self._input_data

    @property
    def output_data(self):
        return self._output_data

    @property
    def shape(self):
        num_rows = 0
        if self.input_data.size != 0:
            num_rows,num_input_cols = self.input_data.shape
        if self.output_data.size != 0:
            num_rows,num_output_cols = self.output_data.shape
        return (num_rows, num_input_cols, num_output_cols)

    def __getitem__(self, idx):
        # TODO, martin: add support for Ellipsis indexing 
        if isinstance(idx, tuple):
            idx_dim = len(idx)
            if idx_dim == 2:
                if isinstance(idx[0], type(Ellipsis)) or isinstance(idx[0], type(Ellipsis)):
                    input_data = self.input_data[idx[0]]
                    output_data = self.output_data[idx[0], idx[1]]
                else:
                    input_data = self.input_data[idx[0], idx[1]]
                    output_data = self.output_data[idx[0]]
            elif idx_dim == 3:
                input_data = self.input_data[idx[0], idx[1]]
                output_data = self.output_data[idx[0], idx[2]]
            else:
                raise IndexError("Indexing using more that three dimensions is an error.")
        else:
            input_data = self.input_data[idx]
            output_data = self.output_data[idx]

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
            return IdentificationData(self._input_data[self._iter_counter-1, :], \
                                        self._output_data[self._iter_counter-1, :])

    def _reset_iter_counter(self):
        self._iter_counter = 0
