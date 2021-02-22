'''_3424.py

ZerolBevelGearSetCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2225
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3422, _3423, _3314
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3294
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'ZerolBevelGearSetCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundSteadyStateSynchronousResponse',)


class ZerolBevelGearSetCompoundSteadyStateSynchronousResponse(_3314.BevelGearSetCompoundSteadyStateSynchronousResponse):
    '''ZerolBevelGearSetCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2225.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2225.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2225.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2225.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_steady_state_synchronous_response(self) -> 'List[_3422.ZerolBevelGearCompoundSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearCompoundSteadyStateSynchronousResponse]: 'ZerolBevelGearsCompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundSteadyStateSynchronousResponse, constructor.new(_3422.ZerolBevelGearCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def zerol_bevel_meshes_compound_steady_state_synchronous_response(self) -> 'List[_3423.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearMeshCompoundSteadyStateSynchronousResponse]: 'ZerolBevelMeshesCompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundSteadyStateSynchronousResponse, constructor.new(_3423.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3294.ZerolBevelGearSetSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearSetSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3294.ZerolBevelGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def assembly_steady_state_synchronous_response_load_cases(self) -> 'List[_3294.ZerolBevelGearSetSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearSetSteadyStateSynchronousResponse]: 'AssemblySteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseLoadCases, constructor.new(_3294.ZerolBevelGearSetSteadyStateSynchronousResponse))
        return value
