'''_6891.py

TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2281
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6762
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6810
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation',)


class TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation(_6810.CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2281.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2281.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6762.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation]':
        '''List[TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6762.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def component_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6762.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation]':
        '''List[TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation]: 'ComponentAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6762.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation))
        return value
