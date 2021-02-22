'''_6880.py

StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _2003
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6751
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6788
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation',)


class StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation(_6788.BevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2003.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2003.StraightBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2003.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2003.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6751.StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6751.StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def connection_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6751.StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation]: 'ConnectionAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6751.StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation))
        return value
