'''_1533.py

Vector4D
'''


from mastapy._internal import constructor
from mastapy.math_utility import _1525
from mastapy._internal.python_net import python_net_import

_VECTOR_4D = python_net_import('SMT.MastaAPI.MathUtility', 'Vector4D')


__docformat__ = 'restructuredtext en'
__all__ = ('Vector4D',)


class Vector4D(_1525.RealVector):
    '''Vector4D

    This is a mastapy class.
    '''

    TYPE = _VECTOR_4D

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Vector4D.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def x(self) -> 'float':
        '''float: 'X' is the original name of this property.'''

        return self.wrapped.X

    @x.setter
    def x(self, value: 'float'):
        self.wrapped.X = float(value) if value else 0.0

    @property
    def y(self) -> 'float':
        '''float: 'Y' is the original name of this property.'''

        return self.wrapped.Y

    @y.setter
    def y(self, value: 'float'):
        self.wrapped.Y = float(value) if value else 0.0

    @property
    def z(self) -> 'float':
        '''float: 'Z' is the original name of this property.'''

        return self.wrapped.Z

    @z.setter
    def z(self, value: 'float'):
        self.wrapped.Z = float(value) if value else 0.0
