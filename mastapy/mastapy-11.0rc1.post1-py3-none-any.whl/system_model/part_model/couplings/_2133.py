'''_2133.py

BeltDrive
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.part_model.couplings import _2134, _2146
from mastapy.system_model.connections_and_sockets import _1851
from mastapy.system_model.part_model import _2039
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'BeltDrive')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDrive',)


class BeltDrive(_2039.SpecialisedAssembly):
    '''BeltDrive

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDrive.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def stiffness(self) -> 'float':
        '''float: 'Stiffness' is the original name of this property.'''

        return self.wrapped.Stiffness

    @stiffness.setter
    def stiffness(self, value: 'float'):
        self.wrapped.Stiffness = float(value) if value else 0.0

    @property
    def stiffness_for_unit_length(self) -> 'float':
        '''float: 'StiffnessForUnitLength' is the original name of this property.'''

        return self.wrapped.StiffnessForUnitLength

    @stiffness_for_unit_length.setter
    def stiffness_for_unit_length(self, value: 'float'):
        self.wrapped.StiffnessForUnitLength = float(value) if value else 0.0

    @property
    def specify_stiffness_for_unit_length(self) -> 'bool':
        '''bool: 'SpecifyStiffnessForUnitLength' is the original name of this property.'''

        return self.wrapped.SpecifyStiffnessForUnitLength

    @specify_stiffness_for_unit_length.setter
    def specify_stiffness_for_unit_length(self, value: 'bool'):
        self.wrapped.SpecifyStiffnessForUnitLength = bool(value) if value else False

    @property
    def pre_tension(self) -> 'float':
        '''float: 'PreTension' is the original name of this property.'''

        return self.wrapped.PreTension

    @pre_tension.setter
    def pre_tension(self, value: 'float'):
        self.wrapped.PreTension = float(value) if value else 0.0

    @property
    def belt_mass_per_unit_length(self) -> 'float':
        '''float: 'BeltMassPerUnitLength' is the original name of this property.'''

        return self.wrapped.BeltMassPerUnitLength

    @belt_mass_per_unit_length.setter
    def belt_mass_per_unit_length(self, value: 'float'):
        self.wrapped.BeltMassPerUnitLength = float(value) if value else 0.0

    @property
    def type_of_belt(self) -> '_2134.BeltDriveType':
        '''BeltDriveType: 'TypeOfBelt' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.TypeOfBelt)
        return constructor.new(_2134.BeltDriveType)(value) if value else None

    @type_of_belt.setter
    def type_of_belt(self, value: '_2134.BeltDriveType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TypeOfBelt = value

    @property
    def belt_mass(self) -> 'float':
        '''float: 'BeltMass' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BeltMass

    @property
    def belt_length(self) -> 'float':
        '''float: 'BeltLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BeltLength

    @property
    def pulleys(self) -> 'List[_2146.Pulley]':
        '''List[Pulley]: 'Pulleys' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Pulleys, constructor.new(_2146.Pulley))
        return value

    @property
    def belt_connections(self) -> 'List[_1851.BeltConnection]':
        '''List[BeltConnection]: 'BeltConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltConnections, constructor.new(_1851.BeltConnection))
        return value
