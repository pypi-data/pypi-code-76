'''_1868.py

PlanetarySocket
'''


from mastapy._internal import constructor
from mastapy.gears import _140
from mastapy.system_model.connections_and_sockets import _1859
from mastapy._internal.python_net import python_net_import

_PLANETARY_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'PlanetarySocket')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetarySocket',)


class PlanetarySocket(_1859.CylindricalSocket):
    '''PlanetarySocket

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetarySocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def draw_on_upper_half_of_2d(self) -> 'bool':
        '''bool: 'DrawOnUpperHalfOf2D' is the original name of this property.'''

        return self.wrapped.DrawOnUpperHalfOf2D

    @draw_on_upper_half_of_2d.setter
    def draw_on_upper_half_of_2d(self, value: 'bool'):
        self.wrapped.DrawOnUpperHalfOf2D = bool(value) if value else False

    @property
    def draw_on_lower_half_of_2d(self) -> 'bool':
        '''bool: 'DrawOnLowerHalfOf2D' is the original name of this property.'''

        return self.wrapped.DrawOnLowerHalfOf2D

    @draw_on_lower_half_of_2d.setter
    def draw_on_lower_half_of_2d(self, value: 'bool'):
        self.wrapped.DrawOnLowerHalfOf2D = bool(value) if value else False

    @property
    def planetary_load_sharing_factor(self) -> 'float':
        '''float: 'PlanetaryLoadSharingFactor' is the original name of this property.'''

        return self.wrapped.PlanetaryLoadSharingFactor

    @planetary_load_sharing_factor.setter
    def planetary_load_sharing_factor(self, value: 'float'):
        self.wrapped.PlanetaryLoadSharingFactor = float(value) if value else 0.0

    @property
    def width(self) -> 'float':
        '''float: 'Width' is the original name of this property.'''

        return self.wrapped.Width

    @width.setter
    def width(self, value: 'float'):
        self.wrapped.Width = float(value) if value else 0.0

    @property
    def planet_tip_clearance(self) -> 'float':
        '''float: 'PlanetTipClearance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PlanetTipClearance

    @property
    def editable_name(self) -> 'str':
        '''str: 'EditableName' is the original name of this property.'''

        return self.wrapped.EditableName

    @editable_name.setter
    def editable_name(self, value: 'str'):
        self.wrapped.EditableName = str(value) if value else None

    @property
    def planetary_details(self) -> '_140.PlanetaryDetail':
        '''PlanetaryDetail: 'PlanetaryDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_140.PlanetaryDetail)(self.wrapped.PlanetaryDetails) if self.wrapped.PlanetaryDetails else None
