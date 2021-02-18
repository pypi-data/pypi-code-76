from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QProgressBar, QPushButton, QLineEdit, QLabel, \
    QVBoxLayout, QHBoxLayout, QGroupBox

from .imageViewerWidget import imageViewerWidget
from .opFlowLabWorker import opFlowLabWorker, opFlowLabConfig
from .styleSheet import invalid_stylesheet, valid_stylesheet, stop_button_stylesheet, start_button_stylesheet


class flowWarpTab(QWidget):
    killSignal = pyqtSignal()
    messageSignal = pyqtSignal(str, str)
    nextSignal = pyqtSignal()

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.forwardPathLabel = QLabel("Forward velocity field folder: ")
        self.layout.addWidget(self.forwardPathLabel)

        self.optionsGroup = QGroupBox("Options")
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)

        self.optionsLayout.addWidget(QLabel("Starting Frame"), 0, 0)
        self.startingFrameLineEdit = QLineEdit("1")
        self.startingFrameLineEdit.setPlaceholderText("Starting Frame")
        self.optionsLayout.addWidget(self.startingFrameLineEdit, 1, 0)

        self.optionsGroup.setLayout(self.optionsLayout)
        self.layout.addWidget(self.optionsGroup)

        self.layout.addStretch()

        self.processButton = QPushButton("Generate FlowWarp")
        self.processButton.setEnabled(False)
        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.processButton)
        self.displayOutput = QPushButton("Display FlowWarp")
        self.displayOutput.setEnabled(False)
        self.buttons.addWidget(self.displayOutput)
        self.nextButton = QPushButton("Next " + u'\u2794')
        self.nextButton.setMaximumWidth(80)
        self.buttons.addWidget(self.nextButton)
        self.nextButton.setEnabled(False)
        self.layout.addLayout(self.buttons)

        self.progressBarLayout = QHBoxLayout()
        self.progressBar = QProgressBar()
        self.progressBarLayout.addWidget(QLabel("Progress:"))
        self.progressBarLayout.addWidget(self.progressBar)
        self.timeLeft = QLabel("Time Left:")
        self.timeLeft.setMinimumWidth(120)
        self.progressBarLayout.addWidget(self.timeLeft)
        self.layout.addLayout(self.progressBarLayout)

        self.imageViewer = imageViewerWidget()
        self.colorWheelViewer = imageViewerWidget()

        self.config = opFlowLabConfig()

        # create thread
        self.thread = QThread()
        # create object which will be moved to another thread
        self.opFlowLabWorker = opFlowLabWorker()

        # move object to another thread
        self.opFlowLabWorker.moveToThread(self.thread)
        self.opFlowLabWorker.progressSignal.connect(self.updateProgressBar)
        self.killSignal.connect(self.opFlowLabWorker.terminateCalculation)
        self.opFlowLabWorker.finishSignal.connect(self.updateToProcessButton)
        self.opFlowLabWorker.updateSignal.connect(self.updateImageViewer)
        self.opFlowLabWorker.timeSignal.connect(self.updateTimeLeft)

        # connect started signal to run method of object in another thread
        self.thread.started.connect(self.opFlowLabWorker.runFlowWarp)

        self.processButton.clicked.connect(self.onProcessButtonClicked)
        self.displayOutput.clicked.connect(self.onDisplayOutputButtonClicked)
        self.nextButton.clicked.connect(self.onNextButtonClicked)

        self.startingFrameLineEdit.editingFinished.connect(self.updateStartFrameValue)

    @pyqtSlot()
    def updateToProcessButton(self):
        print("Calculation has been stopped")
        self.processButton.setStyleSheet(start_button_stylesheet)
        self.processButton.setText("Generate FlowWarp")
        self.nextButton.setEnabled(True)
        self.thread.quit()

    def onProcessButtonClicked(self):
        if self.thread.isRunning():
            self.killSignal.emit()
            self.thread.quit()
        else:
            valid = self.updateStartFrameValue()

            if self.opFlowLabWorker.isImageLoaded() and self.config.forwardFolderPath is not None:
                if valid is True:
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("###################################################", "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("Visualizing FlowWarp with the following parameters:", "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("------------- Folders ------------", "param")
                    self.messageSignal.emit("Image file path: {}".format(self.config.imageFilePath), "param")
                    self.messageSignal.emit("Forward velocity field folder path: {}".format(self.config.forwardFolderPath), "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("----------- Parameters -----------", "param")
                    self.messageSignal.emit("Starting frame: {}".format(self.config.start_frame+1), "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("-------- Save parameters ---------", "param")
                    self.messageSignal.emit("Save location: {}".format(self.config.forwardFolderPath + "/" + self.config.flowWarp_folder), "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("###################################################", "param")

                    # save parameters
                    self.config.saveParameters("FlowWarp", ["imageFilePath", "forwardFolderPath", "start_frame"])

                    # start thread
                    self.thread.start()
                    self.processButton.setStyleSheet(stop_button_stylesheet)
                    self.processButton.setText("Stop FlowWarp")
                    self.displayOutput.setEnabled(True)
                else:
                    self.messageSignal.emit("Please ensure that all inputs are valid", "error")
            else:
                self.messageSignal.emit("Please load image file and forward velocity field folder first!", "error")

    def onFocusUpdate(self):
        self.forwardPathLabel.setText("Forward velocity field folder: {}".format(self.config.forwardFolderPath))
        if self.config.forwardFolderPath is None:
            self.messageSignal.emit("FlowWarp can only be performed when the forward velocity field folder is defined.", "warn")
            self.messageSignal.emit("Please ensure this folder is loaded under the 'Load velocity field' tab.", "warn")
            self.processButton.setEnabled(False)
        else:
            self.processButton.setEnabled(True)

    def updateStartFrameValue(self):
        try:
            start_frame = int(self.startingFrameLineEdit.text())
            assert start_frame >= 1
            self.config.start_frame = start_frame-1
            self.startingFrameLineEdit.setStyleSheet(valid_stylesheet)
            return True
        except ValueError:
            self.startingFrameLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Starting frame should be an integer", "error")
            return False
        except AssertionError:
            self.startingFrameLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Starting frame should be a value greater or equal to 1", "error")
            return False

    def onDisplayOutputButtonClicked(self):
        self.imageViewer.displayImage()
        self.imageViewer.setWindowTitle("FlowTracer")
        if self.config.hasInstance():
            self.imageViewer.updateImageViewer(self.config.images)

    def updateImageViewer(self):
        self.imageViewer.updateImageViewer(self.config.images)

    @pyqtSlot(int)
    def updateProgressBar(self, value):
        self.progressBar.setValue(value)

    @pyqtSlot(float)
    def updateTimeLeft(self, value):
        if value > 60:
            self.timeLeft.setText("Time Left: {:.2f} mins".format(value/60))
        else:
            self.timeLeft.setText("Time Left: {:.2f} secs".format(value))

    def onNextButtonClicked(self):
        self.nextSignal.emit()
