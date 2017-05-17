import os.path
import numpy as np
from matplotlib import pyplot as plt
import collections

def import_data(file):
    d = collections.defaultdict(list)
    with open(file, 'r') as f:
        for line in f:
            columns = line.split("\t")
            for cIdx, c in enumerate(columns):
                d[cIdx].append(float(c.strip()))
    return d
                
def main(ref_file, before_training_file, after_training_file, train_info):
    ref_data = import_data(ref_file)
    bt_data = import_data(before_training_file)
    at_data = import_data(after_training_file)
    info = import_data(train_info)

    # Plot fit
    plt.figure()
    ref, = plt.plot(ref_data[0], ref_data[1], 'b', label="referende data")
    before, = plt.plot(bt_data[0], bt_data[1], 'g+', label="before training")
    after, = plt.plot(at_data[0], at_data[1], 'r', label="after training")
    plt.legend(handles=[ref, before, after])
    plt.draw()

    # Plot error history
    plt.figure()
    error_label, = plt.plot(info[0], info[1], label="error")
    plt.legend(handles=[error_label])
    plt.draw()

    plt.show()

if __name__ == "__main__":
    output_path = r"C:\Users\Martin\Documents\Visual Studio 2015\Projects\NeuralNetwork\NeuralNetworkApp\bin\Debug\NetworkData"
    ref_file = os.path.join(output_path, "neural_net_reference.txt")
    before_training_file = os.path.join(output_path, "neural_net_before_training.txt")
    after_training_file = os.path.join(output_path, "neural_net_after_training.txt")
    training_info_file = os.path.join(output_path, "neural_net_training_info.txt")
    main(ref_file, before_training_file, after_training_file, training_info_file)


