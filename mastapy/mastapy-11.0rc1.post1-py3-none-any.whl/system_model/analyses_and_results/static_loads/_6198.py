'''_6198.py

HarmonicLoadDataImportBase
'''


from typing import (
    Callable, List, Generic, TypeVar
)

from mastapy._internal import constructor
from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy.system_model.analyses_and_results.static_loads import _6179
from mastapy._internal.python_net import python_net_import

_HARMONIC_LOAD_DATA_IMPORT_BASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HarmonicLoadDataImportBase')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicLoadDataImportBase',)


T = TypeVar('T', bound='_6179.ElectricMachineHarmonicLoadImportOptionsBase')


class HarmonicLoadDataImportBase(_0.APIBase, Generic[T]):
    '''HarmonicLoadDataImportBase

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _HARMONIC_LOAD_DATA_IMPORT_BASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HarmonicLoadDataImportBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def file_name(self) -> 'str':
        '''str: 'FileName' is the original name of this property.'''

        return self.wrapped.FileName

    @file_name.setter
    def file_name(self, value: 'str'):
        self.wrapped.FileName = str(value) if value else None

    @property
    def read_data_from_file(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ReadDataFromFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReadDataFromFile

    @property
    def negate_torque_data_on_import(self) -> 'bool':
        '''bool: 'NegateTorqueDataOnImport' is the original name of this property.'''

        return self.wrapped.NegateTorqueDataOnImport

    @negate_torque_data_on_import.setter
    def negate_torque_data_on_import(self, value: 'bool'):
        self.wrapped.NegateTorqueDataOnImport = bool(value) if value else False

    @property
    def negate_stator_radial_load_data_on_import(self) -> 'bool':
        '''bool: 'NegateStatorRadialLoadDataOnImport' is the original name of this property.'''

        return self.wrapped.NegateStatorRadialLoadDataOnImport

    @negate_stator_radial_load_data_on_import.setter
    def negate_stator_radial_load_data_on_import(self, value: 'bool'):
        self.wrapped.NegateStatorRadialLoadDataOnImport = bool(value) if value else False

    @property
    def negate_stator_tangential_load_data_on_import(self) -> 'bool':
        '''bool: 'NegateStatorTangentialLoadDataOnImport' is the original name of this property.'''

        return self.wrapped.NegateStatorTangentialLoadDataOnImport

    @negate_stator_tangential_load_data_on_import.setter
    def negate_stator_tangential_load_data_on_import(self, value: 'bool'):
        self.wrapped.NegateStatorTangentialLoadDataOnImport = bool(value) if value else False

    @property
    def negate_stator_axial_load_data_on_import(self) -> 'bool':
        '''bool: 'NegateStatorAxialLoadDataOnImport' is the original name of this property.'''

        return self.wrapped.NegateStatorAxialLoadDataOnImport

    @negate_stator_axial_load_data_on_import.setter
    def negate_stator_axial_load_data_on_import(self, value: 'bool'):
        self.wrapped.NegateStatorAxialLoadDataOnImport = bool(value) if value else False

    @property
    def negate_speed_data_on_import(self) -> 'bool':
        '''bool: 'NegateSpeedDataOnImport' is the original name of this property.'''

        return self.wrapped.NegateSpeedDataOnImport

    @negate_speed_data_on_import.setter
    def negate_speed_data_on_import(self, value: 'bool'):
        self.wrapped.NegateSpeedDataOnImport = bool(value) if value else False

    @property
    def node_id_of_first_tooth(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'NodeIdOfFirstTooth' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.NodeIdOfFirstTooth) if self.wrapped.NodeIdOfFirstTooth else None

    @node_id_of_first_tooth.setter
    def node_id_of_first_tooth(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.NodeIdOfFirstTooth = value

    @property
    def imported_data_has_different_direction_for_tooth_ids_to_masta_model(self) -> 'bool':
        '''bool: 'ImportedDataHasDifferentDirectionForToothIdsToMASTAModel' is the original name of this property.'''

        return self.wrapped.ImportedDataHasDifferentDirectionForToothIdsToMASTAModel

    @imported_data_has_different_direction_for_tooth_ids_to_masta_model.setter
    def imported_data_has_different_direction_for_tooth_ids_to_masta_model(self, value: 'bool'):
        self.wrapped.ImportedDataHasDifferentDirectionForToothIdsToMASTAModel = bool(value) if value else False

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
