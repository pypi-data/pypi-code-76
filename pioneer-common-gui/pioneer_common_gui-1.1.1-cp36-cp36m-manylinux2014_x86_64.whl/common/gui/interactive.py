from pioneer.common.gui import utils

from PyQt5.QtCore import QVariant, QTimer
from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtQml import QQmlProperty
from PyQt5.QtWidgets import QApplication

import os
import sys
import time
import traceback

class InteractiveHelper(object):
    '''
        Helper to create interactive calls to perception's gui subsystem from a script.
    '''
    def __init__(self, script, qml_dirs = [], img_providers = []):
        '''
            script is assumed to contain a 'key' property which is updated on Keys.onPressed events.
            script's API is assumed to be its root level properties
        '''
        self.app = QApplication(sys.argv)
        ## This remove the following warning at the started of the viewer : QML Settings: The following application identifiers have not been set: QVector("organizationName", "organizationDomain")
        self.app.setOrganizationName("Leddartech")
        self.app.setOrganizationDomain("Advanced_Engineering")
        # https://machinekoder.com/how-to-not-shoot-yourself-in-the-foot-using-python-qt/
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: None)
        self.timer.start(100)
        QSurfaceFormat.setDefaultFormat(utils.create_format())
        self.engine = None
        self.root = None
        self.view = None
        if script:
            self.create_view(script, qml_dirs, img_providers)

    def create_view(self, script, qml_dirs, img_providers = []):
        if self.engine:
            self.view.hide()

        self.view = utils.create_qquick_view(script, qml_dirs, img_providers)
        self.engine = self.view.engine()
        self.root = self.view.rootObject()
    
    @property
    def root(self):
        return self._root.qobject if self._root else None
    
    @root.setter
    def root(self, qobject):
        self._root = utils.QmlWrapper(qobject) if qobject else None
    
    def root_wrapper(self):
        return self._root

    def _check_view(self):
        if self.view is None or self.engine is None:
            raise RuntimeError('you must call create_view() first')

    def set_args(self, **kwargs):
        self._check_view()
        for k,v in kwargs.items():
            self.write_property(k, v)

    def write_property(self, name:str, v):
        self._check_view()
        return QQmlProperty.write(self.root, name, QVariant(v), self.engine)

    def read_property(self, name:str):
        self._check_view()
        return QQmlProperty.read(self.root, name, self.engine)

    def hide(self):
        if self.view:
            self.view.hide()

    def show(self):
        self._check_view()
        if self.view is not None:
            self.view.show()

    def run(self):
        self.show()
        sys.exit(self.app.exec_())

    def wait_key(self, wait_key = None):
        self.show()
        while True:
            try:
                time.sleep(0.01)
                QApplication.processEvents()
                key = self.read_property("key")
                self.write_property("key", '')
                if wait_key is None and key != '':
                    break
                if key == wait_key:
                    break
            except :
                print(traceback.format_exc())
    
    def get_keypress(self, wait_key = None):
        self.show()
       
        try:
            QApplication.processEvents()
            key = self.read_property("key")
            return key
        except :
            print(traceback.format_exc())

class MultiWindowsInteraciveHelper(InteractiveHelper):

    def __init__(self, script, qml_dirs, img_providers = []):
        '''
            script is assumed to contain a 'key' property which is updated on Keys.onPressed events.
            script's API is assumed to be its root level properties
        '''
        super(MultiWindowsInteraciveHelper, self).__init__(script, qml_dirs, img_providers)

    def create_view(self, script, qml_dirs, img_providers = []):
        self.engine = utils.create_multi_windows(script, qml_dirs, img_providers)
        self.root = self.view = self.engine.rootObjects()[0]



def multi_windows_vp(script, qml_dirs, img_providers, **kwargs):
    vp = MultiWindowsInteraciveHelper(utils.try_to_complete_path(script, qml_dirs), qml_dirs, img_providers)
    vp.set_args(**kwargs)
    vp.show()
    vp.hide()
    return vp


def leddar_vp(script = "root_LeddarVP.qml", qml_dirs = [], img_providers = [], **kwargs):
    '''
        Shortcut for creation, set_arg and show for a InteractiveHelper with root_LeddarVP.qml script
    '''
    vp = InteractiveHelper(utils.try_to_complete_path(script, qml_dirs))
    vp.set_args(**kwargs)
    vp.show()
    vp.hide()
    return vp

def point_cloud(**kwargs):
    '''
        Shortcut for creation, set_arg and show for a InteractiveHelper with root_PointCloud.qml script
    '''
    pc = InteractiveHelper(utils.try_to_complete_path("root_PointCloud.qml"))
    pc.set_args(**kwargs)
    vp.show()
    vp.hide()
    return pc

