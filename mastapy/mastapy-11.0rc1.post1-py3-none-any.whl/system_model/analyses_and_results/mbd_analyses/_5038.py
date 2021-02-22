'''_5038.py

BearingMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2114
from mastapy.system_model.analyses_and_results.static_loads import _6451
from mastapy.system_model.analyses_and_results.mbd_analyses.reporting import _5177
from mastapy.system_model.analyses_and_results.mbd_analyses import _5068
from mastapy._internal.python_net import python_net_import

_BEARING_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BearingMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingMultibodyDynamicsAnalysis',)


class BearingMultibodyDynamicsAnalysis(_5068.ConnectorMultibodyDynamicsAnalysis):
    '''BearingMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def iso2812007_basic_rating_life_damage_rate(self) -> 'float':
        '''float: 'ISO2812007BasicRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007BasicRatingLifeDamageRate

    @property
    def iso2812007_basic_rating_life_damage_during_analysis(self) -> 'float':
        '''float: 'ISO2812007BasicRatingLifeDamageDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007BasicRatingLifeDamageDuringAnalysis

    @property
    def iso2812007_modified_rating_life_damage_rate(self) -> 'float':
        '''float: 'ISO2812007ModifiedRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007ModifiedRatingLifeDamageRate

    @property
    def iso2812007_modified_rating_life_damage_during_analysis(self) -> 'float':
        '''float: 'ISO2812007ModifiedRatingLifeDamageDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007ModifiedRatingLifeDamageDuringAnalysis

    @property
    def isots162812008_basic_reference_rating_life_damage_rate(self) -> 'float':
        '''float: 'ISOTS162812008BasicReferenceRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008BasicReferenceRatingLifeDamageRate

    @property
    def isots162812008_basic_reference_rating_life_damage_during_analysis(self) -> 'float':
        '''float: 'ISOTS162812008BasicReferenceRatingLifeDamageDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008BasicReferenceRatingLifeDamageDuringAnalysis

    @property
    def isots162812008_modified_reference_rating_life_damage_rate(self) -> 'float':
        '''float: 'ISOTS162812008ModifiedReferenceRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008ModifiedReferenceRatingLifeDamageRate

    @property
    def isots162812008_modified_reference_rating_life_damage_during_analysis(self) -> 'float':
        '''float: 'ISOTS162812008ModifiedReferenceRatingLifeDamageDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008ModifiedReferenceRatingLifeDamageDuringAnalysis

    @property
    def iso762006_safety_factor_at_current_time(self) -> 'float':
        '''float: 'ISO762006SafetyFactorAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO762006SafetyFactorAtCurrentTime

    @property
    def iso762006_safety_factor(self) -> 'float':
        '''float: 'ISO762006SafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO762006SafetyFactor

    @property
    def ansiabma_static_safety_factor_at_current_time(self) -> 'float':
        '''float: 'ANSIABMAStaticSafetyFactorAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ANSIABMAStaticSafetyFactorAtCurrentTime

    @property
    def ansiabma_static_safety_factor(self) -> 'float':
        '''float: 'ANSIABMAStaticSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ANSIABMAStaticSafetyFactor

    @property
    def ansiabma_basic_rating_life_damage_rate(self) -> 'float':
        '''float: 'ANSIABMABasicRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ANSIABMABasicRatingLifeDamageRate

    @property
    def ansiabma_basic_rating_life_damage_rate_during_analysis(self) -> 'float':
        '''float: 'ANSIABMABasicRatingLifeDamageRateDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ANSIABMABasicRatingLifeDamageRateDuringAnalysis

    @property
    def ansiabma_adjusted_rating_life_damage_rate(self) -> 'float':
        '''float: 'ANSIABMAAdjustedRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ANSIABMAAdjustedRatingLifeDamageRate

    @property
    def ansiabma_adjusted_rating_life_damage_rate_during_analysis(self) -> 'float':
        '''float: 'ANSIABMAAdjustedRatingLifeDamageRateDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ANSIABMAAdjustedRatingLifeDamageRateDuringAnalysis

    @property
    def maximum_static_contact_stress_inner_safety_factor_at_current_time(self) -> 'float':
        '''float: 'MaximumStaticContactStressInnerSafetyFactorAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumStaticContactStressInnerSafetyFactorAtCurrentTime

    @property
    def maximum_static_contact_stress_inner_safety_factor(self) -> 'float':
        '''float: 'MaximumStaticContactStressInnerSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumStaticContactStressInnerSafetyFactor

    @property
    def maximum_element_normal_stress_outer_at_current_time(self) -> 'float':
        '''float: 'MaximumElementNormalStressOuterAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumElementNormalStressOuterAtCurrentTime

    @property
    def maximum_element_normal_stress_outer(self) -> 'float':
        '''float: 'MaximumElementNormalStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumElementNormalStressOuter

    @property
    def maximum_element_normal_stress_inner_at_current_time(self) -> 'float':
        '''float: 'MaximumElementNormalStressInnerAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumElementNormalStressInnerAtCurrentTime

    @property
    def maximum_element_normal_stress_inner(self) -> 'float':
        '''float: 'MaximumElementNormalStressInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumElementNormalStressInner

    @property
    def maximum_static_contact_stress_outer_safety_factor_at_current_time(self) -> 'float':
        '''float: 'MaximumStaticContactStressOuterSafetyFactorAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumStaticContactStressOuterSafetyFactorAtCurrentTime

    @property
    def maximum_static_contact_stress_outer_safety_factor(self) -> 'float':
        '''float: 'MaximumStaticContactStressOuterSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumStaticContactStressOuterSafetyFactor

    @property
    def component_design(self) -> '_2114.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6451.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6451.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def peak_dynamic_force(self) -> '_5177.DynamicForceVector3DResult':
        '''DynamicForceVector3DResult: 'PeakDynamicForce' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5177.DynamicForceVector3DResult)(self.wrapped.PeakDynamicForce) if self.wrapped.PeakDynamicForce else None

    @property
    def planetaries(self) -> 'List[BearingMultibodyDynamicsAnalysis]':
        '''List[BearingMultibodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingMultibodyDynamicsAnalysis))
        return value
