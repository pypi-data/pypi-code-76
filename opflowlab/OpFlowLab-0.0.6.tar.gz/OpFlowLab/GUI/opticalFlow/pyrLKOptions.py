import re
import numpy as np

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt


class pyrLKOptions(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.optionsGroup = QGroupBox("Options")
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)

        self.numLevelsLabel = QLabel("Num pyramidal levels")
        self.optionsLayout.addWidget(self.numLevelsLabel, 0, 0)
        self.levelsLineEdit = QLineEdit("5")
        self.levelsLineEdit.setPlaceholderText("Num pyramidal levels")
        self.optionsLayout.addWidget(self.levelsLineEdit, 1, 0)

        self.windowSizeLabel = QLabel("Window size")
        self.optionsLayout.addWidget(self.windowSizeLabel, 0, 1)
        self.windowSizeLineEdit = QLineEdit("21")
        self.windowSizeLineEdit.setPlaceholderText("Window size")
        self.optionsLayout.addWidget(self.windowSizeLineEdit, 1, 1)

        self.iterationsLabel = QLabel("Num of iterations")
        self.optionsLayout.addWidget(self.iterationsLabel, 2, 0)
        self.iterationsLineEdit = QLineEdit("30")
        self.iterationsLineEdit.setPlaceholderText("Number of iterations")
        self.optionsLayout.addWidget(self.iterationsLineEdit, 3, 0)

        self.halfPrecisionCheckBox = QCheckBox("Use float16 for outputs")
        self.halfPrecisionCheckBox.setChecked(True)
        self.optionsLayout.addWidget(self.halfPrecisionCheckBox, 2, 1)

        self.reverseCheckBox = QCheckBox("Reverse time direction")
        self.optionsLayout.addWidget(self.reverseCheckBox, 3, 1)

        self.tiffCheckBox = QCheckBox("Save velocity components as tiff file")
        self.optionsLayout.addWidget(self.tiffCheckBox, 4, 1)

        self.optionsGroup.setLayout(self.optionsLayout)
        self.layout.addWidget(self.optionsGroup)

    def prepParameters(self, text, type):
        parameter = re.split('[:,-]', text)
        parameter = [type(x) for x in parameter]

        if len(parameter) == 1:
            return parameter
        else:
            return np.arange(*parameter).tolist()

    def getParameters(self):
        numLevels = self.prepParameters(self.levelsLineEdit.text(), int)
        windowSize = self.prepParameters(self.windowSizeLineEdit.text(), int)
        iterations = self.prepParameters(self.iterationsLineEdit.text(), int)

        halfPrecision = self.halfPrecisionCheckBox.isChecked()
        isReverse = self.reverseCheckBox.isChecked()
        save_as_tif = self.tiffCheckBox.isChecked()

        return numLevels, isReverse, windowSize, iterations, halfPrecision, save_as_tif

    def getCommand(self, processPath, imagePath, opticalFlowType):
        processPath = processPath.replace('\\', '/')
        numLevels, isReverse, windowSize, iterations, halfPrecision, save_as_tif = self.getParameters()

        command = []
        for _windowSize in windowSize:
            for _numLevels in numLevels:
                for _iterations in iterations:
                    command.append("\"{}\" {} ".format(processPath, opticalFlowType)
                                   + "--winSize={} ".format(_windowSize)
                                   + "--numLevels={} ".format(_numLevels)
                                   + "--numIters={} ".format(_iterations)
                                   + "{}".format("--use_half_precision " if halfPrecision is True else "")
                                   + "{}".format("--is_reverse " if isReverse is True else "")
                                   + "{}".format("--save_as_img " if save_as_tif is True else "")
                                   + "\"{}\"".format(imagePath))

        param_dict = {"imagePath": imagePath,
                      "type": opticalFlowType,
                      "winSize": windowSize,
                      "numLevels": numLevels,
                      "numIters": iterations,
                      "halfPrecision": halfPrecision,
                      "is_reverse": isReverse,
                      "save_as_tif": save_as_tif
                      }

        return command, param_dict