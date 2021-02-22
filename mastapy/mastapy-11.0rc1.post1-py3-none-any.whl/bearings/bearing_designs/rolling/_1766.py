'''_1766.py

CylindricalRollerBearing
'''


from mastapy._internal import constructor
from mastapy.bearings.bearing_designs.rolling import _1773
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_ROLLER_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'CylindricalRollerBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalRollerBearing',)


class CylindricalRollerBearing(_1773.NonBarrelRollerBearing):
    '''CylindricalRollerBearing

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_ROLLER_BEARING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalRollerBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def reference_rotation_speed(self) -> 'float':
        '''float: 'ReferenceRotationSpeed' is the original name of this property.'''

        return self.wrapped.ReferenceRotationSpeed

    @reference_rotation_speed.setter
    def reference_rotation_speed(self, value: 'float'):
        self.wrapped.ReferenceRotationSpeed = float(value) if value else 0.0
