from cxwidgets import BaseGridW, PSpinBox
from cxwidgets.aQt.QtWidgets import QLabel, QLineEdit
from cxwidgets.aQt.QtCore import Qt
from .general_cm import CXGeneralCM


class CXSpinboxCM(CXGeneralCM):
    def __init__(self, source_w=None, parent=None):
        super().__init__(source_w, parent)

        rc = self.grid.rowCount()

        self.grid.addWidget(QLabel("step"), rc + 2, 0)
        self.step_sb = PSpinBox()
        self.grid.addWidget(self.step_sb, rc + 2, 1)
        self.step_sb.setValue(source_w.singleStep())
        self.step_sb.done.connect(source_w.setSingleStep)

        self.grid.addWidget(QLabel("min"), rc + 3, 0)
        self.min_sb = PSpinBox()
        self.grid.addWidget(self.min_sb, rc + 3, 1)
        self.min_sb.setValue(source_w.minimum())
        self.min_sb.done.connect(source_w.setMinimum)

        self.grid.addWidget(QLabel("max"), rc + 4, 0)
        self.max_sb = PSpinBox()
        self.grid.addWidget(self.max_sb, rc + 4, 1)
        self.max_sb.setValue(source_w.maximum())
        self.max_sb.done.connect(source_w.setMaximum)

        source_w.chan.get_range()
        source_w.chan.get_strings()
        print(source_w.chan.quant)