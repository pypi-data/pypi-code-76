'''_6169.py

ZerolBevelGearMeshCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _2007
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6040
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6059
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ZerolBevelGearMeshCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshCompoundDynamicAnalysis',)


class ZerolBevelGearMeshCompoundDynamicAnalysis(_6059.BevelGearMeshCompoundDynamicAnalysis):
    '''ZerolBevelGearMeshCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2007.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.ZerolBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2007.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6040.ZerolBevelGearMeshDynamicAnalysis]':
        '''List[ZerolBevelGearMeshDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6040.ZerolBevelGearMeshDynamicAnalysis))
        return value

    @property
    def connection_dynamic_analysis_load_cases(self) -> 'List[_6040.ZerolBevelGearMeshDynamicAnalysis]':
        '''List[ZerolBevelGearMeshDynamicAnalysis]: 'ConnectionDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionDynamicAnalysisLoadCases, constructor.new(_6040.ZerolBevelGearMeshDynamicAnalysis))
        return value
