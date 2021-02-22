'''_3097.py

HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1991
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2966
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3039
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed',)


class HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed(_3039.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed):
    '''HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1991.HypoidGearMesh':
        '''HypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1991.HypoidGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1991.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1991.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2966.HypoidGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[HypoidGearMeshSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2966.HypoidGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def connection_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_2966.HypoidGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[HypoidGearMeshSteadyStateSynchronousResponseAtASpeed]: 'ConnectionSteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_2966.HypoidGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value
