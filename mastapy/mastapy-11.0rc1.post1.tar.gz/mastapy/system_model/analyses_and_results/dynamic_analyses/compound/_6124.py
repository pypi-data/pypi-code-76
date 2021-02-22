'''_6124.py

PartToPartShearCouplingHalfCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2260
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5995
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6081
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_HALF_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'PartToPartShearCouplingHalfCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingHalfCompoundDynamicAnalysis',)


class PartToPartShearCouplingHalfCompoundDynamicAnalysis(_6081.CouplingHalfCompoundDynamicAnalysis):
    '''PartToPartShearCouplingHalfCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_HALF_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingHalfCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2260.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2260.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5995.PartToPartShearCouplingHalfDynamicAnalysis]':
        '''List[PartToPartShearCouplingHalfDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5995.PartToPartShearCouplingHalfDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_5995.PartToPartShearCouplingHalfDynamicAnalysis]':
        '''List[PartToPartShearCouplingHalfDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_5995.PartToPartShearCouplingHalfDynamicAnalysis))
        return value
