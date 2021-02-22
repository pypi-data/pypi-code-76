'''_2470.py

GearCompoundSystemDeflection
'''


from mastapy.gears.rating import _157
from mastapy._internal import constructor
from mastapy.gears.rating.worm import _171
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _244
from mastapy.gears.rating.cylindrical import _251
from mastapy.gears.rating.conical import _321
from mastapy.gears.rating.concept import _331
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2490
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'GearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundSystemDeflection',)


class GearCompoundSystemDeflection(_2490.MountableComponentCompoundSystemDeflection):
    '''GearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_rating(self) -> '_157.GearDutyCycleRating':
        '''GearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _157.GearDutyCycleRating.TYPE not in self.wrapped.DutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle_rating to GearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DutyCycleRating.__class__)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_worm_gear_duty_cycle_rating(self) -> '_171.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _171.WormGearDutyCycleRating.TYPE not in self.wrapped.DutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle_rating to WormGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DutyCycleRating.__class__)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_face_gear_duty_cycle_rating(self) -> '_244.FaceGearDutyCycleRating':
        '''FaceGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _244.FaceGearDutyCycleRating.TYPE not in self.wrapped.DutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle_rating to FaceGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DutyCycleRating.__class__)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_cylindrical_gear_duty_cycle_rating(self) -> '_251.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _251.CylindricalGearDutyCycleRating.TYPE not in self.wrapped.DutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle_rating to CylindricalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DutyCycleRating.__class__)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_conical_gear_duty_cycle_rating(self) -> '_321.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _321.ConicalGearDutyCycleRating.TYPE not in self.wrapped.DutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle_rating to ConicalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DutyCycleRating.__class__)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_concept_gear_duty_cycle_rating(self) -> '_331.ConceptGearDutyCycleRating':
        '''ConceptGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _331.ConceptGearDutyCycleRating.TYPE not in self.wrapped.DutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle_rating to ConceptGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DutyCycleRating.__class__)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None
