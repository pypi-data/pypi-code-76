'''_276.py

BevelHypoidGearDesignSettings
'''


from mastapy._internal import constructor
from mastapy.utility import _1348
from mastapy._internal.python_net import python_net_import

_BEVEL_HYPOID_GEAR_DESIGN_SETTINGS = python_net_import('SMT.MastaAPI.Gears', 'BevelHypoidGearDesignSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelHypoidGearDesignSettings',)


class BevelHypoidGearDesignSettings(_1348.PerMachineSettings):
    '''BevelHypoidGearDesignSettings

    This is a mastapy class.
    '''

    TYPE = _BEVEL_HYPOID_GEAR_DESIGN_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelHypoidGearDesignSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def minimum_ratio(self) -> 'float':
        '''float: 'MinimumRatio' is the original name of this property.'''

        return self.wrapped.MinimumRatio

    @minimum_ratio.setter
    def minimum_ratio(self, value: 'float'):
        self.wrapped.MinimumRatio = float(value) if value else 0.0

    @property
    def allow_overriding_manufacturing_config_micro_geometry_in_a_load_case(self) -> 'bool':
        '''bool: 'AllowOverridingManufacturingConfigMicroGeometryInALoadCase' is the original name of this property.'''

        return self.wrapped.AllowOverridingManufacturingConfigMicroGeometryInALoadCase

    @allow_overriding_manufacturing_config_micro_geometry_in_a_load_case.setter
    def allow_overriding_manufacturing_config_micro_geometry_in_a_load_case(self, value: 'bool'):
        self.wrapped.AllowOverridingManufacturingConfigMicroGeometryInALoadCase = bool(value) if value else False
