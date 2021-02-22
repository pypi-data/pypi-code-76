'''_866.py

ProfileReliefWithDeviation
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _783
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _868
from mastapy._internal.python_net import python_net_import

_PROFILE_RELIEF_WITH_DEVIATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'ProfileReliefWithDeviation')


__docformat__ = 'restructuredtext en'
__all__ = ('ProfileReliefWithDeviation',)


class ProfileReliefWithDeviation(_868.ReliefWithDeviation):
    '''ProfileReliefWithDeviation

    This is a mastapy class.
    '''

    TYPE = _PROFILE_RELIEF_WITH_DEVIATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ProfileReliefWithDeviation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def roll_distance(self) -> 'float':
        '''float: 'RollDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RollDistance

    @property
    def profile_relief(self) -> 'float':
        '''float: 'ProfileRelief' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ProfileRelief

    @property
    def position_on_profile(self) -> '_783.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'PositionOnProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_783.CylindricalGearProfileMeasurement)(self.wrapped.PositionOnProfile) if self.wrapped.PositionOnProfile else None
