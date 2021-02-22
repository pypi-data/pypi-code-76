'''_1124.py

Vector2DPolar
'''


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_VECTOR_2D_POLAR = python_net_import('SMT.MastaAPI.MathUtility.MeasuredVectors', 'Vector2DPolar')


__docformat__ = 'restructuredtext en'
__all__ = ('Vector2DPolar',)


class Vector2DPolar(_0.APIBase):
    '''Vector2DPolar

    This is a mastapy class.
    '''

    TYPE = _VECTOR_2D_POLAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Vector2DPolar.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def radius(self) -> 'float':
        '''float: 'Radius' is the original name of this property.'''

        return self.wrapped.Radius

    @radius.setter
    def radius(self, value: 'float'):
        self.wrapped.Radius = float(value) if value else 0.0

    @property
    def theta(self) -> 'float':
        '''float: 'Theta' is the original name of this property.'''

        return self.wrapped.Theta

    @theta.setter
    def theta(self, value: 'float'):
        self.wrapped.Theta = float(value) if value else 0.0

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
