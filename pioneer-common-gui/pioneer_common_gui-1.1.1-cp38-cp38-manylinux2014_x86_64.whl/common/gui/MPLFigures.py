from pioneer.common.gui import Product

import pioneer.common as leddar_utils

from PyQt5.QtCore import Qt, pyqtSignal as Signal, pyqtSlot as Slot

from pioneer.common.gui.qml import backend_qtquick5
import numpy as np

class EchoesMPLFigureProvider( Product.Product ):

    def __init__( self, parent = None ):
        super(EchoesMPLFigureProvider, self).__init__( parent )
        self._packages = None
        self._absoluteMax = 2**20#np.finfo('f4').max
        self._absoluteMin = 0#np.finfo('f4').min
        self._max = self._absoluteMax
        self._min = self._absoluteMin
        self._dynamicMax = self._absoluteMax
        self._dynamicMin = self._absoluteMin
        self._dynamicRange = True
        self._logScale = False
        self._colorMap = 'viridis'
        self._flipud = False
        self._rot90 = False
        self._options = 'amplitudes:max_amplitudes'

        self.shape = None
        self.fig = None
        self.ax = None
        self.ax_img = None



    clicked = Signal(int, int, float, int, arguments = ['v', 'h', 'value', 'button'])
    Product.InputProperty(vars(), Product.VariantProduct, 'packages')
    Product.InputProperty(vars(), float, 'absoluteMax')
    Product.InputProperty(vars(), float, 'absoluteMin')
    Product.InputProperty(vars(), float, 'min')
    Product.InputProperty(vars(), float, 'max')
    Product.InputProperty(vars(), bool, 'dynamicRange')
    Product.InputProperty(vars(), bool, 'logScale')
    Product.InputProperty(vars(), str, 'colorMap')
    Product.InputProperty(vars(), str, 'options')

    Product.ROProperty(vars(), float, 'dynamicMax')
    Product.ROProperty(vars(), float, 'dynamicMin')

    def handle_rotated_changed(self):
        self.ax_img = None
    Product.InputProperty(vars(), bool, 'flipud', handle_rotated_changed)
    Product.InputProperty(vars(), bool, 'rot90', handle_rotated_changed)

    def setCanvas(self, canvas):
        self.canvas = canvas
        self.ax = None
        self.ax_img = None
        self.makeDirty()

    def _update(self):
        if self._packages is not None:
            p = self._packages.variant
            if p is not None:


                if self._options == 'amplitudes:max_amplitudes':
                    self.img = leddar_utils.images.extrema_image(p['v'], p['h'], p['data']
                                                , sort_field = 'amplitudes'
                                                , sort_direction = -1
                                                , dtype = 'f4')

                elif self._options == 'distances:max_amplitudes':
                    _, others = leddar_utils.images.extrema_image(p['v'], p['h'], p['data']
                                                            , sort_field = 'amplitudes'
                                                            , sort_direction = -1
                                                            , other_fields = ['distances']
                                                            , dtype='f4')
                    self.img = others['distances']

                

                # the following is a hack around an hard to overcome architectural flaw
                # We want to reuse EchoesMPLFigureProvider in cheddar_config and das.api, 
                # but we don't yet want them to know about each other, thus we 'hide' a 
                # das.api.samples.Sample instance inside its 'raw' packet so we can orient 
                # the image in a standard way. It is crucial to keep the standard orientation in one place
                if 'das.sample' in p:
                    s = p['das.sample']
                    self.img = s.transform_image(self.img)

                    if 'amplitudes:' in self._options and 'extrema_amp' in s.datasource.sensor.config:
                        self.absoluteMax = s.datasource.sensor.config['extrema_amp']
                    if 'distances:' in self._options and 'extrema_dist' in s.datasource.sensor.config:
                        self.absoluteMax = s.datasource.sensor.config['extrema_dist']
                
                if self.img is None:
                    return

                self.set_dynamicMin(self, self.img.min())
                self.set_dynamicMax(self, self.img.max())

                vmax = self.dynamicMax if self._dynamicRange else self._max
                vmin = self.dynamicMin if self._dynamicRange else self._min

                if self._flipud:
                    self.img = np.flipud(self.img)

                if self._rot90:
                    self.img = np.rot90(self.img)

                color_img = leddar_utils.images.to_color_image(self.img, self._colorMap, vmin = vmin, vmax = vmax, log_scale = self._logScale)


               

                if self.ax is None: 
                    self.ax = self.canvas.getFigure().add_subplot(111)
                    
                    self.helper = backend_qtquick5.MPLImageHelper(self.img, self.ax)
                    
                    def on_click(event):
                        try:
                            col, row = self.helper.to_indices(event.xdata, event.ydata)
                            value = self.img[row,col]
                            if self._rotated:
                                row, col = col, row
                            self.clicked.emit(row, col, value, backend_qtquick5.to_qt_button[event.button])
                        except:
                            pass

                    self.cid = self.canvas.mpl_connect('button_press_event', on_click)

                self.helper.img = self.img

                if self.ax_img is None:
                    self.ax_img = self.ax.imshow(color_img)
                    self.canvas.draw()
                else:
                    self.ax_img.set_data(color_img)
                    self.canvas.draw()

                if self.shape != self.img.shape:
                    self.shape =  self.img.shape


