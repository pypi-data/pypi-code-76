'''_2069.py

PlanetCarrier
'''


from typing import List, Optional

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.part_model import _2040, _2061, _2064
from mastapy.system_model.connections_and_sockets import _1905
from mastapy.system_model.part_model.shaft_model import _2081
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PlanetCarrier')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrier',)


class PlanetCarrier(_2064.MountableComponent):
    '''PlanetCarrier

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrier.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def length(self) -> 'float':
        '''float: 'Length' is the original name of this property.'''

        return self.wrapped.Length

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value else 0.0

    @property
    def planetary_load_sharing_agma_application_level(self) -> '_2040.AGMALoadSharingTableApplicationLevel':
        '''AGMALoadSharingTableApplicationLevel: 'PlanetaryLoadSharingAGMAApplicationLevel' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.PlanetaryLoadSharingAGMAApplicationLevel)
        return constructor.new(_2040.AGMALoadSharingTableApplicationLevel)(value) if value else None

    @planetary_load_sharing_agma_application_level.setter
    def planetary_load_sharing_agma_application_level(self, value: '_2040.AGMALoadSharingTableApplicationLevel'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PlanetaryLoadSharingAGMAApplicationLevel = value

    @property
    def planetary_load_sharing(self) -> '_2061.LoadSharingModes':
        '''LoadSharingModes: 'PlanetaryLoadSharing' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.PlanetaryLoadSharing)
        return constructor.new(_2061.LoadSharingModes)(value) if value else None

    @planetary_load_sharing.setter
    def planetary_load_sharing(self, value: '_2061.LoadSharingModes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PlanetaryLoadSharing = value

    @property
    def number_of_planetary_sockets(self) -> 'int':
        '''int: 'NumberOfPlanetarySockets' is the original name of this property.'''

        return self.wrapped.NumberOfPlanetarySockets

    @number_of_planetary_sockets.setter
    def number_of_planetary_sockets(self, value: 'int'):
        self.wrapped.NumberOfPlanetarySockets = int(value) if value else 0

    @property
    def planetary_sockets(self) -> 'List[_1905.PlanetarySocket]':
        '''List[PlanetarySocket]: 'PlanetarySockets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetarySockets, constructor.new(_1905.PlanetarySocket))
        return value

    def attach_carrier_shaft(self, shaft: '_2081.Shaft', offset: Optional['float'] = float('nan')):
        ''' 'AttachCarrierShaft' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)
        '''

        offset = float(offset)
        self.wrapped.AttachCarrierShaft(shaft.wrapped if shaft else None, offset if offset else 0.0)

    def attach_pin_shaft(self, shaft: '_2081.Shaft', offset: Optional['float'] = float('nan')):
        ''' 'AttachPinShaft' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)
        '''

        offset = float(offset)
        self.wrapped.AttachPinShaft(shaft.wrapped if shaft else None, offset if offset else 0.0)
