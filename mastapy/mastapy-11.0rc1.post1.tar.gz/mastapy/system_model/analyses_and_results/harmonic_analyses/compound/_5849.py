'''_5849.py

MassDiscCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2135
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5689
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5896
from mastapy._internal.python_net import python_net_import

_MASS_DISC_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'MassDiscCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCompoundHarmonicAnalysis',)


class MassDiscCompoundHarmonicAnalysis(_5896.VirtualComponentCompoundHarmonicAnalysis):
    '''MassDiscCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2135.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2135.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5689.MassDiscHarmonicAnalysis]':
        '''List[MassDiscHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5689.MassDiscHarmonicAnalysis))
        return value

    @property
    def component_harmonic_analysis_load_cases(self) -> 'List[_5689.MassDiscHarmonicAnalysis]':
        '''List[MassDiscHarmonicAnalysis]: 'ComponentHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisLoadCases, constructor.new(_5689.MassDiscHarmonicAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[MassDiscCompoundHarmonicAnalysis]':
        '''List[MassDiscCompoundHarmonicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscCompoundHarmonicAnalysis))
        return value
