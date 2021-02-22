'''_4998.py

BearingMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2005
from mastapy.system_model.analyses_and_results.static_loads import _6083
from mastapy.system_model.analyses_and_results.mbd_analyses.reporting import _5132
from mastapy.system_model.analyses_and_results.mbd_analyses import _5028
from mastapy._internal.python_net import python_net_import

_BEARING_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BearingMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingMultiBodyDynamicsAnalysis',)


class BearingMultiBodyDynamicsAnalysis(_5028.ConnectorMultiBodyDynamicsAnalysis):
    '''BearingMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingMultiBodyDynamicsAnalysis.TYPE'):
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
    def component_design(self) -> '_2005.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2005.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6083.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6083.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def peak_dynamic_force(self) -> '_5132.DynamicForceVector3DResult':
        '''DynamicForceVector3DResult: 'PeakDynamicForce' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5132.DynamicForceVector3DResult)(self.wrapped.PeakDynamicForce) if self.wrapped.PeakDynamicForce else None

    @property
    def planetaries(self) -> 'List[BearingMultiBodyDynamicsAnalysis]':
        '''List[BearingMultiBodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingMultiBodyDynamicsAnalysis))
        return value
