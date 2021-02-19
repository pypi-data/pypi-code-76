'''_1340.py

MassPerUnitTime
'''


from mastapy.utility.units_and_measurements import _1274
from mastapy._internal.python_net import python_net_import

_MASS_PER_UNIT_TIME = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'MassPerUnitTime')


__docformat__ = 'restructuredtext en'
__all__ = ('MassPerUnitTime',)


class MassPerUnitTime(_1274.MeasurementBase):
    '''MassPerUnitTime

    This is a mastapy class.
    '''

    TYPE = _MASS_PER_UNIT_TIME

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassPerUnitTime.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
