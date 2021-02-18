from typing import Union
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout



class ErrorDialog(QDialog):

    def __init__(self, *args, name= "ERROR", explanation=None, **kwargs):
        super(ErrorDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle(name)

        buttons = QDialogButtonBox.Ok 

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        if explanation: self.layout.addWidget(QLabel(explanation))
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    @classmethod
    def alert(cls, error: Union[Exception,str], explanation = None):
        instance = cls(name=str(error), explanation= explanation or str(error))
        return instance.exec_()



