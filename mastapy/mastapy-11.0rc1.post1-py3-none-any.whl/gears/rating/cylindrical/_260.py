'''_260.py

CylindricalGearSetDutyCycleRating
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _786, _795
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.cylindrical.optimisation import _292
from mastapy.gears.rating.cylindrical import _263
from mastapy.gears.rating import _161
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalGearSetDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetDutyCycleRating',)


class CylindricalGearSetDutyCycleRating(_161.GearSetDutyCycleRating):
    '''CylindricalGearSetDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_DUTY_CYCLE_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def set_profile_shift_to_maximum_safety_factor_fatigue_and_static(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SetProfileShiftToMaximumSafetyFactorFatigueAndStatic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetProfileShiftToMaximumSafetyFactorFatigueAndStatic

    @property
    def cylindrical_gear_set(self) -> '_786.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'CylindricalGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _786.CylindricalGearSetDesign.TYPE not in self.wrapped.CylindricalGearSet.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_set to CylindricalGearSetDesign. Expected: {}.'.format(self.wrapped.CylindricalGearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalGearSet.__class__)(self.wrapped.CylindricalGearSet) if self.wrapped.CylindricalGearSet else None

    @property
    def optimisations(self) -> '_292.CylindricalGearSetRatingOptimisationHelper':
        '''CylindricalGearSetRatingOptimisationHelper: 'Optimisations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_292.CylindricalGearSetRatingOptimisationHelper)(self.wrapped.Optimisations) if self.wrapped.Optimisations else None

    @property
    def gear_mesh_duty_cycle_ratings(self) -> 'List[_263.CylindricalMeshDutyCycleRating]':
        '''List[CylindricalMeshDutyCycleRating]: 'GearMeshDutyCycleRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearMeshDutyCycleRatings, constructor.new(_263.CylindricalMeshDutyCycleRating))
        return value

    @property
    def cylindrical_mesh_duty_cycle_ratings(self) -> 'List[_263.CylindricalMeshDutyCycleRating]':
        '''List[CylindricalMeshDutyCycleRating]: 'CylindricalMeshDutyCycleRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshDutyCycleRatings, constructor.new(_263.CylindricalMeshDutyCycleRating))
        return value
