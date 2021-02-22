'''_3354.py

GearCompoundSteadyStateSynchronousResponse
'''


from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3373
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'GearCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundSteadyStateSynchronousResponse',)


class GearCompoundSteadyStateSynchronousResponse(_3373.MountableComponentCompoundSteadyStateSynchronousResponse):
    '''GearCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
