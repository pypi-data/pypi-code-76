'''_3554.py

ZerolBevelGearMeshStabilityAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _2007
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6618
from mastapy.system_model.analyses_and_results.stability_analyses import _3441
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ZerolBevelGearMeshStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshStabilityAnalysis',)


class ZerolBevelGearMeshStabilityAnalysis(_3441.BevelGearMeshStabilityAnalysis):
    '''ZerolBevelGearMeshStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2007.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6618.ZerolBevelGearMeshLoadCase':
        '''ZerolBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6618.ZerolBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
