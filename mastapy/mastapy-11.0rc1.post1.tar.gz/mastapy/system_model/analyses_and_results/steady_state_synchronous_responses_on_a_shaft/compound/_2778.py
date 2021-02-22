'''_2778.py

AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _2810
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft',)


class AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft(_2810.ConnectionCompoundSteadyStateSynchronousResponseOnAShaft):
    '''AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
