'''_6863.py

RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2267
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6733
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6810
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation',)


class RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation(_6810.CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2267.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2267.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6733.RollingRingAdvancedTimeSteppingAnalysisForModulation]':
        '''List[RollingRingAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6733.RollingRingAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def component_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6733.RollingRingAdvancedTimeSteppingAnalysisForModulation]':
        '''List[RollingRingAdvancedTimeSteppingAnalysisForModulation]: 'ComponentAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6733.RollingRingAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value
