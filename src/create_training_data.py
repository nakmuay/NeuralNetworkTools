import numpy as np
from matplotlib import pyplot as plt

from identification_data_factory import     FligtIdentificationDataFactory, \
                                            SinusSource, CompoundSource, \
                                            GaussianNoiseModifier
from identification_data import IdentificationDataSet


def main():
    #source = SinusSource(110, amplitude = 10)
    #modifier = GaussianNoiseModifier(0.0, 1)
    #plt.plot(source.generate(modifier))
    #plt.show()

    data_set = IdentificationDataSet()
    for i in range(50):
        sin_source_1 = SinusSource(100, 0.6, 0.05, 2*np.pi * (1.0 - 0.03*i))
        sin_source_2 = SinusSource(100, 0.4, 0.9, 2*np.pi * (1.0 + 0.04*i))
        signal_source = CompoundSource([sin_source_1, sin_source_2])
        factory = FligtIdentificationDataFactory(signal_source)
        data_set.add_data(factory.create())
    data_set.plot()
    plt.show()

if __name__ == "__main__":
    main()
