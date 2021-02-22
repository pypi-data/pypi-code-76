'''_7083.py

CylindricalGearCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2196, _2198
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.cylindrical import _412
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6951
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7094
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'CylindricalGearCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearCompoundAdvancedSystemDeflection',)


class CylindricalGearCompoundAdvancedSystemDeflection(_7094.GearCompoundAdvancedSystemDeflection):
    '''CylindricalGearCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2196.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2196.CylindricalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def gear_duty_cycle_rating(self) -> '_412.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_412.CylindricalGearDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def cylindrical_gear_rating(self) -> '_412.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'CylindricalGearRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_412.CylindricalGearDutyCycleRating)(self.wrapped.CylindricalGearRating) if self.wrapped.CylindricalGearRating else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6951.CylindricalGearAdvancedSystemDeflection]':
        '''List[CylindricalGearAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6951.CylindricalGearAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_6951.CylindricalGearAdvancedSystemDeflection]':
        '''List[CylindricalGearAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_6951.CylindricalGearAdvancedSystemDeflection))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearCompoundAdvancedSystemDeflection]':
        '''List[CylindricalGearCompoundAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearCompoundAdvancedSystemDeflection))
        return value
