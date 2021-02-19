'''_5391.py

GearWhineAnalysisFEExportOptions
'''


from typing import Callable, List

from mastapy._internal.implicit import list_with_selected_item, enum_with_selected_value
from mastapy.system_model.analyses_and_results.gear_whine_analyses import (
    _5399, _5392, _5434, _5383
)
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.utility.units_and_measurements import _1173
from mastapy.nodal_analysis.fe_export_utility import _1474
from mastapy.math_utility import _1080
from mastapy.nodal_analysis.dev_tools_analyses import _1476
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_WHINE_ANALYSIS_FE_EXPORT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'GearWhineAnalysisFEExportOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('GearWhineAnalysisFEExportOptions',)


class GearWhineAnalysisFEExportOptions(_0.APIBase):
    '''GearWhineAnalysisFEExportOptions

    This is a mastapy class.
    '''

    TYPE = _GEAR_WHINE_ANALYSIS_FE_EXPORT_OPTIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearWhineAnalysisFEExportOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def planetary_duplicate_to_export(self) -> 'list_with_selected_item.ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis':
        '''list_with_selected_item.ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis: 'PlanetaryDuplicateToExport' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis)(self.wrapped.PlanetaryDuplicateToExport) if self.wrapped.PlanetaryDuplicateToExport else None

    @planetary_duplicate_to_export.setter
    def planetary_duplicate_to_export(self, value: 'list_with_selected_item.ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.PlanetaryDuplicateToExport = value

    @property
    def distance_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        '''list_with_selected_item.ListWithSelectedItem_Unit: 'DistanceUnit' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Unit)(self.wrapped.DistanceUnit) if self.wrapped.DistanceUnit else None

    @distance_unit.setter
    def distance_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.DistanceUnit = value

    @property
    def force_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        '''list_with_selected_item.ListWithSelectedItem_Unit: 'ForceUnit' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Unit)(self.wrapped.ForceUnit) if self.wrapped.ForceUnit else None

    @force_unit.setter
    def force_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ForceUnit = value

    @property
    def export_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType':
        '''enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType: 'ExportType' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ExportType, value) if self.wrapped.ExportType else None

    @export_type.setter
    def export_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ExportType = value

    @property
    def complex_number_output_option(self) -> 'enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput':
        '''enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput: 'ComplexNumberOutputOption' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ComplexNumberOutputOption, value) if self.wrapped.ComplexNumberOutputOption else None

    @complex_number_output_option.setter
    def complex_number_output_option(self, value: 'enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ComplexNumberOutputOption = value

    @property
    def include_original_fe_file(self) -> 'bool':
        '''bool: 'IncludeOriginalFEFile' is the original name of this property.'''

        return self.wrapped.IncludeOriginalFEFile

    @include_original_fe_file.setter
    def include_original_fe_file(self, value: 'bool'):
        self.wrapped.IncludeOriginalFEFile = bool(value) if value else False

    @property
    def fe_export_format(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FEExportFormat':
        '''enum_with_selected_value.EnumWithSelectedValue_FEExportFormat: 'FEExportFormat' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.FEExportFormat, value) if self.wrapped.FEExportFormat else None

    @fe_export_format.setter
    def fe_export_format(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.FEExportFormat = value

    @property
    def include_rigid_couplings_and_nodes_added_by_masta(self) -> 'bool':
        '''bool: 'IncludeRigidCouplingsAndNodesAddedByMASTA' is the original name of this property.'''

        return self.wrapped.IncludeRigidCouplingsAndNodesAddedByMASTA

    @include_rigid_couplings_and_nodes_added_by_masta.setter
    def include_rigid_couplings_and_nodes_added_by_masta(self, value: 'bool'):
        self.wrapped.IncludeRigidCouplingsAndNodesAddedByMASTA = bool(value) if value else False

    @property
    def use_single_speed(self) -> 'bool':
        '''bool: 'UseSingleSpeed' is the original name of this property.'''

        return self.wrapped.UseSingleSpeed

    @use_single_speed.setter
    def use_single_speed(self, value: 'bool'):
        self.wrapped.UseSingleSpeed = bool(value) if value else False

    @property
    def reference_speed(self) -> 'float':
        '''float: 'ReferenceSpeed' is the original name of this property.'''

        return self.wrapped.ReferenceSpeed

    @reference_speed.setter
    def reference_speed(self, value: 'float'):
        self.wrapped.ReferenceSpeed = float(value) if value else 0.0

    @property
    def combine_excitations_of_same_order(self) -> 'bool':
        '''bool: 'CombineExcitationsOfSameOrder' is the original name of this property.'''

        return self.wrapped.CombineExcitationsOfSameOrder

    @combine_excitations_of_same_order.setter
    def combine_excitations_of_same_order(self, value: 'bool'):
        self.wrapped.CombineExcitationsOfSameOrder = bool(value) if value else False

    @property
    def export_results(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ExportResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportResults

    @property
    def status_message_for_export(self) -> 'str':
        '''str: 'StatusMessageForExport' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StatusMessageForExport

    @property
    def type_of_result_to_export(self) -> 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType':
        '''enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType: 'TypeOfResultToExport' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.TypeOfResultToExport, value) if self.wrapped.TypeOfResultToExport else None

    @type_of_result_to_export.setter
    def type_of_result_to_export(self, value: 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.TypeOfResultToExport = value

    @property
    def analysis_options(self) -> '_5392.GearWhineAnalysisOptions':
        '''GearWhineAnalysisOptions: 'AnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5392.GearWhineAnalysisOptions)(self.wrapped.AnalysisOptions) if self.wrapped.AnalysisOptions else None

    @property
    def reference_speed_options(self) -> '_5434.SpeedOptionsForGearWhineAnalysisResults':
        '''SpeedOptionsForGearWhineAnalysisResults: 'ReferenceSpeedOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5434.SpeedOptionsForGearWhineAnalysisResults)(self.wrapped.ReferenceSpeedOptions) if self.wrapped.ReferenceSpeedOptions else None

    @property
    def frequency_options(self) -> '_5383.FrequencyOptionsForGearWhineAnalysisResults':
        '''FrequencyOptionsForGearWhineAnalysisResults: 'FrequencyOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5383.FrequencyOptionsForGearWhineAnalysisResults)(self.wrapped.FrequencyOptions) if self.wrapped.FrequencyOptions else None

    @property
    def eigenvalue_options(self) -> '_1476.EigenvalueOptions':
        '''EigenvalueOptions: 'EigenvalueOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1476.EigenvalueOptions)(self.wrapped.EigenvalueOptions) if self.wrapped.EigenvalueOptions else None

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def export_to_folder(self, folder_path: 'str') -> 'List[str]':
        ''' 'ExportToFolder' is the original name of this method.

        Args:
            folder_path (str)

        Returns:
            List[str]
        '''

        folder_path = str(folder_path)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.ExportToFolder(folder_path if folder_path else None), str)

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
