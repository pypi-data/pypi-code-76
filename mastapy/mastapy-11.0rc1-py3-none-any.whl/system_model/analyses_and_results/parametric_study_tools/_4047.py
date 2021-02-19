'''_4047.py

ParametricStudyToolOptions
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import overridable, list_with_selected_item, enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.analyses_and_results.static_loads import _6449, _6556
from mastapy.system_model import _1891
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4049, _4050
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PARAMETRIC_STUDY_TOOL_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ParametricStudyToolOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('ParametricStudyToolOptions',)


class ParametricStudyToolOptions(_0.APIBase):
    '''ParametricStudyToolOptions

    This is a mastapy class.
    '''

    TYPE = _PARAMETRIC_STUDY_TOOL_OPTIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParametricStudyToolOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_logging_data(self) -> 'bool':
        '''bool: 'IsLoggingData' is the original name of this property.'''

        return self.wrapped.IsLoggingData

    @is_logging_data.setter
    def is_logging_data(self, value: 'bool'):
        self.wrapped.IsLoggingData = bool(value) if value else False

    @property
    def log_report(self) -> 'bool':
        '''bool: 'LogReport' is the original name of this property.'''

        return self.wrapped.LogReport

    @log_report.setter
    def log_report(self, value: 'bool'):
        self.wrapped.LogReport = bool(value) if value else False

    @property
    def changing_design(self) -> 'bool':
        '''bool: 'ChangingDesign' is the original name of this property.'''

        return self.wrapped.ChangingDesign

    @changing_design.setter
    def changing_design(self, value: 'bool'):
        self.wrapped.ChangingDesign = bool(value) if value else False

    @property
    def save_design_at_each_step(self) -> 'bool':
        '''bool: 'SaveDesignAtEachStep' is the original name of this property.'''

        return self.wrapped.SaveDesignAtEachStep

    @save_design_at_each_step.setter
    def save_design_at_each_step(self, value: 'bool'):
        self.wrapped.SaveDesignAtEachStep = bool(value) if value else False

    @property
    def folder_path_for_saved_files(self) -> 'str':
        '''str: 'FolderPathForSavedFiles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FolderPathForSavedFiles

    @property
    def use_multiple_designs(self) -> 'overridable.Overridable_bool':
        '''overridable.Overridable_bool: 'UseMultipleDesigns' is the original name of this property.'''

        return constructor.new(overridable.Overridable_bool)(self.wrapped.UseMultipleDesigns) if self.wrapped.UseMultipleDesigns else None

    @use_multiple_designs.setter
    def use_multiple_designs(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else False, is_overridden)
        self.wrapped.UseMultipleDesigns = value

    @property
    def maximum_number_of_design_copies_to_use(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'MaximumNumberOfDesignCopiesToUse' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.MaximumNumberOfDesignCopiesToUse) if self.wrapped.MaximumNumberOfDesignCopiesToUse else None

    @maximum_number_of_design_copies_to_use.setter
    def maximum_number_of_design_copies_to_use(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0, is_overridden)
        self.wrapped.MaximumNumberOfDesignCopiesToUse = value

    @property
    def put_newly_added_numerical_variables_into(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'PutNewlyAddedNumericalVariablesInto' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.PutNewlyAddedNumericalVariablesInto) if self.wrapped.PutNewlyAddedNumericalVariablesInto else None

    @put_newly_added_numerical_variables_into.setter
    def put_newly_added_numerical_variables_into(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.PutNewlyAddedNumericalVariablesInto = value

    @property
    def analysis_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_AnalysisType':
        '''enum_with_selected_value.EnumWithSelectedValue_AnalysisType: 'AnalysisType' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_AnalysisType.implicit_type()
        return enum_with_selected_value_runtime.create(self.wrapped.AnalysisType, value) if self.wrapped.AnalysisType else None

    @analysis_type.setter
    def analysis_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_AnalysisType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_AnalysisType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.AnalysisType = value

    @property
    def number_of_steps(self) -> 'int':
        '''int: 'NumberOfSteps' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfSteps

    @property
    def perform_system_optimisation_pst_post_analysis(self) -> 'bool':
        '''bool: 'PerformSystemOptimisationPSTPostAnalysis' is the original name of this property.'''

        return self.wrapped.PerformSystemOptimisationPSTPostAnalysis

    @perform_system_optimisation_pst_post_analysis.setter
    def perform_system_optimisation_pst_post_analysis(self, value: 'bool'):
        self.wrapped.PerformSystemOptimisationPSTPostAnalysis = bool(value) if value else False

    @property
    def steps_for_statistical_study(self) -> 'int':
        '''int: 'StepsForStatisticalStudy' is the original name of this property.'''

        return self.wrapped.StepsForStatisticalStudy

    @steps_for_statistical_study.setter
    def steps_for_statistical_study(self, value: 'int'):
        self.wrapped.StepsForStatisticalStudy = int(value) if value else 0

    @property
    def steps_in_dimension_1(self) -> 'int':
        '''int: 'StepsInDimension1' is the original name of this property.'''

        return self.wrapped.StepsInDimension1

    @steps_in_dimension_1.setter
    def steps_in_dimension_1(self, value: 'int'):
        self.wrapped.StepsInDimension1 = int(value) if value else 0

    @property
    def parametric_study_type(self) -> '_6556.ParametricStudyType':
        '''ParametricStudyType: 'ParametricStudyType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ParametricStudyType)
        return constructor.new(_6556.ParametricStudyType)(value) if value else None

    @parametric_study_type.setter
    def parametric_study_type(self, value: '_6556.ParametricStudyType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ParametricStudyType = value

    @property
    def steps_in_dimension_2(self) -> 'int':
        '''int: 'StepsInDimension2' is the original name of this property.'''

        return self.wrapped.StepsInDimension2

    @steps_in_dimension_2.setter
    def steps_in_dimension_2(self, value: 'int'):
        self.wrapped.StepsInDimension2 = int(value) if value else 0

    @property
    def number_of_analysis_dimensions(self) -> 'int':
        '''int: 'NumberOfAnalysisDimensions' is the original name of this property.'''

        return self.wrapped.NumberOfAnalysisDimensions

    @number_of_analysis_dimensions.setter
    def number_of_analysis_dimensions(self, value: 'int'):
        self.wrapped.NumberOfAnalysisDimensions = int(value) if value else 0

    @property
    def external_full_fe_loader(self) -> '_1891.ExternalFullFELoader':
        '''ExternalFullFELoader: 'ExternalFullFELoader' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1891.ExternalFullFELoader)(self.wrapped.ExternalFullFELoader) if self.wrapped.ExternalFullFELoader else None

    @property
    def step_results(self) -> 'List[_4049.ParametricStudyToolStepResult]':
        '''List[ParametricStudyToolStepResult]: 'StepResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StepResults, constructor.new(_4049.ParametricStudyToolStepResult))
        return value

    @property
    def study_variables(self) -> 'List[_4050.ParametricStudyVariable]':
        '''List[ParametricStudyVariable]: 'StudyVariables' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StudyVariables, constructor.new(_4050.ParametricStudyVariable))
        return value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def edit_folder_path(self):
        ''' 'EditFolderPath' is the original name of this method.'''

        self.wrapped.EditFolderPath()

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
