'''_292.py

CylindricalGearSetRatingOptimisationHelper
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating.cylindrical.optimisation import (
    _293, _297, _296, _298,
    _294
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_RATING_OPTIMISATION_HELPER = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.Optimisation', 'CylindricalGearSetRatingOptimisationHelper')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetRatingOptimisationHelper',)


class CylindricalGearSetRatingOptimisationHelper(_0.APIBase):
    '''CylindricalGearSetRatingOptimisationHelper

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_RATING_OPTIMISATION_HELPER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetRatingOptimisationHelper.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def create_optimisation_report(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CreateOptimisationReport' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateOptimisationReport

    @property
    def set_helix_angle_for_maximum_safety_factor(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SetHelixAngleForMaximumSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetHelixAngleForMaximumSafetyFactor

    @property
    def set_profile_shift_coefficient_for_maximum_safety_factor(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SetProfileShiftCoefficientForMaximumSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetProfileShiftCoefficientForMaximumSafetyFactor

    @property
    def set_normal_module_for_maximum_safety_factor(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SetNormalModuleForMaximumSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetNormalModuleForMaximumSafetyFactor

    @property
    def set_pressure_angle_for_maximum_safety_factor(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SetPressureAngleForMaximumSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetPressureAngleForMaximumSafetyFactor

    @property
    def set_face_widths_for_required_safety_factor(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SetFaceWidthsForRequiredSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetFaceWidthsForRequiredSafetyFactor

    @property
    def calculate_optimisation_charts(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateOptimisationCharts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateOptimisationCharts

    @property
    def profile_shift_coefficient_optimisation_results(self) -> '_293.OptimisationResultsPair[_297.SafetyFactorOptimisationStepResultNumber]':
        '''OptimisationResultsPair[SafetyFactorOptimisationStepResultNumber]: 'ProfileShiftCoefficientOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_293.OptimisationResultsPair)[_297.SafetyFactorOptimisationStepResultNumber](self.wrapped.ProfileShiftCoefficientOptimisationResults) if self.wrapped.ProfileShiftCoefficientOptimisationResults else None

    @property
    def helix_angle_optimisation_results(self) -> '_293.OptimisationResultsPair[_296.SafetyFactorOptimisationStepResultAngle]':
        '''OptimisationResultsPair[SafetyFactorOptimisationStepResultAngle]: 'HelixAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_293.OptimisationResultsPair)[_296.SafetyFactorOptimisationStepResultAngle](self.wrapped.HelixAngleOptimisationResults) if self.wrapped.HelixAngleOptimisationResults else None

    @property
    def normal_module_optimisation_results(self) -> '_293.OptimisationResultsPair[_298.SafetyFactorOptimisationStepResultShortLength]':
        '''OptimisationResultsPair[SafetyFactorOptimisationStepResultShortLength]: 'NormalModuleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_293.OptimisationResultsPair)[_298.SafetyFactorOptimisationStepResultShortLength](self.wrapped.NormalModuleOptimisationResults) if self.wrapped.NormalModuleOptimisationResults else None

    @property
    def pressure_angle_optimisation_results(self) -> '_293.OptimisationResultsPair[_296.SafetyFactorOptimisationStepResultAngle]':
        '''OptimisationResultsPair[SafetyFactorOptimisationStepResultAngle]: 'PressureAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_293.OptimisationResultsPair)[_296.SafetyFactorOptimisationStepResultAngle](self.wrapped.PressureAngleOptimisationResults) if self.wrapped.PressureAngleOptimisationResults else None

    @property
    def all_normal_module_optimisation_results(self) -> 'List[_294.SafetyFactorOptimisationResults[_298.SafetyFactorOptimisationStepResultShortLength]]':
        '''List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultShortLength]]: 'AllNormalModuleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllNormalModuleOptimisationResults, constructor.new(_294.SafetyFactorOptimisationResults)[_298.SafetyFactorOptimisationStepResultShortLength])
        return value

    @property
    def all_helix_angle_optimisation_results(self) -> 'List[_294.SafetyFactorOptimisationResults[_296.SafetyFactorOptimisationStepResultAngle]]':
        '''List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultAngle]]: 'AllHelixAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllHelixAngleOptimisationResults, constructor.new(_294.SafetyFactorOptimisationResults)[_296.SafetyFactorOptimisationStepResultAngle])
        return value

    @property
    def all_normal_pressure_angle_optimisation_results(self) -> 'List[_294.SafetyFactorOptimisationResults[_296.SafetyFactorOptimisationStepResultAngle]]':
        '''List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultAngle]]: 'AllNormalPressureAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllNormalPressureAngleOptimisationResults, constructor.new(_294.SafetyFactorOptimisationResults)[_296.SafetyFactorOptimisationStepResultAngle])
        return value

    @property
    def helix_angle_and_normal_pressure_angle_optimisation_results(self) -> 'List[_294.SafetyFactorOptimisationResults[_296.SafetyFactorOptimisationStepResultAngle]]':
        '''List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultAngle]]: 'HelixAngleAndNormalPressureAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HelixAngleAndNormalPressureAngleOptimisationResults, constructor.new(_294.SafetyFactorOptimisationResults)[_296.SafetyFactorOptimisationStepResultAngle])
        return value

    @property
    def all_profile_shift_optimisation_results(self) -> 'List[_294.SafetyFactorOptimisationResults[_297.SafetyFactorOptimisationStepResultNumber]]':
        '''List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultNumber]]: 'AllProfileShiftOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllProfileShiftOptimisationResults, constructor.new(_294.SafetyFactorOptimisationResults)[_297.SafetyFactorOptimisationStepResultNumber])
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
