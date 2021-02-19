import subprocess
import shlex

from PyQt5.QtCore import QThread, pyqtSlot, QObject, QCoreApplication
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout, QComboBox, QHBoxLayout

from .opFlowLabWorker import opFlowLabConfig
from OpFlowLab.GUI.opticalFlow.nvidiaOptions import nvidiaOFOptions
from .opticalFlow.broxOptions import broxOptions
from .opticalFlow.dualOptions import dualOptions
from .opticalFlow.farnebackOptions import farnebackOptions
from .opticalFlow.pyrLKOptions import pyrLKOptions
from .styleSheet import start_button_stylesheet, stop_button_stylesheet


class opticalFlowTab(QWidget):
    killSignal = pyqtSignal()
    messageSignal = pyqtSignal(str, str)
    nextSignal = pyqtSignal()

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.folderLayout = QGridLayout()
        self.opticalFlowLabel = QLabel("OpFlowLab executable: ")

        self.folderLayout.addWidget(self.opticalFlowLabel, 0, 0, 1, -1)

        self.typeLabel = QLabel("Optical flow type:")
        self.typeLabel.setMaximumWidth(110)
        self.folderLayout.addWidget(self.typeLabel, 1, 0)
        self.opFlowType = "Farneback"
        # TODO: disable NvidiaOF option if unavailable
        self.typeComboBox = QComboBox()
        self.typeComboBox.addItems(["Farneback", "PyrLK", "DualTVL1", "Brox", "NvidiaOF"])
        self.folderLayout.addWidget(self.typeComboBox, 1, 1)

        self.layout.addLayout(self.folderLayout)

        self.optionsWidget = farnebackOptions()
        self.layout.addWidget(self.optionsWidget)

        self.layout.addStretch()

        self.processButton = QPushButton("Calculate optical flow velocity field")

        self.buttons = QHBoxLayout()
        self.processButton = QPushButton("Calculate optical flow velocity field")
        self.processButton.setEnabled(False)
        self.buttons.addWidget(self.processButton)
        self.nextButton = QPushButton("Next " + u'\u2794')
        self.nextButton.setMaximumWidth(80)
        self.buttons.addWidget(self.nextButton)
        self.nextButton.setEnabled(False)
        self.layout.addLayout(self.buttons)

        self.config = opFlowLabConfig()

        # create thread
        self.thread = QThread()

        # create object which will be moved to another thread
        self.worker = OFWorker()
        self.worker.moveToThread(self.thread)

        # connect started signal to run method of object in another thread
        self.thread.started.connect(self.worker.runProcess)

        self.processButton.clicked.connect(self.onProcessButtonClicked)
        self.typeComboBox.currentTextChanged.connect(self.onTypeChange)

        self.worker.finishSignal.connect(self.updateProcessButton)
        self.worker.messageSignal.connect(self.passMessageSignal)
        self.killSignal.connect(self.worker.terminateCalculation)
        self.nextButton.clicked.connect(self.onNextButtonClicked)

    @pyqtSlot(str, str)
    def passMessageSignal(self, msg, msg_type):
        self.messageSignal.emit(msg, msg_type)

    @pyqtSlot()
    def updateProcessButton(self):
        print("Calculation has been stopped")
        self.processButton.setStyleSheet(start_button_stylesheet)
        self.processButton.setText("Calculate optical flow velocity field")
        self.nextButton.setEnabled(True)
        self.thread.terminate()

    def onProcessButtonClicked(self):
        if self.thread.isRunning():
            print("Process will be stopped once the current frame is completed.")
            self.killSignal.emit()
            self.thread.terminate()
        else:
            if self.config.hasInstance():
                valid = True
                # TODO: parameter checks
                if valid is True:
                    processLocation = self.config.executablePath
                    imagePath = self.config.imageFilePath
                    opticalFlowType = self.typeComboBox.currentText()

                    self.worker.command, param_dict = self.optionsWidget.getCommand(processLocation, imagePath, opticalFlowType)
                    self.config.saveParameters("Optical Flow", param_dict)
                    self.runProcess()
                    self.processButton.setStyleSheet(stop_button_stylesheet)
                    self.processButton.setText("Stop calculation of optical flow velocity field")
                else:
                    self.messageSignal.emit("Please ensure that all inputs are valid", "error")
            else:
                self.messageSignal.emit("Please initialize data first!", "error")

    def onTypeChange(self, value):
        self.layout.removeWidget(self.optionsWidget)
        self.optionsWidget.close()
        if value == "NvidiaOF":
            self.optionsWidget = nvidiaOFOptions()
            self.messageSignal.emit("Nvidia hardware optical flow can only be used on Nvidia GPUs from the Turing generation onwards", "warn")
        elif value == "PyrLK":
            self.optionsWidget = pyrLKOptions()
        elif value == "Farneback":
            self.optionsWidget = farnebackOptions()
        elif value == "Brox":
            self.optionsWidget = broxOptions()
        elif value == "DualTVL1":
            self.optionsWidget = dualOptions()

        self.layout.insertWidget(1, self.optionsWidget)
        self.layout.update()
        self.opFlowType = value

    def runProcess(self):
        if self.thread.isRunning():
            self.killSignal.emit()
            self.thread.quit()
        else:
            self.messageSignal.emit("--------------------------", "info")
            self.messageSignal.emit("Motion estimation using {}".format(self.opFlowType), "info")
            # start thread
            self.thread.start()

    def onNextButtonClicked(self):
        self.nextSignal.emit()

    def onFocusUpdate(self):
        self.opticalFlowLabel.setText("OpFlowLab executable: {}".format(self.config.executablePath))
        if self.config.executablePath is None:
            self.messageSignal.emit("OpFlowLab executable is not defined.", "warn")
            self.messageSignal.emit("Please ensure this location of is defined under the 'Advanced config' tab.", "warn")
            self.processButton.setEnabled(False)
        else:
            self.processButton.setEnabled(True)

class OFWorker(QObject):
    finishSignal = pyqtSignal()
    messageSignal = pyqtSignal(str, str)

    def __init__(self):
        super(QObject, self).__init__()
        self.command = None
        self.__abort = False

    def runProcess(self):
        self.__abort = False
        for cmd in self.command:
            self.messageSignal.emit("", "info")
            self.messageSignal.emit("Running command: {}".format(cmd), "info")
            process = subprocess.Popen(shlex.split(cmd), bufsize=1, universal_newlines=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while True:
                QCoreApplication.processEvents()
                output = process.stdout.readline()
                if process.poll() is not None:
                    break
                if output:
                    self.messageSignal.emit(output.strip().replace("\\\\", "/"), "info")

                if self.__abort == True:
                    process.kill()
                    break

            _, errors = process.communicate()
            if errors is not '':
                self.messageSignal.emit(errors.strip(), "error")
                break

            if self.__abort == True:
                break

        self.finishSignal.emit()
        # return rc

    def terminateCalculation(self):
        self.__abort = True
