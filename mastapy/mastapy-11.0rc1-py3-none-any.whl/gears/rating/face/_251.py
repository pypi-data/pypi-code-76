'''_251.py

FaceGearSetDutyCycleRating
'''


from mastapy.gears.rating import _164
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Face', 'FaceGearSetDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetDutyCycleRating',)


class FaceGearSetDutyCycleRating(_164.GearSetDutyCycleRating):
    '''FaceGearSetDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_DUTY_CYCLE_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
