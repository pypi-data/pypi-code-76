'''_6094.py

ExternalCADModelCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2125
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5965
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6067
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ExternalCADModelCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelCompoundDynamicAnalysis',)


class ExternalCADModelCompoundDynamicAnalysis(_6067.ComponentCompoundDynamicAnalysis):
    '''ExternalCADModelCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2125.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2125.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5965.ExternalCADModelDynamicAnalysis]':
        '''List[ExternalCADModelDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5965.ExternalCADModelDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_5965.ExternalCADModelDynamicAnalysis]':
        '''List[ExternalCADModelDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_5965.ExternalCADModelDynamicAnalysis))
        return value
