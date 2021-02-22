'''_3673.py

SynchroniserSleeveCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2277
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3543
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3672
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'SynchroniserSleeveCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveCompoundStabilityAnalysis',)


class SynchroniserSleeveCompoundStabilityAnalysis(_3672.SynchroniserPartCompoundStabilityAnalysis):
    '''SynchroniserSleeveCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2277.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2277.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3543.SynchroniserSleeveStabilityAnalysis]':
        '''List[SynchroniserSleeveStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3543.SynchroniserSleeveStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3543.SynchroniserSleeveStabilityAnalysis]':
        '''List[SynchroniserSleeveStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3543.SynchroniserSleeveStabilityAnalysis))
        return value
