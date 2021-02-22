'''_622.py

CylindricalGearBendingStiffness
'''


from mastapy.gears.ltca import _609
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_BENDING_STIFFNESS = python_net_import('SMT.MastaAPI.Gears.LTCA.Cylindrical', 'CylindricalGearBendingStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearBendingStiffness',)


class CylindricalGearBendingStiffness(_609.GearBendingStiffness):
    '''CylindricalGearBendingStiffness

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_BENDING_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearBendingStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
