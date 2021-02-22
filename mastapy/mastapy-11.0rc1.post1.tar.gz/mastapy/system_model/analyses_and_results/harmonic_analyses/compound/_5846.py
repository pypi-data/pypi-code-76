'''_5846.py

KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2211
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5686
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5840
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis(_5840.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_5686.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5686.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis))
        return value

    @property
    def component_harmonic_analysis_load_cases(self) -> 'List[_5686.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis]: 'ComponentHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisLoadCases, constructor.new(_5686.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis))
        return value
