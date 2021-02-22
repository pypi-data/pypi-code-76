'''_6159.py

TorqueConverterCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2278
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6031
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6079
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'TorqueConverterCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterCompoundDynamicAnalysis',)


class TorqueConverterCompoundDynamicAnalysis(_6079.CouplingCompoundDynamicAnalysis):
    '''TorqueConverterCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2278.TorqueConverter':
        '''TorqueConverter: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2278.TorqueConverter)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2278.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2278.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6031.TorqueConverterDynamicAnalysis]':
        '''List[TorqueConverterDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6031.TorqueConverterDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_6031.TorqueConverterDynamicAnalysis]':
        '''List[TorqueConverterDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_6031.TorqueConverterDynamicAnalysis))
        return value
