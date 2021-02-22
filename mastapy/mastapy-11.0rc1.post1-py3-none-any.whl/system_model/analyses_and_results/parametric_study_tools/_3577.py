'''_3577.py

DutyCycleResultsForSingleBearing
'''


from mastapy.bearings.bearing_results import _1604, _1612, _1615
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_results.rolling import (
    _1641, _1648, _1656, _1672,
    _1696
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE_RESULTS_FOR_SINGLE_BEARING = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'DutyCycleResultsForSingleBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCycleResultsForSingleBearing',)


class DutyCycleResultsForSingleBearing(_0.APIBase):
    '''DutyCycleResultsForSingleBearing

    This is a mastapy class.
    '''

    TYPE = _DUTY_CYCLE_RESULTS_FOR_SINGLE_BEARING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DutyCycleResultsForSingleBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_results(self) -> '_1604.LoadedBearingDutyCycle':
        '''LoadedBearingDutyCycle: 'DutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1604.LoadedBearingDutyCycle.TYPE not in self.wrapped.DutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle_results to LoadedBearingDutyCycle. Expected: {}.'.format(self.wrapped.DutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DutyCycleResults.__class__)(self.wrapped.DutyCycleResults) if self.wrapped.DutyCycleResults else None
