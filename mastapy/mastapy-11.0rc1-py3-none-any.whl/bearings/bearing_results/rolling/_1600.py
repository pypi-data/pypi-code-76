'''_1600.py

BallBearingRaceContactGeometry
'''


from mastapy._internal import constructor
from mastapy.math_utility import _1061
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BALL_BEARING_RACE_CONTACT_GEOMETRY = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'BallBearingRaceContactGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('BallBearingRaceContactGeometry',)


class BallBearingRaceContactGeometry(_0.APIBase):
    '''BallBearingRaceContactGeometry

    This is a mastapy class.
    '''

    TYPE = _BALL_BEARING_RACE_CONTACT_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BallBearingRaceContactGeometry.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def race_groove_radius(self) -> 'float':
        '''float: 'RaceGrooveRadius' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RaceGrooveRadius

    @property
    def ball_diameter(self) -> 'float':
        '''float: 'BallDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BallDiameter

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def race_centre(self) -> '_1061.Vector2D':
        '''Vector2D: 'RaceCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1061.Vector2D)(self.wrapped.RaceCentre) if self.wrapped.RaceCentre else None

    @property
    def ball_centre(self) -> '_1061.Vector2D':
        '''Vector2D: 'BallCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1061.Vector2D)(self.wrapped.BallCentre) if self.wrapped.BallCentre else None
