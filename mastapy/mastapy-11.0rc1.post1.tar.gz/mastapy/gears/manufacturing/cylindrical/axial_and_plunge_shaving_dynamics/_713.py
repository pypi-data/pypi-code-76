'''_713.py

ShavingDynamicsCalculationForDesignedGears
'''


from typing import List, Generic, TypeVar

from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _952
from mastapy._internal.python_net import python_net_import
from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _710, _696, _703, _707,
    _712, _711
)
from mastapy._internal.cast_exception import CastException

_REPORTING_OVERRIDABLE = python_net_import('SMT.MastaAPI.Utility.Property', 'ReportingOverridable')
_SHAVING_DYNAMICS_CALCULATION_FOR_DESIGNED_GEARS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ShavingDynamicsCalculationForDesignedGears')


__docformat__ = 'restructuredtext en'
__all__ = ('ShavingDynamicsCalculationForDesignedGears',)


T = TypeVar('T', bound='_711.ShavingDynamics')


class ShavingDynamicsCalculationForDesignedGears(_712.ShavingDynamicsCalculation['T'], Generic[T]):
    '''ShavingDynamicsCalculationForDesignedGears

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _SHAVING_DYNAMICS_CALCULATION_FOR_DESIGNED_GEARS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShavingDynamicsCalculationForDesignedGears.TYPE'):
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
    def start_of_shaving_profile(self) -> '_952.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'StartOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_952.CylindricalGearProfileMeasurement)(self.wrapped.StartOfShavingProfile.Value) if self.wrapped.StartOfShavingProfile.Value else None

    @property
    def end_of_shaving_profile(self) -> '_952.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'EndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_952.CylindricalGearProfileMeasurement)(self.wrapped.EndOfShavingProfile.Value) if self.wrapped.EndOfShavingProfile.Value else None

    @property
    def redressing(self) -> '_710.ShaverRedressing[T]':
        '''ShaverRedressing[T]: 'Redressing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _710.ShaverRedressing[T].TYPE not in self.wrapped.Redressing.__class__.__mro__:
            raise CastException('Failed to cast redressing to ShaverRedressing[T]. Expected: {}.'.format(self.wrapped.Redressing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Redressing.__class__)(self.wrapped.Redressing) if self.wrapped.Redressing else None

    @property
    def redressing_of_type_axial_shaver_redressing(self) -> '_696.AxialShaverRedressing':
        '''AxialShaverRedressing: 'Redressing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _696.AxialShaverRedressing.TYPE not in self.wrapped.Redressing.__class__.__mro__:
            raise CastException('Failed to cast redressing to AxialShaverRedressing. Expected: {}.'.format(self.wrapped.Redressing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Redressing.__class__)(self.wrapped.Redressing) if self.wrapped.Redressing else None

    @property
    def redressing_of_type_plunge_shaver_redressing(self) -> '_703.PlungeShaverRedressing':
        '''PlungeShaverRedressing: 'Redressing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _703.PlungeShaverRedressing.TYPE not in self.wrapped.Redressing.__class__.__mro__:
            raise CastException('Failed to cast redressing to PlungeShaverRedressing. Expected: {}.'.format(self.wrapped.Redressing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Redressing.__class__)(self.wrapped.Redressing) if self.wrapped.Redressing else None

    @property
    def redressing_settings(self) -> 'List[_707.RedressingSettings[T]]':
        '''List[RedressingSettings[T]]: 'RedressingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RedressingSettings, constructor.new(_707.RedressingSettings)[T])
        return value
