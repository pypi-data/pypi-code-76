'''_2089.py

Bearing
'''


from typing import List, Optional

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.bearings.tolerances import (
    _1601, _1602, _1604, _1615,
    _1610, _1618, _1605, _1619,
    _1611, _1621
)
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.bearings.bearing_results import _1655, _1656
from mastapy.bearings import (
    _1579, _1586, _1575, _1571
)
from mastapy._internal.python_net import python_net_import
from mastapy.materials.efficiency import _255
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_designs import (
    _1815, _1816, _1817, _1818,
    _1819
)
from mastapy.bearings.bearing_designs.rolling import (
    _1820, _1821, _1822, _1823,
    _1824, _1825, _1827, _1832,
    _1833, _1834, _1836, _1838,
    _1839, _1840, _1841, _1844,
    _1845, _1847, _1848, _1849,
    _1850, _1851, _1852
)
from mastapy.bearings.bearing_designs.fluid_film import (
    _1865, _1867, _1869, _1871,
    _1872, _1873
)
from mastapy.bearings.bearing_designs.concept import _1875, _1876, _1877
from mastapy.system_model.part_model import (
    _2088, _2121, _2090, _2094,
    _2096
)
from mastapy.materials import _232
from mastapy.bearings.bearing_results.rolling import _1758
from mastapy.math_utility.measured_vectors import _1563
from mastapy.system_model.part_model.shaft_model import _2129

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_ARRAY = python_net_import('System', 'Array')
_BEARING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bearing')


__docformat__ = 'restructuredtext en'
__all__ = ('Bearing',)


