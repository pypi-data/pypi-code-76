'''_5193.py

BevelDifferentialGearMeshCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1977
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5042
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5198
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MESH_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'BevelDifferentialGearMeshCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearMeshCompoundMultibodyDynamicsAnalysis',)


class BevelDifferentialGearMeshCompoundMultibodyDynamicsAnalysis(_5198.BevelGearMeshCompoundMultibodyDynamicsAnalysis):
    '''BevelDifferentialGearMeshCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MESH_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearMeshCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1977.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1977.BevelDifferentialGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1977.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1977.BevelDifferentialGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5042.BevelDifferentialGearMeshMultibodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearMeshMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5042.BevelDifferentialGearMeshMultibodyDynamicsAnalysis))
        return value

    @property
    def connection_multibody_dynamics_analysis_load_cases(self) -> 'List[_5042.BevelDifferentialGearMeshMultibodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearMeshMultibodyDynamicsAnalysis]: 'ConnectionMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionMultibodyDynamicsAnalysisLoadCases, constructor.new(_5042.BevelDifferentialGearMeshMultibodyDynamicsAnalysis))
        return value
