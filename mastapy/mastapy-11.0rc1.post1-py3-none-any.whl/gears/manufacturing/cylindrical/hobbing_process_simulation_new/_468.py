'''_468.py

ProcessSimulationNew
'''


from typing import List, Generic, TypeVar

from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _464, _466, _465, _463,
    _470, _467
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PROCESS_SIMULATION_NEW = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ProcessSimulationNew')


__docformat__ = 'restructuredtext en'
__all__ = ('ProcessSimulationNew',)


T = TypeVar('T', bound='_467.ProcessSimulationInput')


class ProcessSimulationNew(_0.APIBase, Generic[T]):
    '''ProcessSimulationNew

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _PROCESS_SIMULATION_NEW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ProcessSimulationNew.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def achieved_iso132811995e_quality_grade(self) -> 'float':
        '''float: 'AchievedISO132811995EQualityGrade' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AchievedISO132811995EQualityGrade

    @property
    def achieved_ansiagma20151a01_quality_grade(self) -> 'float':
        '''float: 'AchievedANSIAGMA20151A01QualityGrade' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AchievedANSIAGMA20151A01QualityGrade

    @property
    def input(self) -> 'T':
        '''T: 'Input' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(T)(self.wrapped.Input) if self.wrapped.Input else None

    @property
    def lead_calculation(self) -> '_464.ProcessLeadCalculation':
        '''ProcessLeadCalculation: 'LeadCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_464.ProcessLeadCalculation)(self.wrapped.LeadCalculation) if self.wrapped.LeadCalculation else None

    @property
    def profile_calculation(self) -> '_466.ProcessProfileCalculation':
        '''ProcessProfileCalculation: 'ProfileCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_466.ProcessProfileCalculation)(self.wrapped.ProfileCalculation) if self.wrapped.ProfileCalculation else None

    @property
    def pitch_calculation(self) -> '_465.ProcessPitchCalculation':
        '''ProcessPitchCalculation: 'PitchCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_465.ProcessPitchCalculation)(self.wrapped.PitchCalculation) if self.wrapped.PitchCalculation else None

    @property
    def gear_tooth_shape_calculation(self) -> '_463.ProcessGearShape':
        '''ProcessGearShape: 'GearToothShapeCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_463.ProcessGearShape)(self.wrapped.GearToothShapeCalculation) if self.wrapped.GearToothShapeCalculation else None

    @property
    def total_modification_calculation(self) -> '_470.ProcessTotalModificationCalculation':
        '''ProcessTotalModificationCalculation: 'TotalModificationCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_470.ProcessTotalModificationCalculation)(self.wrapped.TotalModificationCalculation) if self.wrapped.TotalModificationCalculation else None

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
