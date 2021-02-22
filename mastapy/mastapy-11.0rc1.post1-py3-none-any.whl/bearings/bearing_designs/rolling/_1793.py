'''_1793.py

MultiPointContactBallBearing
'''


from mastapy._internal import constructor
from mastapy.bearings.bearing_designs.rolling import _1780
from mastapy._internal.python_net import python_net_import

_MULTI_POINT_CONTACT_BALL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'MultiPointContactBallBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('MultiPointContactBallBearing',)


class MultiPointContactBallBearing(_1780.BallBearing):
    '''MultiPointContactBallBearing

    This is a mastapy class.
    '''

    TYPE = _MULTI_POINT_CONTACT_BALL_BEARING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MultiPointContactBallBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def inner_shim_width(self) -> 'float':
        '''float: 'InnerShimWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerShimWidth

    @property
    def inner_shim_angle(self) -> 'float':
        '''float: 'InnerShimAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerShimAngle
