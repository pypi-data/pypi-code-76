'''_6384.py

MeasurementComponentCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2136
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6255
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6430
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'MeasurementComponentCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentCompoundCriticalSpeedAnalysis',)


class MeasurementComponentCompoundCriticalSpeedAnalysis(_6430.VirtualComponentCompoundCriticalSpeedAnalysis):
    '''MeasurementComponentCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2136.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2136.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6255.MeasurementComponentCriticalSpeedAnalysis]':
        '''List[MeasurementComponentCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6255.MeasurementComponentCriticalSpeedAnalysis))
        return value

    @property
    def component_critical_speed_analysis_load_cases(self) -> 'List[_6255.MeasurementComponentCriticalSpeedAnalysis]':
        '''List[MeasurementComponentCriticalSpeedAnalysis]: 'ComponentCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentCriticalSpeedAnalysisLoadCases, constructor.new(_6255.MeasurementComponentCriticalSpeedAnalysis))
        return value
