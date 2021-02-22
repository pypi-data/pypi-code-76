'''_6019.py

StraightBevelDiffGearMeshDynamicAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _2001
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6591
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5929
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'StraightBevelDiffGearMeshDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearMeshDynamicAnalysis',)


class StraightBevelDiffGearMeshDynamicAnalysis(_5929.BevelGearMeshDynamicAnalysis):
    '''StraightBevelDiffGearMeshDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearMeshDynamicAnalysis.TYPE'):
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
