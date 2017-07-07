import numpy as np
import csv

from named_columns_array import NamedColumnsArray, NamedColumnsArrayBuilder

class IdentificationData():

    def __init__(self, input_data, output_data):
        self._input_data = input_data
        self._output_data = output_data
        self._current_sample = 0

    @property
    def input_data(self):
        return self._input_data

    @property
    def input_names(self):
        return self._input_data.column_names

    @property
    def output_data(self):
        return self._output_data

    @property
    def output_names(self):
        return self._output_data.column_names

    @property
    def shape(self):
        num_rows = 0
        if self.input_data.size != 0:
            num_rows,num_input_cols = self.input_data.shape
        if self.output_data.size != 0:
            num_rows,num_output_cols = self.output_data.shape
        return (num_rows, num_input_cols, num_output_cols)

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_sample > self.shape[0]-1:
            raise StopIteration
        else:
            self._current_sample += 1
            return IdentificationData(self._input_data[self._current_sample-1, :], \
                                        self._output_data[self._current_sample-1, :])


class IdentificationDataFromFileFactory():

    # static variables
    _header_delim = ':' 
    _data_delim = ',' 
    _input_prefix = "input" + _header_delim
    _output_prefix = "output" + _header_delim
    
    _name_format = "name" + _header_delim + "{0}"
    _num_samples_format = "number_of_samples" + _header_delim + "{0}"

    def __init__(self, filename):
        self._filename = filename
        self._input_builder = NamedColumnsArrayBuilder()
        self._output_builder = NamedColumnsArrayBuilder()

    def create(self):
        with open(self._filename) as f:
            header = self._read_header(f)
            input_data, output_data = self._read_data(f)
        return IdentificationData(input_data, output_data)

    def _read_header(self, file_obj):                                               
        """                                                                   
        Helper method which reads header information.                         
        """                                                                   
        header = {"name": '', "number_of_samples": ''}                        
        line = self._read_delimited_line(file_obj, IdentificationDataFromFileFactory._header_delim)
        if len(line) < 2:                                                     
            return None                                                       
        header["name"] = line[1]                                              
                                                                              
        line = self._read_delimited_line(file_obj, IdentificationDataFromFileFactory._header_delim)
        if len(line) < 2:                                                     
            return None                                                       
        header["number_of_samples"] = int(line[1])                            
        return header

    def _read_data(self, fileobj):
        input_prefix = IdentificationDataFromFileFactory._input_prefix
        output_prefix = IdentificationDataFromFileFactory._output_prefix
        
        reader = csv.DictReader(fileobj)
        for row in reader:
            input_dict = {}
            output_dict = {}
            for key in row:
                if key.startswith(input_prefix):
                    name = IdentificationDataFromFileFactory._remove_string_prefix(key, input_prefix)
                    input_dict[name] = row[key]
                elif key.startswith(IdentificationDataFromFileFactory._output_prefix):
                    name = IdentificationDataFromFileFactory._remove_string_prefix(key, output_prefix)
                    output_dict[name] = row[key]
                else:
                    raise ValueError("Unrecognized prefix in header: '{0}'".format(key))
            self._input_builder.append_row(input_dict)
            self._output_builder.append_row(output_dict)

        input_data = self._input_builder.build()
        output_data = self._output_builder.build()
        return (input_data, output_data)

    def _read_delimited_line(self, file_obj, delim=' '):
        line = file_obj.readline()               
        return line.strip().split(delim)         

    def _remove_string_prefix(string, prefix):
        """
        Helper method for removing string prefix.
        """
        if string.startswith(prefix):
            return string[len(prefix):]
        return string
