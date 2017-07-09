import numpy as np
import csv

#from NeuralNetworkTools.core.named_columns_array import NamedColumnsArray, NamedColumnsArrayBuilder
from NeuralNetworkTools.core import * 


def from_file(filename):
    return IdentificationDataParser(filename).create()

class IdentificationDataParser():

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
        line = self._read_delimited_line(file_obj, IdentificationDataParser._header_delim)
        if len(line) < 2:                                                     
            return None                                                       
        header["name"] = line[1]                                              
                                                                              
        line = self._read_delimited_line(file_obj, IdentificationDataParser._header_delim)
        if len(line) < 2:                                                     
            return None                                                       
        header["number_of_samples"] = int(line[1])                            
        return header

    def _read_data(self, fileobj):
        input_prefix = IdentificationDataParser._input_prefix
        output_prefix = IdentificationDataParser._output_prefix
        
        reader = csv.DictReader(fileobj)
        for row in reader:
            input_dict = {}
            output_dict = {}
            for key in row:
                if key.startswith(input_prefix):
                    name = IdentificationDataParser._remove_string_prefix(key, input_prefix)
                    input_dict[name] = row[key]
                elif key.startswith(output_prefix):
                    name = IdentificationDataParser._remove_string_prefix(key, output_prefix)
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
