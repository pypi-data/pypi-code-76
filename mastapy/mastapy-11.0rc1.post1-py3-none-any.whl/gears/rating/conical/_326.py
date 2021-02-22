'''_326.py

ConicalGearSingleFlankRating
'''


from mastapy.gears.rating import _163
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Conical', 'ConicalGearSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearSingleFlankRating',)


class ConicalGearSingleFlankRating(_163.GearSingleFlankRating):
    '''ConicalGearSingleFlankRating

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_SINGLE_FLANK_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
