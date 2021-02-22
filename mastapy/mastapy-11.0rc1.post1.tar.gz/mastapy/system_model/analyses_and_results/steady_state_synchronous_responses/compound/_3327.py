'''_3327.py

ConceptGearSetCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2193
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3325, _3326, _3356
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3193
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'ConceptGearSetCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundSteadyStateSynchronousResponse',)


class ConceptGearSetCompoundSteadyStateSynchronousResponse(_3356.GearSetCompoundSteadyStateSynchronousResponse):
    '''ConceptGearSetCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundSteadyStateSynchronousResponse.TYPE'):
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
    def concept_gears_compound_steady_state_synchronous_response(self) -> 'List[_3325.ConceptGearCompoundSteadyStateSynchronousResponse]':
        '''List[ConceptGearCompoundSteadyStateSynchronousResponse]: 'ConceptGearsCompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundSteadyStateSynchronousResponse, constructor.new(_3325.ConceptGearCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def concept_meshes_compound_steady_state_synchronous_response(self) -> 'List[_3326.ConceptGearMeshCompoundSteadyStateSynchronousResponse]':
        '''List[ConceptGearMeshCompoundSteadyStateSynchronousResponse]: 'ConceptMeshesCompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundSteadyStateSynchronousResponse, constructor.new(_3326.ConceptGearMeshCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3193.ConceptGearSetSteadyStateSynchronousResponse]':
        '''List[ConceptGearSetSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3193.ConceptGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def assembly_steady_state_synchronous_response_load_cases(self) -> 'List[_3193.ConceptGearSetSteadyStateSynchronousResponse]':
        '''List[ConceptGearSetSteadyStateSynchronousResponse]: 'AssemblySteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseLoadCases, constructor.new(_3193.ConceptGearSetSteadyStateSynchronousResponse))
        return value
