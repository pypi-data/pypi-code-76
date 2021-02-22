'''_3108.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2212
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3106, _3107, _3102
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2977
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed(_3102.KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2212.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2212.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2212.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2212.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3106.KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundSteadyStateSynchronousResponseAtASpeed, constructor.new(_3106.KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3107.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundSteadyStateSynchronousResponseAtASpeed, constructor.new(_3107.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_2977.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2977.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def assembly_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_2977.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'AssemblySteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_2977.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed))
        return value
