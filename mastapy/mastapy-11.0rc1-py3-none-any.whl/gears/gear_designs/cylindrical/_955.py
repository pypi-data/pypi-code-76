'''_955.py

CylindricalGearSetDesign
'''


from typing import List, Optional

from mastapy.gears.gear_designs.cylindrical import (
    _927, _972, _995, _989,
    _1012, _956, _986, _941,
    _948, _957
)
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import list_with_selected_item, overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears import _279
from mastapy.materials.efficiency import _257
from mastapy.gears.rating.cylindrical.iso6336 import _464
from mastapy._internal.python_net import python_net_import
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1027
from mastapy.gears.manufacturing.cylindrical import _571
from mastapy.gears.rating.cylindrical import _421
from mastapy.gears.gear_designs import _879

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_CYLINDRICAL_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetDesign',)


class CylindricalGearSetDesign(_879.GearSetDesign):
    '''CylindricalGearSetDesign

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def profile_shift_distribution_rule(self) -> '_927.AddendumModificationDistributionRule':
        '''AddendumModificationDistributionRule: 'ProfileShiftDistributionRule' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ProfileShiftDistributionRule)
        return constructor.new(_927.AddendumModificationDistributionRule)(value) if value else None

    @profile_shift_distribution_rule.setter
    def profile_shift_distribution_rule(self, value: '_927.AddendumModificationDistributionRule'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ProfileShiftDistributionRule = value

    @property
    def gear_tooth_thickness_reduction_allowance(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'GearToothThicknessReductionAllowance' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.GearToothThicknessReductionAllowance) if self.wrapped.GearToothThicknessReductionAllowance else None

    @gear_tooth_thickness_reduction_allowance.setter
    def gear_tooth_thickness_reduction_allowance(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.GearToothThicknessReductionAllowance = value

    @property
    def gear_tooth_thickness_tolerance(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'GearToothThicknessTolerance' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.GearToothThicknessTolerance) if self.wrapped.GearToothThicknessTolerance else None

    @gear_tooth_thickness_tolerance.setter
    def gear_tooth_thickness_tolerance(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.GearToothThicknessTolerance = value

    @property
    def coefficient_of_friction_calculation_method(self) -> 'overridable.Overridable_CoefficientOfFrictionCalculationMethod':
        '''overridable.Overridable_CoefficientOfFrictionCalculationMethod: 'CoefficientOfFrictionCalculationMethod' is the original name of this property.'''

        value = overridable.Overridable_CoefficientOfFrictionCalculationMethod.implicit_type()
        return enum_with_selected_value_runtime.create(self.wrapped.CoefficientOfFrictionCalculationMethod, value) if self.wrapped.CoefficientOfFrictionCalculationMethod else None

    @coefficient_of_friction_calculation_method.setter
    def coefficient_of_friction_calculation_method(self, value: 'overridable.Overridable_CoefficientOfFrictionCalculationMethod.implicit_type()'):
        wrapper_type = overridable.Overridable_CoefficientOfFrictionCalculationMethod.wrapper_type()
        enclosed_type = overridable.Overridable_CoefficientOfFrictionCalculationMethod.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value else None, is_overridden)
        self.wrapped.CoefficientOfFrictionCalculationMethod = value

    @property
    def efficiency_rating_method(self) -> '_257.EfficiencyRatingMethod':
        '''EfficiencyRatingMethod: 'EfficiencyRatingMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.EfficiencyRatingMethod)
        return constructor.new(_257.EfficiencyRatingMethod)(value) if value else None

    @efficiency_rating_method.setter
    def efficiency_rating_method(self, value: '_257.EfficiencyRatingMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.EfficiencyRatingMethod = value

    @property
    def helical_gear_micro_geometry_option(self) -> '_464.HelicalGearMicroGeometryOption':
        '''HelicalGearMicroGeometryOption: 'HelicalGearMicroGeometryOption' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HelicalGearMicroGeometryOption)
        return constructor.new(_464.HelicalGearMicroGeometryOption)(value) if value else None

    @helical_gear_micro_geometry_option.setter
    def helical_gear_micro_geometry_option(self, value: '_464.HelicalGearMicroGeometryOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HelicalGearMicroGeometryOption = value

    @property
    def gear_fit_system(self) -> '_972.GearFitSystems':
        '''GearFitSystems: 'GearFitSystem' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.GearFitSystem)
        return constructor.new(_972.GearFitSystems)(value) if value else None

    @gear_fit_system.setter
    def gear_fit_system(self, value: '_972.GearFitSystems'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GearFitSystem = value

    @property
    def helix_angle(self) -> 'float':
        '''float: 'HelixAngle' is the original name of this property.'''

        return self.wrapped.HelixAngle

    @helix_angle.setter
    def helix_angle(self, value: 'float'):
        self.wrapped.HelixAngle = float(value) if value else 0.0

    @property
    def normal_module_maintain_transverse_profile(self) -> 'float':
        '''float: 'NormalModuleMaintainTransverseProfile' is the original name of this property.'''

        return self.wrapped.NormalModuleMaintainTransverseProfile

    @normal_module_maintain_transverse_profile.setter
    def normal_module_maintain_transverse_profile(self, value: 'float'):
        self.wrapped.NormalModuleMaintainTransverseProfile = float(value) if value else 0.0

    @property
    def helix_angle_maintain_transverse_profile(self) -> 'float':
        '''float: 'HelixAngleMaintainTransverseProfile' is the original name of this property.'''

        return self.wrapped.HelixAngleMaintainTransverseProfile

    @helix_angle_maintain_transverse_profile.setter
    def helix_angle_maintain_transverse_profile(self, value: 'float'):
        self.wrapped.HelixAngleMaintainTransverseProfile = float(value) if value else 0.0

    @property
    def root_gear_profile_shift_coefficient_maintain_tip_and_root_diameters(self) -> 'float':
        '''float: 'RootGearProfileShiftCoefficientMaintainTipAndRootDiameters' is the original name of this property.'''

        return self.wrapped.RootGearProfileShiftCoefficientMaintainTipAndRootDiameters

    @root_gear_profile_shift_coefficient_maintain_tip_and_root_diameters.setter
    def root_gear_profile_shift_coefficient_maintain_tip_and_root_diameters(self, value: 'float'):
        self.wrapped.RootGearProfileShiftCoefficientMaintainTipAndRootDiameters = float(value) if value else 0.0

    @property
    def normal_pressure_angle_maintain_transverse_profile(self) -> 'float':
        '''float: 'NormalPressureAngleMaintainTransverseProfile' is the original name of this property.'''

        return self.wrapped.NormalPressureAngleMaintainTransverseProfile

    @normal_pressure_angle_maintain_transverse_profile.setter
    def normal_pressure_angle_maintain_transverse_profile(self, value: 'float'):
        self.wrapped.NormalPressureAngleMaintainTransverseProfile = float(value) if value else 0.0

    @property
    def helix_angle_calculating_gear_teeth_numbers(self) -> 'float':
        '''float: 'HelixAngleCalculatingGearTeethNumbers' is the original name of this property.'''

        return self.wrapped.HelixAngleCalculatingGearTeethNumbers

    @helix_angle_calculating_gear_teeth_numbers.setter
    def helix_angle_calculating_gear_teeth_numbers(self, value: 'float'):
        self.wrapped.HelixAngleCalculatingGearTeethNumbers = float(value) if value else 0.0

    @property
    def helix_angle_with_centre_distance_adjustment(self) -> 'float':
        '''float: 'HelixAngleWithCentreDistanceAdjustment' is the original name of this property.'''

        return self.wrapped.HelixAngleWithCentreDistanceAdjustment

    @helix_angle_with_centre_distance_adjustment.setter
    def helix_angle_with_centre_distance_adjustment(self, value: 'float'):
        self.wrapped.HelixAngleWithCentreDistanceAdjustment = float(value) if value else 0.0

    @property
    def normal_module(self) -> 'float':
        '''float: 'NormalModule' is the original name of this property.'''

        return self.wrapped.NormalModule

    @normal_module.setter
    def normal_module(self, value: 'float'):
        self.wrapped.NormalModule = float(value) if value else 0.0

    @property
    def normal_module_calculating_gear_teeth_numbers(self) -> 'float':
        '''float: 'NormalModuleCalculatingGearTeethNumbers' is the original name of this property.'''

        return self.wrapped.NormalModuleCalculatingGearTeethNumbers

    @normal_module_calculating_gear_teeth_numbers.setter
    def normal_module_calculating_gear_teeth_numbers(self, value: 'float'):
        self.wrapped.NormalModuleCalculatingGearTeethNumbers = float(value) if value else 0.0

    @property
    def normal_module_with_centre_distance_adjustment(self) -> 'float':
        '''float: 'NormalModuleWithCentreDistanceAdjustment' is the original name of this property.'''

        return self.wrapped.NormalModuleWithCentreDistanceAdjustment

    @normal_module_with_centre_distance_adjustment.setter
    def normal_module_with_centre_distance_adjustment(self, value: 'float'):
        self.wrapped.NormalModuleWithCentreDistanceAdjustment = float(value) if value else 0.0

    @property
    def diametral_pitch_per_inch(self) -> 'float':
        '''float: 'DiametralPitchPerInch' is the original name of this property.'''

        return self.wrapped.DiametralPitchPerInch

    @diametral_pitch_per_inch.setter
    def diametral_pitch_per_inch(self, value: 'float'):
        self.wrapped.DiametralPitchPerInch = float(value) if value else 0.0

    @property
    def transverse_pitch(self) -> 'float':
        '''float: 'TransversePitch' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransversePitch

    @property
    def axial_pitch(self) -> 'float':
        '''float: 'AxialPitch' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialPitch

    @property
    def transverse_module(self) -> 'float':
        '''float: 'TransverseModule' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseModule

    @property
    def is_asymmetric(self) -> 'bool':
        '''bool: 'IsAsymmetric' is the original name of this property.'''

        return self.wrapped.IsAsymmetric

    @is_asymmetric.setter
    def is_asymmetric(self, value: 'bool'):
        self.wrapped.IsAsymmetric = bool(value) if value else False

    @property
    def normal_pitch(self) -> 'float':
        '''float: 'NormalPitch' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalPitch

    @property
    def all_gears_number_of_teeth(self) -> 'List[int]':
        '''List[int]: 'AllGearsNumberOfTeeth' is the original name of this property.'''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllGearsNumberOfTeeth, int)
        return value

    @all_gears_number_of_teeth.setter
    def all_gears_number_of_teeth(self, value: 'List[int]'):
        value = value if value else None
        value = conversion.mp_to_pn_objects_in_list(value)
        self.wrapped.AllGearsNumberOfTeeth = value

    @property
    def parameter_for_calculating_tooth_temperature(self) -> 'float':
        '''float: 'ParameterForCalculatingToothTemperature' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ParameterForCalculatingToothTemperature

    @property
    def fe_model_for_tiff(self) -> 'str':
        '''str: 'FEModelForTIFF' is the original name of this property.'''

        return self.wrapped.FEModelForTIFF.SelectedItemName

    @fe_model_for_tiff.setter
    def fe_model_for_tiff(self, value: 'str'):
        self.wrapped.FEModelForTIFF.SetSelectedItem(str(value) if value else None)

    @property
    def minimum_axial_contact_ratio(self) -> 'float':
        '''float: 'MinimumAxialContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumAxialContactRatio

    @property
    def minimum_tip_thickness(self) -> 'float':
        '''float: 'MinimumTipThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumTipThickness

    @property
    def cylindrical_gear_set_micro_geometry(self) -> '_1027.CylindricalGearSetMicroGeometry':
        '''CylindricalGearSetMicroGeometry: 'CylindricalGearSetMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1027.CylindricalGearSetMicroGeometry)(self.wrapped.CylindricalGearSetMicroGeometry) if self.wrapped.CylindricalGearSetMicroGeometry else None

    @property
    def scuffing(self) -> '_995.Scuffing':
        '''Scuffing: 'Scuffing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_995.Scuffing)(self.wrapped.Scuffing) if self.wrapped.Scuffing else None

    @property
    def micropitting(self) -> '_989.Micropitting':
        '''Micropitting: 'Micropitting' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_989.Micropitting)(self.wrapped.Micropitting) if self.wrapped.Micropitting else None

    @property
    def usage(self) -> '_1012.Usage':
        '''Usage: 'Usage' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1012.Usage)(self.wrapped.Usage) if self.wrapped.Usage else None

    @property
    def left_flank(self) -> '_956.CylindricalGearSetFlankDesign':
        '''CylindricalGearSetFlankDesign: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_956.CylindricalGearSetFlankDesign)(self.wrapped.LeftFlank) if self.wrapped.LeftFlank else None

    @property
    def right_flank(self) -> '_956.CylindricalGearSetFlankDesign':
        '''CylindricalGearSetFlankDesign: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_956.CylindricalGearSetFlankDesign)(self.wrapped.RightFlank) if self.wrapped.RightFlank else None

    @property
    def ltca_settings(self) -> '_986.LtcaSettings':
        '''LtcaSettings: 'LTCASettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_986.LtcaSettings)(self.wrapped.LTCASettings) if self.wrapped.LTCASettings else None

    @property
    def cylindrical_gear_set_manufacturing_configuration(self) -> '_571.CylindricalSetManufacturingConfig':
        '''CylindricalSetManufacturingConfig: 'CylindricalGearSetManufacturingConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_571.CylindricalSetManufacturingConfig)(self.wrapped.CylindricalGearSetManufacturingConfiguration) if self.wrapped.CylindricalGearSetManufacturingConfiguration else None

    @property
    def gears(self) -> 'List[_941.CylindricalGearDesign]':
        '''List[CylindricalGearDesign]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_941.CylindricalGearDesign))
        return value

    @property
    def cylindrical_gears(self) -> 'List[_941.CylindricalGearDesign]':
        '''List[CylindricalGearDesign]: 'CylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGears, constructor.new(_941.CylindricalGearDesign))
        return value

    @property
    def cylindrical_meshes(self) -> 'List[_948.CylindricalGearMeshDesign]':
        '''List[CylindricalGearMeshDesign]: 'CylindricalMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshes, constructor.new(_948.CylindricalGearMeshDesign))
        return value

    @property
    def flanks(self) -> 'List[_956.CylindricalGearSetFlankDesign]':
        '''List[CylindricalGearSetFlankDesign]: 'Flanks' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Flanks, constructor.new(_956.CylindricalGearSetFlankDesign))
        return value

    @property
    def micro_geometries(self) -> 'List[_1027.CylindricalGearSetMicroGeometry]':
        '''List[CylindricalGearSetMicroGeometry]: 'MicroGeometries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MicroGeometries, constructor.new(_1027.CylindricalGearSetMicroGeometry))
        return value

    @property
    def both_flanks(self) -> '_956.CylindricalGearSetFlankDesign':
        '''CylindricalGearSetFlankDesign: 'BothFlanks' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_956.CylindricalGearSetFlankDesign)(self.wrapped.BothFlanks) if self.wrapped.BothFlanks else None

    @property
    def manufacturing_configurations(self) -> 'List[_571.CylindricalSetManufacturingConfig]':
        '''List[CylindricalSetManufacturingConfig]: 'ManufacturingConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ManufacturingConfigurations, constructor.new(_571.CylindricalSetManufacturingConfig))
        return value

    def centre_distance_editor(self):
        ''' 'CentreDistanceEditor' is the original name of this method.'''

        self.wrapped.CentreDistanceEditor()

    def set_helix_angle_for_axial_contact_ratio(self):
        ''' 'SetHelixAngleForAxialContactRatio' is the original name of this method.'''

        self.wrapped.SetHelixAngleForAxialContactRatio()

    def create_optimiser(self, duty_cycle: '_421.CylindricalGearSetDutyCycleRating') -> '_957.CylindricalGearSetMacroGeometryOptimiser':
        ''' 'CreateOptimiser' is the original name of this method.

        Args:
            duty_cycle (mastapy.gears.rating.cylindrical.CylindricalGearSetDutyCycleRating)

        Returns:
            mastapy.gears.gear_designs.cylindrical.CylindricalGearSetMacroGeometryOptimiser
        '''

        method_result = self.wrapped.CreateOptimiser(duty_cycle.wrapped if duty_cycle else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def set_active_manufacturing_configuration(self, value: '_571.CylindricalSetManufacturingConfig'):
        ''' 'SetActiveManufacturingConfiguration' is the original name of this method.

        Args:
            value (mastapy.gears.manufacturing.cylindrical.CylindricalSetManufacturingConfig)
        '''

        self.wrapped.SetActiveManufacturingConfiguration(value.wrapped if value else None)

    def add_new_manufacturing_configuration(self, new_config_name: Optional['str'] = 'None') -> '_571.CylindricalSetManufacturingConfig':
        ''' 'AddNewManufacturingConfiguration' is the original name of this method.

        Args:
            new_config_name (str, optional)

        Returns:
            mastapy.gears.manufacturing.cylindrical.CylindricalSetManufacturingConfig
        '''

        new_config_name = str(new_config_name)
        method_result = self.wrapped.AddNewManufacturingConfiguration(new_config_name if new_config_name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def clear_all_tooth_thickness_specifications(self):
        ''' 'ClearAllToothThicknessSpecifications' is the original name of this method.'''

        self.wrapped.ClearAllToothThicknessSpecifications()

    def delete_unused_manufacturing_configurations(self):
        ''' 'DeleteUnusedManufacturingConfigurations' is the original name of this method.'''

        self.wrapped.DeleteUnusedManufacturingConfigurations()

    def delete_manufacturing_configuration(self, config: '_571.CylindricalSetManufacturingConfig'):
        ''' 'DeleteManufacturingConfiguration' is the original name of this method.

        Args:
            config (mastapy.gears.manufacturing.cylindrical.CylindricalSetManufacturingConfig)
        '''

        self.wrapped.DeleteManufacturingConfiguration(config.wrapped if config else None)

    def try_make_valid(self):
        ''' 'TryMakeValid' is the original name of this method.'''

        self.wrapped.TryMakeValid()

    def add_new_micro_geometry(self) -> '_1027.CylindricalGearSetMicroGeometry':
        ''' 'AddNewMicroGeometry' is the original name of this method.

        Returns:
            mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry
        '''

        method_result = self.wrapped.AddNewMicroGeometry()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def delete_micro_geometry(self, micro_geometry: '_1027.CylindricalGearSetMicroGeometry'):
        ''' 'DeleteMicroGeometry' is the original name of this method.

        Args:
            micro_geometry (mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry)
        '''

        self.wrapped.DeleteMicroGeometry(micro_geometry.wrapped if micro_geometry else None)

    def set_active_micro_geometry(self, value: '_1027.CylindricalGearSetMicroGeometry'):
        ''' 'SetActiveMicroGeometry' is the original name of this method.

        Args:
            value (mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry)
        '''

        self.wrapped.SetActiveMicroGeometry(value.wrapped if value else None)

    def micro_geometry_named(self, micro_geometry_name: 'str') -> '_1027.CylindricalGearSetMicroGeometry':
        ''' 'MicroGeometryNamed' is the original name of this method.

        Args:
            micro_geometry_name (str)

        Returns:
            mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry
        '''

        micro_geometry_name = str(micro_geometry_name)
        method_result = self.wrapped.MicroGeometryNamed(micro_geometry_name if micro_geometry_name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
