'''_245.py

FaceGearMeshDutyCycleRating
'''


from mastapy.gears.rating import _164
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Face', 'FaceGearMeshDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshDutyCycleRating',)


class FaceGearMeshDutyCycleRating(_164.MeshDutyCycleRating):
    '''FaceGearMeshDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_DUTY_CYCLE_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
