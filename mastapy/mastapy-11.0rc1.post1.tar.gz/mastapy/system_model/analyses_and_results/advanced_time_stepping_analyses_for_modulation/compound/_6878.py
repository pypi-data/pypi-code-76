'''_6878.py

StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2217
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6876, _6877, _6789
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6749
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation',)


class StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation(_6789.BevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2217.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2217.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2217.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2217.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_diff_gears_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6876.StraightBevelDiffGearCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelDiffGearCompoundAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelDiffGearsCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6876.StraightBevelDiffGearCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def straight_bevel_diff_meshes_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6877.StraightBevelDiffGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelDiffGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelDiffMeshesCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6877.StraightBevelDiffGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6749.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6749.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6749.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6749.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value
