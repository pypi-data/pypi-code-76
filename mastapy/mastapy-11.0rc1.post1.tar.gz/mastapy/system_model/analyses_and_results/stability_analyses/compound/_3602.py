'''_3602.py

CycloidalDiscCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2240
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3472
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3558
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'CycloidalDiscCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCompoundStabilityAnalysis',)


class CycloidalDiscCompoundStabilityAnalysis(_3558.AbstractShaftCompoundStabilityAnalysis):
    '''CycloidalDiscCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2240.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2240.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3472.CycloidalDiscStabilityAnalysis]':
        '''List[CycloidalDiscStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3472.CycloidalDiscStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3472.CycloidalDiscStabilityAnalysis]':
        '''List[CycloidalDiscStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3472.CycloidalDiscStabilityAnalysis))
        return value
