from pioneer.common.gui import LeddarUtils, Transforms, Array

from PyQt5.QtCore import QUrl, QTimer, QObject, QVariant, pyqtBoundSignal as BoundSignal
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlProperty, QJSValue, QQmlApplicationEngine, qmlRegisterSingletonType
from PyQt5.QtGui import QGuiApplication, QSurfaceFormat, QVector3D, QVector4D, QMatrix3x3, QMatrix4x4, QQuaternion, QColor, QImage
from PyQt5.QtWidgets import QApplication

import numpy as np
import os
import re
import sys
import warnings

from . import LeddarUtils, Transforms, Array
from PIL import Image

#os.environ['QT_OPENGL'] = "dynamic"
#os.environ['QSG_INFO'] = "1"

QMLDIR = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'qml')

class QmlWrapper(object):
    
    _qml_wrapper_attribs = ['qobject', 'wrappers']
    
    def __init__(self, qobject):
        self.qobject = qobject # add to _qml_wrapper_attribs
        self.wrappers = {}     # add to _qml_wrapper_attribs

    @staticmethod
    def warn_name_clash(qobject, name):
        if QQmlProperty(qobject, name).isValid():
            warnings.warn(f"Name clash detected on object {qobject} for property '{name}', property name exists for both QML and QObject API.")

    def __getattribute__(self, name):
        if name in QmlWrapper._qml_wrapper_attribs:
            value = super().__getattribute__(name)
        else:
            qobject = super().__getattribute__("qobject")
            if hasattr(qobject, name):
                value = getattr(qobject, name)
                QmlWrapper.warn_name_clash(qobject, name)
            else:
                value = QQmlProperty.read(qobject, name)

        if isinstance(value, QJSValue):
            return value.toVariant()

        if isinstance(value, BoundSignal):
            # Workaround for a pqt5 bug where the qmlengine may wait for the first read to property named "name" 
            # to make the auto-generated signal e.g. "nameChanged" active, we thus ensure property named "name"
            # is read at least once 
            match = re.match(r"\d*(\D+)Changed", name)
            if match:
                QQmlProperty.read(qobject, match.group(1)) 

        if isinstance(value, QObject):
            if name == "qobject":
                return super().__getattribute__("qobject")
                
            wrappers = super().__getattribute__("wrappers")
            if name not in wrappers:
                wrappers[name] = QmlWrapper(value)
            return wrappers[name] 

        return value
    def __setattr__(self, name, value):
        if name in QmlWrapper._qml_wrapper_attribs:
            super().__setattr__(name, value)
        elif hasattr(self.qobject, name):
            setattr(self.qobject, name, value)
            QmlWrapper.warn_name_clash(self.qobject, name)
        else:
            self[name] = QVariant(value)

    def __getitem__(self, property_name):
        ''' Useful to force using QQmlProperty.read() in the case of a name clash '''
        return QQmlProperty.read(self.qobject, property_name)

    def __setitem__(self, property_name, value):
        ''' Useful to force using QQmlProperty.write() in the case of a name clash '''
        rv = QQmlProperty.write(self.qobject, property_name, QVariant(value))
        if not rv:
            warnings.warn(f"QQmlProperty.write() on object {self.qobject} at {property_name} failed!")
        return value

class ContextCallback(object):
    ''' This class allows you to add a context to a callback. 
        It was designed to be connected to a Qt signal.
        When the signal is emited, your callback will be called with "self" as argument.
        When called back, "self.signal_args" will contains all arguments passed by the signal
    '''

    def __init__(self, cb = None, signals = []):
        self._callback = cb
        self.connections = []
        self.call_args = None
        for signal in signals:
            self.connect_to(signal)
    
    def callback(self, *args, **kwargs):
        self.signal_args = locals()
        self._callback(self)
    
    def disconnect_all(self):
        for connection in self.connections:
            try:
                QObject.disconnect(connection)
            except:
                pass # Probably a PyQt5 bug. At least we tried...

    def connect_to(self, signal):
        self.connections.append(signal.connect(self.callback))




def add_import_paths(engine, qml_dirs):
    engine.addImportPath(QMLDIR)
    for qml_dir in qml_dirs:
        engine.addImportPath(qml_dir)
    
    def create(engine, script_engine):
        return LeddarUtils.LeddarUtils()

    qmlRegisterSingletonType(LeddarUtils.LeddarUtils, "Leddar", 1, 0, "LeddarUtils", create)

def add_image_providers(engine, img_providers):
    for (name, provider) in img_providers:
        engine.addImageProvider(name, provider)
    
def create_format():
    fmt = QSurfaceFormat()
    fmt.setProfile(QSurfaceFormat.CoreProfile)
    fmt.setVersion(3, 3) #vmware max opengl version is 3.3
    fmt.setAlphaBufferSize(8)
    fmt.setStencilBufferSize(8)
    fmt.setDepthBufferSize(24)
    fmt.setOption(QSurfaceFormat.DebugContext)
    return fmt

def create_qquick_view(script_root, qml_dirs = [], img_providers = []):
    view = QQuickView()
    add_import_paths(view.engine(), qml_dirs)
    add_image_providers(view.engine(), img_providers)
    view.setResizeMode( QQuickView.SizeRootObjectToView )
    view.setSource( QUrl.fromLocalFile(script_root) )
    return view

