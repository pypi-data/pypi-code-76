'''_6280.py

WormGearMeshLoadCase
'''


from mastapy.system_model.connections_and_sockets.gears import _1946
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6190
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'WormGearMeshLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshLoadCase',)


class WormGearMeshLoadCase(_6190.GearMeshLoadCase):
    '''WormGearMeshLoadCase

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1946.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1946.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
