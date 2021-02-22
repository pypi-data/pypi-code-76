'''_1727.py

LoadedRollingBearingResults
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings import _1589
from mastapy.bearings.bearing_results.rolling.fitting import _1803, _1801, _1804
from mastapy.bearings.bearing_results.rolling import (
    _1671, _1768, _1668, _1755,
    _1728
)
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_results.rolling.abma import _1807, _1805, _1806
from mastapy.bearings.bearing_results.rolling.iso_rating_results import (
    _1794, _1792, _1798, _1797,
    _1793, _1799, _1795
)
from mastapy.bearings.bearing_results.rolling.skf_module import _1789
from mastapy.bearings.bearing_results import _1654
from mastapy._internal.python_net import python_net_import

_LOADED_ROLLING_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedRollingBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedRollingBearingResults',)


class LoadedRollingBearingResults(_1654.LoadedDetailedBearingResults):
    '''LoadedRollingBearingResults

    This is a mastapy class.
    '''

    TYPE = _LOADED_ROLLING_BEARING_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedRollingBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_to_radial_load_ratio(self) -> 'float':
        '''float: 'AxialToRadialLoadRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialToRadialLoadRatio

    @property
    def static_equivalent_load_capacity_ratio_limit(self) -> 'float':
        '''float: 'StaticEquivalentLoadCapacityRatioLimit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StaticEquivalentLoadCapacityRatioLimit

    @property
    def number_of_elements_in_contact(self) -> 'int':
        '''int: 'NumberOfElementsInContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfElementsInContact

    @property
    def relative_misalignment(self) -> 'float':
        '''float: 'RelativeMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeMisalignment

    @property
    def dynamic_equivalent_load_isotr141792001(self) -> 'float':
        '''float: 'DynamicEquivalentLoadISOTR141792001' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DynamicEquivalentLoadISOTR141792001

    @property
    def dynamic_radial_load_factor_for_isotr141792001(self) -> 'float':
        '''float: 'DynamicRadialLoadFactorForISOTR141792001' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DynamicRadialLoadFactorForISOTR141792001

    @property
    def dynamic_axial_load_factor_for_isotr141792001(self) -> 'float':
        '''float: 'DynamicAxialLoadFactorForISOTR141792001' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DynamicAxialLoadFactorForISOTR141792001

    @property
    def is_inner_ring_rotating_relative_to_load(self) -> 'bool':
        '''bool: 'IsInnerRingRotatingRelativeToLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsInnerRingRotatingRelativeToLoad

    @property
    def is_outer_ring_rotating_relative_to_load(self) -> 'bool':
        '''bool: 'IsOuterRingRotatingRelativeToLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsOuterRingRotatingRelativeToLoad

    @property
    def static_equivalent_load_for_isotr141792001(self) -> 'float':
        '''float: 'StaticEquivalentLoadForISOTR141792001' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StaticEquivalentLoadForISOTR141792001

    @property
    def static_radial_load_factor_for_isotr141792001(self) -> 'float':
        '''float: 'StaticRadialLoadFactorForISOTR141792001' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StaticRadialLoadFactorForISOTR141792001

    @property
    def static_axial_load_factor_for_isotr141792001(self) -> 'float':
        '''float: 'StaticAxialLoadFactorForISOTR141792001' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StaticAxialLoadFactorForISOTR141792001

    @property
    def element_centrifugal_force(self) -> 'float':
        '''float: 'ElementCentrifugalForce' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ElementCentrifugalForce

    @property
    def include_centrifugal_effects(self) -> 'bool':
        '''bool: 'IncludeCentrifugalEffects' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IncludeCentrifugalEffects

    @property
    def include_centrifugal_ring_expansion(self) -> 'bool':
        '''bool: 'IncludeCentrifugalRingExpansion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IncludeCentrifugalRingExpansion

    @property
    def element_surface_velocity(self) -> 'float':
        '''float: 'ElementSurfaceVelocity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ElementSurfaceVelocity

    @property
    def element_angular_velocity(self) -> 'float':
        '''float: 'ElementAngularVelocity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ElementAngularVelocity

    @property
    def cage_angular_velocity(self) -> 'float':
        '''float: 'CageAngularVelocity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CageAngularVelocity

    @property
    def lambda_ratio_inner(self) -> 'float':
        '''float: 'LambdaRatioInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LambdaRatioInner

    @property
    def lambda_ratio_outer(self) -> 'float':
        '''float: 'LambdaRatioOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LambdaRatioOuter

    @property
    def minimum_lubricating_film_thickness_inner(self) -> 'float':
        '''float: 'MinimumLubricatingFilmThicknessInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumLubricatingFilmThicknessInner

    @property
    def minimum_lubricating_film_thickness_outer(self) -> 'float':
        '''float: 'MinimumLubricatingFilmThicknessOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumLubricatingFilmThicknessOuter

    @property
    def maximum_normal_load_inner(self) -> 'float':
        '''float: 'MaximumNormalLoadInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNormalLoadInner

    @property
    def maximum_normal_load_outer(self) -> 'float':
        '''float: 'MaximumNormalLoadOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNormalLoadOuter

    @property
    def maximum_normal_stress(self) -> 'float':
        '''float: 'MaximumNormalStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNormalStress

    @property
    def maximum_normal_stress_inner(self) -> 'float':
        '''float: 'MaximumNormalStressInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNormalStressInner

    @property
    def maximum_normal_stress_outer(self) -> 'float':
        '''float: 'MaximumNormalStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNormalStressOuter

    @property
    def speed_factor_dn(self) -> 'float':
        '''float: 'SpeedFactorDn' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpeedFactorDn

    @property
    def speed_factor_dmn(self) -> 'float':
        '''float: 'SpeedFactorDmn' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpeedFactorDmn

    @property
    def load_dependent_torque(self) -> 'float':
        '''float: 'LoadDependentTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadDependentTorque

    @property
    def frictional_moment_of_the_bearing_seal(self) -> 'float':
        '''float: 'FrictionalMomentOfTheBearingSeal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FrictionalMomentOfTheBearingSeal

    @property
    def no_load_bearing_resistive_torque(self) -> 'float':
        '''float: 'NoLoadBearingResistiveTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NoLoadBearingResistiveTorque

    @property
    def kinematic_viscosity_of_oil_for_efficiency_calculations(self) -> 'float':
        '''float: 'KinematicViscosityOfOilForEfficiencyCalculations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.KinematicViscosityOfOilForEfficiencyCalculations

    @property
    def heat_emitting_reference_surface_area(self) -> 'float':
        '''float: 'HeatEmittingReferenceSurfaceArea' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HeatEmittingReferenceSurfaceArea

    @property
    def power_rating_f0(self) -> 'float':
        '''float: 'PowerRatingF0' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PowerRatingF0

    @property
    def power_rating_f1(self) -> 'float':
        '''float: 'PowerRatingF1' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PowerRatingF1

    @property
    def bearing_dip_factor(self) -> 'float':
        '''float: 'BearingDipFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BearingDipFactor

    @property
    def coefficient_for_no_load_power_loss(self) -> 'float':
        '''float: 'CoefficientForNoLoadPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CoefficientForNoLoadPowerLoss

    @property
    def bearing_dip_factor_min(self) -> 'float':
        '''float: 'BearingDipFactorMin' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BearingDipFactorMin

    @property
    def bearing_dip_factor_max(self) -> 'float':
        '''float: 'BearingDipFactorMax' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BearingDipFactorMax

    @property
    def oil_dip_coefficient(self) -> 'float':
        '''float: 'OilDipCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OilDipCoefficient

    @property
    def oil_dip_coefficient_thermal_speeds(self) -> 'float':
        '''float: 'OilDipCoefficientThermalSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OilDipCoefficientThermalSpeeds

    @property
    def element_temperature(self) -> 'float':
        '''float: 'ElementTemperature' is the original name of this property.'''

        return self.wrapped.ElementTemperature

    @element_temperature.setter
    def element_temperature(self, value: 'float'):
        self.wrapped.ElementTemperature = float(value) if value else 0.0

    @property
    def lubricant_film_temperature(self) -> 'float':
        '''float: 'LubricantFilmTemperature' is the original name of this property.'''

        return self.wrapped.LubricantFilmTemperature

    @lubricant_film_temperature.setter
    def lubricant_film_temperature(self, value: 'float'):
        self.wrapped.LubricantFilmTemperature = float(value) if value else 0.0

    @property
    def fluid_film_temperature_source(self) -> '_1589.FluidFilmTemperatureOptions':
        '''FluidFilmTemperatureOptions: 'FluidFilmTemperatureSource' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.FluidFilmTemperatureSource)
        return constructor.new(_1589.FluidFilmTemperatureOptions)(value) if value else None

    @property
    def lubricant_windage_and_churning_temperature(self) -> 'float':
        '''float: 'LubricantWindageAndChurningTemperature' is the original name of this property.'''

        return self.wrapped.LubricantWindageAndChurningTemperature

    @lubricant_windage_and_churning_temperature.setter
    def lubricant_windage_and_churning_temperature(self, value: 'float'):
        self.wrapped.LubricantWindageAndChurningTemperature = float(value) if value else 0.0

    @property
    def kinematic_viscosity(self) -> 'float':
        '''float: 'KinematicViscosity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.KinematicViscosity

    @property
    def dynamic_viscosity(self) -> 'float':
        '''float: 'DynamicViscosity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DynamicViscosity

    @property
    def fluid_film_density(self) -> 'float':
        '''float: 'FluidFilmDensity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FluidFilmDensity

    @property
    def surrounding_lubricant_density(self) -> 'float':
        '''float: 'SurroundingLubricantDensity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SurroundingLubricantDensity

    @property
    def include_fitting_effects(self) -> 'bool':
        '''bool: 'IncludeFittingEffects' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IncludeFittingEffects

    @property
    def include_thermal_expansion_effects(self) -> 'bool':
        '''bool: 'IncludeThermalExpansionEffects' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IncludeThermalExpansionEffects

    @property
    def include_gear_blank_elastic_distortion(self) -> 'bool':
        '''bool: 'IncludeGearBlankElasticDistortion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IncludeGearBlankElasticDistortion

    @property
    def include_inner_race_deflections(self) -> 'bool':
        '''bool: 'IncludeInnerRaceDeflections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IncludeInnerRaceDeflections

    @property
    def change_in_element_diameter_due_to_thermal_expansion(self) -> 'float':
        '''float: 'ChangeInElementDiameterDueToThermalExpansion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ChangeInElementDiameterDueToThermalExpansion

    @property
    def change_in_operating_radial_internal_clearance_due_to_element_thermal_expansion(self) -> 'float':
        '''float: 'ChangeInOperatingRadialInternalClearanceDueToElementThermalExpansion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ChangeInOperatingRadialInternalClearanceDueToElementThermalExpansion

    @property
    def outer_ring_fitting_at_assembly(self) -> '_1803.OuterRingFittingThermalResults':
        '''OuterRingFittingThermalResults: 'OuterRingFittingAtAssembly' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1803.OuterRingFittingThermalResults)(self.wrapped.OuterRingFittingAtAssembly) if self.wrapped.OuterRingFittingAtAssembly else None

    @property
    def outer_ring_fitting_at_operating_conditions(self) -> '_1803.OuterRingFittingThermalResults':
        '''OuterRingFittingThermalResults: 'OuterRingFittingAtOperatingConditions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1803.OuterRingFittingThermalResults)(self.wrapped.OuterRingFittingAtOperatingConditions) if self.wrapped.OuterRingFittingAtOperatingConditions else None

    @property
    def inner_ring_fitting_at_assembly(self) -> '_1801.InnerRingFittingThermalResults':
        '''InnerRingFittingThermalResults: 'InnerRingFittingAtAssembly' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1801.InnerRingFittingThermalResults)(self.wrapped.InnerRingFittingAtAssembly) if self.wrapped.InnerRingFittingAtAssembly else None

    @property
    def inner_ring_fitting_at_operating_conditions(self) -> '_1801.InnerRingFittingThermalResults':
        '''InnerRingFittingThermalResults: 'InnerRingFittingAtOperatingConditions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1801.InnerRingFittingThermalResults)(self.wrapped.InnerRingFittingAtOperatingConditions) if self.wrapped.InnerRingFittingAtOperatingConditions else None

    @property
    def maximum_operating_internal_clearance(self) -> '_1671.InternalClearance':
        '''InternalClearance: 'MaximumOperatingInternalClearance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1671.InternalClearance.TYPE not in self.wrapped.MaximumOperatingInternalClearance.__class__.__mro__:
            raise CastException('Failed to cast maximum_operating_internal_clearance to InternalClearance. Expected: {}.'.format(self.wrapped.MaximumOperatingInternalClearance.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MaximumOperatingInternalClearance.__class__)(self.wrapped.MaximumOperatingInternalClearance) if self.wrapped.MaximumOperatingInternalClearance else None

    @property
    def minimum_operating_internal_clearance(self) -> '_1671.InternalClearance':
        '''InternalClearance: 'MinimumOperatingInternalClearance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1671.InternalClearance.TYPE not in self.wrapped.MinimumOperatingInternalClearance.__class__.__mro__:
            raise CastException('Failed to cast minimum_operating_internal_clearance to InternalClearance. Expected: {}.'.format(self.wrapped.MinimumOperatingInternalClearance.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MinimumOperatingInternalClearance.__class__)(self.wrapped.MinimumOperatingInternalClearance) if self.wrapped.MinimumOperatingInternalClearance else None

    @property
    def din732(self) -> '_1668.DIN732Results':
        '''DIN732Results: 'DIN732' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1668.DIN732Results)(self.wrapped.DIN732) if self.wrapped.DIN732 else None

    @property
    def ansiabma(self) -> '_1807.ANSIABMAResults':
        '''ANSIABMAResults: 'ANSIABMA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1807.ANSIABMAResults.TYPE not in self.wrapped.ANSIABMA.__class__.__mro__:
            raise CastException('Failed to cast ansiabma to ANSIABMAResults. Expected: {}.'.format(self.wrapped.ANSIABMA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ANSIABMA.__class__)(self.wrapped.ANSIABMA) if self.wrapped.ANSIABMA else None

    @property
    def ansiabma_of_type_ansiabma112014_results(self) -> '_1805.ANSIABMA112014Results':
        '''ANSIABMA112014Results: 'ANSIABMA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1805.ANSIABMA112014Results.TYPE not in self.wrapped.ANSIABMA.__class__.__mro__:
            raise CastException('Failed to cast ansiabma to ANSIABMA112014Results. Expected: {}.'.format(self.wrapped.ANSIABMA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ANSIABMA.__class__)(self.wrapped.ANSIABMA) if self.wrapped.ANSIABMA else None

    @property
    def ansiabma_of_type_ansiabma92015_results(self) -> '_1806.ANSIABMA92015Results':
        '''ANSIABMA92015Results: 'ANSIABMA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1806.ANSIABMA92015Results.TYPE not in self.wrapped.ANSIABMA.__class__.__mro__:
            raise CastException('Failed to cast ansiabma to ANSIABMA92015Results. Expected: {}.'.format(self.wrapped.ANSIABMA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ANSIABMA.__class__)(self.wrapped.ANSIABMA) if self.wrapped.ANSIABMA else None

    @property
    def iso2812007(self) -> '_1794.ISO2812007Results':
        '''ISO2812007Results: 'ISO2812007' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1794.ISO2812007Results.TYPE not in self.wrapped.ISO2812007.__class__.__mro__:
            raise CastException('Failed to cast iso2812007 to ISO2812007Results. Expected: {}.'.format(self.wrapped.ISO2812007.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ISO2812007.__class__)(self.wrapped.ISO2812007) if self.wrapped.ISO2812007 else None

    @property
    def iso2812007_of_type_ball_iso2812007_results(self) -> '_1792.BallISO2812007Results':
        '''BallISO2812007Results: 'ISO2812007' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1792.BallISO2812007Results.TYPE not in self.wrapped.ISO2812007.__class__.__mro__:
            raise CastException('Failed to cast iso2812007 to BallISO2812007Results. Expected: {}.'.format(self.wrapped.ISO2812007.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ISO2812007.__class__)(self.wrapped.ISO2812007) if self.wrapped.ISO2812007 else None

    @property
    def iso2812007_of_type_roller_iso2812007_results(self) -> '_1798.RollerISO2812007Results':
        '''RollerISO2812007Results: 'ISO2812007' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1798.RollerISO2812007Results.TYPE not in self.wrapped.ISO2812007.__class__.__mro__:
            raise CastException('Failed to cast iso2812007 to RollerISO2812007Results. Expected: {}.'.format(self.wrapped.ISO2812007.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ISO2812007.__class__)(self.wrapped.ISO2812007) if self.wrapped.ISO2812007 else None

    @property
    def isots162812008(self) -> '_1797.ISOTS162812008Results':
        '''ISOTS162812008Results: 'ISOTS162812008' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1797.ISOTS162812008Results.TYPE not in self.wrapped.ISOTS162812008.__class__.__mro__:
            raise CastException('Failed to cast isots162812008 to ISOTS162812008Results. Expected: {}.'.format(self.wrapped.ISOTS162812008.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ISOTS162812008.__class__)(self.wrapped.ISOTS162812008) if self.wrapped.ISOTS162812008 else None

    @property
    def isots162812008_of_type_ball_isots162812008_results(self) -> '_1793.BallISOTS162812008Results':
        '''BallISOTS162812008Results: 'ISOTS162812008' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1793.BallISOTS162812008Results.TYPE not in self.wrapped.ISOTS162812008.__class__.__mro__:
            raise CastException('Failed to cast isots162812008 to BallISOTS162812008Results. Expected: {}.'.format(self.wrapped.ISOTS162812008.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ISOTS162812008.__class__)(self.wrapped.ISOTS162812008) if self.wrapped.ISOTS162812008 else None

    @property
    def isots162812008_of_type_roller_isots162812008_results(self) -> '_1799.RollerISOTS162812008Results':
        '''RollerISOTS162812008Results: 'ISOTS162812008' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1799.RollerISOTS162812008Results.TYPE not in self.wrapped.ISOTS162812008.__class__.__mro__:
            raise CastException('Failed to cast isots162812008 to RollerISOTS162812008Results. Expected: {}.'.format(self.wrapped.ISOTS162812008.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ISOTS162812008.__class__)(self.wrapped.ISOTS162812008) if self.wrapped.ISOTS162812008 else None

    @property
    def iso762006(self) -> '_1795.ISO762006Results':
        '''ISO762006Results: 'ISO762006' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1795.ISO762006Results)(self.wrapped.ISO762006) if self.wrapped.ISO762006 else None

    @property
    def maximum_static_contact_stress(self) -> '_1755.MaximumStaticContactStress':
        '''MaximumStaticContactStress: 'MaximumStaticContactStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1755.MaximumStaticContactStress)(self.wrapped.MaximumStaticContactStress) if self.wrapped.MaximumStaticContactStress else None

    @property
    def skf_module_results(self) -> '_1789.SKFModuleResults':
        '''SKFModuleResults: 'SKFModuleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1789.SKFModuleResults)(self.wrapped.SKFModuleResults) if self.wrapped.SKFModuleResults else None

    @property
    def rows(self) -> 'List[_1728.LoadedRollingBearingRow]':
        '''List[LoadedRollingBearingRow]: 'Rows' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Rows, constructor.new(_1728.LoadedRollingBearingRow))
        return value

    @property
    def all_mounting_results(self) -> 'List[_1804.RingFittingThermalResults]':
        '''List[RingFittingThermalResults]: 'AllMountingResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllMountingResults, constructor.new(_1804.RingFittingThermalResults))
        return value
