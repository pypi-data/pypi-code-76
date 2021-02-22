'''_1430.py

Percentage
'''


from mastapy.utility.units_and_measurements.measurements import _1394
from mastapy._internal.python_net import python_net_import

_PERCENTAGE = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Percentage')


__docformat__ = 'restructuredtext en'
__all__ = ('Percentage',)


class Percentage(_1394.FractionMeasurementBase):
    '''Percentage

    This is a mastapy class.
    '''

    TYPE = _PERCENTAGE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Percentage.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
