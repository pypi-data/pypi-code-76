'''_6086.py

CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6066
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis',)


class CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis(_6066.CoaxialConnectionCompoundDynamicAnalysis):
    '''CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
