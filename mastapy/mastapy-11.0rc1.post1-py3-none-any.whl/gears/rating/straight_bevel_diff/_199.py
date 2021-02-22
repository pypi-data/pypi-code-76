'''_199.py

StraightBevelDiffGearSetRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.straight_bevel_diff import _729
from mastapy.gears.rating.straight_bevel_diff import _197, _198
from mastapy.gears.rating.conical import _328
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.StraightBevelDiff', 'StraightBevelDiffGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetRating',)


class StraightBevelDiffGearSetRating(_328.ConicalGearSetRating):
    '''StraightBevelDiffGearSetRating

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetRating.TYPE'):
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
    def straight_bevel_diff_gear_set(self) -> '_729.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'StraightBevelDiffGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_729.StraightBevelDiffGearSetDesign)(self.wrapped.StraightBevelDiffGearSet) if self.wrapped.StraightBevelDiffGearSet else None

    @property
    def straight_bevel_diff_mesh_ratings(self) -> 'List[_197.StraightBevelDiffGearMeshRating]':
        '''List[StraightBevelDiffGearMeshRating]: 'StraightBevelDiffMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshRatings, constructor.new(_197.StraightBevelDiffGearMeshRating))
        return value

    @property
    def straight_bevel_diff_gear_ratings(self) -> 'List[_198.StraightBevelDiffGearRating]':
        '''List[StraightBevelDiffGearRating]: 'StraightBevelDiffGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearRatings, constructor.new(_198.StraightBevelDiffGearRating))
        return value
