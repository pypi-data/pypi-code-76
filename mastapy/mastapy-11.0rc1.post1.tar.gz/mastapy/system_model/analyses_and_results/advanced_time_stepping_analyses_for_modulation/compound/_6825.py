'''_6825.py

FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1987
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6695
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6830
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation',)


class FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation(_6830.GearMeshCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1987.FaceGearMesh':
        '''FaceGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.FaceGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1987.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6695.FaceGearMeshAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FaceGearMeshAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6695.FaceGearMeshAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def connection_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6695.FaceGearMeshAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FaceGearMeshAdvancedTimeSteppingAnalysisForModulation]: 'ConnectionAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6695.FaceGearMeshAdvancedTimeSteppingAnalysisForModulation))
        return value
