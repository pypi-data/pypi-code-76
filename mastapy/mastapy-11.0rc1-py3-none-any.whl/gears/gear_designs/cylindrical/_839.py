'''_839.py

Usage
'''


from mastapy.gears import _145
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _828
from mastapy.utility import _1151
from mastapy._internal.python_net import python_net_import

_USAGE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'Usage')


__docformat__ = 'restructuredtext en'
__all__ = ('Usage',)


class Usage(_1151.IndependentReportablePropertiesBase['Usage']):
    '''Usage

    This is a mastapy class.
    '''

    TYPE = _USAGE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Usage.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def safety_requirement(self) -> '_145.SafetyRequirementsAGMA':
        '''SafetyRequirementsAGMA: 'SafetyRequirement' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.SafetyRequirement)
        return constructor.new(_145.SafetyRequirementsAGMA)(value) if value else None

    @safety_requirement.setter
    def safety_requirement(self, value: '_145.SafetyRequirementsAGMA'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SafetyRequirement = value

    @property
    def leads_modified(self) -> 'bool':
        '''bool: 'LeadsModified' is the original name of this property.'''

        return self.wrapped.LeadsModified

    @leads_modified.setter
    def leads_modified(self, value: 'bool'):
        self.wrapped.LeadsModified = bool(value) if value else False

    @property
    def improved_gearing(self) -> 'bool':
        '''bool: 'ImprovedGearing' is the original name of this property.'''

        return self.wrapped.ImprovedGearing

    @improved_gearing.setter
    def improved_gearing(self, value: 'bool'):
        self.wrapped.ImprovedGearing = bool(value) if value else False

    @property
    def gearing_is_runin(self) -> 'bool':
        '''bool: 'GearingIsRunin' is the original name of this property.'''

        return self.wrapped.GearingIsRunin

    @gearing_is_runin.setter
    def gearing_is_runin(self, value: 'bool'):
        self.wrapped.GearingIsRunin = bool(value) if value else False

    @property
    def spur_gear_load_sharing_code(self) -> '_828.SpurGearLoadSharingCodes':
        '''SpurGearLoadSharingCodes: 'SpurGearLoadSharingCode' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.SpurGearLoadSharingCode)
        return constructor.new(_828.SpurGearLoadSharingCodes)(value) if value else None

    @spur_gear_load_sharing_code.setter
    def spur_gear_load_sharing_code(self, value: '_828.SpurGearLoadSharingCodes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SpurGearLoadSharingCode = value
