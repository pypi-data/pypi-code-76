'''_491.py

ConicalMeshDutyCycleRating
'''


from typing import List

from mastapy.gears.rating.conical import _486
from mastapy._internal import constructor, conversion
from mastapy.gears.rating import _325
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Conical', 'ConicalMeshDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshDutyCycleRating',)


class ConicalMeshDutyCycleRating(_325.MeshDutyCycleRating):
    '''ConicalMeshDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _CONICAL_MESH_DUTY_CYCLE_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalMeshDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def conical_mesh_ratings(self) -> 'List[_486.ConicalGearMeshRating]':
        '''List[ConicalGearMeshRating]: 'ConicalMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConicalMeshRatings, constructor.new(_486.ConicalGearMeshRating))
        return value
