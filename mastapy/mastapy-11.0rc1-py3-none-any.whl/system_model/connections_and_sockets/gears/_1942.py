'''_1942.py

StraightBevelDiffGearMesh
'''


from mastapy.gears.gear_designs.straight_bevel_diff import _727
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.gears import _1920
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelDiffGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearMesh',)


class StraightBevelDiffGearMesh(_1920.BevelGearMesh):
    '''StraightBevelDiffGearMesh

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bevel_gear_mesh_design(self) -> '_727.StraightBevelDiffGearMeshDesign':
        '''StraightBevelDiffGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_727.StraightBevelDiffGearMeshDesign)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign else None

    @property
    def straight_bevel_diff_gear_mesh_design(self) -> '_727.StraightBevelDiffGearMeshDesign':
        '''StraightBevelDiffGearMeshDesign: 'StraightBevelDiffGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_727.StraightBevelDiffGearMeshDesign)(self.wrapped.StraightBevelDiffGearMeshDesign) if self.wrapped.StraightBevelDiffGearMeshDesign else None
