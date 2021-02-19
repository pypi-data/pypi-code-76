'''_337.py

ConceptGearSetRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.concept import _915
from mastapy.gears.rating.concept import _334, _335
from mastapy.gears.rating import _163
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Concept', 'ConceptGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetRating',)


class ConceptGearSetRating(_163.GearSetRating):
    '''ConceptGearSetRating

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetRating.TYPE'):
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
    def concept_gear_set(self) -> '_915.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'ConceptGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_915.ConceptGearSetDesign)(self.wrapped.ConceptGearSet) if self.wrapped.ConceptGearSet else None

    @property
    def concept_mesh_ratings(self) -> 'List[_334.ConceptGearMeshRating]':
        '''List[ConceptGearMeshRating]: 'ConceptMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshRatings, constructor.new(_334.ConceptGearMeshRating))
        return value

    @property
    def gear_ratings(self) -> 'List[_335.ConceptGearRating]':
        '''List[ConceptGearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_335.ConceptGearRating))
        return value

    @property
    def concept_gear_ratings(self) -> 'List[_335.ConceptGearRating]':
        '''List[ConceptGearRating]: 'ConceptGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearRatings, constructor.new(_335.ConceptGearRating))
        return value
