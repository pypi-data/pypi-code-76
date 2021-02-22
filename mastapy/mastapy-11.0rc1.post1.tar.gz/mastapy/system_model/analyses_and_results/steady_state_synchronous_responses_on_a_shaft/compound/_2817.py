'''_2817.py

CVTPulleyCompoundSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _2863
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'CVTPulleyCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundSteadyStateSynchronousResponseOnAShaft',)


class CVTPulleyCompoundSteadyStateSynchronousResponseOnAShaft(_2863.PulleyCompoundSteadyStateSynchronousResponseOnAShaft):
    '''CVTPulleyCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
