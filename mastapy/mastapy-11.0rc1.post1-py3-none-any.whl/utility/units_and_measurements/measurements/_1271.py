'''_1271.py

TimeVeryShort
'''


from mastapy.utility.units_and_measurements import _1168
from mastapy._internal.python_net import python_net_import

_TIME_VERY_SHORT = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'TimeVeryShort')


__docformat__ = 'restructuredtext en'
__all__ = ('TimeVeryShort',)


class TimeVeryShort(_1168.MeasurementBase):
    '''TimeVeryShort

    This is a mastapy class.
    '''

    TYPE = _TIME_VERY_SHORT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TimeVeryShort.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
