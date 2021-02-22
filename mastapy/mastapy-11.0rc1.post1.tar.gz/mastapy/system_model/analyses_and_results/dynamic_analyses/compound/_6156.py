'''_6156.py

SynchroniserHalfCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2275
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6027
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6157
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'SynchroniserHalfCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfCompoundDynamicAnalysis',)


class SynchroniserHalfCompoundDynamicAnalysis(_6157.SynchroniserPartCompoundDynamicAnalysis):
    '''SynchroniserHalfCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2275.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2275.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6027.SynchroniserHalfDynamicAnalysis]':
        '''List[SynchroniserHalfDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6027.SynchroniserHalfDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_6027.SynchroniserHalfDynamicAnalysis]':
        '''List[SynchroniserHalfDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_6027.SynchroniserHalfDynamicAnalysis))
        return value
