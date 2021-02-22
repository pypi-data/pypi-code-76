'''_290.py

GearSetOptimisationResult
'''


from mastapy.gears.gear_designs import _879
from mastapy._internal import constructor
from mastapy.gears.gear_designs.zerol_bevel import _883
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _888
from mastapy.gears.gear_designs.straight_bevel_diff import _892
from mastapy.gears.gear_designs.straight_bevel import _896
from mastapy.gears.gear_designs.spiral_bevel import _900
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _904
from mastapy.gears.gear_designs.klingelnberg_hypoid import _908
from mastapy.gears.gear_designs.klingelnberg_conical import _912
from mastapy.gears.gear_designs.hypoid import _916
from mastapy.gears.gear_designs.face import _924
from mastapy.gears.gear_designs.cylindrical import _955, _966
from mastapy.gears.gear_designs.conical import _1066
from mastapy.gears.gear_designs.concept import _1088
from mastapy.gears.gear_designs.bevel import _1092
from mastapy.gears.gear_designs.agma_gleason_conical import _1105
from mastapy.gears.rating import _315, _322, _323
from mastapy.gears.rating.zerol_bevel import _331
from mastapy.gears.rating.worm import _335, _336
from mastapy.gears.rating.straight_bevel_diff import _357
from mastapy.gears.rating.straight_bevel import _361
from mastapy.gears.rating.spiral_bevel import _364
from mastapy.gears.rating.klingelnberg_spiral_bevel import _367
from mastapy.gears.rating.klingelnberg_hypoid import _370
from mastapy.gears.rating.klingelnberg_conical import _373
from mastapy.gears.rating.hypoid import _400
from mastapy.gears.rating.face import _409, _410
from mastapy.gears.rating.cylindrical import _421, _422
from mastapy.gears.rating.conical import _488, _489
from mastapy.gears.rating.concept import _499, _500
from mastapy.gears.rating.bevel import _503
from mastapy.gears.rating.agma_gleason_conical import _514
from mastapy.math_utility.optimisation import _1306
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_SET_OPTIMISATION_RESULT = python_net_import('SMT.MastaAPI.Gears', 'GearSetOptimisationResult')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetOptimisationResult',)


