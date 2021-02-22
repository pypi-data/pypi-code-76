'''_6826.py

FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2200
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6824, _6825, _6831
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6696
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation',)


class FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation(_6831.GearSetCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2200.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2200.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2200.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2200.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6824.FaceGearCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FaceGearCompoundAdvancedTimeSteppingAnalysisForModulation]: 'FaceGearsCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6824.FaceGearCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def face_meshes_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6825.FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]: 'FaceMeshesCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6825.FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6696.FaceGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FaceGearSetAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6696.FaceGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6696.FaceGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FaceGearSetAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6696.FaceGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value
