'''_6305.py

AdvancedSystemDeflectionOptions
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.ltca import _621
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.part_model.gears import _2130
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ADVANCED_SYSTEM_DEFLECTION_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'AdvancedSystemDeflectionOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('AdvancedSystemDeflectionOptions',)


class AdvancedSystemDeflectionOptions(_0.APIBase):
    '''AdvancedSystemDeflectionOptions

    This is a mastapy class.
    '''

    TYPE = _ADVANCED_SYSTEM_DEFLECTION_OPTIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AdvancedSystemDeflectionOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def seed_analysis(self) -> 'bool':
        '''bool: 'SeedAnalysis' is the original name of this property.'''

        return self.wrapped.SeedAnalysis

    @seed_analysis.setter
    def seed_analysis(self, value: 'bool'):
        self.wrapped.SeedAnalysis = bool(value) if value else False

    @property
    def include_pitch_error(self) -> 'bool':
        '''bool: 'IncludePitchError' is the original name of this property.'''

        return self.wrapped.IncludePitchError

    @include_pitch_error.setter
    def include_pitch_error(self, value: 'bool'):
        self.wrapped.IncludePitchError = bool(value) if value else False

    @property
    def use_advanced_ltca(self) -> '_621.UseAdvancedLTCAOptions':
        '''UseAdvancedLTCAOptions: 'UseAdvancedLTCA' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.UseAdvancedLTCA)
        return constructor.new(_621.UseAdvancedLTCAOptions)(value) if value else None

    @use_advanced_ltca.setter
    def use_advanced_ltca(self, value: '_621.UseAdvancedLTCAOptions'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.UseAdvancedLTCA = value

    @property
    def run_for_single_gear_set(self) -> 'bool':
        '''bool: 'RunForSingleGearSet' is the original name of this property.'''

        return self.wrapped.RunForSingleGearSet

    @run_for_single_gear_set.setter
    def run_for_single_gear_set(self, value: 'bool'):
        self.wrapped.RunForSingleGearSet = bool(value) if value else False

    @property
    def specified_gear_set(self) -> 'list_with_selected_item.ListWithSelectedItem_GearSet':
        '''list_with_selected_item.ListWithSelectedItem_GearSet: 'SpecifiedGearSet' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_GearSet)(self.wrapped.SpecifiedGearSet) if self.wrapped.SpecifiedGearSet else None

    @specified_gear_set.setter
    def specified_gear_set(self, value: 'list_with_selected_item.ListWithSelectedItem_GearSet.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_GearSet.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_GearSet.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.SpecifiedGearSet = value

    @property
    def end_time(self) -> 'float':
        '''float: 'EndTime' is the original name of this property.'''

        return self.wrapped.EndTime

    @end_time.setter
    def end_time(self, value: 'float'):
        self.wrapped.EndTime = float(value) if value else 0.0

    @property
    def start_time(self) -> 'float':
        '''float: 'StartTime' is the original name of this property.'''

        return self.wrapped.StartTime

    @start_time.setter
    def start_time(self, value: 'float'):
        self.wrapped.StartTime = float(value) if value else 0.0

    @property
    def total_time(self) -> 'float':
        '''float: 'TotalTime' is the original name of this property.'''

        return self.wrapped.TotalTime

    @total_time.setter
    def total_time(self, value: 'float'):
        self.wrapped.TotalTime = float(value) if value else 0.0

    @property
    def total_number_of_time_steps(self) -> 'int':
        '''int: 'TotalNumberOfTimeSteps' is the original name of this property.'''

        return self.wrapped.TotalNumberOfTimeSteps

    @total_number_of_time_steps.setter
    def total_number_of_time_steps(self, value: 'int'):
        self.wrapped.TotalNumberOfTimeSteps = int(value) if value else 0

    @property
    def use_data_logger(self) -> 'bool':
        '''bool: 'UseDataLogger' is the original name of this property.'''

        return self.wrapped.UseDataLogger

    @use_data_logger.setter
    def use_data_logger(self, value: 'bool'):
        self.wrapped.UseDataLogger = bool(value) if value else False
