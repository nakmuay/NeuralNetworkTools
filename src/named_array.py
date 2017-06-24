import numpy as np

class NamedArray():
    
    def __init__(self, data, names=None):
        self._data = data
        if not names:
            names = list(range(np.size(data, axis=1)))
        self._names = names
        self._nameidx = dict(zip(names, range(len(names))))

    @property
    def data(self):
        return self._data

    @property
    def names(self):
        return self._names

    def loc(self, keys):
        idx = []
        for key in keys:
            if key not in self.names:
                raise ValueError("Key {0} is not defined in names!")
            idx.append(self._nameidx[key])
        return self.iloc(idx) 
         
    def iloc(self, idx):
        names = [self.names[i] for i in idx]
        return NamedArray(self.data[:, idx], names)

    def __repr__(self):
        return "NamedArray\nnames: {0}\ndata: {1}".format(self.names, self.data)


