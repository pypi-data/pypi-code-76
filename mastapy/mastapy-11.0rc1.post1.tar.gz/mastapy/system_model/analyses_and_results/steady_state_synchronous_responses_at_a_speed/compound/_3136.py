'''_3136.py

SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2271
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3008
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3071
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed',)


class SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed(_3071.CouplingCompoundSteadyStateSynchronousResponseAtASpeed):
    '''SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2271.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2271.SpringDamper)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2271.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2271.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3008.SpringDamperSteadyStateSynchronousResponseAtASpeed]':
        '''List[SpringDamperSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3008.SpringDamperSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def assembly_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_3008.SpringDamperSteadyStateSynchronousResponseAtASpeed]':
        '''List[SpringDamperSteadyStateSynchronousResponseAtASpeed]: 'AssemblySteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_3008.SpringDamperSteadyStateSynchronousResponseAtASpeed))
        return value
