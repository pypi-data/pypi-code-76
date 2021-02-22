'''_550.py

ShavingDynamicsCalculationForHobbedGears
'''


from typing import List, Generic, TypeVar

from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _783
from mastapy._internal.python_net import python_net_import
from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _546, _532, _539, _543,
    _548, _547
)
from mastapy._internal.cast_exception import CastException

_REPORTING_OVERRIDABLE = python_net_import('SMT.MastaAPI.Utility.Property', 'ReportingOverridable')
_SHAVING_DYNAMICS_CALCULATION_FOR_HOBBED_GEARS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ShavingDynamicsCalculationForHobbedGears')


__docformat__ = 'restructuredtext en'
__all__ = ('ShavingDynamicsCalculationForHobbedGears',)


T = TypeVar('T', bound='_547.ShavingDynamics')


class ShavingDynamicsCalculationForHobbedGears(_548.ShavingDynamicsCalculation['T'], Generic[T]):
    '''ShavingDynamicsCalculationForHobbedGears

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _SHAVING_DYNAMICS_CALCULATION_FOR_HOBBED_GEARS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShavingDynamicsCalculationForHobbedGears.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def selected_redressing(self) -> 'list_with_selected_item.ListWithSelectedItem_T':
        '''list_with_selected_item.ListWithSelectedItem_T: 'SelectedRedressing' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_T)(self.wrapped.SelectedRedressing) if self.wrapped.SelectedRedressing else None

    @selected_redressing.setter
    def selected_redressing(self, value: 'list_with_selected_item.ListWithSelectedItem_T.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_T.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_T.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.SelectedRedressing = value

    @property
    def minimum_start_of_shaving_profile(self) -> '_783.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'MinimumStartOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_783.CylindricalGearProfileMeasurement)(self.wrapped.MinimumStartOfShavingProfile.Value) if self.wrapped.MinimumStartOfShavingProfile.Value else None

    @property
    def minimum_end_of_shaving_profile(self) -> '_783.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'MinimumEndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_783.CylindricalGearProfileMeasurement)(self.wrapped.MinimumEndOfShavingProfile.Value) if self.wrapped.MinimumEndOfShavingProfile.Value else None

    @property
    def maximum_start_of_shaving_profile(self) -> '_783.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'MaximumStartOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_783.CylindricalGearProfileMeasurement)(self.wrapped.MaximumStartOfShavingProfile.Value) if self.wrapped.MaximumStartOfShavingProfile.Value else None

    @property
    def maximum_end_of_shaving_profile(self) -> '_783.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'MaximumEndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_783.CylindricalGearProfileMeasurement)(self.wrapped.MaximumEndOfShavingProfile.Value) if self.wrapped.MaximumEndOfShavingProfile.Value else None

    @property
    def redressing_at_minimum_start_and_end_of_shaving_profile(self) -> '_546.ShaverRedressing[T]':
        '''ShaverRedressing[T]: 'RedressingAtMinimumStartAndEndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _546.ShaverRedressing[T].TYPE not in self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile.__class__.__mro__:
            raise CastException('Failed to cast redressing_at_minimum_start_and_end_of_shaving_profile to ShaverRedressing[T]. Expected: {}.'.format(self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile.__class__)(self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile) if self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile else None

    @property
    def redressing_at_minimum_start_and_end_of_shaving_profile_of_type_axial_shaver_redressing(self) -> '_532.AxialShaverRedressing':
        '''AxialShaverRedressing: 'RedressingAtMinimumStartAndEndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _532.AxialShaverRedressing.TYPE not in self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile.__class__.__mro__:
            raise CastException('Failed to cast redressing_at_minimum_start_and_end_of_shaving_profile to AxialShaverRedressing. Expected: {}.'.format(self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile.__class__)(self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile) if self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile else None

    @property
    def redressing_at_minimum_start_and_end_of_shaving_profile_of_type_plunge_shaver_redressing(self) -> '_539.PlungeShaverRedressing':
        '''PlungeShaverRedressing: 'RedressingAtMinimumStartAndEndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _539.PlungeShaverRedressing.TYPE not in self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile.__class__.__mro__:
            raise CastException('Failed to cast redressing_at_minimum_start_and_end_of_shaving_profile to PlungeShaverRedressing. Expected: {}.'.format(self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile.__class__)(self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile) if self.wrapped.RedressingAtMinimumStartAndEndOfShavingProfile else None

    @property
    def redressing_at_minimum_start_and_maximum_end_of_shaving_profile(self) -> '_546.ShaverRedressing[T]':
        '''ShaverRedressing[T]: 'RedressingAtMinimumStartAndMaximumEndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _546.ShaverRedressing[T].TYPE not in self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile.__class__.__mro__:
            raise CastException('Failed to cast redressing_at_minimum_start_and_maximum_end_of_shaving_profile to ShaverRedressing[T]. Expected: {}.'.format(self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile.__class__)(self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile) if self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile else None

    @property
    def redressing_at_minimum_start_and_maximum_end_of_shaving_profile_of_type_axial_shaver_redressing(self) -> '_532.AxialShaverRedressing':
        '''AxialShaverRedressing: 'RedressingAtMinimumStartAndMaximumEndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _532.AxialShaverRedressing.TYPE not in self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile.__class__.__mro__:
            raise CastException('Failed to cast redressing_at_minimum_start_and_maximum_end_of_shaving_profile to AxialShaverRedressing. Expected: {}.'.format(self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile.__class__)(self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile) if self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile else None

    @property
    def redressing_at_minimum_start_and_maximum_end_of_shaving_profile_of_type_plunge_shaver_redressing(self) -> '_539.PlungeShaverRedressing':
        '''PlungeShaverRedressing: 'RedressingAtMinimumStartAndMaximumEndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _539.PlungeShaverRedressing.TYPE not in self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile.__class__.__mro__:
            raise CastException('Failed to cast redressing_at_minimum_start_and_maximum_end_of_shaving_profile to PlungeShaverRedressing. Expected: {}.'.format(self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile.__class__)(self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile) if self.wrapped.RedressingAtMinimumStartAndMaximumEndOfShavingProfile else None

    @property
    def redressing_at_maximum_start_and_end_of_shaving_profile(self) -> '_546.ShaverRedressing[T]':
        '''ShaverRedressing[T]: 'RedressingAtMaximumStartAndEndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _546.ShaverRedressing[T].TYPE not in self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile.__class__.__mro__:
            raise CastException('Failed to cast redressing_at_maximum_start_and_end_of_shaving_profile to ShaverRedressing[T]. Expected: {}.'.format(self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile.__class__)(self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile) if self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile else None

    @property
    def redressing_at_maximum_start_and_end_of_shaving_profile_of_type_axial_shaver_redressing(self) -> '_532.AxialShaverRedressing':
        '''AxialShaverRedressing: 'RedressingAtMaximumStartAndEndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _532.AxialShaverRedressing.TYPE not in self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile.__class__.__mro__:
            raise CastException('Failed to cast redressing_at_maximum_start_and_end_of_shaving_profile to AxialShaverRedressing. Expected: {}.'.format(self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile.__class__)(self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile) if self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile else None

    @property
    def redressing_at_maximum_start_and_end_of_shaving_profile_of_type_plunge_shaver_redressing(self) -> '_539.PlungeShaverRedressing':
        '''PlungeShaverRedressing: 'RedressingAtMaximumStartAndEndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _539.PlungeShaverRedressing.TYPE not in self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile.__class__.__mro__:
            raise CastException('Failed to cast redressing_at_maximum_start_and_end_of_shaving_profile to PlungeShaverRedressing. Expected: {}.'.format(self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile.__class__)(self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile) if self.wrapped.RedressingAtMaximumStartAndEndOfShavingProfile else None

    @property
    def redressing_at_maximum_start_and_minimum_end_of_shaving_profile(self) -> '_546.ShaverRedressing[T]':
        '''ShaverRedressing[T]: 'RedressingAtMaximumStartAndMinimumEndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _546.ShaverRedressing[T].TYPE not in self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile.__class__.__mro__:
            raise CastException('Failed to cast redressing_at_maximum_start_and_minimum_end_of_shaving_profile to ShaverRedressing[T]. Expected: {}.'.format(self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile.__class__)(self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile) if self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile else None

    @property
    def redressing_at_maximum_start_and_minimum_end_of_shaving_profile_of_type_axial_shaver_redressing(self) -> '_532.AxialShaverRedressing':
        '''AxialShaverRedressing: 'RedressingAtMaximumStartAndMinimumEndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _532.AxialShaverRedressing.TYPE not in self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile.__class__.__mro__:
            raise CastException('Failed to cast redressing_at_maximum_start_and_minimum_end_of_shaving_profile to AxialShaverRedressing. Expected: {}.'.format(self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile.__class__)(self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile) if self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile else None

    @property
    def redressing_at_maximum_start_and_minimum_end_of_shaving_profile_of_type_plunge_shaver_redressing(self) -> '_539.PlungeShaverRedressing':
        '''PlungeShaverRedressing: 'RedressingAtMaximumStartAndMinimumEndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _539.PlungeShaverRedressing.TYPE not in self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile.__class__.__mro__:
            raise CastException('Failed to cast redressing_at_maximum_start_and_minimum_end_of_shaving_profile to PlungeShaverRedressing. Expected: {}.'.format(self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile.__class__)(self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile) if self.wrapped.RedressingAtMaximumStartAndMinimumEndOfShavingProfile else None

    @property
    def redressing_settings(self) -> 'List[_543.RedressingSettings[T]]':
        '''List[RedressingSettings[T]]: 'RedressingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RedressingSettings, constructor.new(_543.RedressingSettings)[T])
        return value
