'''_1250.py

PressureViscosityCoefficient
'''


from mastapy.utility.units_and_measurements import _1168
from mastapy._internal.python_net import python_net_import

_PRESSURE_VISCOSITY_COEFFICIENT = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'PressureViscosityCoefficient')


__docformat__ = 'restructuredtext en'
__all__ = ('PressureViscosityCoefficient',)


class PressureViscosityCoefficient(_1168.MeasurementBase):
    '''PressureViscosityCoefficient

    This is a mastapy class.
    '''

    TYPE = _PRESSURE_VISCOSITY_COEFFICIENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PressureViscosityCoefficient.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
