import re
import numpy as np

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt


class broxOptions(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.optionsGroup = QGroupBox("Options")
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)

        self.alphaLabel = QLabel("Smoothness parameter (alpha)")
        self.optionsLayout.addWidget(self.alphaLabel, 0, 0)
        self.alphaLineEdit = QLineEdit("0.197")
        self.alphaLineEdit.setPlaceholderText("Smoothness parameter (alpha)")
        self.optionsLayout.addWidget(self.alphaLineEdit, 1, 0)

        self.gammaLabel = QLabel("Gradient constancy importance parameter (gamma)")
        self.optionsLayout.addWidget(self.gammaLabel, 0, 1)
        self.gammaLineEdit = QLineEdit("50")
        self.gammaLineEdit.setPlaceholderText("Gradient constancy importance parameter (gamma)")
        self.optionsLayout.addWidget(self.gammaLineEdit, 1, 1)

        self.innerLabel = QLabel("Num of inner iterations")
        self.optionsLayout.addWidget(self.innerLabel, 2, 0)
        self.innerLineEdit = QLineEdit("5")
        self.innerLineEdit.setPlaceholderText("Num of inner iterations")
        self.optionsLayout.addWidget(self.innerLineEdit, 3, 0)

        self.outerLabel = QLabel("Num of outer iterations")
        self.optionsLayout.addWidget(self.outerLabel, 2, 1)
        self.outerLineEdit = QLineEdit("150")
        self.outerLineEdit.setPlaceholderText("Num of outer iterations")
        self.optionsLayout.addWidget(self.outerLineEdit, 3, 1)

        self.solverLabel = QLabel("Num of solver iterations")
        self.optionsLayout.addWidget(self.solverLabel, 4, 0)
        self.solverLineEdit = QLineEdit("5")
        self.solverLineEdit.setPlaceholderText("Num of solver iterations")
        self.optionsLayout.addWidget(self.solverLineEdit, 5, 0)

        self.scaleLabel = QLabel("Pyramidal scale factor")
        self.optionsLayout.addWidget(self.scaleLabel, 6, 0)
        self.scaleLineEdit = QLineEdit("0.5")
        self.scaleLineEdit.setPlaceholderText("Pyramidal scale factor")
        self.optionsLayout.addWidget(self.scaleLineEdit, 7, 0)

        self.halfPrecisionCheckBox = QCheckBox("Use float16 for outputs")
        self.halfPrecisionCheckBox.setChecked(True)
        self.optionsLayout.addWidget(self.halfPrecisionCheckBox, 4, 1)

        self.reverseCheckBox = QCheckBox("Reverse time direction")
        self.optionsLayout.addWidget(self.reverseCheckBox, 5, 1)

        self.tiffCheckBox = QCheckBox("Save velocity components as tiff file")
        self.optionsLayout.addWidget(self.tiffCheckBox, 6, 1)

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
        alpha = self.prepParameters(self.alphaLineEdit.text(), float)
        gamma = self.prepParameters(self.gammaLineEdit.text(), float)
        inner = self.prepParameters(self.innerLineEdit.text(), int)

        outer = self.prepParameters(self.outerLineEdit.text(), int)
        solver = self.prepParameters(self.solverLineEdit.text(), int)
        scale = self.prepParameters(self.scaleLineEdit.text(), float)

        halfPrecision = self.halfPrecisionCheckBox.isChecked()
        isReverse = self.reverseCheckBox.isChecked()
        save_as_tif = self.tiffCheckBox.isChecked()

        return alpha, gamma, inner, outer, solver, scale, isReverse, halfPrecision, save_as_tif

    def getCommand(self, processPath, imagePath, opticalFlowType):
        processPath = processPath.replace('\\', '/')
        alpha, gamma, inner, outer, solver, scale, isReverse, halfPrecision, save_as_tif = self.getParameters()

        command = []
        for _alpha in alpha:
            for _gamma in gamma:
                for _inner in inner:
                    for _outer in outer:
                        for _solver in solver:
                            for _scale in scale:
                                command.append("\"{}\" {} ".format(processPath, opticalFlowType)
                                               + "--alpha={} ".format(_alpha)
                                               + "--gamma={} ".format(_gamma)
                                               + "--innerIter={} ".format(_inner)
                                               + "--outerIter={} ".format(_outer)
                                               + "--solverIter={} ".format(_solver)
                                               + "--pyrScale={} ".format(_scale)
                                               + "{}".format("--use_half_precision " if halfPrecision is True else "")
                                               + "{}".format("--is_reverse " if isReverse is True else "")
                                               + "{}".format("--save_as_img " if save_as_tif is True else "")
                                               + "\"{}\"".format(imagePath))

        param_dict = {"imagePath": imagePath,
                      "type": opticalFlowType,
                      "alpha": alpha,
                      "numLevels": gamma,
                      "innerIter": inner,
                      "outerIter": outer,
                      "solverIter": solver,
                      "pyrScale": scale,
                      "halfPrecision": halfPrecision,
                      "is_reverse": isReverse,
                      "save_as_tif": save_as_tif
                      }

        return command, param_dict