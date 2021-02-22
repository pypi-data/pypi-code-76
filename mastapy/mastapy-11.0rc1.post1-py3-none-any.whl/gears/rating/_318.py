'''_318.py

GearDutyCycleRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating import (
    _322, _319, _321, _314
)
from mastapy.gears.rating.worm import _335
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _409
from mastapy.gears.rating.cylindrical import _421, _413, _414
from mastapy.gears.rating.conical import _488
from mastapy.gears.rating.concept import _499
from mastapy._internal.python_net import python_net_import

_GEAR_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating', 'GearDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('GearDutyCycleRating',)


class GearDutyCycleRating(_314.AbstractGearRating):
    '''GearDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _GEAR_DUTY_CYCLE_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def damage_bending(self) -> 'float':
        '''float: 'DamageBending' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DamageBending

    @property
    def damage_contact(self) -> 'float':
        '''float: 'DamageContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DamageContact

    @property
    def maximum_contact_stress(self) -> 'float':
        '''float: 'MaximumContactStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumContactStress

    @property
    def maximum_bending_stress(self) -> 'float':
        '''float: 'MaximumBendingStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumBendingStress

    @property
    def gear_set_design_duty_cycle(self) -> '_322.GearSetDutyCycleRating':
        '''GearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _322.GearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDesignDutyCycle.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design_duty_cycle to GearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDesignDutyCycle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesignDutyCycle.__class__)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def gear_set_design_duty_cycle_of_type_worm_gear_set_duty_cycle_rating(self) -> '_335.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _335.WormGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDesignDutyCycle.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design_duty_cycle to WormGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDesignDutyCycle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesignDutyCycle.__class__)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def gear_set_design_duty_cycle_of_type_face_gear_set_duty_cycle_rating(self) -> '_409.FaceGearSetDutyCycleRating':
        '''FaceGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _409.FaceGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDesignDutyCycle.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design_duty_cycle to FaceGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDesignDutyCycle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesignDutyCycle.__class__)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def gear_set_design_duty_cycle_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_421.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _421.CylindricalGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDesignDutyCycle.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design_duty_cycle to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDesignDutyCycle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesignDutyCycle.__class__)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def gear_set_design_duty_cycle_of_type_conical_gear_set_duty_cycle_rating(self) -> '_488.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _488.ConicalGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDesignDutyCycle.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design_duty_cycle to ConicalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDesignDutyCycle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesignDutyCycle.__class__)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def gear_set_design_duty_cycle_of_type_concept_gear_set_duty_cycle_rating(self) -> '_499.ConceptGearSetDutyCycleRating':
        '''ConceptGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _499.ConceptGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDesignDutyCycle.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design_duty_cycle to ConceptGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDesignDutyCycle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesignDutyCycle.__class__)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def left_flank_rating(self) -> '_319.GearFlankRating':
        '''GearFlankRating: 'LeftFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _319.GearFlankRating.TYPE not in self.wrapped.LeftFlankRating.__class__.__mro__:
            raise CastException('Failed to cast left_flank_rating to GearFlankRating. Expected: {}.'.format(self.wrapped.LeftFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LeftFlankRating.__class__)(self.wrapped.LeftFlankRating) if self.wrapped.LeftFlankRating else None

    @property
    def right_flank_rating(self) -> '_319.GearFlankRating':
        '''GearFlankRating: 'RightFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _319.GearFlankRating.TYPE not in self.wrapped.RightFlankRating.__class__.__mro__:
            raise CastException('Failed to cast right_flank_rating to GearFlankRating. Expected: {}.'.format(self.wrapped.RightFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RightFlankRating.__class__)(self.wrapped.RightFlankRating) if self.wrapped.RightFlankRating else None

    @property
    def gear_ratings(self) -> 'List[_321.GearRating]':
        '''List[GearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_321.GearRating))
        return value
