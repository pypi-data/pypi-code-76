'''_1559.py

SupportDetail
'''


from mastapy._internal import constructor
from mastapy.bearings.tolerances import _1548
from mastapy._internal.python_net import python_net_import

_SUPPORT_DETAIL = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'SupportDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('SupportDetail',)


class SupportDetail(_1548.InterferenceDetail):
    '''SupportDetail

    This is a mastapy class.
    '''

    TYPE = _SUPPORT_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SupportDetail.TYPE'):
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

    @property
    def theta_x(self) -> 'float':
        '''float: 'ThetaX' is the original name of this property.'''

        return self.wrapped.ThetaX

    @theta_x.setter
    def theta_x(self, value: 'float'):
        self.wrapped.ThetaX = float(value) if value else 0.0

    @property
    def theta_y(self) -> 'float':
        '''float: 'ThetaY' is the original name of this property.'''

        return self.wrapped.ThetaY

    @theta_y.setter
    def theta_y(self, value: 'float'):
        self.wrapped.ThetaY = float(value) if value else 0.0

    @property
    def radial_error_magnitude(self) -> 'float':
        '''float: 'RadialErrorMagnitude' is the original name of this property.'''

        return self.wrapped.RadialErrorMagnitude

    @radial_error_magnitude.setter
    def radial_error_magnitude(self, value: 'float'):
        self.wrapped.RadialErrorMagnitude = float(value) if value else 0.0

    @property
    def angle_of_radial_error(self) -> 'float':
        '''float: 'AngleOfRadialError' is the original name of this property.'''

        return self.wrapped.AngleOfRadialError

    @angle_of_radial_error.setter
    def angle_of_radial_error(self, value: 'float'):
        self.wrapped.AngleOfRadialError = float(value) if value else 0.0
