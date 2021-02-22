'''_1188.py

Damage
'''


from mastapy.utility.units_and_measurements.measurements import _1203
from mastapy._internal.python_net import python_net_import

_DAMAGE = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Damage')


__docformat__ = 'restructuredtext en'
__all__ = ('Damage',)


class Damage(_1203.FractionMeasurementBase):
    '''Damage

    This is a mastapy class.
    '''

    TYPE = _DAMAGE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Damage.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
