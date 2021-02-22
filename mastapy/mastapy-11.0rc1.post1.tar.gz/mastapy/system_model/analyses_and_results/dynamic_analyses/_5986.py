'''_5986.py

KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1996
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6548
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5980
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis(_5980.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1996.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1996.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6548.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6548.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
