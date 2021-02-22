'''_2675.py

ConceptGearSetSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.gears import _2193
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6474
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2676, _2674, _2704
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'ConceptGearSetSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetSteadyStateSynchronousResponseOnAShaft',)


class ConceptGearSetSteadyStateSynchronousResponseOnAShaft(_2704.GearSetSteadyStateSynchronousResponseOnAShaft):
    '''ConceptGearSetSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2193.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2193.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6474.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6474.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def concept_gears_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2676.ConceptGearSteadyStateSynchronousResponseOnAShaft]':
        '''List[ConceptGearSteadyStateSynchronousResponseOnAShaft]: 'ConceptGearsSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsSteadyStateSynchronousResponseOnAShaft, constructor.new(_2676.ConceptGearSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def concept_meshes_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2674.ConceptGearMeshSteadyStateSynchronousResponseOnAShaft]':
        '''List[ConceptGearMeshSteadyStateSynchronousResponseOnAShaft]: 'ConceptMeshesSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesSteadyStateSynchronousResponseOnAShaft, constructor.new(_2674.ConceptGearMeshSteadyStateSynchronousResponseOnAShaft))
        return value
