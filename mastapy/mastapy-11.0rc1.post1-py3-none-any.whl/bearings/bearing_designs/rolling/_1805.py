'''_1805.py

ThreePointContactBallBearing
'''


from mastapy.bearings.bearing_designs.rolling import _1793
from mastapy._internal.python_net import python_net_import

_THREE_POINT_CONTACT_BALL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'ThreePointContactBallBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('ThreePointContactBallBearing',)


class ThreePointContactBallBearing(_1793.MultiPointContactBallBearing):
    '''ThreePointContactBallBearing

    This is a mastapy class.
    '''

    TYPE = _THREE_POINT_CONTACT_BALL_BEARING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ThreePointContactBallBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
