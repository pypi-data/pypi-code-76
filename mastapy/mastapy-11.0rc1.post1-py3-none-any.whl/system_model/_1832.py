'''_1832.py

Design
'''


from typing import (
    List, Callable, Optional, TypeVar
)
from os import path

from mastapy._internal import constructor, conversion, enum_with_selected_value_runtime
from mastapy._internal.class_property import classproperty
from mastapy.utility_gui import _1528
from mastapy import _3, _6552, _0
from mastapy._internal.python_net import python_net_import
from mastapy.materials.efficiency import _95
from mastapy._internal.implicit import enum_with_selected_value, overridable, list_with_selected_item
from mastapy.system_model.part_model import (
    _2059, _2056, _2058, _2052,
    _2021, _2022, _2023, _2026,
    _2028, _2029, _2030, _2033,
    _2034, _2037, _2038, _2039,
    _2042, _2046, _2047, _2048,
    _2050, _2053, _2055, _2060,
    _2061, _2062
)
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears import _122, _128
from mastapy.gears.materials import _381
from mastapy.utility import _1149, _1148, _1147
from mastapy.system_model import _1851, _1850
from mastapy.shafts import _34
from mastapy.detailed_rigid_connectors.splines import _980
from mastapy._math.vector_3d import Vector3D
from mastapy.system_model.part_model.gears import (
    _2094, _2115, _2095, _2096,
    _2097, _2098, _2099, _2100,
    _2101, _2102, _2103, _2104,
    _2105, _2106, _2107, _2108,
    _2109, _2110, _2111, _2112,
    _2114, _2116, _2117, _2118,
    _2119, _2120, _2121, _2122,
    _2123, _2124, _2125, _2126,
    _2127, _2128, _2129, _2130,
    _2131, _2132, _2133, _2134,
    _2135, _2136
)
from mastapy.system_model.imported_fes import _1954
from mastapy.bearings.bearing_results.rolling import _1628
from mastapy.system_model.part_model.configurations import _2190, _2188, _2191
from mastapy.system_model.analyses_and_results.load_case_groups import _5283, _5284
from mastapy.system_model.analyses_and_results.static_loads import _6234
from mastapy.utility.model_validation import _1330
from mastapy.system_model.database_access import _1871
from mastapy.bearings.bearing_designs.rolling import _1798
from mastapy.system_model.analyses_and_results.synchroniser_analysis import _2523
from mastapy.system_model.part_model.shaft_model import _2065
from mastapy.system_model.part_model.couplings import (
    _2154, _2156, _2157, _2159,
    _2160, _2161, _2162, _2163,
    _2164, _2165, _2166, _2167,
    _2173, _2174, _2175, _2176,
    _2177, _2178, _2180, _2181,
    _2182, _2183, _2184, _2186
)
from mastapy.system_model.part_model.creation_options import (
    _2150, _2152, _2153, _2151
)
from mastapy.gears.gear_designs.creation_options import _883, _886, _885
from mastapy.nodal_analysis import _1402

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_ARRAY = python_net_import('System', 'Array')
_STRING = python_net_import('System', 'String')
_BOOLEAN = python_net_import('System', 'Boolean')
_TASK_PROGRESS = python_net_import('SMT.MastaAPIUtility', 'TaskProgress')
_DESIGN = python_net_import('SMT.MastaAPI.SystemModel', 'Design')


__docformat__ = 'restructuredtext en'
__all__ = ('Design',)


