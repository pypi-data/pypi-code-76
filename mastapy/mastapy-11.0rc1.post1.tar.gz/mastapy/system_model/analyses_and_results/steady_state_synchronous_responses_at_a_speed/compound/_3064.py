'''_3064.py

ConceptGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1981
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2933
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3093
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'ConceptGearMeshCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshCompoundSteadyStateSynchronousResponseAtASpeed',)


class ConceptGearMeshCompoundSteadyStateSynchronousResponseAtASpeed(_3093.GearMeshCompoundSteadyStateSynchronousResponseAtASpeed):
    '''ConceptGearMeshCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1981.ConceptGearMesh':
        '''ConceptGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.ConceptGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1981.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2933.ConceptGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[ConceptGearMeshSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2933.ConceptGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def connection_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_2933.ConceptGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[ConceptGearMeshSteadyStateSynchronousResponseAtASpeed]: 'ConnectionSteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_2933.ConceptGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value
