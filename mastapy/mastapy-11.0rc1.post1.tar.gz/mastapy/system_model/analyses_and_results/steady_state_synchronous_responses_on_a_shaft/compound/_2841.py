'''_2841.py

KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _2807
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseOnAShaft',)


class KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseOnAShaft(_2807.ConicalGearCompoundSteadyStateSynchronousResponseOnAShaft):
    '''KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
