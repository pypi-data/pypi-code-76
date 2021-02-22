'''_3417.py

UnbalancedMassCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _2150
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3288
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3418
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'UnbalancedMassCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassCompoundSteadyStateSynchronousResponse',)


class UnbalancedMassCompoundSteadyStateSynchronousResponse(_3418.VirtualComponentCompoundSteadyStateSynchronousResponse):
    '''UnbalancedMassCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2150.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2150.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3288.UnbalancedMassSteadyStateSynchronousResponse]':
        '''List[UnbalancedMassSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3288.UnbalancedMassSteadyStateSynchronousResponse))
        return value

    @property
    def component_steady_state_synchronous_response_load_cases(self) -> 'List[_3288.UnbalancedMassSteadyStateSynchronousResponse]':
        '''List[UnbalancedMassSteadyStateSynchronousResponse]: 'ComponentSteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseLoadCases, constructor.new(_3288.UnbalancedMassSteadyStateSynchronousResponse))
        return value
