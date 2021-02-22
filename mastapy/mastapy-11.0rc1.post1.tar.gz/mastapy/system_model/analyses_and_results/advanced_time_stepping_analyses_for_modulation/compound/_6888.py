'''_6888.py

TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2278
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6759
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6808
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation',)


class TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation(_6808.CouplingCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_6759.TorqueConverterAdvancedTimeSteppingAnalysisForModulation]':
        '''List[TorqueConverterAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6759.TorqueConverterAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6759.TorqueConverterAdvancedTimeSteppingAnalysisForModulation]':
        '''List[TorqueConverterAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6759.TorqueConverterAdvancedTimeSteppingAnalysisForModulation))
        return value
