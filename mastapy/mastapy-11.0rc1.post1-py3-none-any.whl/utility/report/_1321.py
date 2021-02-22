'''_1321.py

CustomSubReport
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.utility.report import _1302
from mastapy._internal.python_net import python_net_import

_CUSTOM_SUB_REPORT = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomSubReport')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomSubReport',)


class CustomSubReport(_1302.CustomReportDefinitionItem):
    '''CustomSubReport

    This is a mastapy class.
    '''

    TYPE = _CUSTOM_SUB_REPORT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CustomSubReport.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def show_report_edit_toolbar(self) -> 'bool':
        '''bool: 'ShowReportEditToolbar' is the original name of this property.'''

        return self.wrapped.ShowReportEditToolbar

    @show_report_edit_toolbar.setter
    def show_report_edit_toolbar(self, value: 'bool'):
        self.wrapped.ShowReportEditToolbar = bool(value) if value else False

    @property
    def show_as_report_in_the_editor(self) -> 'bool':
        '''bool: 'ShowAsReportInTheEditor' is the original name of this property.'''

        return self.wrapped.ShowAsReportInTheEditor

    @show_as_report_in_the_editor.setter
    def show_as_report_in_the_editor(self, value: 'bool'):
        self.wrapped.ShowAsReportInTheEditor = bool(value) if value else False

    @property
    def scale(self) -> 'float':
        '''float: 'Scale' is the original name of this property.'''

        return self.wrapped.Scale

    @scale.setter
    def scale(self, value: 'float'):
        self.wrapped.Scale = float(value) if value else 0.0

    @property
    def create_new_page(self) -> 'bool':
        '''bool: 'CreateNewPage' is the original name of this property.'''

        return self.wrapped.CreateNewPage

    @create_new_page.setter
    def create_new_page(self, value: 'bool'):
        self.wrapped.CreateNewPage = bool(value) if value else False

    @property
    def show_table_of_contents(self) -> 'bool':
        '''bool: 'ShowTableOfContents' is the original name of this property.'''

        return self.wrapped.ShowTableOfContents

    @show_table_of_contents.setter
    def show_table_of_contents(self, value: 'bool'):
        self.wrapped.ShowTableOfContents = bool(value) if value else False

    @property
    def report_source(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ReportSource' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportSource
