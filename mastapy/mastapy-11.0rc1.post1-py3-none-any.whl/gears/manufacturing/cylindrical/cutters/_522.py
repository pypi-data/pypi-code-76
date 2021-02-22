'''_522.py

RoughCutterCreationSettings
'''


from mastapy.gears.gear_designs.cylindrical import _833
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _495
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ROUGH_CUTTER_CREATION_SETTINGS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'RoughCutterCreationSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('RoughCutterCreationSettings',)


class RoughCutterCreationSettings(_0.APIBase):
    '''RoughCutterCreationSettings

    This is a mastapy class.
    '''

    TYPE = _ROUGH_CUTTER_CREATION_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RoughCutterCreationSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rough_thickness_used_to_generate_cutter(self) -> '_833.TolerancedMetalMeasurements':
        '''TolerancedMetalMeasurements: 'RoughThicknessUsedToGenerateCutter' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.RoughThicknessUsedToGenerateCutter)
        return constructor.new(_833.TolerancedMetalMeasurements)(value) if value else None

    @rough_thickness_used_to_generate_cutter.setter
    def rough_thickness_used_to_generate_cutter(self, value: '_833.TolerancedMetalMeasurements'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RoughThicknessUsedToGenerateCutter = value

    @property
    def finish_thickness_used_to_generate_cutter(self) -> '_833.TolerancedMetalMeasurements':
        '''TolerancedMetalMeasurements: 'FinishThicknessUsedToGenerateCutter' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.FinishThicknessUsedToGenerateCutter)
        return constructor.new(_833.TolerancedMetalMeasurements)(value) if value else None

    @finish_thickness_used_to_generate_cutter.setter
    def finish_thickness_used_to_generate_cutter(self, value: '_833.TolerancedMetalMeasurements'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FinishThicknessUsedToGenerateCutter = value

    @property
    def rough_tool_clearances(self) -> '_495.ManufacturingOperationConstraints':
        '''ManufacturingOperationConstraints: 'RoughToolClearances' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_495.ManufacturingOperationConstraints)(self.wrapped.RoughToolClearances) if self.wrapped.RoughToolClearances else None

    @property
    def finish_tool_clearances(self) -> '_495.ManufacturingOperationConstraints':
        '''ManufacturingOperationConstraints: 'FinishToolClearances' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_495.ManufacturingOperationConstraints)(self.wrapped.FinishToolClearances) if self.wrapped.FinishToolClearances else None
