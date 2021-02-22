'''_361.py

StraightBevelGearSetRating
'''


from typing import List

from mastapy.gears.gear_designs.straight_bevel import _896
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.straight_bevel import _359, _360
from mastapy.gears.rating.bevel import _503
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.StraightBevel', 'StraightBevelGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetRating',)


class StraightBevelGearSetRating(_503.BevelGearSetRating):
    '''StraightBevelGearSetRating

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def straight_bevel_gear_set(self) -> '_896.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'StraightBevelGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_896.StraightBevelGearSetDesign)(self.wrapped.StraightBevelGearSet) if self.wrapped.StraightBevelGearSet else None

    @property
    def straight_bevel_mesh_ratings(self) -> 'List[_359.StraightBevelGearMeshRating]':
        '''List[StraightBevelGearMeshRating]: 'StraightBevelMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshRatings, constructor.new(_359.StraightBevelGearMeshRating))
        return value

    @property
    def straight_bevel_gear_ratings(self) -> 'List[_360.StraightBevelGearRating]':
        '''List[StraightBevelGearRating]: 'StraightBevelGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearRatings, constructor.new(_360.StraightBevelGearRating))
        return value
