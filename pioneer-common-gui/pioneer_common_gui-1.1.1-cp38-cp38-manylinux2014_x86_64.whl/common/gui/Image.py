from pioneer.common import images
from pioneer.common.gui import Array, Product

from datetime import datetime
from matplotlib import cm
from PyQt5.QtGui import QImage, qRgb
from PyQt5.QtQuick import QQuickPaintedItem
from PyQt5.QtCore import QPointF, pyqtSlot as Slot, pyqtSignal as Signal, pyqtProperty as Property, QVariant

import matplotlib.pyplot as plt
import numpy as np
import pickle
import tarfile
import time
import traceback

class ColorMapArray(Array.ArrayUByte4):
    def __init__(self, parent = None):
        super(ColorMapArray, self).__init__(parent)
        self._colorMap = 'jet'
        self._width = 256
        self._update()

    Product.InputProperty(vars(), str, "colorMap")
    Product.InputProperty(vars(), int, "width")

    def _update(self):
        norm = plt.Normalize(0, self._width)
        colormap = getattr(cm, self._colorMap)(norm(np.arange(self._width)))
        self.ndarray = np.ascontiguousarray(colormap * 255, dtype=np.uint8)

class ImageFilter(Array.Array):
    def __init__(self, parent = None):
        super(ImageFilter, self).__init__(parent)
        self._imageArray = None

    Product.InputProperty(vars(), Array.Array, "imageArray")

    def _update(self):
        raise RuntimeError('not implemented!')

class BGRToRGBFilter(ImageFilter):
    def __init__(self, parent = None):
        super(BGRToRGBFilter, self).__init__(parent)

    def _update(self):
        image = self.imageArray.ndarray
        image = np.ascontiguousarray(image[..., ::-1])
        assert (image.dtype == np.uint8 and image.ndim == 3
                and image.shape[2] == 3), \
                'Invalid image format, dtype: {}, shape: {}'.format(
                    image.dtype, image.shape
                )
        self.ndarray = image

class ColorMapFliter(ImageFilter):
    def __init__(self, parent = None):
        super(ColorMapFliter, self).__init__(parent)
        self._colorMap = 'jet'
        self._min = None
        self._max = None
        self._adaptative = 0
        self._log = False
        self._interpolate = False

    def colorMap_cb(self):
        assert hasattr(cm, self._colorMap)

    Product.InputProperty(vars(), str, 'colorMap', colorMap_cb)

    Product.InputProperty(vars(), float, 'min')

    Product.InputProperty(vars(), float, 'max')

    Product.InputProperty(vars(), bool, 'log')

    Product.InputProperty(vars(), float, 'adaptative')

    #Test, addition of interpolation for missing values
    Product.InputProperty(vars(), bool, 'interpolate')


    def _update(self):
        if self.imageArray is not None and self.imageArray.ndarray.size > 0:
            image = self.imageArray.ndarray #shape (8,32)
            #test interpolation placed here
            if self._interpolate:
                image = images.interpolate_missings(image)

#             if self._adaptative > 0:
#                 image = basics.clean_bleed_amp(image, image, self._adaptative)
            _min = self._min if self._min is not None else image.min()
            _max = self._max if self._max is not None else image.max()

            self.ndarray = images.to_color_image(image, self._colorMap, _min, _max, self._log)







# Inspired from https://gist.github.com/smex/5287589
gray_color_table = [qRgb(i, i, i) for i in range(256)]
def to_QImage(ndarray):
    if ndarray is None:
        return QImage()

    if ndarray.dtype == np.uint8:
        shape = ndarray.shape
        if len(shape) == 2 or shape[2] == 1:
            qim = QImage(ndarray.data, shape[1], shape[0], ndarray.strides[0], QImage.Format_Indexed8)
            qim.setColorTable(gray_color_table)
            return qim

        elif len(shape) == 3:
            if shape[2] == 3:
                qim = QImage(ndarray.data, shape[1], shape[0], ndarray.strides[0], QImage.Format_RGB888);
                return qim
            elif shape[2] == 4:
                qim = QImage(ndarray.data, shape[1], shape[0], ndarray.strides[0], QImage.Format_RGBA8888);
                return qim

    raise RuntimeError('Unsupported ndarray type')

class QImagePainter(QQuickPaintedItem):

    def __init__(self, parent = None):
        super(QImagePainter, self).__init__(parent)
        self._imageArray = None


    imageArrayChanged = Signal()
    @Property(Array.Array, notify = imageArrayChanged)
    def imageArray(self):
        return self._imageArray

    @imageArray.setter
    def imageArray(self, i):
        if i != self._imageArray:
            if self._imageArray is not None:
                self._imageArray.productDirty.disconnect(self.imageChanged)
            self._imageArray = i
            if self._imageArray is not None:
                self._imageArray.productDirty.connect(self.imageChanged)

    @Slot()
    def imageChanged(self):
        self.update()

    @Slot(float, float, result = QPointF)
    def mapToImage(self, x, y):
        
        try:
            r = self.contentsBoundingRect()
            rows, cols = self._imageArray.ndarray.shape[:2]
            x_, y_ = (x-r.x())*cols/r.width(), (y-r.y()) * rows/r.height()
        except:
            print(traceback.format_exc())
            return QPointF(-1, -1)

        return QPointF(x_, y_)


    def paint(self, painter):
        if self._imageArray is not None :
            self._imageArray.update()
            if self._imageArray._error:
                print(self._imageArray._error)
                return

            try:
                qimage = to_QImage(self._imageArray.ndarray)
                painter.drawImage(self.contentsBoundingRect(), qimage)
            except:
                print(traceback.format_exc())
                return
