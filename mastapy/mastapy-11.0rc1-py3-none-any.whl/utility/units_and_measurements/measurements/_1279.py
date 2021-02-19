'''_1279.py

Voltage
'''


from mastapy.utility.units_and_measurements import _1168
from mastapy._internal.python_net import python_net_import

_VOLTAGE = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Voltage')


__docformat__ = 'restructuredtext en'
__all__ = ('Voltage',)


class Voltage(_1168.MeasurementBase):
    '''Voltage

    This is a mastapy class.
    '''

    TYPE = _VOLTAGE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Voltage.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
