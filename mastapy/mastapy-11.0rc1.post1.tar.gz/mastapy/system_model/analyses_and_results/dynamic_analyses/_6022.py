'''_6022.py

StraightBevelGearMeshDynamicAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _2003
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6594
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5929
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'StraightBevelGearMeshDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMeshDynamicAnalysis',)


class StraightBevelGearMeshDynamicAnalysis(_5929.BevelGearMeshDynamicAnalysis):
    '''StraightBevelGearMeshDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMeshDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2003.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2003.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6594.StraightBevelGearMeshLoadCase':
        '''StraightBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6594.StraightBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
