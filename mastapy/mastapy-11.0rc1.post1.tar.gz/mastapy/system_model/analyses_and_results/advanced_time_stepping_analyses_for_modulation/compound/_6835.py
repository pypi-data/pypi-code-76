'''_6835.py

HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2206
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6833, _6834, _6777
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6706
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation',)


class HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation(_6777.AGMAGleasonConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2206.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2206.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2206.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2206.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def hypoid_gears_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6833.HypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[HypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation]: 'HypoidGearsCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6833.HypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def hypoid_meshes_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6834.HypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[HypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]: 'HypoidMeshesCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6834.HypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6706.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[HypoidGearSetAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6706.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6706.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[HypoidGearSetAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6706.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value
