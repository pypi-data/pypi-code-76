'''_6790.py

BoltCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model import _2116
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6660
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6796
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'BoltCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundAdvancedTimeSteppingAnalysisForModulation',)


class BoltCompoundAdvancedTimeSteppingAnalysisForModulation(_6796.ComponentCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''BoltCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2116.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6660.BoltAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BoltAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6660.BoltAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def component_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6660.BoltAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BoltAdvancedTimeSteppingAnalysisForModulation]: 'ComponentAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6660.BoltAdvancedTimeSteppingAnalysisForModulation))
        return value
