'''_6899.py

ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2225
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6897, _6898, _6789
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6770
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation',)


class ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation(_6789.BevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2225.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2225.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2225.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2225.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6897.ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation]: 'ZerolBevelGearsCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6897.ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def zerol_bevel_meshes_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6898.ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]: 'ZerolBevelMeshesCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6898.ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6770.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6770.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6770.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6770.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value
