'''_3069.py

ConnectionCompoundSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7169
from mastapy._internal.python_net import python_net_import

_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'ConnectionCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionCompoundSteadyStateSynchronousResponseAtASpeed',)


class ConnectionCompoundSteadyStateSynchronousResponseAtASpeed(_7169.ConnectionCompoundAnalysis):
    '''ConnectionCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
