'''_2012.py

BaseFEWithSelection
'''


from typing import List

from mastapy._internal import constructor
from mastapy.nodal_analysis.dev_tools_analyses import (
    _164, _149, _163, _156
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BASE_FE_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.FE', 'BaseFEWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('BaseFEWithSelection',)


class BaseFEWithSelection(_0.APIBase):
    '''BaseFEWithSelection

    This is a mastapy class.
    '''

    TYPE = _BASE_FE_WITH_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BaseFEWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_selected_faces(self) -> 'int':
        '''int: 'NumberOfSelectedFaces' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfSelectedFaces

    @property
    def number_of_selected_nodes(self) -> 'int':
        '''int: 'NumberOfSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfSelectedNodes

    @property
    def selected_component(self) -> 'str':
        '''str: 'SelectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectedComponent

    @property
    def node_selection(self) -> '_164.FENodeSelectionDrawStyle':
        '''FENodeSelectionDrawStyle: 'NodeSelection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_164.FENodeSelectionDrawStyle)(self.wrapped.NodeSelection) if self.wrapped.NodeSelection else None

    @property
    def draw_style(self) -> '_149.DrawStyleForFE':
        '''DrawStyleForFE: 'DrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_149.DrawStyleForFE)(self.wrapped.DrawStyle) if self.wrapped.DrawStyle else None

    @property
    def transparency_draw_style(self) -> '_163.FEModelTransparencyDrawStyle':
        '''FEModelTransparencyDrawStyle: 'TransparencyDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_163.FEModelTransparencyDrawStyle)(self.wrapped.TransparencyDrawStyle) if self.wrapped.TransparencyDrawStyle else None

    @property
    def component_draw_style(self) -> '_156.FEModelComponentDrawStyle':
        '''FEModelComponentDrawStyle: 'ComponentDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_156.FEModelComponentDrawStyle)(self.wrapped.ComponentDrawStyle) if self.wrapped.ComponentDrawStyle else None

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
