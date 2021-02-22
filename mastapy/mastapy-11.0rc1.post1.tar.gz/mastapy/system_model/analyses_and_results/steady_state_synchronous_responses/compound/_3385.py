'''_3385.py

RingPinsCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2241
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3253
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3373
from mastapy._internal.python_net import python_net_import

_RING_PINS_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'RingPinsCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsCompoundSteadyStateSynchronousResponse',)


class RingPinsCompoundSteadyStateSynchronousResponse(_3373.MountableComponentCompoundSteadyStateSynchronousResponse):
    '''RingPinsCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2241.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2241.RingPins)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3253.RingPinsSteadyStateSynchronousResponse]':
        '''List[RingPinsSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3253.RingPinsSteadyStateSynchronousResponse))
        return value

    @property
    def component_steady_state_synchronous_response_load_cases(self) -> 'List[_3253.RingPinsSteadyStateSynchronousResponse]':
        '''List[RingPinsSteadyStateSynchronousResponse]: 'ComponentSteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseLoadCases, constructor.new(_3253.RingPinsSteadyStateSynchronousResponse))
        return value
