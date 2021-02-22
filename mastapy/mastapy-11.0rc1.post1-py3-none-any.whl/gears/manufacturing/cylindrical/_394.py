'''_394.py

CylindricalGearManufacturingConfig
'''


from typing import Callable

from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.gears.manufacturing.cylindrical import _406, _405, _393
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy._internal.python_net import python_net_import
from mastapy.gears.manufacturing.cylindrical.cutters import (
    _513, _507, _508, _509,
    _510, _512, _514, _515,
    _518
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical import _799, _775, _796
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import (
    _493, _490, _498, _487,
    _496
)
from mastapy.gears.manufacturing.cylindrical.process_simulation import _421, _422, _423
from mastapy.gears.analysis import _954

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_CYLINDRICAL_GEAR_MANUFACTURING_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalGearManufacturingConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearManufacturingConfig',)


class CylindricalGearManufacturingConfig(_954.GearImplementationDetail):
    '''CylindricalGearManufacturingConfig

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MANUFACTURING_CONFIG

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def roughing_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_CylindricalMftRoughingMethods':
        '''enum_with_selected_value.EnumWithSelectedValue_CylindricalMftRoughingMethods: 'RoughingMethod' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_CylindricalMftRoughingMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.RoughingMethod, value) if self.wrapped.RoughingMethod else None

    @roughing_method.setter
    def roughing_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_CylindricalMftRoughingMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CylindricalMftRoughingMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.RoughingMethod = value

    @property
    def finishing_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_CylindricalMftFinishingMethods':
        '''enum_with_selected_value.EnumWithSelectedValue_CylindricalMftFinishingMethods: 'FinishingMethod' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_CylindricalMftFinishingMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.FinishingMethod, value) if self.wrapped.FinishingMethod else None

    @finishing_method.setter
    def finishing_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_CylindricalMftFinishingMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CylindricalMftFinishingMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.FinishingMethod = value

    @property
    def rough_cutter_database_selector(self) -> 'str':
        '''str: 'RoughCutterDatabaseSelector' is the original name of this property.'''

        return self.wrapped.RoughCutterDatabaseSelector.SelectedItemName

    @rough_cutter_database_selector.setter
    def rough_cutter_database_selector(self, value: 'str'):
        self.wrapped.RoughCutterDatabaseSelector.SetSelectedItem(str(value) if value else None)

    @property
    def finish_cutter_database_selector(self) -> 'str':
        '''str: 'FinishCutterDatabaseSelector' is the original name of this property.'''

        return self.wrapped.FinishCutterDatabaseSelector.SelectedItemName

    @finish_cutter_database_selector.setter
    def finish_cutter_database_selector(self, value: 'str'):
        self.wrapped.FinishCutterDatabaseSelector.SetSelectedItem(str(value) if value else None)

    @property
    def create_new_rough_cutter_compatible_with_gear_in_design_mode(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CreateNewRoughCutterCompatibleWithGearInDesignMode' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateNewRoughCutterCompatibleWithGearInDesignMode

    @property
    def create_new_finish_cutter_compatible_with_gear_in_design_mode(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CreateNewFinishCutterCompatibleWithGearInDesignMode' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateNewFinishCutterCompatibleWithGearInDesignMode

    @property
    def minimum_finish_cutter_gear_root_clearance_factor(self) -> 'float':
        '''float: 'MinimumFinishCutterGearRootClearanceFactor' is the original name of this property.'''

        return self.wrapped.MinimumFinishCutterGearRootClearanceFactor

    @minimum_finish_cutter_gear_root_clearance_factor.setter
    def minimum_finish_cutter_gear_root_clearance_factor(self, value: 'float'):
        self.wrapped.MinimumFinishCutterGearRootClearanceFactor = float(value) if value else 0.0

    @property
    def number_of_points_for_reporting_main_profile_finish_stock(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfPointsForReportingMainProfileFinishStock' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfPointsForReportingMainProfileFinishStock) if self.wrapped.NumberOfPointsForReportingMainProfileFinishStock else None

    @number_of_points_for_reporting_main_profile_finish_stock.setter
    def number_of_points_for_reporting_main_profile_finish_stock(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0, is_overridden)
        self.wrapped.NumberOfPointsForReportingMainProfileFinishStock = value

    @property
    def rough_cutter(self) -> '_513.CylindricalGearRealCutterDesign':
        '''CylindricalGearRealCutterDesign: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _513.CylindricalGearRealCutterDesign.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearRealCutterDesign. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughCutter.__class__)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_cylindrical_gear_form_grinding_wheel(self) -> '_507.CylindricalGearFormGrindingWheel':
        '''CylindricalGearFormGrindingWheel: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _507.CylindricalGearFormGrindingWheel.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearFormGrindingWheel. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughCutter.__class__)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_cylindrical_gear_grinding_worm(self) -> '_508.CylindricalGearGrindingWorm':
        '''CylindricalGearGrindingWorm: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _508.CylindricalGearGrindingWorm.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearGrindingWorm. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughCutter.__class__)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_cylindrical_gear_hob_design(self) -> '_509.CylindricalGearHobDesign':
        '''CylindricalGearHobDesign: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _509.CylindricalGearHobDesign.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearHobDesign. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughCutter.__class__)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_cylindrical_gear_plunge_shaver(self) -> '_510.CylindricalGearPlungeShaver':
        '''CylindricalGearPlungeShaver: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _510.CylindricalGearPlungeShaver.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearPlungeShaver. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughCutter.__class__)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_cylindrical_gear_rack_design(self) -> '_512.CylindricalGearRackDesign':
        '''CylindricalGearRackDesign: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _512.CylindricalGearRackDesign.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearRackDesign. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughCutter.__class__)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_cylindrical_gear_shaper(self) -> '_514.CylindricalGearShaper':
        '''CylindricalGearShaper: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _514.CylindricalGearShaper.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearShaper. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughCutter.__class__)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_cylindrical_gear_shaver(self) -> '_515.CylindricalGearShaver':
        '''CylindricalGearShaver: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _515.CylindricalGearShaver.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearShaver. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughCutter.__class__)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_involute_cutter_design(self) -> '_518.InvoluteCutterDesign':
        '''InvoluteCutterDesign: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _518.InvoluteCutterDesign.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to InvoluteCutterDesign. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughCutter.__class__)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def finish_cutter(self) -> '_513.CylindricalGearRealCutterDesign':
        '''CylindricalGearRealCutterDesign: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _513.CylindricalGearRealCutterDesign.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearRealCutterDesign. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishCutter.__class__)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_cylindrical_gear_form_grinding_wheel(self) -> '_507.CylindricalGearFormGrindingWheel':
        '''CylindricalGearFormGrindingWheel: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _507.CylindricalGearFormGrindingWheel.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearFormGrindingWheel. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishCutter.__class__)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_cylindrical_gear_grinding_worm(self) -> '_508.CylindricalGearGrindingWorm':
        '''CylindricalGearGrindingWorm: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _508.CylindricalGearGrindingWorm.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearGrindingWorm. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishCutter.__class__)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_cylindrical_gear_hob_design(self) -> '_509.CylindricalGearHobDesign':
        '''CylindricalGearHobDesign: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _509.CylindricalGearHobDesign.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearHobDesign. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishCutter.__class__)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_cylindrical_gear_plunge_shaver(self) -> '_510.CylindricalGearPlungeShaver':
        '''CylindricalGearPlungeShaver: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _510.CylindricalGearPlungeShaver.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearPlungeShaver. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishCutter.__class__)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_cylindrical_gear_rack_design(self) -> '_512.CylindricalGearRackDesign':
        '''CylindricalGearRackDesign: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _512.CylindricalGearRackDesign.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearRackDesign. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishCutter.__class__)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_cylindrical_gear_shaper(self) -> '_514.CylindricalGearShaper':
        '''CylindricalGearShaper: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _514.CylindricalGearShaper.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearShaper. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishCutter.__class__)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_cylindrical_gear_shaver(self) -> '_515.CylindricalGearShaver':
        '''CylindricalGearShaver: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _515.CylindricalGearShaver.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearShaver. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishCutter.__class__)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_involute_cutter_design(self) -> '_518.InvoluteCutterDesign':
        '''InvoluteCutterDesign: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _518.InvoluteCutterDesign.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to InvoluteCutterDesign. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishCutter.__class__)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_stock_specification(self) -> '_799.FinishStockSpecification':
        '''FinishStockSpecification: 'FinishStockSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_799.FinishStockSpecification)(self.wrapped.FinishStockSpecification) if self.wrapped.FinishStockSpecification else None

    @property
    def rough_cutter_simulation(self) -> '_493.GearCutterSimulation':
        '''GearCutterSimulation: 'RoughCutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _493.GearCutterSimulation.TYPE not in self.wrapped.RoughCutterSimulation.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter_simulation to GearCutterSimulation. Expected: {}.'.format(self.wrapped.RoughCutterSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughCutterSimulation.__class__)(self.wrapped.RoughCutterSimulation) if self.wrapped.RoughCutterSimulation else None

    @property
    def rough_cutter_simulation_of_type_finish_cutter_simulation(self) -> '_490.FinishCutterSimulation':
        '''FinishCutterSimulation: 'RoughCutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _490.FinishCutterSimulation.TYPE not in self.wrapped.RoughCutterSimulation.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter_simulation to FinishCutterSimulation. Expected: {}.'.format(self.wrapped.RoughCutterSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughCutterSimulation.__class__)(self.wrapped.RoughCutterSimulation) if self.wrapped.RoughCutterSimulation else None

    @property
    def rough_cutter_simulation_of_type_rough_cutter_simulation(self) -> '_498.RoughCutterSimulation':
        '''RoughCutterSimulation: 'RoughCutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _498.RoughCutterSimulation.TYPE not in self.wrapped.RoughCutterSimulation.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter_simulation to RoughCutterSimulation. Expected: {}.'.format(self.wrapped.RoughCutterSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughCutterSimulation.__class__)(self.wrapped.RoughCutterSimulation) if self.wrapped.RoughCutterSimulation else None

    @property
    def rough_process_simulation(self) -> '_421.CutterProcessSimulation':
        '''CutterProcessSimulation: 'RoughProcessSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _421.CutterProcessSimulation.TYPE not in self.wrapped.RoughProcessSimulation.__class__.__mro__:
            raise CastException('Failed to cast rough_process_simulation to CutterProcessSimulation. Expected: {}.'.format(self.wrapped.RoughProcessSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughProcessSimulation.__class__)(self.wrapped.RoughProcessSimulation) if self.wrapped.RoughProcessSimulation else None

    @property
    def rough_process_simulation_of_type_form_wheel_grinding_process_simulation(self) -> '_422.FormWheelGrindingProcessSimulation':
        '''FormWheelGrindingProcessSimulation: 'RoughProcessSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _422.FormWheelGrindingProcessSimulation.TYPE not in self.wrapped.RoughProcessSimulation.__class__.__mro__:
            raise CastException('Failed to cast rough_process_simulation to FormWheelGrindingProcessSimulation. Expected: {}.'.format(self.wrapped.RoughProcessSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughProcessSimulation.__class__)(self.wrapped.RoughProcessSimulation) if self.wrapped.RoughProcessSimulation else None

    @property
    def rough_process_simulation_of_type_shaping_process_simulation(self) -> '_423.ShapingProcessSimulation':
        '''ShapingProcessSimulation: 'RoughProcessSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _423.ShapingProcessSimulation.TYPE not in self.wrapped.RoughProcessSimulation.__class__.__mro__:
            raise CastException('Failed to cast rough_process_simulation to ShapingProcessSimulation. Expected: {}.'.format(self.wrapped.RoughProcessSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RoughProcessSimulation.__class__)(self.wrapped.RoughProcessSimulation) if self.wrapped.RoughProcessSimulation else None

    @property
    def finish_cutter_simulation(self) -> '_493.GearCutterSimulation':
        '''GearCutterSimulation: 'FinishCutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _493.GearCutterSimulation.TYPE not in self.wrapped.FinishCutterSimulation.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter_simulation to GearCutterSimulation. Expected: {}.'.format(self.wrapped.FinishCutterSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishCutterSimulation.__class__)(self.wrapped.FinishCutterSimulation) if self.wrapped.FinishCutterSimulation else None

    @property
    def finish_cutter_simulation_of_type_finish_cutter_simulation(self) -> '_490.FinishCutterSimulation':
        '''FinishCutterSimulation: 'FinishCutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _490.FinishCutterSimulation.TYPE not in self.wrapped.FinishCutterSimulation.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter_simulation to FinishCutterSimulation. Expected: {}.'.format(self.wrapped.FinishCutterSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishCutterSimulation.__class__)(self.wrapped.FinishCutterSimulation) if self.wrapped.FinishCutterSimulation else None

    @property
    def finish_cutter_simulation_of_type_rough_cutter_simulation(self) -> '_498.RoughCutterSimulation':
        '''RoughCutterSimulation: 'FinishCutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _498.RoughCutterSimulation.TYPE not in self.wrapped.FinishCutterSimulation.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter_simulation to RoughCutterSimulation. Expected: {}.'.format(self.wrapped.FinishCutterSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishCutterSimulation.__class__)(self.wrapped.FinishCutterSimulation) if self.wrapped.FinishCutterSimulation else None

    @property
    def finish_process_simulation(self) -> '_421.CutterProcessSimulation':
        '''CutterProcessSimulation: 'FinishProcessSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _421.CutterProcessSimulation.TYPE not in self.wrapped.FinishProcessSimulation.__class__.__mro__:
            raise CastException('Failed to cast finish_process_simulation to CutterProcessSimulation. Expected: {}.'.format(self.wrapped.FinishProcessSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishProcessSimulation.__class__)(self.wrapped.FinishProcessSimulation) if self.wrapped.FinishProcessSimulation else None

    @property
    def finish_process_simulation_of_type_form_wheel_grinding_process_simulation(self) -> '_422.FormWheelGrindingProcessSimulation':
        '''FormWheelGrindingProcessSimulation: 'FinishProcessSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _422.FormWheelGrindingProcessSimulation.TYPE not in self.wrapped.FinishProcessSimulation.__class__.__mro__:
            raise CastException('Failed to cast finish_process_simulation to FormWheelGrindingProcessSimulation. Expected: {}.'.format(self.wrapped.FinishProcessSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishProcessSimulation.__class__)(self.wrapped.FinishProcessSimulation) if self.wrapped.FinishProcessSimulation else None

    @property
    def finish_process_simulation_of_type_shaping_process_simulation(self) -> '_423.ShapingProcessSimulation':
        '''ShapingProcessSimulation: 'FinishProcessSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _423.ShapingProcessSimulation.TYPE not in self.wrapped.FinishProcessSimulation.__class__.__mro__:
            raise CastException('Failed to cast finish_process_simulation to ShapingProcessSimulation. Expected: {}.'.format(self.wrapped.FinishProcessSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FinishProcessSimulation.__class__)(self.wrapped.FinishProcessSimulation) if self.wrapped.FinishProcessSimulation else None

    @property
    def design(self) -> '_775.CylindricalGearDesign':
        '''CylindricalGearDesign: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _775.CylindricalGearDesign.TYPE not in self.wrapped.Design.__class__.__mro__:
            raise CastException('Failed to cast design to CylindricalGearDesign. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Design.__class__)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def rough_gear_specification(self) -> '_487.CylindricalGearSpecification':
        '''CylindricalGearSpecification: 'RoughGearSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_487.CylindricalGearSpecification)(self.wrapped.RoughGearSpecification) if self.wrapped.RoughGearSpecification else None

    @property
    def finished_gear_specification(self) -> '_487.CylindricalGearSpecification':
        '''CylindricalGearSpecification: 'FinishedGearSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_487.CylindricalGearSpecification)(self.wrapped.FinishedGearSpecification) if self.wrapped.FinishedGearSpecification else None

    @property
    def gear_blank(self) -> '_393.CylindricalGearBlank':
        '''CylindricalGearBlank: 'GearBlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_393.CylindricalGearBlank)(self.wrapped.GearBlank) if self.wrapped.GearBlank else None

    @property
    def rough_manufacturing_process_controls(self) -> '_496.ManufacturingProcessControls':
        '''ManufacturingProcessControls: 'RoughManufacturingProcessControls' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_496.ManufacturingProcessControls)(self.wrapped.RoughManufacturingProcessControls) if self.wrapped.RoughManufacturingProcessControls else None

    @property
    def finish_manufacturing_process_controls(self) -> '_496.ManufacturingProcessControls':
        '''ManufacturingProcessControls: 'FinishManufacturingProcessControls' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_496.ManufacturingProcessControls)(self.wrapped.FinishManufacturingProcessControls) if self.wrapped.FinishManufacturingProcessControls else None
