'''_4653.py

ConnectionCompoundModalAnalysisAtASpeed
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7169
from mastapy._internal.python_net import python_net_import

_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'ConnectionCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionCompoundModalAnalysisAtASpeed',)


class ConnectionCompoundModalAnalysisAtASpeed(_7169.ConnectionCompoundAnalysis):
    '''ConnectionCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