class Bearing(_2096.Connector):
    '''Bearing

    This is a mastapy class.
    '''

    TYPE = _BEARING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Bearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def outer_node_position_from_centre(self) -> 'float':
        '''float: 'OuterNodePositionFromCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OuterNodePositionFromCentre

    @property
    def inner_node_position_from_centre(self) -> 'float':
        '''float: 'InnerNodePositionFromCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerNodePositionFromCentre

    @property
    def left_node_position_from_centre(self) -> 'float':
        '''float: 'LeftNodePositionFromCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LeftNodePositionFromCentre

    @property
    def right_node_position_from_centre(self) -> 'float':
        '''float: 'RightNodePositionFromCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RightNodePositionFromCentre

    @property
    def offset_of_contact_on_inner_race_at_nominal_contact_angle(self) -> 'float':
        '''float: 'OffsetOfContactOnInnerRaceAtNominalContactAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OffsetOfContactOnInnerRaceAtNominalContactAngle

    @property
    def offset_of_contact_on_outer_race_at_nominal_contact_angle(self) -> 'float':
        '''float: 'OffsetOfContactOnOuterRaceAtNominalContactAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OffsetOfContactOnOuterRaceAtNominalContactAngle

    @property
    def diameter_of_contact_on_inner_race_at_nominal_contact_angle(self) -> 'float':
        '''float: 'DiameterOfContactOnInnerRaceAtNominalContactAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DiameterOfContactOnInnerRaceAtNominalContactAngle

    @property
    def diameter_of_contact_on_outer_race_at_nominal_contact_angle(self) -> 'float':
        '''float: 'DiameterOfContactOnOuterRaceAtNominalContactAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DiameterOfContactOnOuterRaceAtNominalContactAngle

    @property
    def offset_of_contact_on_left_race(self) -> 'float':
        '''float: 'OffsetOfContactOnLeftRace' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OffsetOfContactOnLeftRace

    @property
    def offset_of_contact_on_right_race(self) -> 'float':
        '''float: 'OffsetOfContactOnRightRace' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OffsetOfContactOnRightRace

    @property
    def diameter_of_contact_on_left_race(self) -> 'float':
        '''float: 'DiameterOfContactOnLeftRace' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DiameterOfContactOnLeftRace

    @property
    def diameter_of_contact_on_right_race(self) -> 'float':
        '''float: 'DiameterOfContactOnRightRace' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DiameterOfContactOnRightRace

    @property
    def bearing_tolerance_class(self) -> 'enum_with_selected_value.EnumWithSelectedValue_BearingToleranceClass':
        '''enum_with_selected_value.EnumWithSelectedValue_BearingToleranceClass: 'BearingToleranceClass' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_BearingToleranceClass.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.BearingToleranceClass, value) if self.wrapped.BearingToleranceClass else None

    @bearing_tolerance_class.setter
    def bearing_tolerance_class(self, value: 'enum_with_selected_value.EnumWithSelectedValue_BearingToleranceClass.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BearingToleranceClass.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.BearingToleranceClass = value

    @property
    def bearing_tolerance_definition(self) -> '_1602.BearingToleranceDefinitionOptions':
        '''BearingToleranceDefinitionOptions: 'BearingToleranceDefinition' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BearingToleranceDefinition)
        return constructor.new(_1602.BearingToleranceDefinitionOptions)(value) if value else None

    @bearing_tolerance_definition.setter
    def bearing_tolerance_definition(self, value: '_1602.BearingToleranceDefinitionOptions'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BearingToleranceDefinition = value

    @property
    def orientation(self) -> '_1655.Orientations':
        '''Orientations: 'Orientation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Orientation)
        return constructor.new(_1655.Orientations)(value) if value else None

    @orientation.setter
    def orientation(self, value: '_1655.Orientations'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Orientation = value

    @property
    def has_radial_mounting_clearance(self) -> 'bool':
        '''bool: 'HasRadialMountingClearance' is the original name of this property.'''

        return self.wrapped.HasRadialMountingClearance

    @has_radial_mounting_clearance.setter
    def has_radial_mounting_clearance(self, value: 'bool'):
        self.wrapped.HasRadialMountingClearance = bool(value) if value else False

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
    def axial_displacement_preload(self) -> 'float':
        '''float: 'AxialDisplacementPreload' is the original name of this property.'''

        return self.wrapped.AxialDisplacementPreload

    @axial_displacement_preload.setter
    def axial_displacement_preload(self, value: 'float'):
        self.wrapped.AxialDisplacementPreload = float(value) if value else 0.0

    @property
    def preload_spring_on_outer(self) -> 'bool':
        '''bool: 'PreloadSpringOnOuter' is the original name of this property.'''

        return self.wrapped.PreloadSpringOnOuter

    @preload_spring_on_outer.setter
    def preload_spring_on_outer(self, value: 'bool'):
        self.wrapped.PreloadSpringOnOuter = bool(value) if value else False

    @property
    def axial_force_preload(self) -> 'float':
        '''float: 'AxialForcePreload' is the original name of this property.'''

        return self.wrapped.AxialForcePreload

    @axial_force_preload.setter
    def axial_force_preload(self, value: 'float'):
        self.wrapped.AxialForcePreload = float(value) if value else 0.0

    @property
    def preload_spring_stiffness(self) -> 'float':
        '''float: 'PreloadSpringStiffness' is the original name of this property.'''

        return self.wrapped.PreloadSpringStiffness

    @preload_spring_stiffness.setter
    def preload_spring_stiffness(self, value: 'float'):
        self.wrapped.PreloadSpringStiffness = float(value) if value else 0.0

    @property
    def preload_spring_initial_compression(self) -> 'float':
        '''float: 'PreloadSpringInitialCompression' is the original name of this property.'''

        return self.wrapped.PreloadSpringInitialCompression

    @preload_spring_initial_compression.setter
    def preload_spring_initial_compression(self, value: 'float'):
        self.wrapped.PreloadSpringInitialCompression = float(value) if value else 0.0

    @property
    def preload_spring_max_travel(self) -> 'float':
        '''float: 'PreloadSpringMaxTravel' is the original name of this property.'''

        return self.wrapped.PreloadSpringMaxTravel

    @preload_spring_max_travel.setter
    def preload_spring_max_travel(self, value: 'float'):
        self.wrapped.PreloadSpringMaxTravel = float(value) if value else 0.0

    @property
    def axial_stiffness_at_mounting_points(self) -> 'float':
        '''float: 'AxialStiffnessAtMountingPoints' is the original name of this property.'''

        return self.wrapped.AxialStiffnessAtMountingPoints

    @axial_stiffness_at_mounting_points.setter
    def axial_stiffness_at_mounting_points(self, value: 'float'):
        self.wrapped.AxialStiffnessAtMountingPoints = float(value) if value else 0.0

    @property
    def preload_is_from_left(self) -> 'bool':
        '''bool: 'PreloadIsFromLeft' is the original name of this property.'''

        return self.wrapped.PreloadIsFromLeft

    @preload_is_from_left.setter
    def preload_is_from_left(self, value: 'bool'):
        self.wrapped.PreloadIsFromLeft = bool(value) if value else False

    @property
    def model(self) -> 'enum_with_selected_value.EnumWithSelectedValue_BearingModel':
        '''enum_with_selected_value.EnumWithSelectedValue_BearingModel: 'Model' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_BearingModel.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.Model, value) if self.wrapped.Model else None

    @model.setter
    def model(self, value: 'enum_with_selected_value.EnumWithSelectedValue_BearingModel.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BearingModel.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.Model = value

    @property
    def journal_bearing_type(self) -> '_1586.JournalBearingType':
        '''JournalBearingType: 'JournalBearingType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.JournalBearingType)
        return constructor.new(_1586.JournalBearingType)(value) if value else None

    @journal_bearing_type.setter
    def journal_bearing_type(self, value: '_1586.JournalBearingType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.JournalBearingType = value

    @property
    def length(self) -> 'float':
        '''float: 'Length' is the original name of this property.'''

        return self.wrapped.Length

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value else 0.0

    @property
    def outer_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'OuterDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.OuterDiameter) if self.wrapped.OuterDiameter else None

    @outer_diameter.setter
    def outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.OuterDiameter = value

    @property
    def inner_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'InnerDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.InnerDiameter) if self.wrapped.InnerDiameter else None

    @inner_diameter.setter
    def inner_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.InnerDiameter = value

    @property
    def difference_between_inner_diameter_and_diameter_of_connected_component_at_inner_connection(self) -> 'float':
        '''float: 'DifferenceBetweenInnerDiameterAndDiameterOfConnectedComponentAtInnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DifferenceBetweenInnerDiameterAndDiameterOfConnectedComponentAtInnerConnection

    @property
    def percentage_difference_between_inner_diameter_and_diameter_of_connected_component_at_inner_connection(self) -> 'float':
        '''float: 'PercentageDifferenceBetweenInnerDiameterAndDiameterOfConnectedComponentAtInnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PercentageDifferenceBetweenInnerDiameterAndDiameterOfConnectedComponentAtInnerConnection

    @property
    def difference_between_outer_diameter_and_diameter_of_connected_component_at_outer_connection(self) -> 'float':
        '''float: 'DifferenceBetweenOuterDiameterAndDiameterOfConnectedComponentAtOuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DifferenceBetweenOuterDiameterAndDiameterOfConnectedComponentAtOuterConnection

    @property
    def percentage_difference_between_outer_diameter_and_diameter_of_connected_component_at_outer_connection(self) -> 'float':
        '''float: 'PercentageDifferenceBetweenOuterDiameterAndDiameterOfConnectedComponentAtOuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PercentageDifferenceBetweenOuterDiameterAndDiameterOfConnectedComponentAtOuterConnection

    @property
    def preload(self) -> 'enum_with_selected_value.EnumWithSelectedValue_PreloadType':
        '''enum_with_selected_value.EnumWithSelectedValue_PreloadType: 'Preload' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_PreloadType.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.Preload, value) if self.wrapped.Preload else None

    @preload.setter
    def preload(self, value: 'enum_with_selected_value.EnumWithSelectedValue_PreloadType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_PreloadType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.Preload = value

    @property
    def override_design_lubrication_detail(self) -> 'bool':
        '''bool: 'OverrideDesignLubricationDetail' is the original name of this property.'''

        return self.wrapped.OverrideDesignLubricationDetail

    @override_design_lubrication_detail.setter
    def override_design_lubrication_detail(self, value: 'bool'):
        self.wrapped.OverrideDesignLubricationDetail = bool(value) if value else False

    @property
    def lubrication_detail(self) -> 'str':
        '''str: 'LubricationDetail' is the original name of this property.'''

        return self.wrapped.LubricationDetail.SelectedItemName

    @lubrication_detail.setter
    def lubrication_detail(self, value: 'str'):
        self.wrapped.LubricationDetail.SetSelectedItem(str(value) if value else None)

    @property
    def damping_options(self) -> '_1575.BearingDampingMatrixOption':
        '''BearingDampingMatrixOption: 'DampingOptions' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.DampingOptions)
        return constructor.new(_1575.BearingDampingMatrixOption)(value) if value else None

    @damping_options.setter
    def damping_options(self, value: '_1575.BearingDampingMatrixOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DampingOptions = value

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
    def maximum_bearing_life_modification_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MaximumBearingLifeModificationFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MaximumBearingLifeModificationFactor) if self.wrapped.MaximumBearingLifeModificationFactor else None

    @maximum_bearing_life_modification_factor.setter
    def maximum_bearing_life_modification_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.MaximumBearingLifeModificationFactor = value

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
    def permissible_track_truncation(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PermissibleTrackTruncation' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PermissibleTrackTruncation) if self.wrapped.PermissibleTrackTruncation else None

    @permissible_track_truncation.setter
    def permissible_track_truncation(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.PermissibleTrackTruncation = value

    @property
    def use_design_iso14179_settings(self) -> 'bool':
        '''bool: 'UseDesignISO14179Settings' is the original name of this property.'''

        return self.wrapped.UseDesignISO14179Settings

    @use_design_iso14179_settings.setter
    def use_design_iso14179_settings(self, value: 'bool'):
        self.wrapped.UseDesignISO14179Settings = bool(value) if value else False

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
    def ring_tolerance_inner(self) -> '_1604.InnerRingTolerance':
        '''InnerRingTolerance: 'RingToleranceInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1604.InnerRingTolerance)(self.wrapped.RingToleranceInner) if self.wrapped.RingToleranceInner else None

    @property
    def ring_tolerance_left(self) -> '_1615.RingTolerance':
        '''RingTolerance: 'RingToleranceLeft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1615.RingTolerance.TYPE not in self.wrapped.RingToleranceLeft.__class__.__mro__:
            raise CastException('Failed to cast ring_tolerance_left to RingTolerance. Expected: {}.'.format(self.wrapped.RingToleranceLeft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RingToleranceLeft.__class__)(self.wrapped.RingToleranceLeft) if self.wrapped.RingToleranceLeft else None

    @property
    def ring_tolerance_left_of_type_inner_ring_tolerance(self) -> '_1604.InnerRingTolerance':
        '''InnerRingTolerance: 'RingToleranceLeft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1604.InnerRingTolerance.TYPE not in self.wrapped.RingToleranceLeft.__class__.__mro__:
            raise CastException('Failed to cast ring_tolerance_left to InnerRingTolerance. Expected: {}.'.format(self.wrapped.RingToleranceLeft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RingToleranceLeft.__class__)(self.wrapped.RingToleranceLeft) if self.wrapped.RingToleranceLeft else None

    @property
    def ring_tolerance_left_of_type_outer_ring_tolerance(self) -> '_1610.OuterRingTolerance':
        '''OuterRingTolerance: 'RingToleranceLeft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1610.OuterRingTolerance.TYPE not in self.wrapped.RingToleranceLeft.__class__.__mro__:
            raise CastException('Failed to cast ring_tolerance_left to OuterRingTolerance. Expected: {}.'.format(self.wrapped.RingToleranceLeft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RingToleranceLeft.__class__)(self.wrapped.RingToleranceLeft) if self.wrapped.RingToleranceLeft else None

    @property
    def ring_tolerance_outer(self) -> '_1610.OuterRingTolerance':
        '''OuterRingTolerance: 'RingToleranceOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1610.OuterRingTolerance)(self.wrapped.RingToleranceOuter) if self.wrapped.RingToleranceOuter else None

    @property
    def ring_tolerance_right(self) -> '_1615.RingTolerance':
        '''RingTolerance: 'RingToleranceRight' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1615.RingTolerance.TYPE not in self.wrapped.RingToleranceRight.__class__.__mro__:
            raise CastException('Failed to cast ring_tolerance_right to RingTolerance. Expected: {}.'.format(self.wrapped.RingToleranceRight.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RingToleranceRight.__class__)(self.wrapped.RingToleranceRight) if self.wrapped.RingToleranceRight else None

    @property
    def ring_tolerance_right_of_type_inner_ring_tolerance(self) -> '_1604.InnerRingTolerance':
        '''InnerRingTolerance: 'RingToleranceRight' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1604.InnerRingTolerance.TYPE not in self.wrapped.RingToleranceRight.__class__.__mro__:
            raise CastException('Failed to cast ring_tolerance_right to InnerRingTolerance. Expected: {}.'.format(self.wrapped.RingToleranceRight.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RingToleranceRight.__class__)(self.wrapped.RingToleranceRight) if self.wrapped.RingToleranceRight else None

    @property
    def ring_tolerance_right_of_type_outer_ring_tolerance(self) -> '_1610.OuterRingTolerance':
        '''OuterRingTolerance: 'RingToleranceRight' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1610.OuterRingTolerance.TYPE not in self.wrapped.RingToleranceRight.__class__.__mro__:
            raise CastException('Failed to cast ring_tolerance_right to OuterRingTolerance. Expected: {}.'.format(self.wrapped.RingToleranceRight.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RingToleranceRight.__class__)(self.wrapped.RingToleranceRight) if self.wrapped.RingToleranceRight else None

    @property
    def inner_support_detail(self) -> '_1618.SupportDetail':
        '''SupportDetail: 'InnerSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1618.SupportDetail)(self.wrapped.InnerSupportDetail) if self.wrapped.InnerSupportDetail else None

    @property
    def left_support_detail(self) -> '_1618.SupportDetail':
        '''SupportDetail: 'LeftSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1618.SupportDetail)(self.wrapped.LeftSupportDetail) if self.wrapped.LeftSupportDetail else None

    @property
    def outer_support_detail(self) -> '_1618.SupportDetail':
        '''SupportDetail: 'OuterSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1618.SupportDetail)(self.wrapped.OuterSupportDetail) if self.wrapped.OuterSupportDetail else None

    @property
    def right_support_detail(self) -> '_1618.SupportDetail':
        '''SupportDetail: 'RightSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1618.SupportDetail)(self.wrapped.RightSupportDetail) if self.wrapped.RightSupportDetail else None

    @property
    def support_tolerance_inner(self) -> '_1605.InnerSupportTolerance':
        '''InnerSupportTolerance: 'SupportToleranceInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1605.InnerSupportTolerance)(self.wrapped.SupportToleranceInner) if self.wrapped.SupportToleranceInner else None

    @property
    def support_tolerance_left(self) -> '_1619.SupportTolerance':
        '''SupportTolerance: 'SupportToleranceLeft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1619.SupportTolerance.TYPE not in self.wrapped.SupportToleranceLeft.__class__.__mro__:
            raise CastException('Failed to cast support_tolerance_left to SupportTolerance. Expected: {}.'.format(self.wrapped.SupportToleranceLeft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SupportToleranceLeft.__class__)(self.wrapped.SupportToleranceLeft) if self.wrapped.SupportToleranceLeft else None

    @property
    def support_tolerance_left_of_type_inner_support_tolerance(self) -> '_1605.InnerSupportTolerance':
        '''InnerSupportTolerance: 'SupportToleranceLeft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1605.InnerSupportTolerance.TYPE not in self.wrapped.SupportToleranceLeft.__class__.__mro__:
            raise CastException('Failed to cast support_tolerance_left to InnerSupportTolerance. Expected: {}.'.format(self.wrapped.SupportToleranceLeft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SupportToleranceLeft.__class__)(self.wrapped.SupportToleranceLeft) if self.wrapped.SupportToleranceLeft else None

    @property
    def support_tolerance_left_of_type_outer_support_tolerance(self) -> '_1611.OuterSupportTolerance':
        '''OuterSupportTolerance: 'SupportToleranceLeft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1611.OuterSupportTolerance.TYPE not in self.wrapped.SupportToleranceLeft.__class__.__mro__:
            raise CastException('Failed to cast support_tolerance_left to OuterSupportTolerance. Expected: {}.'.format(self.wrapped.SupportToleranceLeft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SupportToleranceLeft.__class__)(self.wrapped.SupportToleranceLeft) if self.wrapped.SupportToleranceLeft else None

    @property
    def support_tolerance_outer(self) -> '_1611.OuterSupportTolerance':
        '''OuterSupportTolerance: 'SupportToleranceOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1611.OuterSupportTolerance)(self.wrapped.SupportToleranceOuter) if self.wrapped.SupportToleranceOuter else None

    @property
    def support_tolerance_right(self) -> '_1619.SupportTolerance':
        '''SupportTolerance: 'SupportToleranceRight' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1619.SupportTolerance.TYPE not in self.wrapped.SupportToleranceRight.__class__.__mro__:
            raise CastException('Failed to cast support_tolerance_right to SupportTolerance. Expected: {}.'.format(self.wrapped.SupportToleranceRight.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SupportToleranceRight.__class__)(self.wrapped.SupportToleranceRight) if self.wrapped.SupportToleranceRight else None

    @property
    def support_tolerance_right_of_type_inner_support_tolerance(self) -> '_1605.InnerSupportTolerance':
        '''InnerSupportTolerance: 'SupportToleranceRight' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1605.InnerSupportTolerance.TYPE not in self.wrapped.SupportToleranceRight.__class__.__mro__:
            raise CastException('Failed to cast support_tolerance_right to InnerSupportTolerance. Expected: {}.'.format(self.wrapped.SupportToleranceRight.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SupportToleranceRight.__class__)(self.wrapped.SupportToleranceRight) if self.wrapped.SupportToleranceRight else None

    @property
    def support_tolerance_right_of_type_outer_support_tolerance(self) -> '_1611.OuterSupportTolerance':
        '''OuterSupportTolerance: 'SupportToleranceRight' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1611.OuterSupportTolerance.TYPE not in self.wrapped.SupportToleranceRight.__class__.__mro__:
            raise CastException('Failed to cast support_tolerance_right to OuterSupportTolerance. Expected: {}.'.format(self.wrapped.SupportToleranceRight.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SupportToleranceRight.__class__)(self.wrapped.SupportToleranceRight) if self.wrapped.SupportToleranceRight else None

    @property
    def inner_mounting_sleeve_bore_tolerance(self) -> '_1611.OuterSupportTolerance':
        '''OuterSupportTolerance: 'InnerMountingSleeveBoreTolerance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1611.OuterSupportTolerance)(self.wrapped.InnerMountingSleeveBoreTolerance) if self.wrapped.InnerMountingSleeveBoreTolerance else None

    @property
    def inner_mounting_sleeve_outer_diameter_tolerance(self) -> '_1605.InnerSupportTolerance':
        '''InnerSupportTolerance: 'InnerMountingSleeveOuterDiameterTolerance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1605.InnerSupportTolerance)(self.wrapped.InnerMountingSleeveOuterDiameterTolerance) if self.wrapped.InnerMountingSleeveOuterDiameterTolerance else None

    @property
    def outer_mounting_sleeve_bore_tolerance(self) -> '_1611.OuterSupportTolerance':
        '''OuterSupportTolerance: 'OuterMountingSleeveBoreTolerance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1611.OuterSupportTolerance)(self.wrapped.OuterMountingSleeveBoreTolerance) if self.wrapped.OuterMountingSleeveBoreTolerance else None

    @property
    def outer_mounting_sleeve_outer_diameter_tolerance(self) -> '_1605.InnerSupportTolerance':
        '''InnerSupportTolerance: 'OuterMountingSleeveOuterDiameterTolerance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1605.InnerSupportTolerance)(self.wrapped.OuterMountingSleeveOuterDiameterTolerance) if self.wrapped.OuterMountingSleeveOuterDiameterTolerance else None

    @property
    def simple_bearing_detail_property(self) -> '_1815.BearingDesign':
        '''BearingDesign: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1815.BearingDesign.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to BearingDesign. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_detailed_bearing(self) -> '_1816.DetailedBearing':
        '''DetailedBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1816.DetailedBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to DetailedBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_dummy_rolling_bearing(self) -> '_1817.DummyRollingBearing':
        '''DummyRollingBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1817.DummyRollingBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to DummyRollingBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_linear_bearing(self) -> '_1818.LinearBearing':
        '''LinearBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1818.LinearBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to LinearBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_non_linear_bearing(self) -> '_1819.NonLinearBearing':
        '''NonLinearBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1819.NonLinearBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to NonLinearBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_angular_contact_ball_bearing(self) -> '_1820.AngularContactBallBearing':
        '''AngularContactBallBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1820.AngularContactBallBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to AngularContactBallBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_angular_contact_thrust_ball_bearing(self) -> '_1821.AngularContactThrustBallBearing':
        '''AngularContactThrustBallBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1821.AngularContactThrustBallBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to AngularContactThrustBallBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_asymmetric_spherical_roller_bearing(self) -> '_1822.AsymmetricSphericalRollerBearing':
        '''AsymmetricSphericalRollerBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1822.AsymmetricSphericalRollerBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to AsymmetricSphericalRollerBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_axial_thrust_cylindrical_roller_bearing(self) -> '_1823.AxialThrustCylindricalRollerBearing':
        '''AxialThrustCylindricalRollerBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1823.AxialThrustCylindricalRollerBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to AxialThrustCylindricalRollerBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_axial_thrust_needle_roller_bearing(self) -> '_1824.AxialThrustNeedleRollerBearing':
        '''AxialThrustNeedleRollerBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1824.AxialThrustNeedleRollerBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to AxialThrustNeedleRollerBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_ball_bearing(self) -> '_1825.BallBearing':
        '''BallBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1825.BallBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to BallBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_barrel_roller_bearing(self) -> '_1827.BarrelRollerBearing':
        '''BarrelRollerBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1827.BarrelRollerBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to BarrelRollerBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_crossed_roller_bearing(self) -> '_1832.CrossedRollerBearing':
        '''CrossedRollerBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1832.CrossedRollerBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to CrossedRollerBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_cylindrical_roller_bearing(self) -> '_1833.CylindricalRollerBearing':
        '''CylindricalRollerBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1833.CylindricalRollerBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to CylindricalRollerBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_deep_groove_ball_bearing(self) -> '_1834.DeepGrooveBallBearing':
        '''DeepGrooveBallBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1834.DeepGrooveBallBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to DeepGrooveBallBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_four_point_contact_ball_bearing(self) -> '_1836.FourPointContactBallBearing':
        '''FourPointContactBallBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1836.FourPointContactBallBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to FourPointContactBallBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_multi_point_contact_ball_bearing(self) -> '_1838.MultiPointContactBallBearing':
        '''MultiPointContactBallBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1838.MultiPointContactBallBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to MultiPointContactBallBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_needle_roller_bearing(self) -> '_1839.NeedleRollerBearing':
        '''NeedleRollerBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1839.NeedleRollerBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to NeedleRollerBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_non_barrel_roller_bearing(self) -> '_1840.NonBarrelRollerBearing':
        '''NonBarrelRollerBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1840.NonBarrelRollerBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to NonBarrelRollerBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_roller_bearing(self) -> '_1841.RollerBearing':
        '''RollerBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1841.RollerBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to RollerBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_rolling_bearing(self) -> '_1844.RollingBearing':
        '''RollingBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1844.RollingBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to RollingBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_self_aligning_ball_bearing(self) -> '_1845.SelfAligningBallBearing':
        '''SelfAligningBallBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1845.SelfAligningBallBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to SelfAligningBallBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_spherical_roller_bearing(self) -> '_1847.SphericalRollerBearing':
        '''SphericalRollerBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1847.SphericalRollerBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to SphericalRollerBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_spherical_roller_thrust_bearing(self) -> '_1848.SphericalRollerThrustBearing':
        '''SphericalRollerThrustBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1848.SphericalRollerThrustBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to SphericalRollerThrustBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_taper_roller_bearing(self) -> '_1849.TaperRollerBearing':
        '''TaperRollerBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1849.TaperRollerBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to TaperRollerBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_three_point_contact_ball_bearing(self) -> '_1850.ThreePointContactBallBearing':
        '''ThreePointContactBallBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1850.ThreePointContactBallBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to ThreePointContactBallBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_thrust_ball_bearing(self) -> '_1851.ThrustBallBearing':
        '''ThrustBallBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1851.ThrustBallBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to ThrustBallBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_toroidal_roller_bearing(self) -> '_1852.ToroidalRollerBearing':
        '''ToroidalRollerBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1852.ToroidalRollerBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to ToroidalRollerBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_pad_fluid_film_bearing(self) -> '_1865.PadFluidFilmBearing':
        '''PadFluidFilmBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1865.PadFluidFilmBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to PadFluidFilmBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_plain_grease_filled_journal_bearing(self) -> '_1867.PlainGreaseFilledJournalBearing':
        '''PlainGreaseFilledJournalBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1867.PlainGreaseFilledJournalBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to PlainGreaseFilledJournalBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_plain_journal_bearing(self) -> '_1869.PlainJournalBearing':
        '''PlainJournalBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1869.PlainJournalBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to PlainJournalBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_plain_oil_fed_journal_bearing(self) -> '_1871.PlainOilFedJournalBearing':
        '''PlainOilFedJournalBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1871.PlainOilFedJournalBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to PlainOilFedJournalBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_tilting_pad_journal_bearing(self) -> '_1872.TiltingPadJournalBearing':
        '''TiltingPadJournalBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1872.TiltingPadJournalBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to TiltingPadJournalBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_tilting_pad_thrust_bearing(self) -> '_1873.TiltingPadThrustBearing':
        '''TiltingPadThrustBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1873.TiltingPadThrustBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to TiltingPadThrustBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_concept_axial_clearance_bearing(self) -> '_1875.ConceptAxialClearanceBearing':
        '''ConceptAxialClearanceBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1875.ConceptAxialClearanceBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to ConceptAxialClearanceBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_concept_clearance_bearing(self) -> '_1876.ConceptClearanceBearing':
        '''ConceptClearanceBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1876.ConceptClearanceBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to ConceptClearanceBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def simple_bearing_detail_property_of_type_concept_radial_clearance_bearing(self) -> '_1877.ConceptRadialClearanceBearing':
        '''ConceptRadialClearanceBearing: 'SimpleBearingDetailProperty' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1877.ConceptRadialClearanceBearing.TYPE not in self.wrapped.SimpleBearingDetailProperty.__class__.__mro__:
            raise CastException('Failed to cast simple_bearing_detail_property to ConceptRadialClearanceBearing. Expected: {}.'.format(self.wrapped.SimpleBearingDetailProperty.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SimpleBearingDetailProperty.__class__)(self.wrapped.SimpleBearingDetailProperty) if self.wrapped.SimpleBearingDetailProperty else None

    @property
    def detail(self) -> '_1815.BearingDesign':
        '''BearingDesign: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1815.BearingDesign.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to BearingDesign. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_detailed_bearing(self) -> '_1816.DetailedBearing':
        '''DetailedBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1816.DetailedBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to DetailedBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_dummy_rolling_bearing(self) -> '_1817.DummyRollingBearing':
        '''DummyRollingBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1817.DummyRollingBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to DummyRollingBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_linear_bearing(self) -> '_1818.LinearBearing':
        '''LinearBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1818.LinearBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to LinearBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_non_linear_bearing(self) -> '_1819.NonLinearBearing':
        '''NonLinearBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1819.NonLinearBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to NonLinearBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_angular_contact_ball_bearing(self) -> '_1820.AngularContactBallBearing':
        '''AngularContactBallBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1820.AngularContactBallBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to AngularContactBallBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_angular_contact_thrust_ball_bearing(self) -> '_1821.AngularContactThrustBallBearing':
        '''AngularContactThrustBallBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1821.AngularContactThrustBallBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to AngularContactThrustBallBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_asymmetric_spherical_roller_bearing(self) -> '_1822.AsymmetricSphericalRollerBearing':
        '''AsymmetricSphericalRollerBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1822.AsymmetricSphericalRollerBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to AsymmetricSphericalRollerBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_axial_thrust_cylindrical_roller_bearing(self) -> '_1823.AxialThrustCylindricalRollerBearing':
        '''AxialThrustCylindricalRollerBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1823.AxialThrustCylindricalRollerBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to AxialThrustCylindricalRollerBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_axial_thrust_needle_roller_bearing(self) -> '_1824.AxialThrustNeedleRollerBearing':
        '''AxialThrustNeedleRollerBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1824.AxialThrustNeedleRollerBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to AxialThrustNeedleRollerBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_ball_bearing(self) -> '_1825.BallBearing':
        '''BallBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1825.BallBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to BallBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_barrel_roller_bearing(self) -> '_1827.BarrelRollerBearing':
        '''BarrelRollerBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1827.BarrelRollerBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to BarrelRollerBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_crossed_roller_bearing(self) -> '_1832.CrossedRollerBearing':
        '''CrossedRollerBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1832.CrossedRollerBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to CrossedRollerBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_cylindrical_roller_bearing(self) -> '_1833.CylindricalRollerBearing':
        '''CylindricalRollerBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1833.CylindricalRollerBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to CylindricalRollerBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_deep_groove_ball_bearing(self) -> '_1834.DeepGrooveBallBearing':
        '''DeepGrooveBallBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1834.DeepGrooveBallBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to DeepGrooveBallBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_four_point_contact_ball_bearing(self) -> '_1836.FourPointContactBallBearing':
        '''FourPointContactBallBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1836.FourPointContactBallBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to FourPointContactBallBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_multi_point_contact_ball_bearing(self) -> '_1838.MultiPointContactBallBearing':
        '''MultiPointContactBallBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1838.MultiPointContactBallBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to MultiPointContactBallBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_needle_roller_bearing(self) -> '_1839.NeedleRollerBearing':
        '''NeedleRollerBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1839.NeedleRollerBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to NeedleRollerBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_non_barrel_roller_bearing(self) -> '_1840.NonBarrelRollerBearing':
        '''NonBarrelRollerBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1840.NonBarrelRollerBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to NonBarrelRollerBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_roller_bearing(self) -> '_1841.RollerBearing':
        '''RollerBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1841.RollerBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to RollerBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_rolling_bearing(self) -> '_1844.RollingBearing':
        '''RollingBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1844.RollingBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to RollingBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_self_aligning_ball_bearing(self) -> '_1845.SelfAligningBallBearing':
        '''SelfAligningBallBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1845.SelfAligningBallBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to SelfAligningBallBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_spherical_roller_bearing(self) -> '_1847.SphericalRollerBearing':
        '''SphericalRollerBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1847.SphericalRollerBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to SphericalRollerBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_spherical_roller_thrust_bearing(self) -> '_1848.SphericalRollerThrustBearing':
        '''SphericalRollerThrustBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1848.SphericalRollerThrustBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to SphericalRollerThrustBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_taper_roller_bearing(self) -> '_1849.TaperRollerBearing':
        '''TaperRollerBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1849.TaperRollerBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to TaperRollerBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_three_point_contact_ball_bearing(self) -> '_1850.ThreePointContactBallBearing':
        '''ThreePointContactBallBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1850.ThreePointContactBallBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to ThreePointContactBallBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_thrust_ball_bearing(self) -> '_1851.ThrustBallBearing':
        '''ThrustBallBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1851.ThrustBallBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to ThrustBallBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_toroidal_roller_bearing(self) -> '_1852.ToroidalRollerBearing':
        '''ToroidalRollerBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1852.ToroidalRollerBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to ToroidalRollerBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_pad_fluid_film_bearing(self) -> '_1865.PadFluidFilmBearing':
        '''PadFluidFilmBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1865.PadFluidFilmBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to PadFluidFilmBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_plain_grease_filled_journal_bearing(self) -> '_1867.PlainGreaseFilledJournalBearing':
        '''PlainGreaseFilledJournalBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1867.PlainGreaseFilledJournalBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to PlainGreaseFilledJournalBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_plain_journal_bearing(self) -> '_1869.PlainJournalBearing':
        '''PlainJournalBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1869.PlainJournalBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to PlainJournalBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_plain_oil_fed_journal_bearing(self) -> '_1871.PlainOilFedJournalBearing':
        '''PlainOilFedJournalBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1871.PlainOilFedJournalBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to PlainOilFedJournalBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_tilting_pad_journal_bearing(self) -> '_1872.TiltingPadJournalBearing':
        '''TiltingPadJournalBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1872.TiltingPadJournalBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to TiltingPadJournalBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_tilting_pad_thrust_bearing(self) -> '_1873.TiltingPadThrustBearing':
        '''TiltingPadThrustBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1873.TiltingPadThrustBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to TiltingPadThrustBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_concept_axial_clearance_bearing(self) -> '_1875.ConceptAxialClearanceBearing':
        '''ConceptAxialClearanceBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1875.ConceptAxialClearanceBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to ConceptAxialClearanceBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_concept_clearance_bearing(self) -> '_1876.ConceptClearanceBearing':
        '''ConceptClearanceBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1876.ConceptClearanceBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to ConceptClearanceBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def detail_of_type_concept_radial_clearance_bearing(self) -> '_1877.ConceptRadialClearanceBearing':
        '''ConceptRadialClearanceBearing: 'Detail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1877.ConceptRadialClearanceBearing.TYPE not in self.wrapped.Detail.__class__.__mro__:
            raise CastException('Failed to cast detail to ConceptRadialClearanceBearing. Expected: {}.'.format(self.wrapped.Detail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Detail.__class__)(self.wrapped.Detail) if self.wrapped.Detail else None

    @property
    def axial_internal_clearance_tolerance(self) -> '_2088.AxialInternalClearanceTolerance':
        '''AxialInternalClearanceTolerance: 'AxialInternalClearanceTolerance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2088.AxialInternalClearanceTolerance)(self.wrapped.AxialInternalClearanceTolerance) if self.wrapped.AxialInternalClearanceTolerance else None

    @property
    def radial_internal_clearance_tolerance(self) -> '_2121.RadialInternalClearanceTolerance':
        '''RadialInternalClearanceTolerance: 'RadialInternalClearanceTolerance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2121.RadialInternalClearanceTolerance)(self.wrapped.RadialInternalClearanceTolerance) if self.wrapped.RadialInternalClearanceTolerance else None

    @property
    def overridden_lubrication_detail(self) -> '_232.LubricationDetail':
        '''LubricationDetail: 'OverriddenLubricationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_232.LubricationDetail)(self.wrapped.OverriddenLubricationDetail) if self.wrapped.OverriddenLubricationDetail else None

    @property
    def friction_coefficients(self) -> '_1758.RollingBearingFrictionCoefficients':
        '''RollingBearingFrictionCoefficients: 'FrictionCoefficients' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1758.RollingBearingFrictionCoefficients)(self.wrapped.FrictionCoefficients) if self.wrapped.FrictionCoefficients else None

    @property
    def force_at_zero_displacement(self) -> '_1563.VectorWithLinearAndAngularComponents':
        '''VectorWithLinearAndAngularComponents: 'ForceAtZeroDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1563.VectorWithLinearAndAngularComponents)(self.wrapped.ForceAtZeroDisplacement) if self.wrapped.ForceAtZeroDisplacement else None

    @property
    def tolerance_combinations(self) -> 'List[_1621.ToleranceCombination]':
        '''List[ToleranceCombination]: 'ToleranceCombinations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ToleranceCombinations, constructor.new(_1621.ToleranceCombination))
        return value

    @property
    def mounting(self) -> 'List[_2090.BearingRaceMountingOptions]':
        '''List[BearingRaceMountingOptions]: 'Mounting' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Mounting, constructor.new(_2090.BearingRaceMountingOptions))
        return value

    @property
    def is_radial_bearing(self) -> 'bool':
        '''bool: 'IsRadialBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsRadialBearing

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

    def set_detail_from_catalogue(self, catalogue: '_1571.BearingCatalog', designation: 'str'):
        ''' 'SetDetailFromCatalogue' is the original name of this method.

        Args:
            catalogue (mastapy.bearings.BearingCatalog)
            designation (str)
        '''

        catalogue = conversion.mp_to_pn_enum(catalogue)
        designation = str(designation)
        self.wrapped.SetDetailFromCatalogue(catalogue, designation if designation else None)

    def try_attach_left_side_to(self, shaft: '_2129.Shaft', offset: Optional['float'] = float('nan')) -> '_2094.ComponentsConnectedResult':
        ''' 'TryAttachLeftSideTo' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        offset = float(offset)
        method_result = self.wrapped.TryAttachLeftSideTo(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def try_attach_right_side_to(self, shaft: '_2129.Shaft', offset: Optional['float'] = float('nan')) -> '_2094.ComponentsConnectedResult':
        ''' 'TryAttachRightSideTo' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        offset = float(offset)
        method_result = self.wrapped.TryAttachRightSideTo(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
