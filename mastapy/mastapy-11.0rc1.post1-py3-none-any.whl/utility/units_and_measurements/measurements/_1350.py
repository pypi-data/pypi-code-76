'''_1350.py

PowerSmallPerArea
'''


from mastapy.utility.units_and_measurements import _1274
from mastapy._internal.python_net import python_net_import

_POWER_SMALL_PER_AREA = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'PowerSmallPerArea')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerSmallPerArea',)


class PowerSmallPerArea(_1274.MeasurementBase):
    '''PowerSmallPerArea

    This is a mastapy class.
    '''

    TYPE = _POWER_SMALL_PER_AREA

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerSmallPerArea.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
