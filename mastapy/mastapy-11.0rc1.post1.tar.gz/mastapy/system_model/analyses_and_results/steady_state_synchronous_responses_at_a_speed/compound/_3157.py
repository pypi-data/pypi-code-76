'''_3157.py

WormGearCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2222
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3030
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3092
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'WormGearCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearCompoundSteadyStateSynchronousResponseAtASpeed',)


class WormGearCompoundSteadyStateSynchronousResponseAtASpeed(_3092.GearCompoundSteadyStateSynchronousResponseAtASpeed):
    '''WormGearCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2222.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2222.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3030.WormGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[WormGearSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3030.WormGearSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def component_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_3030.WormGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[WormGearSteadyStateSynchronousResponseAtASpeed]: 'ComponentSteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_3030.WormGearSteadyStateSynchronousResponseAtASpeed))
        return value
