'''_3603.py

CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2014
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3471
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3560
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis',)


class CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis(_3560.AbstractShaftToMountableComponentConnectionCompoundStabilityAnalysis):
    '''CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2014.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2014.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2014.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2014.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3471.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis]':
        '''List[CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3471.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis))
        return value

    @property
    def connection_stability_analysis_load_cases(self) -> 'List[_3471.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis]':
        '''List[CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis]: 'ConnectionStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionStabilityAnalysisLoadCases, constructor.new(_3471.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis))
        return value
