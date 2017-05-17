import os.path
import csv
from collections import defaultdict
import numpy as np
from matplotlib import pyplot as plt

def write_line(file_obj, value=''):
    file_obj.write("{0}\n".format(value))

def read_delimited_line(file_obj, delim=' '):
    line = file_obj.readline()
    return line.strip().split(delim)

class IdentificationDataSet:
    """Class which represents a set of input/output-data from a simulated system.  
    """

    # Static variables
    _header_delim = ':'
    _set_size_format = 'set_size' + _header_delim + '{0}'

    # Static methods
    def from_file(file_obj):
        """Factory method for creating object from file.  
        """
        data_set = []
        _ = next(file_obj)                                  # skip one line
        while True:
            _ = next(file_obj)                              # skip one line
            data = IdentificationData.from_file(file_obj)  # read data
            if data:
                data_set.append(data)
            else:
                break
            
        # return object
        return IdentificationDataSet(data_set)

    def __init__(self, data_set=[]):
        """The constructor.  
        """
        self.data_set = []
        self.set_size = 0
        self.add_data(data_set)

    def add_data(self, data):
        # TODO [martin]: add some validation of data here, e.g. check data size etc.
        if data:
            self.data_set.append(data)
            self.set_size += 1
        else:
            print("Noting to add.")

    def to_file(self, file_obj):
        write_line(file_obj, self._set_size_format.format(self.set_size))
        write_line(file_obj)
        for iddata in self.data_set:
            iddata.to_file(file_obj)
            write_line(file_obj)

    def plot(self):
        """Plot object data.  
        """
        for iddata in self.data_set:
            plt.figure()
            iddata.plot()


