'''_6518.py

FlexiblePinAssemblyLoadCase
'''


from mastapy.utility import _1346
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.system_model.part_model import _2127
from mastapy.system_model.analyses_and_results.static_loads import _6581
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'FlexiblePinAssemblyLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyLoadCase',)


class FlexiblePinAssemblyLoadCase(_6581.SpecialisedAssemblyLoadCase):
    '''FlexiblePinAssemblyLoadCase

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def include_inner_race_distortion_for_flexible_pin_spindle(self) -> '_1346.LoadCaseOverrideOption':
        '''LoadCaseOverrideOption: 'IncludeInnerRaceDistortionForFlexiblePinSpindle' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle)
        return constructor.new(_1346.LoadCaseOverrideOption)(value) if value else None

    @include_inner_race_distortion_for_flexible_pin_spindle.setter
    def include_inner_race_distortion_for_flexible_pin_spindle(self, value: '_1346.LoadCaseOverrideOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle = value

    @property
    def assembly_design(self) -> '_2127.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2127.FlexiblePinAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
