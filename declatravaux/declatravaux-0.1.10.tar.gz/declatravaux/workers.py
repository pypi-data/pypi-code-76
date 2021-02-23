import time

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from declatravaux.transmission_process import TransmissionProcess
from declatravaux.archives import Declaration


class TransmissionWorker(QObject):

    step_signal = pyqtSignal(int, str, int)

    @pyqtSlot(Declaration, bool)
    def run(self, declaration, fake_emailing):
        for step_num, step_text, step_add in TransmissionProcess(declaration=declaration,
                                                                 fake_emailing=fake_emailing):
            self.step_signal.emit(step_num, step_text, step_add)


class ProgressWorker(QObject):

    progress_signal = pyqtSignal()

    @pyqtSlot()
    def run(self):
        while True:
            self.progress_signal.emit()
            time.sleep(1)
