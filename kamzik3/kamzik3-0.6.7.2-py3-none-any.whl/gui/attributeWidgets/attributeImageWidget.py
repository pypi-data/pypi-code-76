import time

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QSizePolicy
from pyqtgraph.widgets.RawImageWidget import RawImageWidget

from kamzik3.constants import *
from kamzik3.gui.attributeWidgets.attributeWidget import AttributeWidget


class AttributeImageWidget(AttributeWidget):
    lt = time.perf_counter_ns()

    def _set_input_widget(self):
        self.input_widget = RawImageWidget(scaled=True)
        # self.input_widget = pg.ImageView()
        # self.input_widget = GraphicsView(useOpenGL=True)
        # self.image_item = ImageItem()
        # self.input_widget.addItem(self.image_item)
        if self.attribute[DESCRIPTION] is not None:
            self.input_widget.setToolTip(self.attribute[DESCRIPTION])
        self.input_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_value(self, value):
        # self.image_item.setImage(value, autoLevels=False, autoRange=False, scaled=True)
        # self.input_widget.scaleToImage(self.image_item)
        self.input_widget.setImage(value)
        self.input_widget.setMaximumSize(QSize(*value.shape))

    def get_attribute_value(self):
        return None

    def get_widget_value(self):
        return None
