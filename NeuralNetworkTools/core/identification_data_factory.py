from abc import ABCMeta, abstractmethod
import numpy as np

from identification_data import IdentificationData, IdentificationDataSet

# ----------------------------------------------------------------------------
class SignalModifier(metaclass=ABCMeta):
    """
    Interface for signal source modifiers
    """

    @abstractmethod
    def apply(self, source):
        pass
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
class GaussianNoiseModifier(metaclass=ABCMeta):
    """
    Class which adds gaussian noise to a signal
    """

    def __init__(self, mean=0.0, std=1.0):
        self._mean = mean
        self._std = std

    def apply(self, signal):
        signal = signal + np.random.normal(self._mean, self._std, len(signal))
        return signal
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
class NormalizingModifier(metaclass=ABCMeta):
    """
    Class which normalizes a signal
    """

    def __init__(self):
        self._name = "test"

    def apply(self, signal):
        # remove mean
        signal = signal - np.mean(signal)
        denominator = np.max(np.abs(signal))
        if denominator == 0.0:
            print("Division by zero!")
        signal = signal / denominator
        return signal
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
class SignalSource(metaclass=ABCMeta):
    """
    Interface for signal sources
    """

    @abstractmethod
    def generate(self):
        pass
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
class SinusSource(SignalSource):

    def __init__(self, number_of_samples,  amplitude=1.0, frequency=1.0, phase_shift=0.0):
        self._number_of_samples = number_of_samples
        self._amplitude = amplitude
        self._frequency = frequency
        self._phase_shift = phase_shift

    def generate(self):
        time_vector = np.linspace(0, 1, self._number_of_samples)
        signal = self._amplitude * np.sin(2.0*np.pi * self._frequency * time_vector + self._phase_shift)
        return signal
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
class CompoundSource(SignalSource):

    def __init__(self, sources):
        self._sources = sources
        
    def generate(self):
        signal = self._sources[0].generate()
        for source in self._sources:
            signal = signal + source.generate()
        return signal
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
class IdentificationDataFactory(metaclass=ABCMeta):

    """
    Identification data factory interface
    """

    @abstractmethod
    def create(self, generator):
        pass
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
class FligtIdentificationDataFactory(IdentificationDataFactory):

    def __init__(self, generator):
        self._generator = generator

    def create(self):
        # generate a signal
        input_signal = self._generator.generate()

        # normalize signal
        norm_modifier = NormalizingModifier()
        input_signal = norm_modifier.apply(input_signal)
        input_data = {"input_1": input_signal}

        # add some noise to output
        output_signal = input_signal**2
        noise_modifier = GaussianNoiseModifier(0.0, 0.1)
        output_signal = noise_modifier.apply(output_signal)
        
        # normalize output
        output_signal = norm_modifier.apply(output_signal)

        # create identification data
        output_data = {"output_1": output_signal}
        dat = IdentificationData(input_data, output_data)
        return dat
# ----------------------------------------------------------------------------
