'''_555.py

ShavingDynamicsViewModel
'''


from typing import (
    Callable, List, Generic, TypeVar
)

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.gears.gear_designs.cylindrical import _831, _785
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _534, _551, _537, _538,
    _543, _544, _546, _556,
    _550
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SHAVING_DYNAMICS_VIEW_MODEL = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ShavingDynamicsViewModel')


__docformat__ = 'restructuredtext en'
__all__ = ('ShavingDynamicsViewModel',)


T = TypeVar('T', bound='_550.ShavingDynamics')


class ShavingDynamicsViewModel(_556.ShavingDynamicsViewModelBase, Generic[T]):
    '''ShavingDynamicsViewModel

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _SHAVING_DYNAMICS_VIEW_MODEL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShavingDynamicsViewModel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def calculate(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'Calculate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Calculate

    @property
    def selected_measurement_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ThicknessType':
        '''enum_with_selected_value.EnumWithSelectedValue_ThicknessType: 'SelectedMeasurementMethod' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_ThicknessType.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.SelectedMeasurementMethod, value) if self.wrapped.SelectedMeasurementMethod else None

    @selected_measurement_method.setter
    def selected_measurement_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ThicknessType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ThicknessType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.SelectedMeasurementMethod = value

    @property
    def shaver_tip_diameter_adjustment(self) -> 'float':
        '''float: 'ShaverTipDiameterAdjustment' is the original name of this property.'''

        return self.wrapped.ShaverTipDiameterAdjustment

    @shaver_tip_diameter_adjustment.setter
    def shaver_tip_diameter_adjustment(self, value: 'float'):
        self.wrapped.ShaverTipDiameterAdjustment = float(value) if value else 0.0

    @property
    def chart_display_method(self) -> '_785.CylindricalGearProfileMeasurementType':
        '''CylindricalGearProfileMeasurementType: 'ChartDisplayMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ChartDisplayMethod)
        return constructor.new(_785.CylindricalGearProfileMeasurementType)(value) if value else None

    @chart_display_method.setter
    def chart_display_method(self, value: '_785.CylindricalGearProfileMeasurementType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ChartDisplayMethod = value

    @property
    def active_profile_range_calculation_source(self) -> '_534.ActiveProfileRangeCalculationSource':
        '''ActiveProfileRangeCalculationSource: 'ActiveProfileRangeCalculationSource' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ActiveProfileRangeCalculationSource)
        return constructor.new(_534.ActiveProfileRangeCalculationSource)(value) if value else None

    @active_profile_range_calculation_source.setter
    def active_profile_range_calculation_source(self, value: '_534.ActiveProfileRangeCalculationSource'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ActiveProfileRangeCalculationSource = value

    @property
    def use_shaver_from_database(self) -> 'bool':
        '''bool: 'UseShaverFromDatabase' is the original name of this property.'''

        return self.wrapped.UseShaverFromDatabase

    @use_shaver_from_database.setter
    def use_shaver_from_database(self, value: 'bool'):
        self.wrapped.UseShaverFromDatabase = bool(value) if value else False

    @property
    def add_shaver_to_database(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddShaverToDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddShaverToDatabase

    @property
    def calculation(self) -> '_551.ShavingDynamicsCalculation[T]':
        '''ShavingDynamicsCalculation[T]: 'Calculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _551.ShavingDynamicsCalculation[T].TYPE not in self.wrapped.Calculation.__class__.__mro__:
            raise CastException('Failed to cast calculation to ShavingDynamicsCalculation[T]. Expected: {}.'.format(self.wrapped.Calculation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Calculation.__class__)(self.wrapped.Calculation) if self.wrapped.Calculation else None

    @property
    def calculation_of_type_conventional_shaving_dynamics_calculation_for_designed_gears(self) -> '_537.ConventionalShavingDynamicsCalculationForDesignedGears':
        '''ConventionalShavingDynamicsCalculationForDesignedGears: 'Calculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _537.ConventionalShavingDynamicsCalculationForDesignedGears.TYPE not in self.wrapped.Calculation.__class__.__mro__:
            raise CastException('Failed to cast calculation to ConventionalShavingDynamicsCalculationForDesignedGears. Expected: {}.'.format(self.wrapped.Calculation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Calculation.__class__)(self.wrapped.Calculation) if self.wrapped.Calculation else None

    @property
    def calculation_of_type_conventional_shaving_dynamics_calculation_for_hobbed_gears(self) -> '_538.ConventionalShavingDynamicsCalculationForHobbedGears':
        '''ConventionalShavingDynamicsCalculationForHobbedGears: 'Calculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _538.ConventionalShavingDynamicsCalculationForHobbedGears.TYPE not in self.wrapped.Calculation.__class__.__mro__:
            raise CastException('Failed to cast calculation to ConventionalShavingDynamicsCalculationForHobbedGears. Expected: {}.'.format(self.wrapped.Calculation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Calculation.__class__)(self.wrapped.Calculation) if self.wrapped.Calculation else None

    @property
    def calculation_of_type_plunge_shaving_dynamics_calculation_for_designed_gears(self) -> '_543.PlungeShavingDynamicsCalculationForDesignedGears':
        '''PlungeShavingDynamicsCalculationForDesignedGears: 'Calculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _543.PlungeShavingDynamicsCalculationForDesignedGears.TYPE not in self.wrapped.Calculation.__class__.__mro__:
            raise CastException('Failed to cast calculation to PlungeShavingDynamicsCalculationForDesignedGears. Expected: {}.'.format(self.wrapped.Calculation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Calculation.__class__)(self.wrapped.Calculation) if self.wrapped.Calculation else None

    @property
    def calculation_of_type_plunge_shaving_dynamics_calculation_for_hobbed_gears(self) -> '_544.PlungeShavingDynamicsCalculationForHobbedGears':
        '''PlungeShavingDynamicsCalculationForHobbedGears: 'Calculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _544.PlungeShavingDynamicsCalculationForHobbedGears.TYPE not in self.wrapped.Calculation.__class__.__mro__:
            raise CastException('Failed to cast calculation to PlungeShavingDynamicsCalculationForHobbedGears. Expected: {}.'.format(self.wrapped.Calculation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Calculation.__class__)(self.wrapped.Calculation) if self.wrapped.Calculation else None

    @property
    def redressing_settings(self) -> 'List[_546.RedressingSettings[T]]':
        '''List[RedressingSettings[T]]: 'RedressingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RedressingSettings, constructor.new(_546.RedressingSettings)[T])
        return value
