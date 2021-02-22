'''_1023.py

CylindricalGearMicroGeometryDutyCycle
'''


from mastapy.gears.analysis import _1125
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MICRO_GEOMETRY_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearMicroGeometryDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMicroGeometryDutyCycle',)


class CylindricalGearMicroGeometryDutyCycle(_1125.GearDesignAnalysis):
    '''CylindricalGearMicroGeometryDutyCycle

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MICRO_GEOMETRY_DUTY_CYCLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMicroGeometryDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