class GearSetOptimisationResult(_0.APIBase):
    '''GearSetOptimisationResult

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_OPTIMISATION_RESULT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetOptimisationResult.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set(self) -> '_879.GearSetDesign':
        '''GearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _879.GearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to GearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_zerol_bevel_gear_set_design(self) -> '_883.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _883.ZerolBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_worm_gear_set_design(self) -> '_888.WormGearSetDesign':
        '''WormGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _888.WormGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to WormGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_straight_bevel_diff_gear_set_design(self) -> '_892.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _892.StraightBevelDiffGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_straight_bevel_gear_set_design(self) -> '_896.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _896.StraightBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_spiral_bevel_gear_set_design(self) -> '_900.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _900.SpiralBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_904.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _904.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_908.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _908.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_klingelnberg_conical_gear_set_design(self) -> '_912.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _912.KlingelnbergConicalGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_hypoid_gear_set_design(self) -> '_916.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _916.HypoidGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to HypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_face_gear_set_design(self) -> '_924.FaceGearSetDesign':
        '''FaceGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _924.FaceGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to FaceGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_cylindrical_gear_set_design(self) -> '_955.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _955.CylindricalGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to CylindricalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_cylindrical_planetary_gear_set_design(self) -> '_966.CylindricalPlanetaryGearSetDesign':
        '''CylindricalPlanetaryGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _966.CylindricalPlanetaryGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to CylindricalPlanetaryGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_conical_gear_set_design(self) -> '_1066.ConicalGearSetDesign':
        '''ConicalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1066.ConicalGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to ConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_concept_gear_set_design(self) -> '_1088.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1088.ConceptGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to ConceptGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_bevel_gear_set_design(self) -> '_1092.BevelGearSetDesign':
        '''BevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1092.BevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to BevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_agma_gleason_conical_gear_set_design(self) -> '_1105.AGMAGleasonConicalGearSetDesign':
        '''AGMAGleasonConicalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1105.AGMAGleasonConicalGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def rating(self) -> '_315.AbstractGearSetRating':
        '''AbstractGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _315.AbstractGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to AbstractGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_gear_set_duty_cycle_rating(self) -> '_322.GearSetDutyCycleRating':
        '''GearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _322.GearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to GearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_gear_set_rating(self) -> '_323.GearSetRating':
        '''GearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _323.GearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to GearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_zerol_bevel_gear_set_rating(self) -> '_331.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _331.ZerolBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ZerolBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_worm_gear_set_duty_cycle_rating(self) -> '_335.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _335.WormGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to WormGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_worm_gear_set_rating(self) -> '_336.WormGearSetRating':
        '''WormGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _336.WormGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to WormGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_straight_bevel_diff_gear_set_rating(self) -> '_357.StraightBevelDiffGearSetRating':
        '''StraightBevelDiffGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _357.StraightBevelDiffGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to StraightBevelDiffGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_straight_bevel_gear_set_rating(self) -> '_361.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _361.StraightBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to StraightBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_spiral_bevel_gear_set_rating(self) -> '_364.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _364.SpiralBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to SpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_rating(self) -> '_367.KlingelnbergCycloPalloidSpiralBevelGearSetRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _367.KlingelnbergCycloPalloidSpiralBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidSpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_rating(self) -> '_370.KlingelnbergCycloPalloidHypoidGearSetRating':
        '''KlingelnbergCycloPalloidHypoidGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _370.KlingelnbergCycloPalloidHypoidGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidHypoidGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_conical_gear_set_rating(self) -> '_373.KlingelnbergCycloPalloidConicalGearSetRating':
        '''KlingelnbergCycloPalloidConicalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _373.KlingelnbergCycloPalloidConicalGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidConicalGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_hypoid_gear_set_rating(self) -> '_400.HypoidGearSetRating':
        '''HypoidGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _400.HypoidGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to HypoidGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_face_gear_set_duty_cycle_rating(self) -> '_409.FaceGearSetDutyCycleRating':
        '''FaceGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _409.FaceGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to FaceGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_face_gear_set_rating(self) -> '_410.FaceGearSetRating':
        '''FaceGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _410.FaceGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to FaceGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_421.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _421.CylindricalGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_cylindrical_gear_set_rating(self) -> '_422.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _422.CylindricalGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to CylindricalGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_conical_gear_set_duty_cycle_rating(self) -> '_488.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _488.ConicalGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ConicalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_conical_gear_set_rating(self) -> '_489.ConicalGearSetRating':
        '''ConicalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _489.ConicalGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ConicalGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_concept_gear_set_duty_cycle_rating(self) -> '_499.ConceptGearSetDutyCycleRating':
        '''ConceptGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _499.ConceptGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ConceptGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_concept_gear_set_rating(self) -> '_500.ConceptGearSetRating':
        '''ConceptGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _500.ConceptGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ConceptGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_bevel_gear_set_rating(self) -> '_503.BevelGearSetRating':
        '''BevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _503.BevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to BevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_agma_gleason_conical_gear_set_rating(self) -> '_514.AGMAGleasonConicalGearSetRating':
        '''AGMAGleasonConicalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _514.AGMAGleasonConicalGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to AGMAGleasonConicalGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def optimisation_history(self) -> '_1306.OptimisationHistory':
        '''OptimisationHistory: 'OptimisationHistory' is the original name of this property.'''

        return constructor.new(_1306.OptimisationHistory)(self.wrapped.OptimisationHistory) if self.wrapped.OptimisationHistory else None

    @optimisation_history.setter
    def optimisation_history(self, value: '_1306.OptimisationHistory'):
        value = value.wrapped if value else None
        self.wrapped.OptimisationHistory = value

    @property
    def is_optimized(self) -> 'bool':
        '''bool: 'IsOptimized' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsOptimized
