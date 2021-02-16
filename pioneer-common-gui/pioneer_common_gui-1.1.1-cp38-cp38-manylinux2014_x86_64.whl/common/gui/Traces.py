from __future__ import division

from pioneer.common.gui import Array, Product

from PyQt5.QtCore import pyqtSlot, pyqtSignal, pyqtProperty, QVariant, QObject
from PyQt5.QtGui import QPolygonF
try:
    from PyQt5.QtChart import QAbstractSeries
except:
    print('Warning. QtChart could not be imported.')

import numpy as np

def series_to_polyline(xdata, ydata):

    #inspired from https://github.com/PierreRaybaut/plotpy/wiki/Using-Qt-Charts-(PyQtChart)-to-plot-curves-efficiently-in-Python!
    size = len(xdata)
    polyline = QPolygonF(size)
    pointer = polyline.data()
    dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
    pointer.setsize(2*polyline.size()*tinfo(dtype).dtype.itemsize)
    memory = np.frombuffer(pointer, dtype)
    memory[:(size-1)*2+1:2] = xdata
    memory[1:(size-1)*2+2:2] = ydata
    return polyline


class TracesDataSource(Product.Product):
    def __init__(self, parent = None):
        super(TracesDataSource, self).__init__(parent)
        self._traces = None
        self._xdata = None
        self._spacing = 500.0
        self._normalize = False
#         pen = self.pen()
#         pen.setWidthF(.1)
#         self.setPen(pen)
#         self.xdata = np.linspace(0., 512., 512, np.float32)
#         self.append(series_to_polyline(self.xdata, np.sin(self.xdata)))

        #self.setUseOpenGL(True)


    def _trcaes_cb(self):
        self._xdata = None

    Product.InputProperty(vars(), Product.VariantProduct, "traces", _trcaes_cb)

    Product.InputProperty(vars(), float, "spacing")

    Product.InputProperty(vars(), bool, "normalize")

    @pyqtSlot(result = list)
    def getROI(self):
        if self._traces is not None:
            self._traces.update()
            if self._traces._variant:
                return [self._traces._variant['start_index'], self._traces._variant['data'].shape[0]]
        return [0,0]

    @pyqtSlot(QAbstractSeries, int, int)
    def refresh(self, series, index, channel):
        '''
            index: the series index
            channel: the channel index (relative to roi start)
        '''
        self.update()
        if self._traces is not None and self._traces._variant:
            data = self._traces._variant['data']
            if data.size > 0 and channel < data.shape[0]:
                if self._xdata is None:
                    self._xdata = np.linspace(0, data.shape[1], data.shape[1], np.float32)

                channel_data = data[channel,:].astype(np.float32)

                if self._normalize:
                    channel_data -= np.mean(channel_data)

                polygon = series_to_polyline(self._xdata, channel_data + index * self.spacing * (1 if index%2 == 0 else -1))

                if series.count() > 0:
                    series.replace(polygon)
                else:
                    series.append(polygon)


class TracesGeometry( Array.ArrayFloat2 ):

    def __init__(self, parent = None):

        super(TracesGeometry, self).__init__(parent)

        self.ndarray = np.empty((0, 2), dtype = np.float32)
        #inputs:
        self._traces = None
        self._specs = None

        #outputs:
        self._indices = Array.ArrayUInt1()
        self._indices.set_producer(self)

        self._saturationIndices = Array.ArrayUInt1()
        self._saturationIndices.set_producer(self)

    specsChanged = pyqtSignal()
    @pyqtProperty(QVariant, notify = specsChanged)
    def specs(self):
        return QVariant(self._specs)

    @specs.setter
    def specs(self, s):
        Product.assign_input(self, "specs", s)

    tracesChanged = pyqtSignal()
    @pyqtProperty(Product.VariantProduct, notify = tracesChanged)
    def traces(self):
        return self._traces

    @traces.setter
    def traces(self, t):
        Product.assign_input(self, "traces", t)

    @pyqtProperty(Array.ArrayUInt1, constant = True)
    def indices(self):
        return self._indices

    @pyqtProperty(Array.ArrayUInt1, constant = True)
    def saturationIndices(self):
        return self._saturationIndices

    def _update(self):
        if self._traces is None or not self._traces._variant:
            return

        data = self._traces._variant['data']
        n_channels, n_samples = data.shape

        self.indices.resize(n_samples*n_channels + n_channels)
        self.resize(n_channels * n_samples)
        x_axis = np.arange(n_samples, dtype = np.float32)/n_samples

        v = self._specs["v"]

        t_min, t_max = np.iinfo(data.dtype).min, np.iinfo(data.dtype).max
        r = t_max - t_min
        for c in range(n_channels):
            begin = c * n_samples
            end = (c+1) * n_samples
            samples = data[c,:]
            self.indices.ndarray[begin + c:end + c] = np.arange(begin, end)
            self.indices.ndarray[end + c] = 0xFFFFFFFF #primitive restart
            self.ndarray[begin:end,0] = x_axis + c//v * 1.1
            self.ndarray[begin:end,1] = samples.astype(np.float32)/r + c%v * 1.1 # the y axis

        flat_data = data.flatten()
        self.saturationIndices.ndarray = np.where(np.logical_or(flat_data >= t_max, flat_data <= t_min))[0]



