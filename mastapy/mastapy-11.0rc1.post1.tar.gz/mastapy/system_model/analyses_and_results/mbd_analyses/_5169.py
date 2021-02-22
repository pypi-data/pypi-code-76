'''_5169.py

WormGearMeshMultibodyDynamicsAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _2005
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6615
from mastapy.system_model.analyses_and_results.mbd_analyses import _5090
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'WormGearMeshMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshMultibodyDynamicsAnalysis',)


class WormGearMeshMultibodyDynamicsAnalysis(_5090.GearMeshMultibodyDynamicsAnalysis):
    '''WormGearMeshMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2005.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2005.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6615.WormGearMeshLoadCase':
        '''WormGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6615.WormGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
