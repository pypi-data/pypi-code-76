'''_1568.py

RollerBearingCrownedProfile
'''


from mastapy._internal import constructor
from mastapy.bearings.roller_bearing_profiles import _1573
from mastapy._internal.python_net import python_net_import

_ROLLER_BEARING_CROWNED_PROFILE = python_net_import('SMT.MastaAPI.Bearings.RollerBearingProfiles', 'RollerBearingCrownedProfile')


__docformat__ = 'restructuredtext en'
__all__ = ('RollerBearingCrownedProfile',)


class RollerBearingCrownedProfile(_1573.RollerBearingProfile):
    '''RollerBearingCrownedProfile

    This is a mastapy class.
    '''

    TYPE = _ROLLER_BEARING_CROWNED_PROFILE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollerBearingCrownedProfile.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def crown_radius(self) -> 'float':
        '''float: 'CrownRadius' is the original name of this property.'''

        return self.wrapped.CrownRadius

    @crown_radius.setter
    def crown_radius(self, value: 'float'):
        self.wrapped.CrownRadius = float(value) if value else 0.0

    @property
    def parallel_length(self) -> 'float':
        '''float: 'ParallelLength' is the original name of this property.'''

        return self.wrapped.ParallelLength

    @parallel_length.setter
    def parallel_length(self, value: 'float'):
        self.wrapped.ParallelLength = float(value) if value else 0.0

    @property
    def offset(self) -> 'float':
        '''float: 'Offset' is the original name of this property.'''

        return self.wrapped.Offset

    @offset.setter
    def offset(self, value: 'float'):
        self.wrapped.Offset = float(value) if value else 0.0