def create_multi_windows(script_root, qml_dirs = [], img_providers = [], parent = None):
    engine = QQmlApplicationEngine(parent = parent)
    add_import_paths(engine, qml_dirs)
    add_image_providers(engine, img_providers)
    engine.load(script_root)
    return engine

def try_to_complete_path(script, qml_dirs = []):
    
    qml_dirs.append(QMLDIR)

    if os.path.isfile(script):
        return script

    for d in qml_dirs:
        path = os.path.join(d, script)
        
        if os.path.isfile(path):
            return path

    raise FileNotFoundError(script)



def qt_qml_opengl(multi_windows_script = '', qml_dirs = [], img_providers = []):
    # Create the application instance.
    # app = QGuiApplication(sys.argv) --> CRASH
    app = QApplication(sys.argv)
    
    #https://machinekoder.com/how-to-not-shoot-yourself-in-the-foot-using-python-qt/
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)

    # app = QApplication(sys.argv)
    QSurfaceFormat.setDefaultFormat(create_format())

    if multi_windows_script:
        engine = create_multi_windows(try_to_complete_path(multi_windows_script, qml_dirs), qml_dirs, img_providers, app)
        view = engine.rootObjects()[0]
    else:
        view = create_qquick_view(os.path.join(QMLDIR, "root.qml"), qml_dirs, img_providers)

    view.show()

    exit(app.exec_())

def QImage_to_numpy(qimage):
    '''  
        Converts a QImage into an opencv MAT format
        https://stackoverflow.com/questions/19902183/qimage-to-numpy-array-using-pyside  
    '''

    qimage = qimage.convertToFormat(QImage.Format.Format_RGBA8888)

    width = qimage.width()
    height = qimage.height()

    ptr = qimage.constBits()
    ptr.setsize(height * width * 4)
    arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))

    # ptr = qimage.constBits()
    # arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    return arr


def tf(tx, ty, tz, angle_deg=0, vx=1, vy=0, vz=0):
    m = QMatrix4x4()
    m.translate(tx, ty, tz)
    if isinstance(angle_deg, QQuaternion):
        m.rotate(angle_deg)
    else:
        if isinstance(vx, QVector3D):
            vy = vx.y()
            vz = vx.z()
            vx = vx.x()
            
        m.rotate(angle_deg, vx, vy, vz)
    return m

def from_numpy(v):
    if v.size == 3:
        return QVector3D(v[0], v[1], v[2])
    if v.size == 4:
        return QVector4D(v[0], v[1], v[2], v[3])
    if v.shape == (3,3):
        return QMatrix3x3(v.flatten().tolist())

    if v.shape == (4,4):
        return QMatrix4x4(v.flatten().tolist())



def to_numpy(v, dtype = np.float32):

    if isinstance(v, (list, tuple)):
        return np.array(v, dtype)

    if isinstance(v, QColor):
        return np.array([v.redF(), v.greenF(), v.blueF(), v.alphaF()], dtype)

    if isinstance(v, QVector3D):
        return np.array([v[i] for i in range(3)], dtype)
    if isinstance(v, QVector4D):
        return np.array([v[i] for i in range(4)], dtype)
    if isinstance(v, QMatrix3x3):
        return np.array(    [[v[0,0], v[0,1], v[0,2]]
                            ,[v[1,0], v[1,1], v[1,2]]
                            ,[v[2,0], v[2,1], v[2,2]]], dtype)

    if isinstance(v, QMatrix4x4):
        return np.array(    [[v[0,0], v[0,1], v[0,2], v[0,3]]
                            ,[v[1,0], v[1,1], v[1,2], v[1,3]]
                            ,[v[2,0], v[2,1], v[2,2], v[2,3]]
                            ,[v[3,0], v[3,1], v[3,2], v[3,3]]], dtype)
    if isinstance(v, Transforms.Transform):
        return to_numpy(v.worldTransform(True))

    return v


def tf_to_numpy(transform):
    if transform:
        return to_numpy(transform)
    else:
        return np.eye(4, dtype = 'f4')

def unpack_floats(ndarray_4_uint8):
    '''
        Meant to be used along with CustomEffects.depth()
    '''
    scale = np.array([1.0/(256**3), 1.0/(256**2), 1.0/256, 1.0], np.float32)
    return np.dot(ndarray_4_uint8[...,:], scale)

def load_texture(path_or_Image, tile = (1,1)):
    ''' Loads a texture in RGBA format, using an OpenGL-ready memory layout
        Note: if you want to display that array using pyplot, fix it with texture_to_MxN()
    '''
    if isinstance(path_or_Image, str):
        path_or_Image = Image.open(path_or_Image)

    mode = path_or_Image.mode
    if mode == 'RGBA':
        export_mode = 'RGBA'
    elif path_or_Image.mode == 'RGB':
        export_mode = 'RGBX'
    else:
        raise RuntimeError('unsupported PIL mode')
    
    ndarray = np.frombuffer(path_or_Image.tobytes('raw', export_mode, 0, -1), 'u1').reshape(path_or_Image.size[1], path_or_Image.size[0], 4)
    return np.tile(ndarray, tuple(tile) + (1,)).reshape(ndarray.shape[1] * tile[0], ndarray.shape[0] * tile[1], ndarray.shape[2])

def texture_to_MxN(ndarray):
    if len(ndarray.shape) == 3:
        return np.flipud(ndarray.reshape(ndarray.shape[1], ndarray.shape[0], ndarray.shape[2]))
    return ndarray

