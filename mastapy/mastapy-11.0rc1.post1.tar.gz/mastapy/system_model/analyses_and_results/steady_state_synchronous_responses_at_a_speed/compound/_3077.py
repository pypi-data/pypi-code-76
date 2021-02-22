'''_3077.py

CycloidalAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2239
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2947
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3132
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'CycloidalAssemblyCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblyCompoundSteadyStateSynchronousResponseAtASpeed',)


class CycloidalAssemblyCompoundSteadyStateSynchronousResponseAtASpeed(_3132.SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed):
    '''CycloidalAssemblyCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalAssemblyCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2239.CycloidalAssembly':
        '''CycloidalAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2239.CycloidalAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2239.CycloidalAssembly':
        '''CycloidalAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2239.CycloidalAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2947.CycloidalAssemblySteadyStateSynchronousResponseAtASpeed]':
        '''List[CycloidalAssemblySteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2947.CycloidalAssemblySteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def assembly_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_2947.CycloidalAssemblySteadyStateSynchronousResponseAtASpeed]':
        '''List[CycloidalAssemblySteadyStateSynchronousResponseAtASpeed]: 'AssemblySteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_2947.CycloidalAssemblySteadyStateSynchronousResponseAtASpeed))
        return value
