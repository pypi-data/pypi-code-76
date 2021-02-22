'''_5869.py

ShaftCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2154
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5710
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5775
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'ShaftCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundHarmonicAnalysis',)


class ShaftCompoundHarmonicAnalysis(_5775.AbstractShaftCompoundHarmonicAnalysis):
    '''ShaftCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2154.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2154.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5710.ShaftHarmonicAnalysis]':
        '''List[ShaftHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5710.ShaftHarmonicAnalysis))
        return value

    @property
    def component_harmonic_analysis_load_cases(self) -> 'List[_5710.ShaftHarmonicAnalysis]':
        '''List[ShaftHarmonicAnalysis]: 'ComponentHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisLoadCases, constructor.new(_5710.ShaftHarmonicAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundHarmonicAnalysis]':
        '''List[ShaftCompoundHarmonicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundHarmonicAnalysis))
        return value
