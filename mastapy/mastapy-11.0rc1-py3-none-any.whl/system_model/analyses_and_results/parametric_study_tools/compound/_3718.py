'''_3718.py

GearSetCompoundParametricStudyTool
'''


from mastapy.gears.rating import _161
from mastapy._internal import constructor
from mastapy.gears.rating.worm import _174
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _248
from mastapy.gears.rating.cylindrical import _260
from mastapy.gears.rating.conical import _324
from mastapy.gears.rating.concept import _335
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3755
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'GearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetCompoundParametricStudyTool',)


class GearSetCompoundParametricStudyTool(_3755.SpecialisedAssemblyCompoundParametricStudyTool):
    '''GearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set_duty_cycle_results(self) -> '_161.GearSetDutyCycleRating':
        '''GearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _161.GearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to GearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDutyCycleResults.__class__)(self.wrapped.GearSetDutyCycleResults) if self.wrapped.GearSetDutyCycleResults else None

    @property
    def gear_set_duty_cycle_results_of_type_worm_gear_set_duty_cycle_rating(self) -> '_174.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _174.WormGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to WormGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDutyCycleResults.__class__)(self.wrapped.GearSetDutyCycleResults) if self.wrapped.GearSetDutyCycleResults else None

    @property
    def gear_set_duty_cycle_results_of_type_face_gear_set_duty_cycle_rating(self) -> '_248.FaceGearSetDutyCycleRating':
        '''FaceGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _248.FaceGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to FaceGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDutyCycleResults.__class__)(self.wrapped.GearSetDutyCycleResults) if self.wrapped.GearSetDutyCycleResults else None

    @property
    def gear_set_duty_cycle_results_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_260.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _260.CylindricalGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDutyCycleResults.__class__)(self.wrapped.GearSetDutyCycleResults) if self.wrapped.GearSetDutyCycleResults else None

    @property
    def gear_set_duty_cycle_results_of_type_conical_gear_set_duty_cycle_rating(self) -> '_324.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _324.ConicalGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to ConicalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDutyCycleResults.__class__)(self.wrapped.GearSetDutyCycleResults) if self.wrapped.GearSetDutyCycleResults else None

    @property
    def gear_set_duty_cycle_results_of_type_concept_gear_set_duty_cycle_rating(self) -> '_335.ConceptGearSetDutyCycleRating':
        '''ConceptGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _335.ConceptGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to ConceptGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDutyCycleResults.__class__)(self.wrapped.GearSetDutyCycleResults) if self.wrapped.GearSetDutyCycleResults else None
