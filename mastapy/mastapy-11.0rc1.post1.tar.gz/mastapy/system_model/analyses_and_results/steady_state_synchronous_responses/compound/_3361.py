'''_3361.py

InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse
'''


from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3331
from mastapy._internal.python_net import python_net_import

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse',)


class InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse(_3331.ConnectionCompoundSteadyStateSynchronousResponse):
    '''InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
