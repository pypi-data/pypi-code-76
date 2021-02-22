'''_250.py

FaceGearSetRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.face import _761
from mastapy.gears.rating.face import _247, _248
from mastapy.gears.rating import _163
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Face', 'FaceGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetRating',)


class FaceGearSetRating(_163.GearSetRating):
    '''FaceGearSetRating

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetRating.TYPE'):
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
    def face_gear_set(self) -> '_761.FaceGearSetDesign':
        '''FaceGearSetDesign: 'FaceGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_761.FaceGearSetDesign)(self.wrapped.FaceGearSet) if self.wrapped.FaceGearSet else None

    @property
    def face_mesh_ratings(self) -> 'List[_247.FaceGearMeshRating]':
        '''List[FaceGearMeshRating]: 'FaceMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshRatings, constructor.new(_247.FaceGearMeshRating))
        return value

    @property
    def gear_ratings(self) -> 'List[_248.FaceGearRating]':
        '''List[FaceGearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_248.FaceGearRating))
        return value

    @property
    def face_gear_ratings(self) -> 'List[_248.FaceGearRating]':
        '''List[FaceGearRating]: 'FaceGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearRatings, constructor.new(_248.FaceGearRating))
        return value
