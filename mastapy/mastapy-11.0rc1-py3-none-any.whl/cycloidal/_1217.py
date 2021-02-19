'''_1217.py

CycloidalDiscDesign
'''


from typing import List

from mastapy._internal import constructor
from mastapy.cycloidal import _1220
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_DESIGN = python_net_import('SMT.MastaAPI.Cycloidal', 'CycloidalDiscDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscDesign',)


class CycloidalDiscDesign(_0.APIBase):
    '''CycloidalDiscDesign

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def disc_id(self) -> 'int':
        '''int: 'DiscID' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DiscID

    @property
    def face_width(self) -> 'float':
        '''float: 'FaceWidth' is the original name of this property.'''

        return self.wrapped.FaceWidth

    @face_width.setter
    def face_width(self, value: 'float'):
        self.wrapped.FaceWidth = float(value) if value else 0.0

    @property
    def generating_wheel_diameter(self) -> 'float':
        '''float: 'GeneratingWheelDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GeneratingWheelDiameter

    @property
    def generating_wheel_centre_circle_diameter(self) -> 'float':
        '''float: 'GeneratingWheelCentreCircleDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GeneratingWheelCentreCircleDiameter

    @property
    def lobe_symmetry_angle_with_no_lobe_modifications(self) -> 'float':
        '''float: 'LobeSymmetryAngleWithNoLobeModifications' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LobeSymmetryAngleWithNoLobeModifications

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def modifications_specification(self) -> '_1220.CycloidalDiscModificationsSpecification':
        '''CycloidalDiscModificationsSpecification: 'ModificationsSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1220.CycloidalDiscModificationsSpecification)(self.wrapped.ModificationsSpecification) if self.wrapped.ModificationsSpecification else None

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
