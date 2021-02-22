'''_6137.py

ShaftCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2154
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6008
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6043
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ShaftCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundDynamicAnalysis',)


class ShaftCompoundDynamicAnalysis(_6043.AbstractShaftCompoundDynamicAnalysis):
    '''ShaftCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundDynamicAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_6008.ShaftDynamicAnalysis]':
        '''List[ShaftDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6008.ShaftDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_6008.ShaftDynamicAnalysis]':
        '''List[ShaftDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_6008.ShaftDynamicAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundDynamicAnalysis]':
        '''List[ShaftCompoundDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundDynamicAnalysis))
        return value
