'''_1933.py

BatchOperations
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.imported_fes import _1948
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BATCH_OPERATIONS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'BatchOperations')


__docformat__ = 'restructuredtext en'
__all__ = ('BatchOperations',)


class BatchOperations(_0.APIBase):
    '''BatchOperations

    This is a mastapy class.
    '''

    TYPE = _BATCH_OPERATIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BatchOperations.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def all_selected(self) -> 'bool':
        '''bool: 'AllSelected' is the original name of this property.'''

        return self.wrapped.AllSelected

    @all_selected.setter
    def all_selected(self, value: 'bool'):
        self.wrapped.AllSelected = bool(value) if value else False

    @property
    def select_all_to_be_unloaded(self) -> 'bool':
        '''bool: 'SelectAllToBeUnloaded' is the original name of this property.'''

        return self.wrapped.SelectAllToBeUnloaded

    @select_all_to_be_unloaded.setter
    def select_all_to_be_unloaded(self, value: 'bool'):
        self.wrapped.SelectAllToBeUnloaded = bool(value) if value else False

    @property
    def perform_reduction_for_selected(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'PerformReductionForSelected' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PerformReductionForSelected

    @property
    def remove_all_full_fe_meshes_in_design(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'RemoveAllFullFEMeshesInDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RemoveAllFullFEMeshesInDesign

    @property
    def load_all_selected_external_files(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'LoadAllSelectedExternalFiles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadAllSelectedExternalFiles

    @property
    def unload_all_selected_external_files(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'UnloadAllSelectedExternalFiles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.UnloadAllSelectedExternalFiles

    @property
    def total_memory_for_all_loaded_external_fes(self) -> 'str':
        '''str: 'TotalMemoryForAllLoadedExternalFEs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalMemoryForAllLoadedExternalFEs

    @property
    def total_memory_for_all_files_selected_to_unload(self) -> 'str':
        '''str: 'TotalMemoryForAllFilesSelectedToUnload' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalMemoryForAllFilesSelectedToUnload

    @property
    def fe_components(self) -> 'List[_1948.FEComponentWithBatchOptions]':
        '''List[FEComponentWithBatchOptions]: 'FEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEComponents, constructor.new(_1948.FEComponentWithBatchOptions))
        return value

    @property
    def fe_components_with_external_files(self) -> 'List[_1948.FEComponentWithBatchOptions]':
        '''List[FEComponentWithBatchOptions]: 'FEComponentsWithExternalFiles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEComponentsWithExternalFiles, constructor.new(_1948.FEComponentWithBatchOptions))
        return value

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
