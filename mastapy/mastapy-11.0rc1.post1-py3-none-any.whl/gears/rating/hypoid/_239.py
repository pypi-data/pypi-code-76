'''_239.py

HypoidGearSetRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.gear_designs.hypoid import _752
from mastapy.gears.rating.hypoid import _237, _238
from mastapy.gears.rating.agma_gleason_conical import _350
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Hypoid', 'HypoidGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetRating',)


class HypoidGearSetRating(_350.AGMAGleasonConicalGearSetRating):
    '''HypoidGearSetRating

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetRating.TYPE'):
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
    def size_factor_bending(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SizeFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SizeFactorBending) if self.wrapped.SizeFactorBending else None

    @property
    def size_factor_contact(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SizeFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SizeFactorContact) if self.wrapped.SizeFactorContact else None

    @property
    def hypoid_gear_set(self) -> '_752.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'HypoidGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_752.HypoidGearSetDesign)(self.wrapped.HypoidGearSet) if self.wrapped.HypoidGearSet else None

    @property
    def hypoid_mesh_ratings(self) -> 'List[_237.HypoidGearMeshRating]':
        '''List[HypoidGearMeshRating]: 'HypoidMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshRatings, constructor.new(_237.HypoidGearMeshRating))
        return value

    @property
    def hypoid_gear_ratings(self) -> 'List[_238.HypoidGearRating]':
        '''List[HypoidGearRating]: 'HypoidGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearRatings, constructor.new(_238.HypoidGearRating))
        return value
