'''_3332.py

ConnectorCompoundSteadyStateSynchronousResponse
'''


from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3373
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'ConnectorCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorCompoundSteadyStateSynchronousResponse',)


class ConnectorCompoundSteadyStateSynchronousResponse(_3373.MountableComponentCompoundSteadyStateSynchronousResponse):
    '''ConnectorCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectorCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
