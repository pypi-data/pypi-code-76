'''_2871.py

ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2269
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2740
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _2811
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft',)


class ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft(_2811.ConnectorCompoundSteadyStateSynchronousResponseOnAShaft):
    '''ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2269.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2269.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2740.ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft]':
        '''List[ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2740.ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def component_steady_state_synchronous_response_on_a_shaft_load_cases(self) -> 'List[_2740.ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft]':
        '''List[ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft]: 'ComponentSteadyStateSynchronousResponseOnAShaftLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseOnAShaftLoadCases, constructor.new(_2740.ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft))
        return value
