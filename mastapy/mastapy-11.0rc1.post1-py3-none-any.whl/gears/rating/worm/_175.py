'''_175.py

WormGearSetRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.worm import _724
from mastapy.gears.rating.worm import _172, _173
from mastapy.gears.rating import _162
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Worm', 'WormGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetRating',)


class WormGearSetRating(_162.GearSetRating):
    '''WormGearSetRating

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rating(self) -> 'str':
        '''str: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Rating

    @property
    def worm_gear_set(self) -> '_724.WormGearSetDesign':
        '''WormGearSetDesign: 'WormGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_724.WormGearSetDesign)(self.wrapped.WormGearSet) if self.wrapped.WormGearSet else None

    @property
    def worm_mesh_ratings(self) -> 'List[_172.WormGearMeshRating]':
        '''List[WormGearMeshRating]: 'WormMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshRatings, constructor.new(_172.WormGearMeshRating))
        return value

    @property
    def gear_ratings(self) -> 'List[_173.WormGearRating]':
        '''List[WormGearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_173.WormGearRating))
        return value

    @property
    def worm_gear_ratings(self) -> 'List[_173.WormGearRating]':
        '''List[WormGearRating]: 'WormGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearRatings, constructor.new(_173.WormGearRating))
        return value
