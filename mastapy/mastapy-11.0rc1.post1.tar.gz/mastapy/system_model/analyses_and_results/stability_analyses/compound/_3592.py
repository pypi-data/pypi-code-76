'''_3592.py

ConnectionCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7169
from mastapy._internal.python_net import python_net_import

_CONNECTION_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ConnectionCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionCompoundStabilityAnalysis',)


class ConnectionCompoundStabilityAnalysis(_7169.ConnectionCompoundAnalysis):
    '''ConnectionCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
