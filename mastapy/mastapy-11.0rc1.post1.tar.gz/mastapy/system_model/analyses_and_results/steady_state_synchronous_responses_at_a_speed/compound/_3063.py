'''_3063.py

ConceptGearCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2192
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2935
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3092
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'ConceptGearCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearCompoundSteadyStateSynchronousResponseAtASpeed',)


class ConceptGearCompoundSteadyStateSynchronousResponseAtASpeed(_3092.GearCompoundSteadyStateSynchronousResponseAtASpeed):
    '''ConceptGearCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2192.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2192.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2935.ConceptGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[ConceptGearSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2935.ConceptGearSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def component_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_2935.ConceptGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[ConceptGearSteadyStateSynchronousResponseAtASpeed]: 'ComponentSteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_2935.ConceptGearSteadyStateSynchronousResponseAtASpeed))
        return value
