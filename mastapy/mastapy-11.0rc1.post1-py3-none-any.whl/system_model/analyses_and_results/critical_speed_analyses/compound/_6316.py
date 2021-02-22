'''_6316.py

BearingCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2114
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6185
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6344
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'BearingCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundCriticalSpeedAnalysis',)


class BearingCompoundCriticalSpeedAnalysis(_6344.ConnectorCompoundCriticalSpeedAnalysis):
    '''BearingCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2114.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6185.BearingCriticalSpeedAnalysis]':
        '''List[BearingCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6185.BearingCriticalSpeedAnalysis))
        return value

    @property
    def component_critical_speed_analysis_load_cases(self) -> 'List[_6185.BearingCriticalSpeedAnalysis]':
        '''List[BearingCriticalSpeedAnalysis]: 'ComponentCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentCriticalSpeedAnalysisLoadCases, constructor.new(_6185.BearingCriticalSpeedAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[BearingCompoundCriticalSpeedAnalysis]':
        '''List[BearingCompoundCriticalSpeedAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingCompoundCriticalSpeedAnalysis))
        return value
