'''_6166.py

WormGearMeshCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _2005
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6037
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6101
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'WormGearMeshCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshCompoundDynamicAnalysis',)


class WormGearMeshCompoundDynamicAnalysis(_6101.GearMeshCompoundDynamicAnalysis):
    '''WormGearMeshCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2005.WormGearMesh':
        '''WormGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2005.WormGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2005.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2005.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6037.WormGearMeshDynamicAnalysis]':
        '''List[WormGearMeshDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6037.WormGearMeshDynamicAnalysis))
        return value

    @property
    def connection_dynamic_analysis_load_cases(self) -> 'List[_6037.WormGearMeshDynamicAnalysis]':
        '''List[WormGearMeshDynamicAnalysis]: 'ConnectionDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionDynamicAnalysisLoadCases, constructor.new(_6037.WormGearMeshDynamicAnalysis))
        return value