class Design(_0.APIBase):
    '''Design

    This is a mastapy class.
    '''

    TYPE = _DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Design.TYPE' = None):
        super().__init__(instance_to_wrap if instance_to_wrap else Design.TYPE())
        self._freeze()

    @classproperty
    def available_examples(cls) -> 'List[str]':
        '''List[str]: 'AvailableExamples' is the original name of this property.'''

        value = conversion.pn_to_mp_objects_in_list(Design.TYPE.AvailableExamples, str)
        return value

    @property
    def masta_gui(self) -> '_1528.MASTAGUI':
        '''MASTAGUI: 'MastaGUI' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1528.MASTAGUI)(self.wrapped.MastaGUI) if self.wrapped.MastaGUI else None

    @property
    def masta_settings(self) -> '_3.MastaSettings':
        '''MastaSettings: 'MastaSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3.MastaSettings)(self.wrapped.MastaSettings) if self.wrapped.MastaSettings else None

    @property
    def change_gears_to_clones_where_suitable(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ChangeGearsToClonesWhereSuitable' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ChangeGearsToClonesWhereSuitable

    @property
    def iso14179_part_1_coefficient_of_friction_constants_and_exponents_for_external_external_meshes_database(self) -> 'str':
        '''str: 'ISO14179Part1CoefficientOfFrictionConstantsAndExponentsForExternalExternalMeshesDatabase' is the original name of this property.'''

        return self.wrapped.ISO14179Part1CoefficientOfFrictionConstantsAndExponentsForExternalExternalMeshesDatabase.SelectedItemName

    @iso14179_part_1_coefficient_of_friction_constants_and_exponents_for_external_external_meshes_database.setter
    def iso14179_part_1_coefficient_of_friction_constants_and_exponents_for_external_external_meshes_database(self, value: 'str'):
        self.wrapped.ISO14179Part1CoefficientOfFrictionConstantsAndExponentsForExternalExternalMeshesDatabase.SetSelectedItem(str(value) if value else None)

    @property
    def iso14179_part_1_coefficient_of_friction_constants_and_exponents_for_internal_external_meshes_database(self) -> 'str':
        '''str: 'ISO14179Part1CoefficientOfFrictionConstantsAndExponentsForInternalExternalMeshesDatabase' is the original name of this property.'''

        return self.wrapped.ISO14179Part1CoefficientOfFrictionConstantsAndExponentsForInternalExternalMeshesDatabase.SelectedItemName

    @iso14179_part_1_coefficient_of_friction_constants_and_exponents_for_internal_external_meshes_database.setter
    def iso14179_part_1_coefficient_of_friction_constants_and_exponents_for_internal_external_meshes_database(self, value: 'str'):
        self.wrapped.ISO14179Part1CoefficientOfFrictionConstantsAndExponentsForInternalExternalMeshesDatabase.SetSelectedItem(str(value) if value else None)

    @property
    def volumetric_oil_air_mixture_ratio(self) -> 'float':
        '''float: 'VolumetricOilAirMixtureRatio' is the original name of this property.'''

        return self.wrapped.VolumetricOilAirMixtureRatio

    @volumetric_oil_air_mixture_ratio.setter
    def volumetric_oil_air_mixture_ratio(self, value: 'float'):
        self.wrapped.VolumetricOilAirMixtureRatio = float(value) if value else 0.0

    @property
    def coefficient_of_friction(self) -> 'float':
        '''float: 'CoefficientOfFriction' is the original name of this property.'''

        return self.wrapped.CoefficientOfFriction

    @coefficient_of_friction.setter
    def coefficient_of_friction(self, value: 'float'):
        self.wrapped.CoefficientOfFriction = float(value) if value else 0.0

    @property
    def efficiency_rating_method_for_bearings(self) -> '_95.BearingEfficiencyRatingMethod':
        '''BearingEfficiencyRatingMethod: 'EfficiencyRatingMethodForBearings' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.EfficiencyRatingMethodForBearings)
        return constructor.new(_95.BearingEfficiencyRatingMethod)(value) if value else None

    @efficiency_rating_method_for_bearings.setter
    def efficiency_rating_method_for_bearings(self, value: '_95.BearingEfficiencyRatingMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.EfficiencyRatingMethodForBearings = value

    @property
    def shaft_diameter_modification_due_to_rolling_bearing_rings(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing':
        '''enum_with_selected_value.EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing: 'ShaftDiameterModificationDueToRollingBearingRings' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ShaftDiameterModificationDueToRollingBearingRings, value) if self.wrapped.ShaftDiameterModificationDueToRollingBearingRings else None

    @shaft_diameter_modification_due_to_rolling_bearing_rings.setter
    def shaft_diameter_modification_due_to_rolling_bearing_rings(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ShaftDiameterModificationDueToRollingBearingRings = value

    @property
    def manufacturer(self) -> 'str':
        '''str: 'Manufacturer' is the original name of this property.'''

        return self.wrapped.Manufacturer

    @manufacturer.setter
    def manufacturer(self, value: 'str'):
        self.wrapped.Manufacturer = str(value) if value else None

    @property
    def housing_material_for_grounded_connections(self) -> 'str':
        '''str: 'HousingMaterialForGroundedConnections' is the original name of this property.'''

        return self.wrapped.HousingMaterialForGroundedConnections.SelectedItemName

    @housing_material_for_grounded_connections.setter
    def housing_material_for_grounded_connections(self, value: 'str'):
        self.wrapped.HousingMaterialForGroundedConnections.SetSelectedItem(str(value) if value else None)

    @property
    def comment(self) -> 'str':
        '''str: 'Comment' is the original name of this property.'''

        return self.wrapped.Comment

    @comment.setter
    def comment(self, value: 'str'):
        self.wrapped.Comment = str(value) if value else None

    @property
    def node_size(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NodeSize' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NodeSize) if self.wrapped.NodeSize else None

    @node_size.setter
    def node_size(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.NodeSize = value

    @property
    def use_expanded_2d_projection_mode(self) -> 'bool':
        '''bool: 'UseExpanded2DProjectionMode' is the original name of this property.'''

        return self.wrapped.UseExpanded2DProjectionMode

    @use_expanded_2d_projection_mode.setter
    def use_expanded_2d_projection_mode(self, value: 'bool'):
        self.wrapped.UseExpanded2DProjectionMode = bool(value) if value else False

    @property
    def gravity_magnitude(self) -> 'float':
        '''float: 'GravityMagnitude' is the original name of this property.'''

        return self.wrapped.GravityMagnitude

    @gravity_magnitude.setter
    def gravity_magnitude(self, value: 'float'):
        self.wrapped.GravityMagnitude = float(value) if value else 0.0

    @property
    def input_power_load(self) -> 'list_with_selected_item.ListWithSelectedItem_PowerLoad':
        '''list_with_selected_item.ListWithSelectedItem_PowerLoad: 'InputPowerLoad' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_PowerLoad)(self.wrapped.InputPowerLoad) if self.wrapped.InputPowerLoad else None

    @input_power_load.setter
    def input_power_load(self, value: 'list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.InputPowerLoad = value

    @property
    def output_power_load(self) -> 'list_with_selected_item.ListWithSelectedItem_PowerLoad':
        '''list_with_selected_item.ListWithSelectedItem_PowerLoad: 'OutputPowerLoad' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_PowerLoad)(self.wrapped.OutputPowerLoad) if self.wrapped.OutputPowerLoad else None

    @output_power_load.setter
    def output_power_load(self, value: 'list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.OutputPowerLoad = value

    @property
    def design_name(self) -> 'str':
        '''str: 'DesignName' is the original name of this property.'''

        return self.wrapped.DesignName

    @design_name.setter
    def design_name(self, value: 'str'):
        self.wrapped.DesignName = str(value) if value else None

    @property
    def file_name(self) -> 'str':
        '''str: 'FileName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FileName

    @property
    def clear_undo_redo_stacks(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ClearUndoRedoStacks' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ClearUndoRedoStacks

    @property
    def gear_set_configuration(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'GearSetConfiguration' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.GearSetConfiguration) if self.wrapped.GearSetConfiguration else None

    @gear_set_configuration.setter
    def gear_set_configuration(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.GearSetConfiguration = value

    @property
    def number_of_gear_set_configurations(self) -> 'int':
        '''int: 'NumberOfGearSetConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfGearSetConfigurations

    @property
    def delete_all_inactive_gear_set_designs(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'DeleteAllInactiveGearSetDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeleteAllInactiveGearSetDesigns

    @property
    def add_gear_set_configuration(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddGearSetConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddGearSetConfiguration

    @property
    def delete_multiple_gear_set_configurations(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'DeleteMultipleGearSetConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeleteMultipleGearSetConfigurations

    @property
    def shaft_detail_configuration(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'ShaftDetailConfiguration' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.ShaftDetailConfiguration) if self.wrapped.ShaftDetailConfiguration else None

    @shaft_detail_configuration.setter
    def shaft_detail_configuration(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.ShaftDetailConfiguration = value

    @property
    def imported_fe_configuration(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'ImportedFEConfiguration' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.ImportedFEConfiguration) if self.wrapped.ImportedFEConfiguration else None

    @imported_fe_configuration.setter
    def imported_fe_configuration(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.ImportedFEConfiguration = value

    @property
    def bearing_configuration(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'BearingConfiguration' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.BearingConfiguration) if self.wrapped.BearingConfiguration else None

    @bearing_configuration.setter
    def bearing_configuration(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.BearingConfiguration = value

    @property
    def add_shaft_detail_configuration(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddShaftDetailConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddShaftDetailConfiguration

    @property
    def delete_multiple_shaft_detail_configurations(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'DeleteMultipleShaftDetailConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeleteMultipleShaftDetailConfigurations

    @property
    def add_bearing_detail_configuration_all_bearings(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddBearingDetailConfigurationAllBearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddBearingDetailConfigurationAllBearings

    @property
    def add_bearing_detail_configuration_rolling_bearings(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddBearingDetailConfigurationRollingBearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddBearingDetailConfigurationRollingBearings

    @property
    def delete_multiple_bearing_detail_configurations(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'DeleteMultipleBearingDetailConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeleteMultipleBearingDetailConfigurations

    @property
    def add_imported_fe_configuration(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddImportedFEConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddImportedFEConfiguration

    @property
    def delete_multiple_imported_fe_configurations(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'DeleteMultipleImportedFEConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeleteMultipleImportedFEConfigurations

    @property
    def delete_all_gear_set_configurations_that_have_errors_or_warnings(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'DeleteAllGearSetConfigurationsThatHaveErrorsOrWarnings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeleteAllGearSetConfigurationsThatHaveErrorsOrWarnings

    @property
    def delete_all_gear_sets_designs_that_are_not_used_in_configurations(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'DeleteAllGearSetsDesignsThatAreNotUsedInConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeleteAllGearSetsDesignsThatAreNotUsedInConfigurations

    @property
    def transverse_contact_ratio_requirement(self) -> '_122.ContactRatioRequirements':
        '''ContactRatioRequirements: 'TransverseContactRatioRequirement' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.TransverseContactRatioRequirement)
        return constructor.new(_122.ContactRatioRequirements)(value) if value else None

    @transverse_contact_ratio_requirement.setter
    def transverse_contact_ratio_requirement(self, value: '_122.ContactRatioRequirements'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TransverseContactRatioRequirement = value

    @property
    def axial_contact_ratio_requirement(self) -> '_122.ContactRatioRequirements':
        '''ContactRatioRequirements: 'AxialContactRatioRequirement' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.AxialContactRatioRequirement)
        return constructor.new(_122.ContactRatioRequirements)(value) if value else None

    @axial_contact_ratio_requirement.setter
    def axial_contact_ratio_requirement(self, value: '_122.ContactRatioRequirements'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AxialContactRatioRequirement = value

    @property
    def maximum_acceptable_axial_contact_ratio(self) -> 'float':
        '''float: 'MaximumAcceptableAxialContactRatio' is the original name of this property.'''

        return self.wrapped.MaximumAcceptableAxialContactRatio

    @maximum_acceptable_axial_contact_ratio.setter
    def maximum_acceptable_axial_contact_ratio(self, value: 'float'):
        self.wrapped.MaximumAcceptableAxialContactRatio = float(value) if value else 0.0

    @property
    def minimum_acceptable_axial_contact_ratio(self) -> 'float':
        '''float: 'MinimumAcceptableAxialContactRatio' is the original name of this property.'''

        return self.wrapped.MinimumAcceptableAxialContactRatio

    @minimum_acceptable_axial_contact_ratio.setter
    def minimum_acceptable_axial_contact_ratio(self, value: 'float'):
        self.wrapped.MinimumAcceptableAxialContactRatio = float(value) if value else 0.0

    @property
    def maximum_acceptable_axial_contact_ratio_above_integer(self) -> 'float':
        '''float: 'MaximumAcceptableAxialContactRatioAboveInteger' is the original name of this property.'''

        return self.wrapped.MaximumAcceptableAxialContactRatioAboveInteger

    @maximum_acceptable_axial_contact_ratio_above_integer.setter
    def maximum_acceptable_axial_contact_ratio_above_integer(self, value: 'float'):
        self.wrapped.MaximumAcceptableAxialContactRatioAboveInteger = float(value) if value else 0.0

    @property
    def minimum_acceptable_axial_contact_ratio_below_integer(self) -> 'float':
        '''float: 'MinimumAcceptableAxialContactRatioBelowInteger' is the original name of this property.'''

        return self.wrapped.MinimumAcceptableAxialContactRatioBelowInteger

    @minimum_acceptable_axial_contact_ratio_below_integer.setter
    def minimum_acceptable_axial_contact_ratio_below_integer(self, value: 'float'):
        self.wrapped.MinimumAcceptableAxialContactRatioBelowInteger = float(value) if value else 0.0

    @property
    def maximum_acceptable_transverse_contact_ratio(self) -> 'float':
        '''float: 'MaximumAcceptableTransverseContactRatio' is the original name of this property.'''

        return self.wrapped.MaximumAcceptableTransverseContactRatio

    @maximum_acceptable_transverse_contact_ratio.setter
    def maximum_acceptable_transverse_contact_ratio(self, value: 'float'):
        self.wrapped.MaximumAcceptableTransverseContactRatio = float(value) if value else 0.0

    @property
    def minimum_acceptable_transverse_contact_ratio(self) -> 'float':
        '''float: 'MinimumAcceptableTransverseContactRatio' is the original name of this property.'''

        return self.wrapped.MinimumAcceptableTransverseContactRatio

    @minimum_acceptable_transverse_contact_ratio.setter
    def minimum_acceptable_transverse_contact_ratio(self, value: 'float'):
        self.wrapped.MinimumAcceptableTransverseContactRatio = float(value) if value else 0.0

    @property
    def maximum_acceptable_transverse_contact_ratio_above_integer(self) -> 'float':
        '''float: 'MaximumAcceptableTransverseContactRatioAboveInteger' is the original name of this property.'''

        return self.wrapped.MaximumAcceptableTransverseContactRatioAboveInteger

    @maximum_acceptable_transverse_contact_ratio_above_integer.setter
    def maximum_acceptable_transverse_contact_ratio_above_integer(self, value: 'float'):
        self.wrapped.MaximumAcceptableTransverseContactRatioAboveInteger = float(value) if value else 0.0

    @property
    def minimum_acceptable_transverse_contact_ratio_below_integer(self) -> 'float':
        '''float: 'MinimumAcceptableTransverseContactRatioBelowInteger' is the original name of this property.'''

        return self.wrapped.MinimumAcceptableTransverseContactRatioBelowInteger

    @minimum_acceptable_transverse_contact_ratio_below_integer.setter
    def minimum_acceptable_transverse_contact_ratio_below_integer(self, value: 'float'):
        self.wrapped.MinimumAcceptableTransverseContactRatioBelowInteger = float(value) if value else 0.0

    @property
    def compare_results_to_previous_masta_version(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CompareResultsToPreviousMASTAVersion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CompareResultsToPreviousMASTAVersion

    @property
    def iso14179_coefficient_of_friction_constants_and_exponents_for_external_external_meshes(self) -> '_381.ISOTR1417912001CoefficientOfFrictionConstants':
        '''ISOTR1417912001CoefficientOfFrictionConstants: 'ISO14179CoefficientOfFrictionConstantsAndExponentsForExternalExternalMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_381.ISOTR1417912001CoefficientOfFrictionConstants)(self.wrapped.ISO14179CoefficientOfFrictionConstantsAndExponentsForExternalExternalMeshes) if self.wrapped.ISO14179CoefficientOfFrictionConstantsAndExponentsForExternalExternalMeshes else None

    @property
    def iso14179_coefficient_of_friction_constants_and_exponents_for_internal_external_meshes(self) -> '_381.ISOTR1417912001CoefficientOfFrictionConstants':
        '''ISOTR1417912001CoefficientOfFrictionConstants: 'ISO14179CoefficientOfFrictionConstantsAndExponentsForInternalExternalMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_381.ISOTR1417912001CoefficientOfFrictionConstants)(self.wrapped.ISO14179CoefficientOfFrictionConstantsAndExponentsForInternalExternalMeshes) if self.wrapped.ISO14179CoefficientOfFrictionConstantsAndExponentsForInternalExternalMeshes else None

    @property
    def file_save_details_most_recent(self) -> '_1149.FileHistoryItem':
        '''FileHistoryItem: 'FileSaveDetailsMostRecent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1149.FileHistoryItem)(self.wrapped.FileSaveDetailsMostRecent) if self.wrapped.FileSaveDetailsMostRecent else None

    @property
    def default_system_temperatures(self) -> '_1851.TransmissionTemperatureSet':
        '''TransmissionTemperatureSet: 'DefaultSystemTemperatures' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1851.TransmissionTemperatureSet)(self.wrapped.DefaultSystemTemperatures) if self.wrapped.DefaultSystemTemperatures else None

    @property
    def shafts(self) -> '_34.ShaftSafetyFactorSettings':
        '''ShaftSafetyFactorSettings: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_34.ShaftSafetyFactorSettings)(self.wrapped.Shafts) if self.wrapped.Shafts else None

    @property
    def detailed_spline_settings(self) -> '_980.DetailedSplineJointSettings':
        '''DetailedSplineJointSettings: 'DetailedSplineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_980.DetailedSplineJointSettings)(self.wrapped.DetailedSplineSettings) if self.wrapped.DetailedSplineSettings else None

    @property
    def gravity_vector_components(self) -> 'Vector3D':
        '''Vector3D: 'GravityVectorComponents' is the original name of this property.'''

        value = conversion.pn_to_mp_vector3d(self.wrapped.GravityVectorComponents)
        return value

    @gravity_vector_components.setter
    def gravity_vector_components(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.GravityVectorComponents = value

    @property
    def gravity_orientation(self) -> 'Vector3D':
        '''Vector3D: 'GravityOrientation' is the original name of this property.'''

        value = conversion.pn_to_mp_vector3d(self.wrapped.GravityOrientation)
        return value

    @gravity_orientation.setter
    def gravity_orientation(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.GravityOrientation = value

    @property
    def file_save_details_all(self) -> '_1148.FileHistory':
        '''FileHistory: 'FileSaveDetailsAll' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1148.FileHistory)(self.wrapped.FileSaveDetailsAll) if self.wrapped.FileSaveDetailsAll else None

    @property
    def gear_set_design_group(self) -> '_128.GearSetDesignGroup':
        '''GearSetDesignGroup: 'GearSetDesignGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_128.GearSetDesignGroup)(self.wrapped.GearSetDesignGroup) if self.wrapped.GearSetDesignGroup else None

    @property
    def selected_gear_set_selection_group(self) -> '_2094.ActiveGearSetDesignSelectionGroup':
        '''ActiveGearSetDesignSelectionGroup: 'SelectedGearSetSelectionGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2094.ActiveGearSetDesignSelectionGroup)(self.wrapped.SelectedGearSetSelectionGroup) if self.wrapped.SelectedGearSetSelectionGroup else None

    @property
    def system(self) -> '_1850.SystemReporting':
        '''SystemReporting: 'System' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1850.SystemReporting)(self.wrapped.System) if self.wrapped.System else None

    @property
    def fe_batch_operations(self) -> '_1954.BatchOperations':
        '''BatchOperations: 'FEBatchOperations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1954.BatchOperations)(self.wrapped.FEBatchOperations) if self.wrapped.FEBatchOperations else None

    @property
    def iso14179_settings_per_bearing_type(self) -> 'List[_1628.ISO14179SettingsPerBearingType]':
        '''List[ISO14179SettingsPerBearingType]: 'ISO14179SettingsPerBearingType' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ISO14179SettingsPerBearingType, constructor.new(_1628.ISO14179SettingsPerBearingType))
        return value

    @property
    def gear_set_configurations(self) -> 'List[_2094.ActiveGearSetDesignSelectionGroup]':
        '''List[ActiveGearSetDesignSelectionGroup]: 'GearSetConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearSetConfigurations, constructor.new(_2094.ActiveGearSetDesignSelectionGroup))
        return value

    @property
    def shaft_detail_configurations(self) -> 'List[_2190.ActiveShaftDesignSelectionGroup]':
        '''List[ActiveShaftDesignSelectionGroup]: 'ShaftDetailConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftDetailConfigurations, constructor.new(_2190.ActiveShaftDesignSelectionGroup))
        return value

    @property
    def imported_fe_configurations(self) -> 'List[_2188.ActiveImportedFESelectionGroup]':
        '''List[ActiveImportedFESelectionGroup]: 'ImportedFEConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEConfigurations, constructor.new(_2188.ActiveImportedFESelectionGroup))
        return value

    @property
    def bearing_detail_configurations(self) -> 'List[_2191.BearingDetailConfiguration]':
        '''List[BearingDetailConfiguration]: 'BearingDetailConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BearingDetailConfigurations, constructor.new(_2191.BearingDetailConfiguration))
        return value

    @property
    def design_states(self) -> 'List[_5283.DesignState]':
        '''List[DesignState]: 'DesignStates' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DesignStates, constructor.new(_5283.DesignState))
        return value

    @property
    def static_loads(self) -> 'List[_6234.StaticLoadCase]':
        '''List[StaticLoadCase]: 'StaticLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StaticLoads, constructor.new(_6234.StaticLoadCase))
        return value

    @property
    def duty_cycles(self) -> 'List[_5284.DutyCycle]':
        '''List[DutyCycle]: 'DutyCycles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DutyCycles, constructor.new(_5284.DutyCycle))
        return value

    @property
    def root_assembly(self) -> '_2058.RootAssembly':
        '''RootAssembly: 'RootAssembly' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2058.RootAssembly)(self.wrapped.RootAssembly) if self.wrapped.RootAssembly else None

    @property
    def gear_set_config(self) -> '_2115.GearSetConfiguration':
        '''GearSetConfiguration: 'GearSetConfig' is the original name of this property.'''

        return constructor.new(_2115.GearSetConfiguration)(self.wrapped.GearSetConfig) if self.wrapped.GearSetConfig else None

    @gear_set_config.setter
    def gear_set_config(self, value: '_2115.GearSetConfiguration'):
        value = value.wrapped if value else None
        self.wrapped.GearSetConfig = value

    @property
    def status(self) -> '_1330.Status':
        '''Status: 'Status' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1330.Status)(self.wrapped.Status) if self.wrapped.Status else None

    @property
    def databases(self) -> '_1871.Databases':
        '''Databases: 'Databases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1871.Databases)(self.wrapped.Databases) if self.wrapped.Databases else None

    def clear_design(self):
        ''' 'ClearDesign' is the original name of this method.'''

        self.wrapped.ClearDesign()

    def remove_bearing_from_database(self, rolling_bearing: '_1798.RollingBearing'):
        ''' 'RemoveBearingFromDatabase' is the original name of this method.

        Args:
            rolling_bearing (mastapy.bearings.bearing_designs.rolling.RollingBearing)
        '''

        self.wrapped.RemoveBearingFromDatabase(rolling_bearing.wrapped if rolling_bearing else None)

    def design_state_named(self, name: 'str') -> '_5283.DesignState':
        ''' 'DesignStateNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.analyses_and_results.load_case_groups.DesignState
        '''

        name = str(name)
        method_result = self.wrapped.DesignStateNamed(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def duty_cycle_named(self, name: 'str') -> '_5284.DutyCycle':
        ''' 'DutyCycleNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.analyses_and_results.load_case_groups.DutyCycle
        '''

        name = str(name)
        method_result = self.wrapped.DutyCycleNamed(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def __copy__(self) -> 'Design':
        ''' 'Copy' is the original name of this method.

        Returns:
            mastapy.system_model.Design
        '''

        method_result = self.wrapped.Copy()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def __deepcopy__(self, memo) -> 'Design':
        ''' 'Copy' is the original name of this method.

        Returns:
            mastapy.system_model.Design
        '''

        method_result = self.wrapped.Copy()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def save(self, file_name: 'str', save_results: 'bool') -> '_1330.Status':
        ''' 'Save' is the original name of this method.

        Args:
            file_name (str)
            save_results (bool)

        Returns:
            mastapy.utility.model_validation.Status
        '''

        file_name = str(file_name)
        save_results = bool(save_results)
        method_result = self.wrapped.Save.Overloads[_STRING, _BOOLEAN](file_name if file_name else None, save_results if save_results else False)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def save_with_progess(self, file_name: 'str', save_results: 'bool', progress: '_6552.TaskProgress') -> '_1330.Status':
        ''' 'Save' is the original name of this method.

        Args:
            file_name (str)
            save_results (bool)
            progress (mastapy.TaskProgress)

        Returns:
            mastapy.utility.model_validation.Status
        '''

        file_name = str(file_name)
        save_results = bool(save_results)
        method_result = self.wrapped.Save.Overloads[_STRING, _BOOLEAN, _TASK_PROGRESS](file_name if file_name else None, save_results if save_results else False, progress.wrapped if progress else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def remove_synchroniser_shift(self, shift: '_2523.SynchroniserShift'):
        ''' 'RemoveSynchroniserShift' is the original name of this method.

        Args:
            shift (mastapy.system_model.analyses_and_results.synchroniser_analysis.SynchroniserShift)
        '''

        self.wrapped.RemoveSynchroniserShift(shift.wrapped if shift else None)

    def add_synchroniser_shift(self, name: 'str') -> '_2523.SynchroniserShift':
        ''' 'AddSynchroniserShift' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.analyses_and_results.synchroniser_analysis.SynchroniserShift
        '''

        name = str(name)
        method_result = self.wrapped.AddSynchroniserShift.Overloads[_STRING](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_synchroniser_shift_empty(self) -> '_2523.SynchroniserShift':
        ''' 'AddSynchroniserShift' is the original name of this method.

        Returns:
            mastapy.system_model.analyses_and_results.synchroniser_analysis.SynchroniserShift
        '''

        method_result = self.wrapped.AddSynchroniserShift()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_design_state(self, name: Optional['str'] = 'New Design State') -> '_5283.DesignState':
        ''' 'AddDesignState' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.analyses_and_results.load_case_groups.DesignState
        '''

        name = str(name)
        method_result = self.wrapped.AddDesignState(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_duty_cycle(self, name: Optional['str'] = 'New Duty Cycle') -> '_5284.DutyCycle':
        ''' 'AddDutyCycle' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.analyses_and_results.load_case_groups.DutyCycle
        '''

        name = str(name)
        method_result = self.wrapped.AddDutyCycle(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def dispose(self):
        ''' 'Dispose' is the original name of this method.'''

        self.wrapped.Dispose()

    def all_parts(self) -> 'List[_2052.Part]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Part]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2052.Part.TYPE](), constructor.new(_2052.Part))

    def all_parts_of_type_assembly(self) -> 'List[_2021.Assembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Assembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2021.Assembly.TYPE](), constructor.new(_2021.Assembly))

    def all_parts_of_type_abstract_assembly(self) -> 'List[_2022.AbstractAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.AbstractAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2022.AbstractAssembly.TYPE](), constructor.new(_2022.AbstractAssembly))

    def all_parts_of_type_abstract_shaft_or_housing(self) -> 'List[_2023.AbstractShaftOrHousing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.AbstractShaftOrHousing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2023.AbstractShaftOrHousing.TYPE](), constructor.new(_2023.AbstractShaftOrHousing))

    def all_parts_of_type_bearing(self) -> 'List[_2026.Bearing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Bearing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2026.Bearing.TYPE](), constructor.new(_2026.Bearing))

    def all_parts_of_type_bolt(self) -> 'List[_2028.Bolt]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Bolt]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2028.Bolt.TYPE](), constructor.new(_2028.Bolt))

    def all_parts_of_type_bolted_joint(self) -> 'List[_2029.BoltedJoint]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.BoltedJoint]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2029.BoltedJoint.TYPE](), constructor.new(_2029.BoltedJoint))

    def all_parts_of_type_component(self) -> 'List[_2030.Component]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Component]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2030.Component.TYPE](), constructor.new(_2030.Component))

    def all_parts_of_type_connector(self) -> 'List[_2033.Connector]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Connector]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2033.Connector.TYPE](), constructor.new(_2033.Connector))

    def all_parts_of_type_datum(self) -> 'List[_2034.Datum]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Datum]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2034.Datum.TYPE](), constructor.new(_2034.Datum))

    def all_parts_of_type_external_cad_model(self) -> 'List[_2037.ExternalCADModel]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.ExternalCADModel]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2037.ExternalCADModel.TYPE](), constructor.new(_2037.ExternalCADModel))

    def all_parts_of_type_flexible_pin_assembly(self) -> 'List[_2038.FlexiblePinAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.FlexiblePinAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2038.FlexiblePinAssembly.TYPE](), constructor.new(_2038.FlexiblePinAssembly))

    def all_parts_of_type_guide_dxf_model(self) -> 'List[_2039.GuideDxfModel]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.GuideDxfModel]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2039.GuideDxfModel.TYPE](), constructor.new(_2039.GuideDxfModel))

    def all_parts_of_type_imported_fe_component(self) -> 'List[_2042.ImportedFEComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.ImportedFEComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2042.ImportedFEComponent.TYPE](), constructor.new(_2042.ImportedFEComponent))

    def all_parts_of_type_mass_disc(self) -> 'List[_2046.MassDisc]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MassDisc]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2046.MassDisc.TYPE](), constructor.new(_2046.MassDisc))

    def all_parts_of_type_measurement_component(self) -> 'List[_2047.MeasurementComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MeasurementComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2047.MeasurementComponent.TYPE](), constructor.new(_2047.MeasurementComponent))

    def all_parts_of_type_mountable_component(self) -> 'List[_2048.MountableComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MountableComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2048.MountableComponent.TYPE](), constructor.new(_2048.MountableComponent))

    def all_parts_of_type_oil_seal(self) -> 'List[_2050.OilSeal]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.OilSeal]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2050.OilSeal.TYPE](), constructor.new(_2050.OilSeal))

    def all_parts_of_type_planet_carrier(self) -> 'List[_2053.PlanetCarrier]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PlanetCarrier]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2053.PlanetCarrier.TYPE](), constructor.new(_2053.PlanetCarrier))

    def all_parts_of_type_point_load(self) -> 'List[_2055.PointLoad]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PointLoad]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2055.PointLoad.TYPE](), constructor.new(_2055.PointLoad))

    def all_parts_of_type_power_load(self) -> 'List[_2056.PowerLoad]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PowerLoad]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2056.PowerLoad.TYPE](), constructor.new(_2056.PowerLoad))

    def all_parts_of_type_root_assembly(self) -> 'List[_2058.RootAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.RootAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2058.RootAssembly.TYPE](), constructor.new(_2058.RootAssembly))

    def all_parts_of_type_specialised_assembly(self) -> 'List[_2060.SpecialisedAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.SpecialisedAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2060.SpecialisedAssembly.TYPE](), constructor.new(_2060.SpecialisedAssembly))

    def all_parts_of_type_unbalanced_mass(self) -> 'List[_2061.UnbalancedMass]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.UnbalancedMass]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2061.UnbalancedMass.TYPE](), constructor.new(_2061.UnbalancedMass))

    def all_parts_of_type_virtual_component(self) -> 'List[_2062.VirtualComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.VirtualComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2062.VirtualComponent.TYPE](), constructor.new(_2062.VirtualComponent))

    def all_parts_of_type_shaft(self) -> 'List[_2065.Shaft]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.shaft_model.Shaft]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2065.Shaft.TYPE](), constructor.new(_2065.Shaft))

    def all_parts_of_type_agma_gleason_conical_gear(self) -> 'List[_2095.AGMAGleasonConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.AGMAGleasonConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2095.AGMAGleasonConicalGear.TYPE](), constructor.new(_2095.AGMAGleasonConicalGear))

    def all_parts_of_type_agma_gleason_conical_gear_set(self) -> 'List[_2096.AGMAGleasonConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2096.AGMAGleasonConicalGearSet.TYPE](), constructor.new(_2096.AGMAGleasonConicalGearSet))

    def all_parts_of_type_bevel_differential_gear(self) -> 'List[_2097.BevelDifferentialGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2097.BevelDifferentialGear.TYPE](), constructor.new(_2097.BevelDifferentialGear))

    def all_parts_of_type_bevel_differential_gear_set(self) -> 'List[_2098.BevelDifferentialGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2098.BevelDifferentialGearSet.TYPE](), constructor.new(_2098.BevelDifferentialGearSet))

    def all_parts_of_type_bevel_differential_planet_gear(self) -> 'List[_2099.BevelDifferentialPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2099.BevelDifferentialPlanetGear.TYPE](), constructor.new(_2099.BevelDifferentialPlanetGear))

    def all_parts_of_type_bevel_differential_sun_gear(self) -> 'List[_2100.BevelDifferentialSunGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialSunGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2100.BevelDifferentialSunGear.TYPE](), constructor.new(_2100.BevelDifferentialSunGear))

    def all_parts_of_type_bevel_gear(self) -> 'List[_2101.BevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2101.BevelGear.TYPE](), constructor.new(_2101.BevelGear))

    def all_parts_of_type_bevel_gear_set(self) -> 'List[_2102.BevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2102.BevelGearSet.TYPE](), constructor.new(_2102.BevelGearSet))

    def all_parts_of_type_concept_gear(self) -> 'List[_2103.ConceptGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConceptGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2103.ConceptGear.TYPE](), constructor.new(_2103.ConceptGear))

    def all_parts_of_type_concept_gear_set(self) -> 'List[_2104.ConceptGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConceptGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2104.ConceptGearSet.TYPE](), constructor.new(_2104.ConceptGearSet))

    def all_parts_of_type_conical_gear(self) -> 'List[_2105.ConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2105.ConicalGear.TYPE](), constructor.new(_2105.ConicalGear))

    def all_parts_of_type_conical_gear_set(self) -> 'List[_2106.ConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2106.ConicalGearSet.TYPE](), constructor.new(_2106.ConicalGearSet))

    def all_parts_of_type_cylindrical_gear(self) -> 'List[_2107.CylindricalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2107.CylindricalGear.TYPE](), constructor.new(_2107.CylindricalGear))

    def all_parts_of_type_cylindrical_gear_set(self) -> 'List[_2108.CylindricalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2108.CylindricalGearSet.TYPE](), constructor.new(_2108.CylindricalGearSet))

    def all_parts_of_type_cylindrical_planet_gear(self) -> 'List[_2109.CylindricalPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2109.CylindricalPlanetGear.TYPE](), constructor.new(_2109.CylindricalPlanetGear))

    def all_parts_of_type_face_gear(self) -> 'List[_2110.FaceGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.FaceGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2110.FaceGear.TYPE](), constructor.new(_2110.FaceGear))

    def all_parts_of_type_face_gear_set(self) -> 'List[_2111.FaceGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.FaceGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2111.FaceGearSet.TYPE](), constructor.new(_2111.FaceGearSet))

    def all_parts_of_type_gear(self) -> 'List[_2112.Gear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.Gear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2112.Gear.TYPE](), constructor.new(_2112.Gear))

    def all_parts_of_type_gear_set(self) -> 'List[_2114.GearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.GearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2114.GearSet.TYPE](), constructor.new(_2114.GearSet))

    def all_parts_of_type_hypoid_gear(self) -> 'List[_2116.HypoidGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.HypoidGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2116.HypoidGear.TYPE](), constructor.new(_2116.HypoidGear))

    def all_parts_of_type_hypoid_gear_set(self) -> 'List[_2117.HypoidGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.HypoidGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2117.HypoidGearSet.TYPE](), constructor.new(_2117.HypoidGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> 'List[_2118.KlingelnbergCycloPalloidConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2118.KlingelnbergCycloPalloidConicalGear.TYPE](), constructor.new(_2118.KlingelnbergCycloPalloidConicalGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> 'List[_2119.KlingelnbergCycloPalloidConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2119.KlingelnbergCycloPalloidConicalGearSet.TYPE](), constructor.new(_2119.KlingelnbergCycloPalloidConicalGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> 'List[_2120.KlingelnbergCycloPalloidHypoidGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2120.KlingelnbergCycloPalloidHypoidGear.TYPE](), constructor.new(_2120.KlingelnbergCycloPalloidHypoidGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> 'List[_2121.KlingelnbergCycloPalloidHypoidGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2121.KlingelnbergCycloPalloidHypoidGearSet.TYPE](), constructor.new(_2121.KlingelnbergCycloPalloidHypoidGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> 'List[_2122.KlingelnbergCycloPalloidSpiralBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2122.KlingelnbergCycloPalloidSpiralBevelGear.TYPE](), constructor.new(_2122.KlingelnbergCycloPalloidSpiralBevelGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> 'List[_2123.KlingelnbergCycloPalloidSpiralBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2123.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE](), constructor.new(_2123.KlingelnbergCycloPalloidSpiralBevelGearSet))

    def all_parts_of_type_planetary_gear_set(self) -> 'List[_2124.PlanetaryGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.PlanetaryGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2124.PlanetaryGearSet.TYPE](), constructor.new(_2124.PlanetaryGearSet))

    def all_parts_of_type_spiral_bevel_gear(self) -> 'List[_2125.SpiralBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.SpiralBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2125.SpiralBevelGear.TYPE](), constructor.new(_2125.SpiralBevelGear))

    def all_parts_of_type_spiral_bevel_gear_set(self) -> 'List[_2126.SpiralBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.SpiralBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2126.SpiralBevelGearSet.TYPE](), constructor.new(_2126.SpiralBevelGearSet))

    def all_parts_of_type_straight_bevel_diff_gear(self) -> 'List[_2127.StraightBevelDiffGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelDiffGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2127.StraightBevelDiffGear.TYPE](), constructor.new(_2127.StraightBevelDiffGear))

    def all_parts_of_type_straight_bevel_diff_gear_set(self) -> 'List[_2128.StraightBevelDiffGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelDiffGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2128.StraightBevelDiffGearSet.TYPE](), constructor.new(_2128.StraightBevelDiffGearSet))

    def all_parts_of_type_straight_bevel_gear(self) -> 'List[_2129.StraightBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2129.StraightBevelGear.TYPE](), constructor.new(_2129.StraightBevelGear))

    def all_parts_of_type_straight_bevel_gear_set(self) -> 'List[_2130.StraightBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2130.StraightBevelGearSet.TYPE](), constructor.new(_2130.StraightBevelGearSet))

    def all_parts_of_type_straight_bevel_planet_gear(self) -> 'List[_2131.StraightBevelPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2131.StraightBevelPlanetGear.TYPE](), constructor.new(_2131.StraightBevelPlanetGear))

    def all_parts_of_type_straight_bevel_sun_gear(self) -> 'List[_2132.StraightBevelSunGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelSunGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2132.StraightBevelSunGear.TYPE](), constructor.new(_2132.StraightBevelSunGear))

    def all_parts_of_type_worm_gear(self) -> 'List[_2133.WormGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.WormGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2133.WormGear.TYPE](), constructor.new(_2133.WormGear))

    def all_parts_of_type_worm_gear_set(self) -> 'List[_2134.WormGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.WormGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2134.WormGearSet.TYPE](), constructor.new(_2134.WormGearSet))

    def all_parts_of_type_zerol_bevel_gear(self) -> 'List[_2135.ZerolBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ZerolBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2135.ZerolBevelGear.TYPE](), constructor.new(_2135.ZerolBevelGear))

    def all_parts_of_type_zerol_bevel_gear_set(self) -> 'List[_2136.ZerolBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ZerolBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2136.ZerolBevelGearSet.TYPE](), constructor.new(_2136.ZerolBevelGearSet))

    def all_parts_of_type_belt_drive(self) -> 'List[_2154.BeltDrive]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.BeltDrive]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2154.BeltDrive.TYPE](), constructor.new(_2154.BeltDrive))

    def all_parts_of_type_clutch(self) -> 'List[_2156.Clutch]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Clutch]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2156.Clutch.TYPE](), constructor.new(_2156.Clutch))

    def all_parts_of_type_clutch_half(self) -> 'List[_2157.ClutchHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ClutchHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2157.ClutchHalf.TYPE](), constructor.new(_2157.ClutchHalf))

    def all_parts_of_type_concept_coupling(self) -> 'List[_2159.ConceptCoupling]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ConceptCoupling]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2159.ConceptCoupling.TYPE](), constructor.new(_2159.ConceptCoupling))

    def all_parts_of_type_concept_coupling_half(self) -> 'List[_2160.ConceptCouplingHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ConceptCouplingHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2160.ConceptCouplingHalf.TYPE](), constructor.new(_2160.ConceptCouplingHalf))

    def all_parts_of_type_coupling(self) -> 'List[_2161.Coupling]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Coupling]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2161.Coupling.TYPE](), constructor.new(_2161.Coupling))

    def all_parts_of_type_coupling_half(self) -> 'List[_2162.CouplingHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CouplingHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2162.CouplingHalf.TYPE](), constructor.new(_2162.CouplingHalf))

    def all_parts_of_type_cvt(self) -> 'List[_2163.CVT]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CVT]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2163.CVT.TYPE](), constructor.new(_2163.CVT))

    def all_parts_of_type_cvt_pulley(self) -> 'List[_2164.CVTPulley]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CVTPulley]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2164.CVTPulley.TYPE](), constructor.new(_2164.CVTPulley))

    def all_parts_of_type_part_to_part_shear_coupling(self) -> 'List[_2165.PartToPartShearCoupling]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.PartToPartShearCoupling]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2165.PartToPartShearCoupling.TYPE](), constructor.new(_2165.PartToPartShearCoupling))

    def all_parts_of_type_part_to_part_shear_coupling_half(self) -> 'List[_2166.PartToPartShearCouplingHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2166.PartToPartShearCouplingHalf.TYPE](), constructor.new(_2166.PartToPartShearCouplingHalf))

    def all_parts_of_type_pulley(self) -> 'List[_2167.Pulley]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Pulley]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2167.Pulley.TYPE](), constructor.new(_2167.Pulley))

    def all_parts_of_type_rolling_ring(self) -> 'List[_2173.RollingRing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.RollingRing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2173.RollingRing.TYPE](), constructor.new(_2173.RollingRing))

    def all_parts_of_type_rolling_ring_assembly(self) -> 'List[_2174.RollingRingAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.RollingRingAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2174.RollingRingAssembly.TYPE](), constructor.new(_2174.RollingRingAssembly))

    def all_parts_of_type_shaft_hub_connection(self) -> 'List[_2175.ShaftHubConnection]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ShaftHubConnection]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2175.ShaftHubConnection.TYPE](), constructor.new(_2175.ShaftHubConnection))

    def all_parts_of_type_spring_damper(self) -> 'List[_2176.SpringDamper]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SpringDamper]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2176.SpringDamper.TYPE](), constructor.new(_2176.SpringDamper))

    def all_parts_of_type_spring_damper_half(self) -> 'List[_2177.SpringDamperHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SpringDamperHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2177.SpringDamperHalf.TYPE](), constructor.new(_2177.SpringDamperHalf))

    def all_parts_of_type_synchroniser(self) -> 'List[_2178.Synchroniser]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Synchroniser]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2178.Synchroniser.TYPE](), constructor.new(_2178.Synchroniser))

    def all_parts_of_type_synchroniser_half(self) -> 'List[_2180.SynchroniserHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2180.SynchroniserHalf.TYPE](), constructor.new(_2180.SynchroniserHalf))

    def all_parts_of_type_synchroniser_part(self) -> 'List[_2181.SynchroniserPart]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserPart]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2181.SynchroniserPart.TYPE](), constructor.new(_2181.SynchroniserPart))

    def all_parts_of_type_synchroniser_sleeve(self) -> 'List[_2182.SynchroniserSleeve]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserSleeve]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2182.SynchroniserSleeve.TYPE](), constructor.new(_2182.SynchroniserSleeve))

    def all_parts_of_type_torque_converter(self) -> 'List[_2183.TorqueConverter]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverter]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2183.TorqueConverter.TYPE](), constructor.new(_2183.TorqueConverter))

    def all_parts_of_type_torque_converter_pump(self) -> 'List[_2184.TorqueConverterPump]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverterPump]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2184.TorqueConverterPump.TYPE](), constructor.new(_2184.TorqueConverterPump))

    def all_parts_of_type_torque_converter_turbine(self) -> 'List[_2186.TorqueConverterTurbine]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverterTurbine]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2186.TorqueConverterTurbine.TYPE](), constructor.new(_2186.TorqueConverterTurbine))

    @staticmethod
    def load(file_path: 'str', load_full_fe_option: Optional['_1147.ExternalFullFEFileOption'] = _1147.ExternalFullFEFileOption.MESH_AND_EXPANSION_VECTORS) -> 'Design':
        ''' 'Load' is the original name of this method.

        Args:
            file_path (str)
            load_full_fe_option (mastapy.utility.ExternalFullFEFileOption, optional)

        Returns:
            mastapy.system_model.Design
        '''

        file_path = str(file_path)
        file_path = path.abspath(file_path)
        load_full_fe_option = conversion.mp_to_pn_enum(load_full_fe_option)
        method_result = Design.TYPE.Load(file_path if file_path else None, load_full_fe_option)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    @staticmethod
    def load_example(example_string: 'str') -> 'Design':
        ''' 'LoadExample' is the original name of this method.

        Args:
            example_string (str)

        Returns:
            mastapy.system_model.Design
        '''

        example_string = str(example_string)
        method_result = Design.TYPE.LoadExample(example_string if example_string else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def compare_for_test_only(self, design: 'Design', sb: 'str') -> 'bool':
        ''' 'CompareForTestOnly' is the original name of this method.

        Args:
            design (mastapy.system_model.Design)
            sb (str)

        Returns:
            bool
        '''

        sb = str(sb)
        method_result = self.wrapped.CompareForTestOnly(design.wrapped if design else None, sb if sb else None)
        return method_result

    def new_belt_creation_options(self, centre_distance: Optional['float'] = 0.1, pulley_a_diameter: Optional['float'] = 0.08, pulley_b_diameter: Optional['float'] = 0.08, name: Optional['str'] = 'Belt Drive') -> '_2150.BeltCreationOptions':
        ''' 'NewBeltCreationOptions' is the original name of this method.

        Args:
            centre_distance (float, optional)
            pulley_a_diameter (float, optional)
            pulley_b_diameter (float, optional)
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.creation_options.BeltCreationOptions
        '''

        centre_distance = float(centre_distance)
        pulley_a_diameter = float(pulley_a_diameter)
        pulley_b_diameter = float(pulley_b_diameter)
        name = str(name)
        method_result = self.wrapped.NewBeltCreationOptions(centre_distance if centre_distance else 0.0, pulley_a_diameter if pulley_a_diameter else 0.0, pulley_b_diameter if pulley_b_diameter else 0.0, name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def new_planet_carrier_creation_options(self, number_of_planets: Optional['int'] = 3, diameter: Optional['float'] = 0.05) -> '_2152.PlanetCarrierCreationOptions':
        ''' 'NewPlanetCarrierCreationOptions' is the original name of this method.

        Args:
            number_of_planets (int, optional)
            diameter (float, optional)

        Returns:
            mastapy.system_model.part_model.creation_options.PlanetCarrierCreationOptions
        '''

        number_of_planets = int(number_of_planets)
        diameter = float(diameter)
        method_result = self.wrapped.NewPlanetCarrierCreationOptions(number_of_planets if number_of_planets else 0, diameter if diameter else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def new_shaft_creation_options(self, length: Optional['float'] = 0.1, outer_diameter: Optional['float'] = 0.025, bore: Optional['float'] = 0.0, name: Optional['str'] = 'Shaft') -> '_2153.ShaftCreationOptions':
        ''' 'NewShaftCreationOptions' is the original name of this method.

        Args:
            length (float, optional)
            outer_diameter (float, optional)
            bore (float, optional)
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.creation_options.ShaftCreationOptions
        '''

        length = float(length)
        outer_diameter = float(outer_diameter)
        bore = float(bore)
        name = str(name)
        method_result = self.wrapped.NewShaftCreationOptions(length if length else 0.0, outer_diameter if outer_diameter else 0.0, bore if bore else 0.0, name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def new_cylindrical_gear_pair_creation_options(self) -> '_883.CylindricalGearPairCreationOptions':
        ''' 'NewCylindricalGearPairCreationOptions' is the original name of this method.

        Returns:
            mastapy.gears.gear_designs.creation_options.CylindricalGearPairCreationOptions
        '''

        method_result = self.wrapped.NewCylindricalGearPairCreationOptions()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def new_cylindrical_gear_linear_train_creation_options(self, number_of_gears: Optional['int'] = 3, name: Optional['str'] = 'Gear Train') -> '_2151.CylindricalGearLinearTrainCreationOptions':
        ''' 'NewCylindricalGearLinearTrainCreationOptions' is the original name of this method.

        Args:
            number_of_gears (int, optional)
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.creation_options.CylindricalGearLinearTrainCreationOptions
        '''

        number_of_gears = int(number_of_gears)
        name = str(name)
        method_result = self.wrapped.NewCylindricalGearLinearTrainCreationOptions(number_of_gears if number_of_gears else 0, name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def new_spiral_bevel_gear_set_creation_options(self) -> '_886.SpiralBevelGearSetCreationOptions':
        ''' 'NewSpiralBevelGearSetCreationOptions' is the original name of this method.

        Returns:
            mastapy.gears.gear_designs.creation_options.SpiralBevelGearSetCreationOptions
        '''

        method_result = self.wrapped.NewSpiralBevelGearSetCreationOptions()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def new_hypoid_gear_set_creation_options(self) -> '_885.HypoidGearSetCreationOptions':
        ''' 'NewHypoidGearSetCreationOptions' is the original name of this method.

        Returns:
            mastapy.gears.gear_designs.creation_options.HypoidGearSetCreationOptions
        '''

        method_result = self.wrapped.NewHypoidGearSetCreationOptions()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def new_nodal_matrix(self, dense_matrix: 'List[List[float]]') -> '_1402.NodalMatrix':
        ''' 'NewNodalMatrix' is the original name of this method.

        Args:
            dense_matrix (List[List[float]])

        Returns:
            mastapy.nodal_analysis.NodalMatrix
        '''

        dense_matrix = conversion.mp_to_pn_list_float_2d(dense_matrix)
        method_result = self.wrapped.NewNodalMatrix(dense_matrix)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.dispose()
