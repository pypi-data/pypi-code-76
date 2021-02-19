from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, \
    QVBoxLayout, QGroupBox

from os import path

_dir = path.dirname(__file__)
with open(path.join(_dir, '..', 'version.py'), encoding="utf-8") as f:
    exec(f.read())

class aboutTab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)
        self.optionsLayout.addWidget(QLabel("OpFlowLab version: {}".format(__version__)), 0, 0)

        self.documentationLabel = QLabel("Documentation: <a href=\"https://opflowlab.readthedocs.io/\">https://opflowlab.readthedocs.io/</a>")
        self.documentationLabel.setOpenExternalLinks(True)
        self.optionsLayout.addWidget(self.documentationLabel, 1, 0)

        self.opflowlabSourceLabel = QLabel("OpFlowlab source: <a href=\"https://gitlab.com/xianbin.yong13/OpFlowLab\">https://gitlab.com/xianbin.yong13/OpFlowLab</a>")
        self.opflowlabSourceLabel.setOpenExternalLinks(True)
        self.optionsLayout.addWidget(self.opflowlabSourceLabel, 2, 0)

        self.opflowlabSourceLabel = QLabel("OpFlowlab executable source: <a href=\"https://gitlab.com/xianbin.yong13/optical-flow-opencv\">https://gitlab.com/xianbin.yong13/optical-flow-opencv</a>")
        self.opflowlabSourceLabel.setOpenExternalLinks(True)
        self.optionsLayout.addWidget(self.opflowlabSourceLabel, 3, 0)

        self.layout.addLayout(self.optionsLayout)
        self.layout.addStretch()