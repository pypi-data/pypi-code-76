'''_1460.py

Time
'''


from mastapy.utility.units_and_measurements import _1359
from mastapy._internal.python_net import python_net_import

_TIME = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Time')


__docformat__ = 'restructuredtext en'
__all__ = ('Time',)


class Time(_1359.MeasurementBase):
    '''Time

    This is a mastapy class.
    '''

    TYPE = _TIME

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Time.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
