'''_1349.py

PowerSmall
'''


from mastapy.utility.units_and_measurements import _1274
from mastapy._internal.python_net import python_net_import

_POWER_SMALL = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'PowerSmall')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerSmall',)


class PowerSmall(_1274.MeasurementBase):
    '''PowerSmall

    This is a mastapy class.
    '''

    TYPE = _POWER_SMALL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerSmall.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
