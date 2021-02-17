from pioneer.common.gui import Product

from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot, pyqtProperty as Property
from PyQt5.QtGui import QVector3D

import numpy as np

class Array( Product.Product ):

    arrayChanged = Signal()

    def __init__(self, parent = None, ndarray = None):
        super(Array, self).__init__(parent)
        self._input = None
        self.ndarray = None
        self._timestamp = 0
        self.productClean.connect(self.arrayChanged)
        
        self.set_ndarray(ndarray)


    def set_ndarray(self, ndarray):
        if (ndarray is not None or self.ndarray is not None ): # if both array are None, we know they're the same, otherwise, we assume they're not
            self.ndarray = ndarray
            self.makeDirty()
    
    def input_cb(self):
        if self._input:
            if isinstance(self._input, list):
                if len(self._input) > 0 and isinstance(self._input[0], QVector3D):
                    self._input = [[v.x(), v.y(), v.z()] for v in self._input]
                a = np.array(self._input, self.ndarray.dtype)
            elif isinstance(self._input, np.array):
                a = self._input.as_type(self.ndarray.type)

        if len(a.shape) == 1 and len(self.ndarray.shape) == 2:
            a = np.expand_dims(a, axis=1) # the most frequent case

        assert len(a.shape) == len(self.ndarray.shape)
        for i in range(1,len(a.shape)):
            assert a.shape[i] == self.ndarray.shape[i]
        self.ndarray = a

    Product.InputProperty(vars(), 'QVariant', 'input', input_cb)

    @Slot(result = 'QVariant')
    def values(self):
        return self.ndarray.tolist()

    @staticmethod
    def recurse_value(a, indices):
        if len(indices) == 1:
            return a[int(indices[0])]
        return Array.recurse_value(a[int(indices[0])], indices[1:])

    @Slot(list, result = float)
    def value(self, indices):
        assert len(indices) == len(self.ndarray.shape)
        return float(self.ndarray.dtype.type(Array.recurse_value(self.ndarray, indices)))

    @Property(int, notify = arrayChanged)
    def size(self):
        return self.ndarray.size

    @Property(list, notify = arrayChanged)
    def shape(self):
        return list(self.ndarray.shape)

    @Slot()
    def resize(self, new_size):
        '''
        Resizes dim 0 only
        '''
        s = list(self.ndarray.shape)
        s[0] = new_size
        self.ndarray.resize(tuple(s), refcheck = False)

class ArrayFloat1(Array):
    def __init__(self, parent = None):
        super(ArrayFloat1, self).__init__(parent)
        self.ndarray = np.empty((0, 1), dtype = np.float32)
class ArrayFloat2(Array):
    def __init__(self, parent = None):
        super(ArrayFloat2, self).__init__(parent)
        self.ndarray = np.empty((0, 2), dtype = np.float32)
class ArrayFloat3(Array):
    def __init__(self, parent = None):
        super(ArrayFloat3, self).__init__(parent)
        self.ndarray = np.empty((0, 3), dtype = np.float32)
class ArrayFloat4(Array):
    def __init__(self, parent = None):
        super(ArrayFloat4, self).__init__(parent)
        self.ndarray = np.empty((0, 4), dtype = np.float32)

class ArrayDouble1(Array):
    def __init__(self, parent = None):
        super(ArrayDouble1, self).__init__(parent)
        self.ndarray = np.empty((0, 1), dtype = np.float64)
class ArrayDouble2(Array):
    def __init__(self, parent = None):
        super(ArrayDouble2, self).__init__(parent)
        self.ndarray = np.empty((0, 2), dtype = np.float64)
class ArrayDouble3(Array):
    def __init__(self, parent = None):
        super(ArrayDouble3, self).__init__(parent)
        self.ndarray = np.empty((0, 3), dtype = np.float64)
class ArrayDouble4(Array):
    def __init__(self, parent = None):
        super(ArrayDouble4, self).__init__(parent)
        self.ndarray = np.empty((0, 4), dtype = np.float64)
class ArrayUInt1(Array):
    def __init__(self, parent = None):
        super(ArrayUInt1, self).__init__(parent)
        self.ndarray = np.empty((0,), dtype = np.uint32)

class ArrayInt1(Array):
    def __init__(self, parent = None):
        super(ArrayInt1, self).__init__(parent)
        self.ndarray = np.empty((0,), dtype = np.int32)

class ArrayShort512(Array):
    def __init__(self, parent = None):
        super(ArrayShort512, self).__init__(parent)
        self.ndarray = np.empty((0,512), dtype = np.int16)

class ArrayUShort1(Array):
    def __init__(self, parent = None):
        super(ArrayUShort1, self).__init__(parent)
        self.ndarray = np.empty((0,), dtype = np.uint16)


class ArrayUByte3(Array):
    def __init__(self, parent = None):
        super(ArrayUByte3, self).__init__(parent)
        self.ndarray = np.empty((0,3), dtype = np.uint8)

class ArrayUByte4(Array):
    def __init__(self, parent = None):
        super(ArrayUByte4, self).__init__(parent)
        self.ndarray = np.empty((0,4), dtype = np.uint8)
