"""Application module.

For more information on the underlying Qt5 objects see
[QCoreApplication](https://doc.qt.io/qt-5/qcoreapplication.html),
[QGuiApplication](https://doc.qt.io/qt-5/qguiapplication.html) and
[QApplication](https://doc.qt.io/qt-5/qapplication.html).
"""

import signal
import sys

from .qutie import QtCore
from .qutie import QtGui
from .qutie import QtWidgets

from .icon import Icon
from .object import Object

__all__ = ['CoreApplication', 'GuiApplication', 'Application']

class CoreApplication(Object):
    """CoreApplication

    Properties
     - name
     - version
     - organization
     - domain

    Callbacks
     - name_changed(name)
     - version_changed(version)
     - organization_changed(organization)
     - domain_changed(name)
    """

    QtClass = QtCore.QCoreApplication

    name_changed = None
    version_changed = None
    organization_changed = None
    domain_changed = None

    def __init__(self, name=None, *, version=None, organization=None,
                 domain=None, name_changed=None, version_changed=None,
                 organization_changed=None, domain_changed=None, **kwargs):
        super().__init__(qt=(sys.argv,), **kwargs)
        # Properties
        if name is not None:
            self.name = name
        if version is not None:
            self.version = version
        if organization is not None:
            self.organization = organization
        if domain is not None:
            self.domain = domain
        # Callbacks
        self.name_changed = name_changed
        self.version_changed = version_changed
        self.organization_changed = organization_changed
        self.domain_changed = domain_changed
        # Connect signals
        self.qt.applicationNameChanged.connect(lambda: self.emit(self.name_changed, self.name))
        self.qt.applicationVersionChanged.connect(lambda: self.emit(self.version_changed, self.version))
        self.qt.organizationNameChanged.connect(lambda: self.emit(self.organization_changed, self.organization))
        self.qt.organizationDomainChanged.connect(lambda: self.emit(self.domain_changed, self.domain))

    @classmethod
    def instance(cls):
        if cls.QtClass.instance() is not None:
            return cls.QtClass.instance().reflection()
        return None

    @property
    def name(self) -> str:
        return self.qt.applicationName()

    @name.setter
    def name(self, value: str):
        self.qt.setApplicationName(value)

    @property
    def version(self) -> str:
        return self.qt.applicationVersion()

    @version.setter
    def version(self, value: str):
        self.qt.setApplicationVersion(value)

    @property
    def organization(self) -> str:
        return self.qt.organizationName()

    @organization.setter
    def organization(self, value: str):
        self.qt.setOrganizationName(value)

    @property
    def domain(self) -> str:
        return self.qt.organizationDomain()

    @domain.setter
    def domain(self, value: str):
        self.qt.setOrganizationDomain(value)

    def run(self):
        # Register interupt signal handler
        def signal_handler(signum, frame):
            if signum == signal.SIGINT:
                self.quit()
        signal.signal(signal.SIGINT, signal_handler)

        # Run timer to process interrupt signals
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(250)

        return self.qt.exec_()

    def quit(self):
        self.qt.quit()

class GuiApplication(CoreApplication):
    """GuiApplication

    Properties
     - display_name
     - icon

    Callbacks
     - display_name_changed(display_name)
     - last_window_closed()
    """

    QtClass = QtGui.QGuiApplication

    display_name_changed = None
    last_window_closed = None

    def __init__(self, name=None, *, display_name=None, icon=None,
                 display_name_changed=None, last_window_closed=None, **kwargs):
        super().__init__(name=name, **kwargs)
        # Properties
        if display_name is not None:
            self.display_name = display_name
        if icon is not None:
            self.icon = icon
        # Callbacks
        self.display_name_changed = display_name_changed
        self.last_window_closed = last_window_closed
        # Connect signals
        self.qt.applicationDisplayNameChanged.connect(lambda: self.emit(self.display_name_changed, self.display_name))
        self.qt.lastWindowClosed.connect(lambda: self.emit(self.last_window_closed))

    @property
    def display_name(self) -> str:
        return self.qt.applicationDisplayName()

    @display_name.setter
    def display_name(self, value: str):
        self.qt.setApplicationDisplayName(value)

    @property
    def icon(self):
        icon = self.qt.windowIcon()
        if icon.isNull():
            return None
        return Icon(qt=icon)

    @icon.setter
    def icon(self, value):
        if value is None:
            self.qt.setWindowIcon(QtGui.QIcon())
        else:
            if not isinstance(value, Icon):
                value = Icon(value)
            self.qt.setWindowIcon(value.qt)

class Application(GuiApplication):
    """Application

    Callbacks
     - focus_changed()
    """

    QtClass = QtWidgets.QApplication

    focus_changed = None

    def __init__(self, name=None, *, focus_changed=None, **kwargs):
        super().__init__(name=name, **kwargs)
        # Callbacks
        self.focus_changed = focus_changed
        # Connect signals
        self.qt.focusChanged.connect(lambda old, now: self.emit(self.focus_changed, old, now))

    def quit(self):
        """Request quit application by closing all windows."""
        self.qt.closeAllWindows()
