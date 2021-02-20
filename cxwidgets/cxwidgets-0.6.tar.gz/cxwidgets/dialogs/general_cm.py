from cxwidgets import BaseGridW, PSpinBox
from cxwidgets.aQt.QtWidgets import QLabel, QLineEdit, QTextEdit
from cxwidgets.aQt.QtCore import Qt


class CXGeneralCM(BaseGridW):
    def __init__(self, source_w=None, parent=None):
        super().__init__(parent)
        self.source_w = source_w
        self.grid.addWidget(QLabel("handle info"), 0, 0, 1, 2, Qt.AlignHCenter)

        self.grid.addWidget(QLabel("name"), 1, 0)
        self.name_line = QLineEdit()
        self.grid.addWidget(self.name_line, 1, 1)
        self.name_line.setText(self.source_w.cname)
        self.name_line.setReadOnly(True)

        self.grid.addWidget(QLabel("flags"), 2, 0, 1, 2, Qt.AlignHCenter)
        self.flags_te = QTextEdit()
        self.grid.addWidget(self.flags_te, 3, 0, 1, 2, Qt.AlignHCenter)
        ft = source_w.chan.rflags_text()
        self.flags_te.setText('\n'.join(ft))
