'''_796.py

CylindricalMeshLoadDistributionAtRotation
'''


from typing import List

from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1035
from mastapy._internal import constructor, conversion
from mastapy.gears.ltca.cylindrical import _793
from mastapy.gears.ltca import _779
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MESH_LOAD_DISTRIBUTION_AT_ROTATION = python_net_import('SMT.MastaAPI.Gears.LTCA.Cylindrical', 'CylindricalMeshLoadDistributionAtRotation')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalMeshLoadDistributionAtRotation',)


class CylindricalMeshLoadDistributionAtRotation(_779.GearMeshLoadDistributionAtRotation):
    '''CylindricalMeshLoadDistributionAtRotation

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_MESH_LOAD_DISTRIBUTION_AT_ROTATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalMeshLoadDistributionAtRotation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mesh_alignment(self) -> '_1035.MeshAlignment':
        '''MeshAlignment: 'MeshAlignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1035.MeshAlignment)(self.wrapped.MeshAlignment) if self.wrapped.MeshAlignment else None

    @property
    def loaded_contact_lines(self) -> 'List[_793.CylindricalGearMeshLoadedContactLine]':
        '''List[CylindricalGearMeshLoadedContactLine]: 'LoadedContactLines' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadedContactLines, constructor.new(_793.CylindricalGearMeshLoadedContactLine))
        return value
