'''_6330.py

ClutchConnectionCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2018
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6198
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6346
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'ClutchConnectionCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionCompoundCriticalSpeedAnalysis',)


class ClutchConnectionCompoundCriticalSpeedAnalysis(_6346.CouplingConnectionCompoundCriticalSpeedAnalysis):
    '''ClutchConnectionCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2018.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.ClutchConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2018.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6198.ClutchConnectionCriticalSpeedAnalysis]':
        '''List[ClutchConnectionCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6198.ClutchConnectionCriticalSpeedAnalysis))
        return value

    @property
    def connection_critical_speed_analysis_load_cases(self) -> 'List[_6198.ClutchConnectionCriticalSpeedAnalysis]':
        '''List[ClutchConnectionCriticalSpeedAnalysis]: 'ConnectionCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionCriticalSpeedAnalysisLoadCases, constructor.new(_6198.ClutchConnectionCriticalSpeedAnalysis))
        return value
