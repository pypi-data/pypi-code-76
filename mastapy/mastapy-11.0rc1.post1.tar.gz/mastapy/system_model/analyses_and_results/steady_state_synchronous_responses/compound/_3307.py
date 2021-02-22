'''_3307.py

BevelDifferentialGearCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2186, _2188, _2189
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3176
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3312
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'BevelDifferentialGearCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearCompoundSteadyStateSynchronousResponse',)


class BevelDifferentialGearCompoundSteadyStateSynchronousResponse(_3312.BevelGearCompoundSteadyStateSynchronousResponse):
    '''BevelDifferentialGearCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2186.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2186.BevelDifferentialGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3176.BevelDifferentialGearSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3176.BevelDifferentialGearSteadyStateSynchronousResponse))
        return value

    @property
    def component_steady_state_synchronous_response_load_cases(self) -> 'List[_3176.BevelDifferentialGearSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearSteadyStateSynchronousResponse]: 'ComponentSteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseLoadCases, constructor.new(_3176.BevelDifferentialGearSteadyStateSynchronousResponse))
        return value
