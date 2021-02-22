'''_7135.py

SpiralBevelGearCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2214
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7005
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7052
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'SpiralBevelGearCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearCompoundAdvancedSystemDeflection',)


class SpiralBevelGearCompoundAdvancedSystemDeflection(_7052.BevelGearCompoundAdvancedSystemDeflection):
    '''SpiralBevelGearCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2214.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2214.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_7005.SpiralBevelGearAdvancedSystemDeflection]':
        '''List[SpiralBevelGearAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_7005.SpiralBevelGearAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_7005.SpiralBevelGearAdvancedSystemDeflection]':
        '''List[SpiralBevelGearAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_7005.SpiralBevelGearAdvancedSystemDeflection))
        return value
