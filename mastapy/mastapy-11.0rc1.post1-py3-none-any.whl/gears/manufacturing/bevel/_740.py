'''_740.py

ConicalWheelManufacturingConfig
'''


from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import
from mastapy.gears.manufacturing.bevel.cutters import _762, _761
from mastapy.gears.manufacturing.bevel.basic_machine_settings import (
    _770, _767, _768, _769
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel import _722

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_CONICAL_WHEEL_MANUFACTURING_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalWheelManufacturingConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalWheelManufacturingConfig',)


class ConicalWheelManufacturingConfig(_722.ConicalGearManufacturingConfig):
    '''ConicalWheelManufacturingConfig

    This is a mastapy class.
    '''

    TYPE = _CONICAL_WHEEL_MANUFACTURING_CONFIG

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalWheelManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def use_cutter_tilt(self) -> 'bool':
        '''bool: 'UseCutterTilt' is the original name of this property.'''

        return self.wrapped.UseCutterTilt

    @use_cutter_tilt.setter
    def use_cutter_tilt(self, value: 'bool'):
        self.wrapped.UseCutterTilt = bool(value) if value else False

    @property
    def wheel_finish_manufacturing_machine(self) -> 'str':
        '''str: 'WheelFinishManufacturingMachine' is the original name of this property.'''

        return self.wrapped.WheelFinishManufacturingMachine.SelectedItemName

    @wheel_finish_manufacturing_machine.setter
    def wheel_finish_manufacturing_machine(self, value: 'str'):
        self.wrapped.WheelFinishManufacturingMachine.SetSelectedItem(str(value) if value else None)

    @property
    def wheel_rough_manufacturing_machine(self) -> 'str':
        '''str: 'WheelRoughManufacturingMachine' is the original name of this property.'''

        return self.wrapped.WheelRoughManufacturingMachine.SelectedItemName

    @wheel_rough_manufacturing_machine.setter
    def wheel_rough_manufacturing_machine(self, value: 'str'):
        self.wrapped.WheelRoughManufacturingMachine.SetSelectedItem(str(value) if value else None)

    @property
    def wheel_rough_cutter(self) -> '_762.WheelRoughCutter':
        '''WheelRoughCutter: 'WheelRoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_762.WheelRoughCutter)(self.wrapped.WheelRoughCutter) if self.wrapped.WheelRoughCutter else None

    @property
    def wheel_finish_cutter(self) -> '_761.WheelFinishCutter':
        '''WheelFinishCutter: 'WheelFinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_761.WheelFinishCutter)(self.wrapped.WheelFinishCutter) if self.wrapped.WheelFinishCutter else None

    @property
    def specified_cradle_style_machine_settings(self) -> '_770.CradleStyleConicalMachineSettingsGenerated':
        '''CradleStyleConicalMachineSettingsGenerated: 'SpecifiedCradleStyleMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_770.CradleStyleConicalMachineSettingsGenerated)(self.wrapped.SpecifiedCradleStyleMachineSettings) if self.wrapped.SpecifiedCradleStyleMachineSettings else None

    @property
    def specified_machine_settings(self) -> '_767.BasicConicalGearMachineSettings':
        '''BasicConicalGearMachineSettings: 'SpecifiedMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _767.BasicConicalGearMachineSettings.TYPE not in self.wrapped.SpecifiedMachineSettings.__class__.__mro__:
            raise CastException('Failed to cast specified_machine_settings to BasicConicalGearMachineSettings. Expected: {}.'.format(self.wrapped.SpecifiedMachineSettings.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SpecifiedMachineSettings.__class__)(self.wrapped.SpecifiedMachineSettings) if self.wrapped.SpecifiedMachineSettings else None

    @property
    def specified_machine_settings_of_type_basic_conical_gear_machine_settings_formate(self) -> '_768.BasicConicalGearMachineSettingsFormate':
        '''BasicConicalGearMachineSettingsFormate: 'SpecifiedMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _768.BasicConicalGearMachineSettingsFormate.TYPE not in self.wrapped.SpecifiedMachineSettings.__class__.__mro__:
            raise CastException('Failed to cast specified_machine_settings to BasicConicalGearMachineSettingsFormate. Expected: {}.'.format(self.wrapped.SpecifiedMachineSettings.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SpecifiedMachineSettings.__class__)(self.wrapped.SpecifiedMachineSettings) if self.wrapped.SpecifiedMachineSettings else None

    @property
    def specified_machine_settings_of_type_basic_conical_gear_machine_settings_generated(self) -> '_769.BasicConicalGearMachineSettingsGenerated':
        '''BasicConicalGearMachineSettingsGenerated: 'SpecifiedMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _769.BasicConicalGearMachineSettingsGenerated.TYPE not in self.wrapped.SpecifiedMachineSettings.__class__.__mro__:
            raise CastException('Failed to cast specified_machine_settings to BasicConicalGearMachineSettingsGenerated. Expected: {}.'.format(self.wrapped.SpecifiedMachineSettings.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SpecifiedMachineSettings.__class__)(self.wrapped.SpecifiedMachineSettings) if self.wrapped.SpecifiedMachineSettings else None
