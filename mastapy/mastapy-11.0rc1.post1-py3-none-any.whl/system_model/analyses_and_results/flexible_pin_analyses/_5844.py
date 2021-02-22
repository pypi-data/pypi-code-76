'''_5844.py

WindTurbineCertificationReport
'''


from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.analyses_and_results.static_loads import _6234
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.load_case_groups import _5284
from mastapy.system_model.part_model import _2058
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2487
from mastapy.system_model.analyses_and_results.system_deflections import _2349
from mastapy.system_model.analyses_and_results.flexible_pin_analyses import _5836
from mastapy._internal.python_net import python_net_import

_WIND_TURBINE_CERTIFICATION_REPORT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses', 'WindTurbineCertificationReport')


__docformat__ = 'restructuredtext en'
__all__ = ('WindTurbineCertificationReport',)


class WindTurbineCertificationReport(_5836.CombinationAnalysis):
    '''WindTurbineCertificationReport

    This is a mastapy class.
    '''

    TYPE = _WIND_TURBINE_CERTIFICATION_REPORT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WindTurbineCertificationReport.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def extreme_load_case(self) -> 'list_with_selected_item.ListWithSelectedItem_StaticLoadCase':
        '''list_with_selected_item.ListWithSelectedItem_StaticLoadCase: 'ExtremeLoadCase' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_StaticLoadCase)(self.wrapped.ExtremeLoadCase) if self.wrapped.ExtremeLoadCase else None

    @extreme_load_case.setter
    def extreme_load_case(self, value: 'list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_StaticLoadCase.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ExtremeLoadCase = value

    @property
    def ldd(self) -> 'list_with_selected_item.ListWithSelectedItem_DutyCycle':
        '''list_with_selected_item.ListWithSelectedItem_DutyCycle: 'LDD' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_DutyCycle)(self.wrapped.LDD) if self.wrapped.LDD else None

    @ldd.setter
    def ldd(self, value: 'list_with_selected_item.ListWithSelectedItem_DutyCycle.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_DutyCycle.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_DutyCycle.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.LDD = value

    @property
    def nominal_load_case(self) -> 'list_with_selected_item.ListWithSelectedItem_StaticLoadCase':
        '''list_with_selected_item.ListWithSelectedItem_StaticLoadCase: 'NominalLoadCase' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_StaticLoadCase)(self.wrapped.NominalLoadCase) if self.wrapped.NominalLoadCase else None

    @nominal_load_case.setter
    def nominal_load_case(self, value: 'list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_StaticLoadCase.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.NominalLoadCase = value

    @property
    def design(self) -> '_2058.RootAssembly':
        '''RootAssembly: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2058.RootAssembly)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def ldd_static_analysis(self) -> '_2487.RootAssemblyCompoundSystemDeflection':
        '''RootAssemblyCompoundSystemDeflection: 'LDDStaticAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2487.RootAssemblyCompoundSystemDeflection)(self.wrapped.LDDStaticAnalysis) if self.wrapped.LDDStaticAnalysis else None

    @property
    def nominal_load_case_static_analysis(self) -> '_2349.RootAssemblySystemDeflection':
        '''RootAssemblySystemDeflection: 'NominalLoadCaseStaticAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2349.RootAssemblySystemDeflection)(self.wrapped.NominalLoadCaseStaticAnalysis) if self.wrapped.NominalLoadCaseStaticAnalysis else None

    @property
    def extreme_load_case_static_analysis(self) -> '_2349.RootAssemblySystemDeflection':
        '''RootAssemblySystemDeflection: 'ExtremeLoadCaseStaticAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2349.RootAssemblySystemDeflection)(self.wrapped.ExtremeLoadCaseStaticAnalysis) if self.wrapped.ExtremeLoadCaseStaticAnalysis else None
