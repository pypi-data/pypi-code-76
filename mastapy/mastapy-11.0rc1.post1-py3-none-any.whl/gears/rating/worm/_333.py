'''_333.py

WormGearMeshRating
'''


from typing import List

from mastapy.gears.gear_designs.worm import _887
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.worm import _334
from mastapy.gears.rating import _320
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Worm', 'WormGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshRating',)


class WormGearMeshRating(_320.GearMeshRating):
    '''WormGearMeshRating

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def worm_gear_mesh(self) -> '_887.WormGearMeshDesign':
        '''WormGearMeshDesign: 'WormGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_887.WormGearMeshDesign)(self.wrapped.WormGearMesh) if self.wrapped.WormGearMesh else None

    @property
    def worm_gear_ratings(self) -> 'List[_334.WormGearRating]':
        '''List[WormGearRating]: 'WormGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearRatings, constructor.new(_334.WormGearRating))
        return value
