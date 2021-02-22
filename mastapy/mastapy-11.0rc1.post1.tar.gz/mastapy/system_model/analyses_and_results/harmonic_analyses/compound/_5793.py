'''_5793.py

BoltCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2116
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5610
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5799
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'BoltCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundHarmonicAnalysis',)


class BoltCompoundHarmonicAnalysis(_5799.ComponentCompoundHarmonicAnalysis):
    '''BoltCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2116.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5610.BoltHarmonicAnalysis]':
        '''List[BoltHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5610.BoltHarmonicAnalysis))
        return value

    @property
    def component_harmonic_analysis_load_cases(self) -> 'List[_5610.BoltHarmonicAnalysis]':
        '''List[BoltHarmonicAnalysis]: 'ComponentHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisLoadCases, constructor.new(_5610.BoltHarmonicAnalysis))
        return value
