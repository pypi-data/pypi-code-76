'''_6843.py

KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2211
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6714
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6837
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation',)


class KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation(_6837.KlingelnbergCycloPalloidConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2211.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2211.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6714.KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6714.KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def component_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6714.KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation]: 'ComponentAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6714.KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation))
        return value
