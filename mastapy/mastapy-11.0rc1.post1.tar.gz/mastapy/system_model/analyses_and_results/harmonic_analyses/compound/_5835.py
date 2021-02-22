'''_5835.py

GuideDxfModelCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2128
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5669
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5799
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'GuideDxfModelCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelCompoundHarmonicAnalysis',)


class GuideDxfModelCompoundHarmonicAnalysis(_5799.ComponentCompoundHarmonicAnalysis):
    '''GuideDxfModelCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2128.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2128.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5669.GuideDxfModelHarmonicAnalysis]':
        '''List[GuideDxfModelHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5669.GuideDxfModelHarmonicAnalysis))
        return value

    @property
    def component_harmonic_analysis_load_cases(self) -> 'List[_5669.GuideDxfModelHarmonicAnalysis]':
        '''List[GuideDxfModelHarmonicAnalysis]: 'ComponentHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisLoadCases, constructor.new(_5669.GuideDxfModelHarmonicAnalysis))
        return value
