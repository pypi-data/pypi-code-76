import re
import sys
from datetime import datetime

from OpFlowLab.GUI.opFlowLabWorker import opFlowLabConfig
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextBrowser, QWidget, QPushButton, \
    QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect, QFileDialog

# Internal imports
from .GUI.XStream import XStream, XStreamError
from .GUI.advancedConfigTab import advancedConfigTab
from .GUI.flowDerivativesTab import flowDerivativesTab
from .GUI.flowMatchTab import flowMatchTab
from .GUI.flowPathTab import flowPathTab
from .GUI.flowTracerTab import flowTracerTab
from .GUI.flowWarpTab import flowWarpTab
from .GUI.loadImageTab import loadImageTab
from .GUI.loadVelocityTab import loadVelocityTab
from .GUI.opticalFlowTab import opticalFlowTab
from .GUI.aboutTab import aboutTab
from .GUI.styleSheet import qss


class opFlowLabGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'OpFlowLab GUI'
        self.left = 100
        self.top = 100
        self.width = 1100
        self.height = 800
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = tabWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class dropShadow():
    def __init__(self, radius=10, xoffset=2, yoffset=2):
        self.color = Qt.gray
        self.radius = radius
        self.xoffset = xoffset
        self.yoffset = yoffset

    def effect(self):
        dropShadowEffect = QGraphicsDropShadowEffect()
        dropShadowEffect.setColor(self.color)
        dropShadowEffect.setBlurRadius(self.radius)
        dropShadowEffect.setXOffset(self.xoffset)
        dropShadowEffect.setYOffset(self.yoffset)

        return dropShadowEffect


class tabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.loadImageTab = loadImageTab(self)
        self.opticalFlowTab = opticalFlowTab(self)
        self.loadVelocityTab = loadVelocityTab(self)
        self.flowMatchTab = flowMatchTab(self)
        self.flowPathTab = flowPathTab(self)
        self.flowWarpTab = flowWarpTab(self)
        self.flowTracerTab = flowTracerTab(self)
        self.flowDerivativesTab = flowDerivativesTab(self)
        self.advancedConfigTab = advancedConfigTab(self)
        self.aboutTab = aboutTab(self)

        # Add tabs
        self.tabs.addTab(self.loadImageTab, "Load images")
        self.tabs.addTab(self.opticalFlowTab, "Optical flow calculation")
        self.tabs.addTab(self.loadVelocityTab, "Load velocity field")
        self.tabs.addTab(self.flowMatchTab, "FlowMatch")
        self.tabs.addTab(self.flowWarpTab, "FlowWarp")
        self.tabs.addTab(self.flowPathTab, "FlowPath")
        self.tabs.addTab(self.flowTracerTab, "FlowTracer")
        self.tabs.addTab(self.flowDerivativesTab, "FlowDerivative")
        self.tabs.addTab(self.advancedConfigTab, "Advanced config")
        self.tabs.addTab(self.aboutTab, "Help/About")

        # Add tabs to widget
        self.tabs.setGraphicsEffect(dropShadow().effect())
        self.layout.addWidget(self.tabs)

        self.consoleLayout = QVBoxLayout()
        self.consoleLayout.setSpacing(0)

        self.consoleHeaderLayout = QHBoxLayout()
        self.consoleLabel = QLabel("Console output")
        self.consoleLabel.setStyleSheet("QLabel{"
                                        "background: #20639B;"
                                        "color: white;"
                                        "margin: 0 0 0 7px;"
                                        "padding: 7px;"
                                        "border: 0px solid transparent;"
                                        "border-bottom: 0px solid transparent;"
                                        "border-top-left-radius: 7px;"
                                        "font: bold"
                                        "}")
        self.consoleHeaderLayout.addWidget(self.consoleLabel, 10)
        self.consoleButton = QPushButton("Save console log")
        self.consoleButton.setStyleSheet("QPushButton{"
                                         "background: #20639B;"
                                         "color: white;"
                                         "margin: 0 7 0 0px;"
                                         "padding: 7px;"
                                         "border: 0px solid transparent;"
                                         "border-radius: 0px;"
                                         "border-top-right-radius: 7px;"
                                         "font: normal;"
                                         "text-align: right;"
                                         "}"
                                         "QPushButton:hover{"
                                         "text-decoration: underline"
                                         "}"
                                         )
        self.consoleHeaderLayout.addWidget(self.consoleButton, 1)
        self.consoleLayout.addLayout(self.consoleHeaderLayout)

        self.console = QTextBrowser(self)
        self.console.setOpenExternalLinks(True)
        self.console.setGraphicsEffect(dropShadow().effect())
        self.consoleLayout.addWidget(self.console)

        self.layout.addLayout(self.consoleLayout)

        # create connections
        XStream.stdout().messageWritten.connect(self.updateConsole)
        XStreamError.stderr().errorWritten.connect(self.updateConsoleError)
        self.loadImageTab.messageSignal.connect(self.updateConsoleSignal)
        self.opticalFlowTab.messageSignal.connect(self.updateConsoleSignal)
        self.loadVelocityTab.messageSignal.connect(self.updateConsoleSignal)
        self.flowMatchTab.messageSignal.connect(self.updateConsoleSignal)
        self.flowPathTab.messageSignal.connect(self.updateConsoleSignal)
        self.flowWarpTab.messageSignal.connect(self.updateConsoleSignal)
        self.flowTracerTab.messageSignal.connect(self.updateConsoleSignal)
        self.flowDerivativesTab.messageSignal.connect(self.updateConsoleSignal)
        self.advancedConfigTab.messageSignal.connect(self.updateConsoleSignal)

        self.loadImageTab.nextSignal.connect(self.nextTab)
        self.opticalFlowTab.nextSignal.connect(self.nextTab)
        self.loadVelocityTab.nextSignal.connect(self.nextTab)
        self.flowMatchTab.nextSignal.connect(self.nextTab)
        self.flowPathTab.nextSignal.connect(self.nextTab)
        self.flowWarpTab.nextSignal.connect(self.nextTab)
        self.flowTracerTab.nextSignal.connect(self.nextTab)

        self.consoleButton.clicked.connect(self.onConsoleButtonClicked)

        self.setLayout(self.layout)

        self.tabs.currentChanged.connect(self.updateTab)

    @pyqtSlot(str)
    def updateConsole(self, text):
        self.updateConsoleSignal(text.rstrip("\r\n"), "info")

    @pyqtSlot(str)
    def updateConsoleError(self, text):
        self.updateConsoleSignal(text, "error")

    @pyqtSlot(str, str)
    def updateConsoleSignal(self, text, signal_type):
        self.console.moveCursor(QTextCursor.End)
        tf = self.console.currentCharFormat()
        if signal_type == "error":
            color = "191, 43, 86"
        elif signal_type == "warn":
            color = "226, 112, 0"
        elif signal_type == "load":
            color = "37, 112, 88"
        elif signal_type == "param":
            color = "40, 114, 143"
        else:
            signal_type = "info"
            color = "0, 0, 0"

        # catch folders and add hyperlink
        if ":/" in text:
            pattern = re.compile(r'''((?:[^ "']|"[^"]*"|'[^']*')+)''')
            parts = pattern.split(text)
            text = ""
            for part in parts:
                if ":/" in part:
                    text += "<a href={}>{}</a>".format(part, part)
                else:
                    text += part

        self.console.insertHtml("<span style=\"color:rgb({})\">  [{} | {}] {}</span><br>".format(color, datetime.now().strftime("%x %X"), signal_type, text))
        self.console.moveCursor(QTextCursor.End)
        self.console.ensureCursorVisible()

    @pyqtSlot(int)
    def updateTab(self, value):
        if value == 1:
            self.opticalFlowTab.onFocusUpdate()
        elif value == 2:
            self.loadVelocityTab.onFocusUpdate()
        elif value == 3:
            self.flowMatchTab.onFocusUpdate()
        elif value == 4:
            self.flowWarpTab.onFocusUpdate()
        elif value == 5:
            self.flowPathTab.onFocusUpdate()
        elif value == 6:
            self.flowTracerTab.onFocusUpdate()
        elif value == 7:
            self.flowDerivativesTab.onFocusUpdate()

    @pyqtSlot()
    def nextTab(self):
        self.tabs.setCurrentIndex(self.tabs.currentIndex() + 1)

    def onConsoleButtonClicked(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Choose folder to save console log", "", filter="Text file (*.txt);;")
        print("Console log saved to {}".format(filepath))
        with open(filepath, 'w') as file:
            file.write(str(self.console.toPlainText()))


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet(qss)

    gui = opFlowLabGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
