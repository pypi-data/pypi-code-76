from pioneer.common.gui import Product

from PyQt5.QtCore import pyqtProperty as Property, pyqtSignal as Signal, pyqtSlot as Slot, Q_CLASSINFO
from PyQt5.QtGui import QMatrix4x4, QVector3D, QQuaternion

import math

class Transform( Product.Product ):

    def __init__( self, parent = None ):
        super(Transform, self).__init__( parent )
        self._localTransform = QMatrix4x4()
        self._parentTransform = None

    Q_CLASSINFO('DefaultProperty', 'parentTransform')

    localTransformChanged = Signal()

    def local_transform(self):
        return self._localTransform

    localTransform = Property(QMatrix4x4, local_transform, notify = localTransformChanged)

    def set_local_transform(self, matrix4x4):
        if matrix4x4 is None:
            matrix4x4 = QMatrix4x4()
        Product.assign_input(self, "localTransform", matrix4x4)

    Product.InputProperty(vars(), Product.Product, 'parentTransform')


    @Slot(result = QMatrix4x4)
    def worldTransform(self, update = False):
        if update:
            self.update()
        assert not self.dirty
        return self.localTransform if self.parentTransform is None \
               else self.parentTransform.worldTransform() * self.localTransform

    @Slot(QVector3D, float, result = QQuaternion)
    def qFromAA(self, axis, angle_rad):
        return QQuaternion.fromAxisAndAngle(axis, math.degrees(angle_rad))

    @Slot(float, float, float, result = QQuaternion)
    def qFromEuler(self, roll, pitch, yaw):
        return QQuaternion.fromEulerAngles(math.degrees(roll), math.degrees(pitch), math.degrees(yaw))

    @Slot(QQuaternion, QVector3D, result = QMatrix4x4)
    def mFromTQ(self, t = QVector3D(), q = QQuaternion()):
        m = QMatrix4x4()
        m.rotate(q)
        m.translate(t)
        return m

class Translation( Transform ):

    def __init__( self, parent = None ):
        super(Translation, self).__init__( parent )
        self._translate = QVector3D()


    def translate_cb(self):
        m = QMatrix4x4()
        m.translate(self._translate)
        self.set_local_transform(m)

    Product.InputProperty(vars(), QVector3D, 'translate', translate_cb)

class Rotation( Transform ):

    def __init__( self, parent = None ):
        super(Rotation, self).__init__( parent )
        self._quaternion = QQuaternion()


    def quaternion_cb(self):
        m = QMatrix4x4()
        m.rotate(self._quaternion)
        self.set_local_transform(m)

    Product.InputProperty(vars(), QQuaternion, 'quaternion', quaternion_cb)

class MatrixTransform( Transform ):

    def __init__( self, parent = None, matrix = QMatrix4x4() ):
        super(MatrixTransform, self).__init__( parent )
        self._matrix = None

        self.matrix = matrix

    def matrix_cb(self):
        self.set_local_transform(self._matrix)

    Product.InputProperty(vars(), QMatrix4x4, 'matrix', matrix_cb)


