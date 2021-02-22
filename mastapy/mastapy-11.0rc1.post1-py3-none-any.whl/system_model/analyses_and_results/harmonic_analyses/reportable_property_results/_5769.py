'''_5769.py

ResultsForOrder
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
    _5763, _5766, _5767, _5764
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_RESULTS_FOR_ORDER = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults', 'ResultsForOrder')


__docformat__ = 'restructuredtext en'
__all__ = ('ResultsForOrder',)


class ResultsForOrder(_0.APIBase):
    '''ResultsForOrder

    This is a mastapy class.
    '''

    TYPE = _RESULTS_FOR_ORDER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ResultsForOrder.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def order(self) -> 'str':
        '''str: 'Order' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Order

    @property
    def component(self) -> '_5763.HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic':
        '''HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5763.HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def node_results_global_coordinate_system(self) -> 'List[_5766.HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic]':
        '''List[HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic]: 'NodeResultsGlobalCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.NodeResultsGlobalCoordinateSystem, constructor.new(_5766.HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic))
        return value

    @property
    def node_results_local_coordinate_system(self) -> 'List[_5766.HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic]':
        '''List[HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic]: 'NodeResultsLocalCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.NodeResultsLocalCoordinateSystem, constructor.new(_5766.HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic))
        return value

    @property
    def fe_surfaces(self) -> 'List[_5767.HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic]':
        '''List[HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic]: 'FESurfaces' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FESurfaces, constructor.new(_5767.HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic))
        return value

    @property
    def groups(self) -> 'List[_5764.HarmonicAnalysisResultsBrokenDownByGroupsWithinAHarmonic]':
        '''List[HarmonicAnalysisResultsBrokenDownByGroupsWithinAHarmonic]: 'Groups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Groups, constructor.new(_5764.HarmonicAnalysisResultsBrokenDownByGroupsWithinAHarmonic))
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
