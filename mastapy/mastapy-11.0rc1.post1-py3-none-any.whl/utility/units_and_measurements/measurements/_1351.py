'''_1351.py

PowerSmallPerUnitAreaPerUnitTime
'''


from mastapy.utility.units_and_measurements import _1274
from mastapy._internal.python_net import python_net_import

_POWER_SMALL_PER_UNIT_AREA_PER_UNIT_TIME = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'PowerSmallPerUnitAreaPerUnitTime')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerSmallPerUnitAreaPerUnitTime',)


class PowerSmallPerUnitAreaPerUnitTime(_1274.MeasurementBase):
    '''PowerSmallPerUnitAreaPerUnitTime

    This is a mastapy class.
    '''

    TYPE = _POWER_SMALL_PER_UNIT_AREA_PER_UNIT_TIME

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerSmallPerUnitAreaPerUnitTime.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
