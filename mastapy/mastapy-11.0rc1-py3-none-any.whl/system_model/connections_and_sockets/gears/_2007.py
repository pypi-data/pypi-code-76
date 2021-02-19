'''_2007.py

ZerolBevelGearMesh
'''


from mastapy.gears.gear_designs.zerol_bevel import _882
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.gears import _1979
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ZerolBevelGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMesh',)


class ZerolBevelGearMesh(_1979.BevelGearMesh):
    '''ZerolBevelGearMesh

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bevel_gear_mesh_design(self) -> '_882.ZerolBevelGearMeshDesign':
        '''ZerolBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_882.ZerolBevelGearMeshDesign)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign else None

    @property
    def zerol_bevel_gear_mesh_design(self) -> '_882.ZerolBevelGearMeshDesign':
        '''ZerolBevelGearMeshDesign: 'ZerolBevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_882.ZerolBevelGearMeshDesign)(self.wrapped.ZerolBevelGearMeshDesign) if self.wrapped.ZerolBevelGearMeshDesign else None
