'''_1872.py

GearWhineAnalysisViewable
'''


from mastapy._internal.implicit import enum_with_selected_value, list_with_selected_item
from mastapy.system_model.drawing.options import _1886
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5319, _5395
from mastapy.utility.generics import _1346
from mastapy.math_utility import _1100
from mastapy.system_model.analyses_and_results.system_deflections import _2329
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5912
from mastapy.system_model.analyses_and_results.modal_analyses import _4840
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.drawing import _1871
from mastapy._internal.python_net import python_net_import

_GEAR_WHINE_ANALYSIS_VIEWABLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'GearWhineAnalysisViewable')


__docformat__ = 'restructuredtext en'
__all__ = ('GearWhineAnalysisViewable',)


class GearWhineAnalysisViewable(_1871.DynamicAnalysisViewable):
    '''GearWhineAnalysisViewable

    This is a mastapy class.
    '''

    TYPE = _GEAR_WHINE_ANALYSIS_VIEWABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearWhineAnalysisViewable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def view_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ExcitationAnalysisViewOption':
        '''enum_with_selected_value.EnumWithSelectedValue_ExcitationAnalysisViewOption: 'ViewType' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_ExcitationAnalysisViewOption.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ViewType, value) if self.wrapped.ViewType else None

    @view_type.setter
    def view_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ExcitationAnalysisViewOption.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ExcitationAnalysisViewOption.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ViewType = value

    @property
    def excitation(self) -> 'list_with_selected_item.ListWithSelectedItem_AbstractPeriodicExcitationDetail':
        '''list_with_selected_item.ListWithSelectedItem_AbstractPeriodicExcitationDetail: 'Excitation' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_AbstractPeriodicExcitationDetail)(self.wrapped.Excitation) if self.wrapped.Excitation else None

    @excitation.setter
    def excitation(self, value: 'list_with_selected_item.ListWithSelectedItem_AbstractPeriodicExcitationDetail.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_AbstractPeriodicExcitationDetail.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_AbstractPeriodicExcitationDetail.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.Excitation = value

    @property
    def harmonic(self) -> 'int':
        '''int: 'Harmonic' is the original name of this property.'''

        return self.wrapped.Harmonic

    @harmonic.setter
    def harmonic(self, value: 'int'):
        self.wrapped.Harmonic = int(value) if value else 0

    @property
    def order(self) -> 'list_with_selected_item.ListWithSelectedItem_NamedTuple1_RoundedOrder':
        '''list_with_selected_item.ListWithSelectedItem_NamedTuple1_RoundedOrder: 'Order' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_NamedTuple1_RoundedOrder)(self.wrapped.Order) if self.wrapped.Order else None

    @order.setter
    def order(self, value: 'list_with_selected_item.ListWithSelectedItem_NamedTuple1_RoundedOrder.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_NamedTuple1_RoundedOrder.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_NamedTuple1_RoundedOrder.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.Order = value

    @property
    def reference_power_load_speed(self) -> 'float':
        '''float: 'ReferencePowerLoadSpeed' is the original name of this property.'''

        return self.wrapped.ReferencePowerLoadSpeed

    @reference_power_load_speed.setter
    def reference_power_load_speed(self, value: 'float'):
        self.wrapped.ReferencePowerLoadSpeed = float(value) if value else 0.0

    @property
    def frequency(self) -> 'float':
        '''float: 'Frequency' is the original name of this property.'''

        return self.wrapped.Frequency

    @frequency.setter
    def frequency(self, value: 'float'):
        self.wrapped.Frequency = float(value) if value else 0.0

    @property
    def uncoupled_mesh(self) -> 'list_with_selected_item.ListWithSelectedItem_GearMeshSystemDeflection':
        '''list_with_selected_item.ListWithSelectedItem_GearMeshSystemDeflection: 'UncoupledMesh' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_GearMeshSystemDeflection)(self.wrapped.UncoupledMesh) if self.wrapped.UncoupledMesh else None

    @uncoupled_mesh.setter
    def uncoupled_mesh(self, value: 'list_with_selected_item.ListWithSelectedItem_GearMeshSystemDeflection.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_GearMeshSystemDeflection.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_GearMeshSystemDeflection.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.UncoupledMesh = value

    @property
    def dynamic_analysis_draw_style(self) -> '_5912.DynamicAnalysisDrawStyle':
        '''DynamicAnalysisDrawStyle: 'DynamicAnalysisDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5912.DynamicAnalysisDrawStyle.TYPE not in self.wrapped.DynamicAnalysisDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast dynamic_analysis_draw_style to DynamicAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.DynamicAnalysisDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DynamicAnalysisDrawStyle.__class__)(self.wrapped.DynamicAnalysisDrawStyle) if self.wrapped.DynamicAnalysisDrawStyle else None

    @property
    def dynamic_analysis_draw_style_of_type_modal_analysis_draw_style(self) -> '_4840.ModalAnalysisDrawStyle':
        '''ModalAnalysisDrawStyle: 'DynamicAnalysisDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4840.ModalAnalysisDrawStyle.TYPE not in self.wrapped.DynamicAnalysisDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast dynamic_analysis_draw_style to ModalAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.DynamicAnalysisDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DynamicAnalysisDrawStyle.__class__)(self.wrapped.DynamicAnalysisDrawStyle) if self.wrapped.DynamicAnalysisDrawStyle else None

    @property
    def dynamic_analysis_draw_style_of_type_harmonic_analysis_draw_style(self) -> '_5395.HarmonicAnalysisDrawStyle':
        '''HarmonicAnalysisDrawStyle: 'DynamicAnalysisDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5395.HarmonicAnalysisDrawStyle.TYPE not in self.wrapped.DynamicAnalysisDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast dynamic_analysis_draw_style to HarmonicAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.DynamicAnalysisDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DynamicAnalysisDrawStyle.__class__)(self.wrapped.DynamicAnalysisDrawStyle) if self.wrapped.DynamicAnalysisDrawStyle else None
