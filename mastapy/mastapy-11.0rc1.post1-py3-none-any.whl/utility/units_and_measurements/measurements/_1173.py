'''_1173.py

Cycles
'''


from mastapy.utility.units_and_measurements import _1154
from mastapy._internal.python_net import python_net_import

_CYCLES = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Cycles')


__docformat__ = 'restructuredtext en'
__all__ = ('Cycles',)


class Cycles(_1154.MeasurementBase):
    '''Cycles

    This is a mastapy class.
    '''

    TYPE = _CYCLES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Cycles.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
