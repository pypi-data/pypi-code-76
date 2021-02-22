'''_2692.py

CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1985
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6494
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2703
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft',)


class CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft(_2703.GearMeshSteadyStateSynchronousResponseOnAShaft):
    '''CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1985.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6494.CylindricalGearMeshLoadCase':
        '''CylindricalGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6494.CylindricalGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft]':
        '''List[CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft))
        return value
