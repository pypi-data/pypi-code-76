'''_2060.py

InternalClearanceTolerance
'''


from typing import List

from mastapy._internal.implicit import enum_with_selected_value
from mastapy.bearings.tolerances import _1566, _1564
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_INTERNAL_CLEARANCE_TOLERANCE = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'InternalClearanceTolerance')


__docformat__ = 'restructuredtext en'
__all__ = ('InternalClearanceTolerance',)


class InternalClearanceTolerance(_0.APIBase):
    '''InternalClearanceTolerance

    This is a mastapy class.
    '''

    TYPE = _INTERNAL_CLEARANCE_TOLERANCE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'InternalClearanceTolerance.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def definition_option(self) -> 'enum_with_selected_value.EnumWithSelectedValue_BearingToleranceDefinitionOptions':
        '''enum_with_selected_value.EnumWithSelectedValue_BearingToleranceDefinitionOptions: 'DefinitionOption' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_BearingToleranceDefinitionOptions.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.DefinitionOption, value) if self.wrapped.DefinitionOption else None

    @definition_option.setter
    def definition_option(self, value: 'enum_with_selected_value.EnumWithSelectedValue_BearingToleranceDefinitionOptions.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BearingToleranceDefinitionOptions.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.DefinitionOption = value

    @property
    def clearance_class(self) -> 'enum_with_selected_value.EnumWithSelectedValue_InternalClearanceClass':
        '''enum_with_selected_value.EnumWithSelectedValue_InternalClearanceClass: 'ClearanceClass' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_InternalClearanceClass.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ClearanceClass, value) if self.wrapped.ClearanceClass else None

    @clearance_class.setter
    def clearance_class(self, value: 'enum_with_selected_value.EnumWithSelectedValue_InternalClearanceClass.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_InternalClearanceClass.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ClearanceClass = value

    @property
    def minimum(self) -> 'float':
        '''float: 'Minimum' is the original name of this property.'''

        return self.wrapped.Minimum

    @minimum.setter
    def minimum(self, value: 'float'):
        self.wrapped.Minimum = float(value) if value else 0.0

    @property
    def maximum(self) -> 'float':
        '''float: 'Maximum' is the original name of this property.'''

        return self.wrapped.Maximum

    @maximum.setter
    def maximum(self, value: 'float'):
        self.wrapped.Maximum = float(value) if value else 0.0

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result
