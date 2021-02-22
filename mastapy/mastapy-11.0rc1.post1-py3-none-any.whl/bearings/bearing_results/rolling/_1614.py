'''_1614.py

LoadedAngularContactThrustBallBearingRow
'''


from mastapy.bearings.bearing_results.rolling import _1613, _1611
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_LOADED_ANGULAR_CONTACT_THRUST_BALL_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedAngularContactThrustBallBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedAngularContactThrustBallBearingRow',)


class LoadedAngularContactThrustBallBearingRow(_1611.LoadedAngularContactBallBearingRow):
    '''LoadedAngularContactThrustBallBearingRow

    This is a mastapy class.
    '''

    TYPE = _LOADED_ANGULAR_CONTACT_THRUST_BALL_BEARING_ROW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedAngularContactThrustBallBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def loaded_bearing(self) -> '_1613.LoadedAngularContactThrustBallBearingResults':
        '''LoadedAngularContactThrustBallBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1613.LoadedAngularContactThrustBallBearingResults)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None
