'''_6548.py

KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase
'''


from mastapy.system_model.connections_and_sockets.gears import _1996
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6542
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase',)


class KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase(_6542.KlingelnbergCycloPalloidConicalGearMeshLoadCase):
    '''KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1996.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1996.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
