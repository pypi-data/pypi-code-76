'''_5148.py

StraightBevelDiffGearMeshMultibodyDynamicsAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _2001
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6591
from mastapy.system_model.analyses_and_results.mbd_analyses import _5047
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'StraightBevelDiffGearMeshMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearMeshMultibodyDynamicsAnalysis',)


class StraightBevelDiffGearMeshMultibodyDynamicsAnalysis(_5047.BevelGearMeshMultibodyDynamicsAnalysis):
    '''StraightBevelDiffGearMeshMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearMeshMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2001.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2001.StraightBevelDiffGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6591.StraightBevelDiffGearMeshLoadCase':
        '''StraightBevelDiffGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6591.StraightBevelDiffGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
