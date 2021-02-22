'''_2806.py

ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.gears import _2193
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _2804, _2805, _2835
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2675
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft',)


class ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft(_2835.GearSetCompoundSteadyStateSynchronousResponseOnAShaft):
    '''ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2193.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2193.ConceptGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2193.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2193.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def concept_gears_compound_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2804.ConceptGearCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ConceptGearCompoundSteadyStateSynchronousResponseOnAShaft]: 'ConceptGearsCompoundSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundSteadyStateSynchronousResponseOnAShaft, constructor.new(_2804.ConceptGearCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def concept_meshes_compound_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2805.ConceptGearMeshCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ConceptGearMeshCompoundSteadyStateSynchronousResponseOnAShaft]: 'ConceptMeshesCompoundSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundSteadyStateSynchronousResponseOnAShaft, constructor.new(_2805.ConceptGearMeshCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_2675.ConceptGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[ConceptGearSetSteadyStateSynchronousResponseOnAShaft]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2675.ConceptGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def assembly_steady_state_synchronous_response_on_a_shaft_load_cases(self) -> 'List[_2675.ConceptGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[ConceptGearSetSteadyStateSynchronousResponseOnAShaft]: 'AssemblySteadyStateSynchronousResponseOnAShaftLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseOnAShaftLoadCases, constructor.new(_2675.ConceptGearSetSteadyStateSynchronousResponseOnAShaft))
        return value
