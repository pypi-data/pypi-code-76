'''_3124.py

RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2017
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2994
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3099
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed',)


class RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed(_3099.InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed):
    '''RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_TO_DISC_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2017.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2017.RingPinsToDiscConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2017.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2017.RingPinsToDiscConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2994.RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed]':
        '''List[RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2994.RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def connection_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_2994.RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed]':
        '''List[RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed]: 'ConnectionSteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_2994.RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed))
        return value
