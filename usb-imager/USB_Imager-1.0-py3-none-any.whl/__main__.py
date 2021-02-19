#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__main__"""

import os
import sys
from PySide2.QtCore import QCoreApplication, Qt
from PySide2.QtWidgets import QApplication, QMessageBox

try:
    import appinfo
    from gui_qt import Application
    from modules.udisks2 import UDisks2
except ImportError:
    # Works for pip installation
    from usb_imager import appinfo
    from usb_imager.gui_qt import Application
    from usb_imager.modules.udisks2 import UDisks2


def _check_deps() -> None:
    is_gui = bool(os.getenv('DESKTOP_SESSION'))
    # Check for platform 'linux'
    if not sys.platform.startswith('linux'):
        if is_gui:
            message = "Programm only supports Unix!"
            QMessageBox.critical(None, "Failure", message)
        sys.exit(message)

    # Check for installed UDisks2/D-Bus
    if not UDisks2.has_udisks2():
        if is_gui:
            message = "UDisks2 was not found!"
            QMessageBox.critical(None, "Failure", message)
        sys.exit(message)


def main() -> int:
    """Start application"""

    app_name = f'{appinfo.__appname__} - Version {appinfo.__version__}'

    # Suppress some Qt logging messages when using QFileDialog
    os.environ["QT_LOGGING_RULES"] = "qt.qpa.*=false;kf.kio.*=false"

    # Build application
    app = QApplication.instance()
    if app is None:
        # Application settings
        QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

        # print(QStyleFactory.keys())
        # QApplication.setStyle('Fusion')

        QCoreApplication.setApplicationName(app_name)
        # For screenshots
        # QCoreApplication.setApplicationName(appinfo.__appname__)
        QCoreApplication.setApplicationVersion(appinfo.__version__)
        QCoreApplication.setOrganizationName(appinfo.__organisation__)
        QCoreApplication.setOrganizationDomain(appinfo.__domain__)

        app = Application(sys.argv)

    # Check dependencies
    _check_deps()

    # Execute application
    app.show_mainwindow()

    return app.exec_()


if __name__ == "__main__":
    main()
