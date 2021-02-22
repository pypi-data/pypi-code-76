'''_6418.py

BearingLoadCase
'''


from typing import List

from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.math_utility.hertzian_contact import _1569
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy.utility import _1261
from mastapy.materials.efficiency import _255
from mastapy.system_model.analyses_and_results.mbd_analyses import _5010
from mastapy.system_model.part_model import _2089
from mastapy.bearings.tolerances import _1612, _1618
from mastapy.bearings.bearing_results.rolling import _1758
from mastapy.math_utility.measured_vectors import _1563
from mastapy._internal.python_net import python_net_import
from mastapy.system_model.analyses_and_results.static_loads import _6448

_ARRAY = python_net_import('System', 'Array')
_BEARING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BearingLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingLoadCase',)


class BearingLoadCase(_6448.ConnectorLoadCase):
    '''BearingLoadCase

    This is a mastapy class.
    '''

    TYPE = _BEARING_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def hertzian_contact_deflection_calculation_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod':
        '''enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod: 'HertzianContactDeflectionCalculationMethod' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.HertzianContactDeflectionCalculationMethod, value) if self.wrapped.HertzianContactDeflectionCalculationMethod else None

    @hertzian_contact_deflection_calculation_method.setter
    def hertzian_contact_deflection_calculation_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.HertzianContactDeflectionCalculationMethod = value

    @property
    def include_fitting_effects(self) -> '_1261.LoadCaseOverrideOption':
        '''LoadCaseOverrideOption: 'IncludeFittingEffects' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.IncludeFittingEffects)
        return constructor.new(_1261.LoadCaseOverrideOption)(value) if value else None

    @include_fitting_effects.setter
    def include_fitting_effects(self, value: '_1261.LoadCaseOverrideOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.IncludeFittingEffects = value

    @property
    def include_thermal_expansion_effects(self) -> '_1261.LoadCaseOverrideOption':
        '''LoadCaseOverrideOption: 'IncludeThermalExpansionEffects' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.IncludeThermalExpansionEffects)
        return constructor.new(_1261.LoadCaseOverrideOption)(value) if value else None

    @include_thermal_expansion_effects.setter
    def include_thermal_expansion_effects(self, value: '_1261.LoadCaseOverrideOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.IncludeThermalExpansionEffects = value

    @property
    def include_ring_ovality(self) -> '_1261.LoadCaseOverrideOption':
        '''LoadCaseOverrideOption: 'IncludeRingOvality' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.IncludeRingOvality)
        return constructor.new(_1261.LoadCaseOverrideOption)(value) if value else None

    @include_ring_ovality.setter
    def include_ring_ovality(self, value: '_1261.LoadCaseOverrideOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.IncludeRingOvality = value

    @property
    def inner_node_meaning(self) -> 'str':
        '''str: 'InnerNodeMeaning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerNodeMeaning

    @property
    def outer_node_meaning(self) -> 'str':
        '''str: 'OuterNodeMeaning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OuterNodeMeaning

    @property
    def override_design_left_support_detail(self) -> 'bool':
        '''bool: 'OverrideDesignLeftSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideDesignLeftSupportDetail

    @override_design_left_support_detail.setter
    def override_design_left_support_detail(self, value: 'bool'):
        self.wrapped.OverrideDesignLeftSupportDetail = bool(value) if value else False

    @property
    def override_all_planets_left_support_detail(self) -> 'bool':
        '''bool: 'OverrideAllPlanetsLeftSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideAllPlanetsLeftSupportDetail

    @override_all_planets_left_support_detail.setter
    def override_all_planets_left_support_detail(self, value: 'bool'):
        self.wrapped.OverrideAllPlanetsLeftSupportDetail = bool(value) if value else False

    @property
    def override_design_right_support_detail(self) -> 'bool':
        '''bool: 'OverrideDesignRightSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideDesignRightSupportDetail

    @override_design_right_support_detail.setter
    def override_design_right_support_detail(self, value: 'bool'):
        self.wrapped.OverrideDesignRightSupportDetail = bool(value) if value else False

    @property
    def override_all_planets_right_support_detail(self) -> 'bool':
        '''bool: 'OverrideAllPlanetsRightSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideAllPlanetsRightSupportDetail

    @override_all_planets_right_support_detail.setter
    def override_all_planets_right_support_detail(self, value: 'bool'):
        self.wrapped.OverrideAllPlanetsRightSupportDetail = bool(value) if value else False

    @property
    def use_design_friction_coefficients(self) -> 'bool':
        '''bool: 'UseDesignFrictionCoefficients' is the original name of this property.'''

        return self.wrapped.UseDesignFrictionCoefficients

    @use_design_friction_coefficients.setter
    def use_design_friction_coefficients(self, value: 'bool'):
        self.wrapped.UseDesignFrictionCoefficients = bool(value) if value else False

    @property
    def override_design_inner_support_detail(self) -> 'bool':
        '''bool: 'OverrideDesignInnerSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideDesignInnerSupportDetail

    @override_design_inner_support_detail.setter
    def override_design_inner_support_detail(self, value: 'bool'):
        self.wrapped.OverrideDesignInnerSupportDetail = bool(value) if value else False

    @property
    def override_all_planets_inner_support_detail(self) -> 'bool':
        '''bool: 'OverrideAllPlanetsInnerSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideAllPlanetsInnerSupportDetail

    @override_all_planets_inner_support_detail.setter
    def override_all_planets_inner_support_detail(self, value: 'bool'):
        self.wrapped.OverrideAllPlanetsInnerSupportDetail = bool(value) if value else False

    @property
    def override_design_outer_support_detail(self) -> 'bool':
        '''bool: 'OverrideDesignOuterSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideDesignOuterSupportDetail

    @override_design_outer_support_detail.setter
    def override_design_outer_support_detail(self, value: 'bool'):
        self.wrapped.OverrideDesignOuterSupportDetail = bool(value) if value else False

    @property
    def override_all_planets_outer_support_detail(self) -> 'bool':
        '''bool: 'OverrideAllPlanetsOuterSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideAllPlanetsOuterSupportDetail

    @override_all_planets_outer_support_detail.setter
    def override_all_planets_outer_support_detail(self, value: 'bool'):
        self.wrapped.OverrideAllPlanetsOuterSupportDetail = bool(value) if value else False

    @property
    def inner_mounting_sleeve_temperature(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'InnerMountingSleeveTemperature' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.InnerMountingSleeveTemperature) if self.wrapped.InnerMountingSleeveTemperature else None

    @inner_mounting_sleeve_temperature.setter
    def inner_mounting_sleeve_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.InnerMountingSleeveTemperature = value

    @property
    def outer_mounting_sleeve_temperature(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'OuterMountingSleeveTemperature' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.OuterMountingSleeveTemperature) if self.wrapped.OuterMountingSleeveTemperature else None

    @outer_mounting_sleeve_temperature.setter
    def outer_mounting_sleeve_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.OuterMountingSleeveTemperature = value

    @property
    def inner_mounting_sleeve_bore_tolerance_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'InnerMountingSleeveBoreToleranceFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.InnerMountingSleeveBoreToleranceFactor) if self.wrapped.InnerMountingSleeveBoreToleranceFactor else None

    @inner_mounting_sleeve_bore_tolerance_factor.setter
    def inner_mounting_sleeve_bore_tolerance_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.InnerMountingSleeveBoreToleranceFactor = value

    @property
    def inner_mounting_sleeve_outer_diameter_tolerance_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'InnerMountingSleeveOuterDiameterToleranceFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.InnerMountingSleeveOuterDiameterToleranceFactor) if self.wrapped.InnerMountingSleeveOuterDiameterToleranceFactor else None

    @inner_mounting_sleeve_outer_diameter_tolerance_factor.setter
    def inner_mounting_sleeve_outer_diameter_tolerance_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.InnerMountingSleeveOuterDiameterToleranceFactor = value

    @property
    def outer_mounting_sleeve_bore_tolerance_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'OuterMountingSleeveBoreToleranceFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.OuterMountingSleeveBoreToleranceFactor) if self.wrapped.OuterMountingSleeveBoreToleranceFactor else None

    @outer_mounting_sleeve_bore_tolerance_factor.setter
    def outer_mounting_sleeve_bore_tolerance_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.OuterMountingSleeveBoreToleranceFactor = value

    @property
    def outer_mounting_sleeve_outer_diameter_tolerance_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'OuterMountingSleeveOuterDiameterToleranceFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.OuterMountingSleeveOuterDiameterToleranceFactor) if self.wrapped.OuterMountingSleeveOuterDiameterToleranceFactor else None

    @outer_mounting_sleeve_outer_diameter_tolerance_factor.setter
    def outer_mounting_sleeve_outer_diameter_tolerance_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.OuterMountingSleeveOuterDiameterToleranceFactor = value

    @property
    def axial_force_preload(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AxialForcePreload' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AxialForcePreload) if self.wrapped.AxialForcePreload else None

    @axial_force_preload.setter
    def axial_force_preload(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.AxialForcePreload = value

    @property
    def preload_spring_initial_compression(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PreloadSpringInitialCompression' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PreloadSpringInitialCompression) if self.wrapped.PreloadSpringInitialCompression else None

    @preload_spring_initial_compression.setter
    def preload_spring_initial_compression(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.PreloadSpringInitialCompression = value

    @property
    def contact_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ContactAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ContactAngle) if self.wrapped.ContactAngle else None

    @contact_angle.setter
    def contact_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ContactAngle = value

    @property
    def axial_displacement_preload(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AxialDisplacementPreload' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AxialDisplacementPreload) if self.wrapped.AxialDisplacementPreload else None

    @axial_displacement_preload.setter
    def axial_displacement_preload(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.AxialDisplacementPreload = value

    @property
    def axial_internal_clearance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AxialInternalClearance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AxialInternalClearance) if self.wrapped.AxialInternalClearance else None

    @axial_internal_clearance.setter
    def axial_internal_clearance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.AxialInternalClearance = value

    @property
    def axial_internal_clearance_tolerance_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AxialInternalClearanceToleranceFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AxialInternalClearanceToleranceFactor) if self.wrapped.AxialInternalClearanceToleranceFactor else None

    @axial_internal_clearance_tolerance_factor.setter
    def axial_internal_clearance_tolerance_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.AxialInternalClearanceToleranceFactor = value

    @property
    def radial_internal_clearance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RadialInternalClearance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RadialInternalClearance) if self.wrapped.RadialInternalClearance else None

    @radial_internal_clearance.setter
    def radial_internal_clearance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.RadialInternalClearance = value

    @property
    def radial_internal_clearance_tolerance_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RadialInternalClearanceToleranceFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RadialInternalClearanceToleranceFactor) if self.wrapped.RadialInternalClearanceToleranceFactor else None

    @radial_internal_clearance_tolerance_factor.setter
    def radial_internal_clearance_tolerance_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.RadialInternalClearanceToleranceFactor = value

    @property
    def coefficient_of_friction(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CoefficientOfFriction' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CoefficientOfFriction) if self.wrapped.CoefficientOfFriction else None

    @coefficient_of_friction.setter
    def coefficient_of_friction(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.CoefficientOfFriction = value

    @property
    def efficiency_rating_method(self) -> 'overridable.Overridable_BearingEfficiencyRatingMethod':
        '''overridable.Overridable_BearingEfficiencyRatingMethod: 'EfficiencyRatingMethod' is the original name of this property.'''

        value = overridable.Overridable_BearingEfficiencyRatingMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.EfficiencyRatingMethod, value) if self.wrapped.EfficiencyRatingMethod else None

    @efficiency_rating_method.setter
    def efficiency_rating_method(self, value: 'overridable.Overridable_BearingEfficiencyRatingMethod.implicit_type()'):
        wrapper_type = overridable.Overridable_BearingEfficiencyRatingMethod.wrapper_type()
        enclosed_type = overridable.Overridable_BearingEfficiencyRatingMethod.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value else None, is_overridden)
        self.wrapped.EfficiencyRatingMethod = value

    @property
    def element_temperature(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ElementTemperature' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ElementTemperature) if self.wrapped.ElementTemperature else None

    @element_temperature.setter
    def element_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ElementTemperature = value

    @property
    def lubricant_film_temperature(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'LubricantFilmTemperature' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.LubricantFilmTemperature) if self.wrapped.LubricantFilmTemperature else None

    @lubricant_film_temperature.setter
    def lubricant_film_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.LubricantFilmTemperature = value

    @property
    def lubricant_windage_churning_temperature(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'LubricantWindageChurningTemperature' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.LubricantWindageChurningTemperature) if self.wrapped.LubricantWindageChurningTemperature else None

    @lubricant_windage_churning_temperature.setter
    def lubricant_windage_churning_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.LubricantWindageChurningTemperature = value

    @property
    def oil_inlet_temperature(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'OilInletTemperature' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.OilInletTemperature) if self.wrapped.OilInletTemperature else None

    @oil_inlet_temperature.setter
    def oil_inlet_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.OilInletTemperature = value

    @property
    def first_element_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'FirstElementAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.FirstElementAngle) if self.wrapped.FirstElementAngle else None

    @first_element_angle.setter
    def first_element_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.FirstElementAngle = value

    @property
    def bearing_stiffness_model(self) -> '_5010.BearingStiffnessModel':
        '''BearingStiffnessModel: 'BearingStiffnessModel' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BearingStiffnessModel)
        return constructor.new(_5010.BearingStiffnessModel)(value) if value else None

    @bearing_stiffness_model.setter
    def bearing_stiffness_model(self, value: '_5010.BearingStiffnessModel'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BearingStiffnessModel = value

    @property
    def bearing_stiffness_model_used_in_analysis(self) -> '_5010.BearingStiffnessModel':
        '''BearingStiffnessModel: 'BearingStiffnessModelUsedInAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.BearingStiffnessModelUsedInAnalysis)
        return constructor.new(_5010.BearingStiffnessModel)(value) if value else None

    @property
    def minimum_force_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumForceForBearingToBeConsideredLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumForceForBearingToBeConsideredLoaded) if self.wrapped.MinimumForceForBearingToBeConsideredLoaded else None

    @minimum_force_for_bearing_to_be_considered_loaded.setter
    def minimum_force_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.MinimumForceForBearingToBeConsideredLoaded = value

    @property
    def minimum_moment_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumMomentForBearingToBeConsideredLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumMomentForBearingToBeConsideredLoaded) if self.wrapped.MinimumMomentForBearingToBeConsideredLoaded else None

    @minimum_moment_for_bearing_to_be_considered_loaded.setter
    def minimum_moment_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.MinimumMomentForBearingToBeConsideredLoaded = value

    @property
    def viscosity_ratio(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ViscosityRatio' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ViscosityRatio) if self.wrapped.ViscosityRatio else None

    @viscosity_ratio.setter
    def viscosity_ratio(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ViscosityRatio = value

    @property
    def ring_ovality_scaling(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RingOvalityScaling' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RingOvalityScaling) if self.wrapped.RingOvalityScaling else None

    @ring_ovality_scaling.setter
    def ring_ovality_scaling(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.RingOvalityScaling = value

    @property
    def bearing_life_modification_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'BearingLifeModificationFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.BearingLifeModificationFactor) if self.wrapped.BearingLifeModificationFactor else None

    @bearing_life_modification_factor.setter
    def bearing_life_modification_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.BearingLifeModificationFactor = value

    @property
    def bearing_life_adjustment_factor_for_special_bearing_properties(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'BearingLifeAdjustmentFactorForSpecialBearingProperties' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.BearingLifeAdjustmentFactorForSpecialBearingProperties) if self.wrapped.BearingLifeAdjustmentFactorForSpecialBearingProperties else None

    @bearing_life_adjustment_factor_for_special_bearing_properties.setter
    def bearing_life_adjustment_factor_for_special_bearing_properties(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.BearingLifeAdjustmentFactorForSpecialBearingProperties = value

    @property
    def bearing_life_adjustment_factor_for_operating_conditions(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'BearingLifeAdjustmentFactorForOperatingConditions' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.BearingLifeAdjustmentFactorForOperatingConditions) if self.wrapped.BearingLifeAdjustmentFactorForOperatingConditions else None

    @bearing_life_adjustment_factor_for_operating_conditions.setter
    def bearing_life_adjustment_factor_for_operating_conditions(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.BearingLifeAdjustmentFactorForOperatingConditions = value

    @property
    def use_specified_contact_stiffness(self) -> 'overridable.Overridable_bool':
        '''overridable.Overridable_bool: 'UseSpecifiedContactStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_bool)(self.wrapped.UseSpecifiedContactStiffness) if self.wrapped.UseSpecifiedContactStiffness else None

    @use_specified_contact_stiffness.setter
    def use_specified_contact_stiffness(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else False, is_overridden)
        self.wrapped.UseSpecifiedContactStiffness = value

    @property
    def contact_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ContactStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ContactStiffness) if self.wrapped.ContactStiffness else None

    @contact_stiffness.setter
    def contact_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ContactStiffness = value

    @property
    def x_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'XStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.XStiffness) if self.wrapped.XStiffness else None

    @x_stiffness.setter
    def x_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.XStiffness = value

    @property
    def y_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'YStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.YStiffness) if self.wrapped.YStiffness else None

    @y_stiffness.setter
    def y_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.YStiffness = value

    @property
    def model_bearing_mounting_clearances_automatically(self) -> 'overridable.Overridable_bool':
        '''overridable.Overridable_bool: 'ModelBearingMountingClearancesAutomatically' is the original name of this property.'''

        return constructor.new(overridable.Overridable_bool)(self.wrapped.ModelBearingMountingClearancesAutomatically) if self.wrapped.ModelBearingMountingClearancesAutomatically else None

    @model_bearing_mounting_clearances_automatically.setter
    def model_bearing_mounting_clearances_automatically(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else False, is_overridden)
        self.wrapped.ModelBearingMountingClearancesAutomatically = value

    @property
    def number_of_strips_for_roller_calculation(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfStripsForRollerCalculation' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfStripsForRollerCalculation) if self.wrapped.NumberOfStripsForRollerCalculation else None

    @number_of_strips_for_roller_calculation.setter
    def number_of_strips_for_roller_calculation(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0, is_overridden)
        self.wrapped.NumberOfStripsForRollerCalculation = value

    @property
    def use_node_per_row_inner(self) -> 'overridable.Overridable_bool':
        '''overridable.Overridable_bool: 'UseNodePerRowInner' is the original name of this property.'''

        return constructor.new(overridable.Overridable_bool)(self.wrapped.UseNodePerRowInner) if self.wrapped.UseNodePerRowInner else None

    @use_node_per_row_inner.setter
    def use_node_per_row_inner(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else False, is_overridden)
        self.wrapped.UseNodePerRowInner = value

    @property
    def use_node_per_row_outer(self) -> 'overridable.Overridable_bool':
        '''overridable.Overridable_bool: 'UseNodePerRowOuter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_bool)(self.wrapped.UseNodePerRowOuter) if self.wrapped.UseNodePerRowOuter else None

    @use_node_per_row_outer.setter
    def use_node_per_row_outer(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else False, is_overridden)
        self.wrapped.UseNodePerRowOuter = value

    @property
    def override_design_specified_stiffness_matrix(self) -> 'bool':
        '''bool: 'OverrideDesignSpecifiedStiffnessMatrix' is the original name of this property.'''

        return self.wrapped.OverrideDesignSpecifiedStiffnessMatrix

    @override_design_specified_stiffness_matrix.setter
    def override_design_specified_stiffness_matrix(self, value: 'bool'):
        self.wrapped.OverrideDesignSpecifiedStiffnessMatrix = bool(value) if value else False

    @property
    def component_design(self) -> '_2089.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2089.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def left_ring_detail(self) -> '_1612.RaceDetail':
        '''RaceDetail: 'LeftRingDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1612.RaceDetail)(self.wrapped.LeftRingDetail) if self.wrapped.LeftRingDetail else None

    @property
    def right_ring_detail(self) -> '_1612.RaceDetail':
        '''RaceDetail: 'RightRingDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1612.RaceDetail)(self.wrapped.RightRingDetail) if self.wrapped.RightRingDetail else None

    @property
    def left_support_detail(self) -> '_1618.SupportDetail':
        '''SupportDetail: 'LeftSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1618.SupportDetail)(self.wrapped.LeftSupportDetail) if self.wrapped.LeftSupportDetail else None

    @property
    def right_support_detail(self) -> '_1618.SupportDetail':
        '''SupportDetail: 'RightSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1618.SupportDetail)(self.wrapped.RightSupportDetail) if self.wrapped.RightSupportDetail else None

    @property
    def inner_ring_detail(self) -> '_1612.RaceDetail':
        '''RaceDetail: 'InnerRingDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1612.RaceDetail)(self.wrapped.InnerRingDetail) if self.wrapped.InnerRingDetail else None

    @property
    def friction_coefficients(self) -> '_1758.RollingBearingFrictionCoefficients':
        '''RollingBearingFrictionCoefficients: 'FrictionCoefficients' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1758.RollingBearingFrictionCoefficients)(self.wrapped.FrictionCoefficients) if self.wrapped.FrictionCoefficients else None

    @property
    def outer_ring_detail(self) -> '_1612.RaceDetail':
        '''RaceDetail: 'OuterRingDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1612.RaceDetail)(self.wrapped.OuterRingDetail) if self.wrapped.OuterRingDetail else None

    @property
    def inner_support_detail(self) -> '_1618.SupportDetail':
        '''SupportDetail: 'InnerSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1618.SupportDetail)(self.wrapped.InnerSupportDetail) if self.wrapped.InnerSupportDetail else None

    @property
    def outer_support_detail(self) -> '_1618.SupportDetail':
        '''SupportDetail: 'OuterSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1618.SupportDetail)(self.wrapped.OuterSupportDetail) if self.wrapped.OuterSupportDetail else None

    @property
    def force_at_zero_displacement(self) -> '_1563.VectorWithLinearAndAngularComponents':
        '''VectorWithLinearAndAngularComponents: 'ForceAtZeroDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1563.VectorWithLinearAndAngularComponents)(self.wrapped.ForceAtZeroDisplacement) if self.wrapped.ForceAtZeroDisplacement else None

    @property
    def specified_stiffness_for_linear_bearing_in_local_coordinate_system(self) -> 'List[List[float]]':
        '''List[List[float]]: 'SpecifiedStiffnessForLinearBearingInLocalCoordinateSystem' is the original name of this property.'''

        value = conversion.pn_to_mp_list_float_2d(self.wrapped.SpecifiedStiffnessForLinearBearingInLocalCoordinateSystem)
        return value

    @specified_stiffness_for_linear_bearing_in_local_coordinate_system.setter
    def specified_stiffness_for_linear_bearing_in_local_coordinate_system(self, value: 'List[List[float]]'):
        value = value if value else None
        value = conversion.mp_to_pn_list_float_2d(value)
        self.wrapped.SpecifiedStiffnessForLinearBearingInLocalCoordinateSystem = value
