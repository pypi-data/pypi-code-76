'''_3629.py

KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2211
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3500
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3623
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis(_3623.KlingelnbergCycloPalloidConicalGearCompoundStabilityAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3500.KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3500.KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3500.KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3500.KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis))
        return value
