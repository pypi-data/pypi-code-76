'''_2022.py

RaceBearingFE
'''


from typing import Callable, List

from mastapy.system_model.imported_fes import _1966, _1972
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.part_model import _2050
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_RACE_BEARING_FE = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'RaceBearingFE')


__docformat__ = 'restructuredtext en'
__all__ = ('RaceBearingFE',)


class RaceBearingFE(_0.APIBase):
    '''RaceBearingFE

    This is a mastapy class.
    '''

    TYPE = _RACE_BEARING_FE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RaceBearingFE.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def alignment_method(self) -> '_1966.AlignmentMethodForRaceBearing':
        '''AlignmentMethodForRaceBearing: 'AlignmentMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.AlignmentMethod)
        return constructor.new(_1966.AlignmentMethodForRaceBearing)(value) if value else None

    @alignment_method.setter
    def alignment_method(self, value: '_1966.AlignmentMethodForRaceBearing'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AlignmentMethod = value

    @property
    def fe_filename(self) -> 'str':
        '''str: 'FEFilename' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FEFilename

    @property
    def import_fe_mesh(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ImportFEMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ImportFEMesh

    @property
    def find_nodes_for_links(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'FindNodesForLinks' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FindNodesForLinks

    @property
    def datum(self) -> 'list_with_selected_item.ListWithSelectedItem_Datum':
        '''list_with_selected_item.ListWithSelectedItem_Datum: 'Datum' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Datum)(self.wrapped.Datum) if self.wrapped.Datum else None

    @datum.setter
    def datum(self, value: 'list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Datum.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.Datum = value

    @property
    def copy_datum_to_manual(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CopyDatumToManual' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CopyDatumToManual

    @property
    def links(self) -> 'List[_1972.BearingRaceNodeLink]':
        '''List[BearingRaceNodeLink]: 'Links' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Links, constructor.new(_1972.BearingRaceNodeLink))
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
