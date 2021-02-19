'''_1308.py

ForcePerUnitTemperature
'''


from mastapy.utility.units_and_measurements import _1274
from mastapy._internal.python_net import python_net_import

_FORCE_PER_UNIT_TEMPERATURE = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'ForcePerUnitTemperature')


__docformat__ = 'restructuredtext en'
__all__ = ('ForcePerUnitTemperature',)


class ForcePerUnitTemperature(_1274.MeasurementBase):
    '''ForcePerUnitTemperature

    This is a mastapy class.
    '''

    TYPE = _FORCE_PER_UNIT_TEMPERATURE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ForcePerUnitTemperature.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
