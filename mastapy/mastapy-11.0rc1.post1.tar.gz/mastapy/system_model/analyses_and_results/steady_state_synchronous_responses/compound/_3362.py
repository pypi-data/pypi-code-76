'''_3362.py

KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponse
'''


from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3328
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponse',)


class KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponse(_3328.ConicalGearCompoundSteadyStateSynchronousResponse):
    '''KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
