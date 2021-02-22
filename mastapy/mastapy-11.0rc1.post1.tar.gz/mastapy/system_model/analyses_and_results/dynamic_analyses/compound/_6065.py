'''_6065.py

ClutchHalfCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2250
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5935
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6081
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ClutchHalfCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfCompoundDynamicAnalysis',)


class ClutchHalfCompoundDynamicAnalysis(_6081.CouplingHalfCompoundDynamicAnalysis):
    '''ClutchHalfCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2250.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2250.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5935.ClutchHalfDynamicAnalysis]':
        '''List[ClutchHalfDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5935.ClutchHalfDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_5935.ClutchHalfDynamicAnalysis]':
        '''List[ClutchHalfDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_5935.ClutchHalfDynamicAnalysis))
        return value
