from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from functools import wraps
import traceback
import os

from skippy import utils.logger
from skippy import utils.decorator
from skippy import config


@utils.decorator.decorator
def critical(call):
    try:
        call()
    except Exception as e:
        utils.logger.log.error(e, exc_info=True)
        dialog = QMessageBox()
        dialog.setWindowTitle(f"Error: {str(e)}")
        dialog.setWindowIcon(QIcon(os.path.join(config.ASSETS_FOLDER, "skippy.ico")))
        dialog.setText(traceback.format_exc())
        dialog.setIcon(QMessageBox.Critical)
        dialog.exec_()
