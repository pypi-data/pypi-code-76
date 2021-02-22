'''_2149.py

RigidConnectorToothLocation
'''


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_RIGID_CONNECTOR_TOOTH_LOCATION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RigidConnectorToothLocation')


__docformat__ = 'restructuredtext en'
__all__ = ('RigidConnectorToothLocation',)


class RigidConnectorToothLocation(_0.APIBase):
    '''RigidConnectorToothLocation

    This is a mastapy class.
    '''

    TYPE = _RIGID_CONNECTOR_TOOTH_LOCATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RigidConnectorToothLocation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def start_angle(self) -> 'float':
        '''float: 'StartAngle' is the original name of this property.'''

        return self.wrapped.StartAngle

    @start_angle.setter
    def start_angle(self, value: 'float'):
        self.wrapped.StartAngle = float(value) if value else 0.0

    @property
    def end_angle(self) -> 'float':
        '''float: 'EndAngle' is the original name of this property.'''

        return self.wrapped.EndAngle

    @end_angle.setter
    def end_angle(self, value: 'float'):
        self.wrapped.EndAngle = float(value) if value else 0.0

    @property
    def centre_angle(self) -> 'float':
        '''float: 'CentreAngle' is the original name of this property.'''

        return self.wrapped.CentreAngle

    @centre_angle.setter
    def centre_angle(self, value: 'float'):
        self.wrapped.CentreAngle = float(value) if value else 0.0

    @property
    def extent(self) -> 'float':
        '''float: 'Extent' is the original name of this property.'''

        return self.wrapped.Extent

    @extent.setter
    def extent(self, value: 'float'):
        self.wrapped.Extent = float(value) if value else 0.0
