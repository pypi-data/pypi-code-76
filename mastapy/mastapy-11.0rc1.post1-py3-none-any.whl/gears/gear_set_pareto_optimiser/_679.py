'''_679.py

GearSetOptimiserCandidate
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.gears.rating import _154, _161, _162
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.zerol_bevel import _170
from mastapy.gears.rating.worm import _174, _175
from mastapy.gears.rating.straight_bevel_diff import _196
from mastapy.gears.rating.straight_bevel import _200
from mastapy.gears.rating.spiral_bevel import _203
from mastapy.gears.rating.klingelnberg_spiral_bevel import _206
from mastapy.gears.rating.klingelnberg_hypoid import _209
from mastapy.gears.rating.klingelnberg_conical import _212
from mastapy.gears.rating.hypoid import _239
from mastapy.gears.rating.face import _248, _249
from mastapy.gears.rating.cylindrical import _260, _261
from mastapy.gears.rating.conical import _324, _325
from mastapy.gears.rating.concept import _335, _336
from mastapy.gears.rating.bevel import _339
from mastapy.gears.rating.agma_gleason_conical import _350
from mastapy.gears.gear_set_pareto_optimiser import _675
from mastapy._internal.python_net import python_net_import

_GEAR_SET_OPTIMISER_CANDIDATE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'GearSetOptimiserCandidate')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetOptimiserCandidate',)


class GearSetOptimiserCandidate(_675.DesignSpaceSearchCandidateBase['_154.AbstractGearSetRating', 'GearSetOptimiserCandidate']):
    '''GearSetOptimiserCandidate

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_OPTIMISER_CANDIDATE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetOptimiserCandidate.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def add_design(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddDesign

    @property
    def candidate(self) -> '_154.AbstractGearSetRating':
        '''AbstractGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _154.AbstractGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to AbstractGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_gear_set_duty_cycle_rating(self) -> '_161.GearSetDutyCycleRating':
        '''GearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _161.GearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to GearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_gear_set_rating(self) -> '_162.GearSetRating':
        '''GearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _162.GearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to GearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_zerol_bevel_gear_set_rating(self) -> '_170.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _170.ZerolBevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ZerolBevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_worm_gear_set_duty_cycle_rating(self) -> '_174.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _174.WormGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to WormGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_worm_gear_set_rating(self) -> '_175.WormGearSetRating':
        '''WormGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _175.WormGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to WormGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_straight_bevel_diff_gear_set_rating(self) -> '_196.StraightBevelDiffGearSetRating':
        '''StraightBevelDiffGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _196.StraightBevelDiffGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to StraightBevelDiffGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_straight_bevel_gear_set_rating(self) -> '_200.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _200.StraightBevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to StraightBevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_spiral_bevel_gear_set_rating(self) -> '_203.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _203.SpiralBevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to SpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_rating(self) -> '_206.KlingelnbergCycloPalloidSpiralBevelGearSetRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _206.KlingelnbergCycloPalloidSpiralBevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to KlingelnbergCycloPalloidSpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_rating(self) -> '_209.KlingelnbergCycloPalloidHypoidGearSetRating':
        '''KlingelnbergCycloPalloidHypoidGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _209.KlingelnbergCycloPalloidHypoidGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to KlingelnbergCycloPalloidHypoidGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_klingelnberg_cyclo_palloid_conical_gear_set_rating(self) -> '_212.KlingelnbergCycloPalloidConicalGearSetRating':
        '''KlingelnbergCycloPalloidConicalGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _212.KlingelnbergCycloPalloidConicalGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to KlingelnbergCycloPalloidConicalGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_hypoid_gear_set_rating(self) -> '_239.HypoidGearSetRating':
        '''HypoidGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _239.HypoidGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to HypoidGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_face_gear_set_duty_cycle_rating(self) -> '_248.FaceGearSetDutyCycleRating':
        '''FaceGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _248.FaceGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to FaceGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_face_gear_set_rating(self) -> '_249.FaceGearSetRating':
        '''FaceGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _249.FaceGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to FaceGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_260.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _260.CylindricalGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_cylindrical_gear_set_rating(self) -> '_261.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _261.CylindricalGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to CylindricalGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_conical_gear_set_duty_cycle_rating(self) -> '_324.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _324.ConicalGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ConicalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_conical_gear_set_rating(self) -> '_325.ConicalGearSetRating':
        '''ConicalGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _325.ConicalGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ConicalGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_concept_gear_set_duty_cycle_rating(self) -> '_335.ConceptGearSetDutyCycleRating':
        '''ConceptGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _335.ConceptGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ConceptGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_concept_gear_set_rating(self) -> '_336.ConceptGearSetRating':
        '''ConceptGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _336.ConceptGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ConceptGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_bevel_gear_set_rating(self) -> '_339.BevelGearSetRating':
        '''BevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _339.BevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to BevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_agma_gleason_conical_gear_set_rating(self) -> '_350.AGMAGleasonConicalGearSetRating':
        '''AGMAGleasonConicalGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _350.AGMAGleasonConicalGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to AGMAGleasonConicalGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None
