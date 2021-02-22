'''_2776.py

AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _2777
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft',)


class AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft(_2777.AbstractShaftOrHousingCompoundSteadyStateSynchronousResponseOnAShaft):
    '''AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
