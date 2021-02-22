'''_6352.py

CycloidalDiscCentralBearingConnectionCompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6332
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'CycloidalDiscCentralBearingConnectionCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCentralBearingConnectionCompoundCriticalSpeedAnalysis',)


class CycloidalDiscCentralBearingConnectionCompoundCriticalSpeedAnalysis(_6332.CoaxialConnectionCompoundCriticalSpeedAnalysis):
    '''CycloidalDiscCentralBearingConnectionCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCentralBearingConnectionCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
