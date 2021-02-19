'''_1364.py

SpecificHeat
'''


from mastapy.utility.units_and_measurements import _1274
from mastapy._internal.python_net import python_net_import

_SPECIFIC_HEAT = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'SpecificHeat')


__docformat__ = 'restructuredtext en'
__all__ = ('SpecificHeat',)


class SpecificHeat(_1274.MeasurementBase):
    '''SpecificHeat

    This is a mastapy class.
    '''

    TYPE = _SPECIFIC_HEAT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpecificHeat.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