class IdentificationData:
    """Class which represent input/output-data from a simulated system.  
    """

    # static variables
    _header_delim = ':'
    _data_delim = ','
    _input_prefix = "input" + _header_delim
    _output_prefix = "output" + _header_delim

    _name_format = "name" + _header_delim + "{0}"
    _num_samples_format = "number_of_samples" + _header_delim + "{0}"
    
    # static methods
    def from_file(file_obj):
        """Factory method for creating object from file.  
        """
        header = IdentificationData._read_header(file_obj)
        if not header:
            print("Nothing to read. Quiting...")
            return
        
        # read first line and allocate data
        reader = csv.DictReader(file_obj)
        input_data, output_data, input_key_map, output_key_map = IdentificationData._allocate_data(reader, \
                                                                                                    header["number_of_samples"])
        # read remaining data
        input_data, output_data = IdentificationData._read_data(reader, \
                                                                 input_data, output_data, \
                                                                 input_key_map, output_key_map, \
                                                                 header["number_of_samples"]-2)
        return IdentificationData(input_data, output_data, name=header["name"])

    def _read_header(file_obj):
        """Helper method which reads header information.  
        """
        header = {"name": '', "number_of_samples": ''}
        line = read_delimited_line(file_obj, IdentificationData._header_delim)
        if len(line) < 2:
            return None
        header["name"] = line[1]
        
        line = read_delimited_line(file_obj, IdentificationData._header_delim)
        if len(line) < 2:
            return None
        header["number_of_samples"] = int(line[1])
        return header

    def _allocate_data(reader, num_samples):
        """Helper method for allocating data.  
        """
        # declare key maps to map from header in file to dictionary keys
        input_key_map = {}
        output_key_map = {}
        # declare dictionaries to hold results
        input_data = {}
        output_data = {}

        # read first row and allocate data
        first_row = next(reader)
        for key in first_row:
            if key.startswith(IdentificationData._input_prefix):
                input_key = IdentificationData._remove_string_prefix(key, IdentificationData._input_prefix)
                input_key_map[key] = input_key
                input_data[input_key_map[key]] = np.empty(num_samples)
                input_data[input_key_map[key]][0] = np.float(first_row[key])
            elif key.startswith(IdentificationData._output_prefix):
                output_key = IdentificationData._remove_string_prefix(key, IdentificationData._output_prefix)
                output_key_map[key] = output_key
                output_data[output_key_map[key]] = np.empty(num_samples)
                output_data[output_key_map[key]][0] = np.float(first_row[key])
            else:
                raise ValueError("Unrecognized prefix in header: '{0}'".format(key))
        return (input_data, output_data, input_key_map, output_key_map)

    def _read_data(reader, input_data, output_data, input_key_map, output_key_map, num_samples):
        """Helper method for reading data.
        """
        for row_nr, row in enumerate(reader):
            for key in row:
                # read input
                if "input" in key:
                    input_data[input_key_map[key]][row_nr+1] = np.float(row[key])
                # read output
                if "output" in key:
                    output_data[output_key_map[key]][row_nr+1] = np.float(row[key])
            if row_nr == num_samples:
                break
        return (input_data, output_data)
        
    def _remove_string_prefix(string, prefix):
        """Helper method for removing string prefix.  
        """
        if string.startswith(prefix):
            return string[len(prefix):]
        return string

    def _get_header_at(self, key):
        if self.input_data and key in self.input_data.keys():
            return self._input_prefix + key
        if self.output_data and key in self.output_data.keys():
            return self._output_prefix + key
        return None

    def _get_data_at(self, key, idx):
        if self.input_data and key in self.input_data.keys():
            return self.input_data[key][idx]
        if self.output_data and key in self.output_data.keys():
            return self.output_data[key][idx]
        return None

    def __init__(self, input_data, output_data, name=''):
        """The constructor.  
        """
        self.input_data = input_data
        self.output_data = output_data
        self.name = name

        # TODO [martin]: this should be cleaned up
        if self.input_data:
            self.number_of_samples = len(next(iter(self.input_data.values())))
        elif self.output_data:
            self.number_of_samples = len(next(iter(self.output_data.values())))
        else:
            self.number_of_samples = 0

    def get_inputs(self):
        if self.input_data:
            return list(self.input_data.keys())
        return []

    def get_input_data(self, var):
        return self.input_data[var]

    def get_outputs(self):
        if self.output_data:
            return list(self.output_data.keys())
        return []

    def get_output_data(self, var):
        return output_data[var]

    def to_file(self, file_obj):
        # write header
        self._write_header_to_file(file_obj)

        # write column headers
        self._write_colheaders_to_file(file_obj)
            
        # write data
        self._write_data_to_file(file_obj)

    def _write_header_to_file(self, file_obj):
        write_line(file_obj, self._name_format.format(self.name))
        write_line(file_obj, self._num_samples_format.format(self.number_of_samples))

    def _write_colheaders_to_file(self, file_obj):
        header_keys = self._get_colheader_keys()
        num_colheaders = len(header_keys)
        for idx, key in enumerate(header_keys):
            file_obj.write(self._get_header_at(key))
            if idx < num_colheaders-1:
                file_obj.write(self._data_delim)
        file_obj.write("\n")

    def _write_data_to_file(self, file_obj):
        header_keys = self._get_colheader_keys()
        num_colheaders = len(header_keys)
        for row in range(self.number_of_samples):
            for idx, key in enumerate(header_keys):
                file_obj.write("{0}".format(self._get_data_at(key, row)))
                if idx < num_colheaders-1:
                    file_obj.write(self._data_delim)
                if idx == num_colheaders-1:
                    file_obj.write("\n")

    def _get_colheader_keys(self):
        return self.get_inputs() + self.get_outputs()

    def plot(self):
        """Plot object data.  
        """
        plt.subplot(2, 1, 1)
        output_var = self.get_outputs()[0]
        output_h, = plt.plot(self.output_data[output_var], label=output_var)
        plt.legend(handles=[output_h])

        plt.subplot(2, 1, 2)
        input_var = self.get_inputs()[0]
        input_h, = plt.plot(self.input_data[input_var], label=input_var)
        plt.legend(handles=[input_h])
        
        
def main(file):
    """
    # read data
    with open(file) as f:
        idset = IdentificationDataSet.from_file(f)

    # plot data
    idset.plot()
    plt.draw()
    plt.show()
    """

    input_data = {"input_var_0": np.array(range(10))}
    output_data = {"output_var_0": 2 * np.array(range(10)), "output_var_1": 3 * np.array(range(10))}
    
    indat = IdentificationData(input_data, [], name="only_input")
    outdat = IdentificationData([], output_data, name="only_output")
    inoutdat = IdentificationData(input_data, output_data, name="input_and_output")

    idset = IdentificationDataSet()
    idset.add_data(indat)
    idset.add_data(outdat)
    idset.add_data(inoutdat)
    with open("IdentificationData_serialization_test.txt", 'w') as f:
        idset.to_file(f)

    for d in idset.data_set:
        print(d.get_inputs())

if __name__ == "__main__":
    # Boiler plate function
    #input_path = r"C:\Users\Martin\Documents\Visual Studio 2015\Projects\NeuralNetwork\NeuralNetworkApp\bin\Debug\NetworkData"
    #iddata_file = os.path.join(input_path, "neural_net_reference_set.txt")

    iddata_file = "neural_net_reference_set_error_1.txt"
    main(iddata_file)



