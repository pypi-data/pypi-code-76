'''_6417.py

StraightBevelGearMeshCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _2003
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6288
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6325
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'StraightBevelGearMeshCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMeshCompoundCriticalSpeedAnalysis',)


class StraightBevelGearMeshCompoundCriticalSpeedAnalysis(_6325.BevelGearMeshCompoundCriticalSpeedAnalysis):
    '''StraightBevelGearMeshCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMeshCompoundCriticalSpeedAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_6288.StraightBevelGearMeshCriticalSpeedAnalysis]':
        '''List[StraightBevelGearMeshCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6288.StraightBevelGearMeshCriticalSpeedAnalysis))
        return value

    @property
    def connection_critical_speed_analysis_load_cases(self) -> 'List[_6288.StraightBevelGearMeshCriticalSpeedAnalysis]':
        '''List[StraightBevelGearMeshCriticalSpeedAnalysis]: 'ConnectionCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionCriticalSpeedAnalysisLoadCases, constructor.new(_6288.StraightBevelGearMeshCriticalSpeedAnalysis))
        return value
