from PyQt5.QtWidgets import QDialog

from qalx_orcaflex.gui.batch.requeue_jobs_dialog_ui import Ui_RequeueDialog


class ReQueueDialog(QDialog, Ui_RequeueDialog):
    """Custom dialog that can be used to confirm job requeue"""

    def __init__(self, parent=None, queue_name="", warn_states=None):
        super().__init__(parent)
        self.setupUi(self)
        self.queue_name = queue_name
        self.warn_states = warn_states
        self.should_requeue = False
        self._initialise_ui()
        self.buttonBox.accepted.connect(self.requeue_confirm)
        self.buttonBox.rejected.connect(self.requeue_cancel)
        self.exec_()

    @staticmethod
    def html_warn(txt, s):
        return f"<P><b><font color='#ff0000' font_size={s}>{txt}</font></b></P>"

    @staticmethod
    def html_li(txt):
        return f"<li>{txt}</li>"

    def _initialise_ui(self):
        """
        Customises the text box font and the window title. When there are job
        states to warn about, these will be highlighted in red bold font
        """
        self.queueNameEdit.setText(self.queue_name)
        if self.warn_states:
            s = self.textBrowser.font().pointSize() + 2
            text = (
                f"{self.html_warn('WARNING', s)}"
                + "There are selected jobs with the following "
                + "states:<ul>{}</ul>Requeue such jobs with caution. "
                + "Click OK to proceed."
            ).format(
                "".join((self.html_li(self.html_warn(_, s)) for _ in self.warn_states))
            )
        else:
            text = "Click OK to proceed."
        self.textBrowser.setText(text)
        self.setWindowTitle("Requeue Jobs")

    def requeue_confirm(self):
        self.should_requeue = True
        self.queue_name = self.queueNameEdit.text()
        self.close()

    def requeue_cancel(self):
        self.should_requeue = False
        self.close()
