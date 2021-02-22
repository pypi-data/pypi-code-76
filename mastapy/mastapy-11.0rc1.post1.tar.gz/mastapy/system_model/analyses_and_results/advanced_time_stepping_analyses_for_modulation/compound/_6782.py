'''_6782.py

BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2186, _2188, _2189
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6652
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6787
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation',)


class BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation(_6787.BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2186.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2186.BevelDifferentialGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6652.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6652.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def component_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6652.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation]: 'ComponentAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6652.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation))
        return value
