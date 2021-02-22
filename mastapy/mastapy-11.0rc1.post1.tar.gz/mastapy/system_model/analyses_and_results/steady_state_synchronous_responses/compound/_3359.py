'''_3359.py

HypoidGearMeshCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1991
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3226
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3301
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'HypoidGearMeshCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshCompoundSteadyStateSynchronousResponse',)


class HypoidGearMeshCompoundSteadyStateSynchronousResponse(_3301.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponse):
    '''HypoidGearMeshCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshCompoundSteadyStateSynchronousResponse.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3226.HypoidGearMeshSteadyStateSynchronousResponse]':
        '''List[HypoidGearMeshSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3226.HypoidGearMeshSteadyStateSynchronousResponse))
        return value

    @property
    def connection_steady_state_synchronous_response_load_cases(self) -> 'List[_3226.HypoidGearMeshSteadyStateSynchronousResponse]':
        '''List[HypoidGearMeshSteadyStateSynchronousResponse]: 'ConnectionSteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSteadyStateSynchronousResponseLoadCases, constructor.new(_3226.HypoidGearMeshSteadyStateSynchronousResponse))
        return value
