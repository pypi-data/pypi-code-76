'''_2850.py

MassDiscCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model import _2135
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2720
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _2897
from mastapy._internal.python_net import python_net_import

_MASS_DISC_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'MassDiscCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCompoundSteadyStateSynchronousResponseOnAShaft',)


class MassDiscCompoundSteadyStateSynchronousResponseOnAShaft(_2897.VirtualComponentCompoundSteadyStateSynchronousResponseOnAShaft):
    '''MassDiscCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2135.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2135.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2720.MassDiscSteadyStateSynchronousResponseOnAShaft]':
        '''List[MassDiscSteadyStateSynchronousResponseOnAShaft]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2720.MassDiscSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def component_steady_state_synchronous_response_on_a_shaft_load_cases(self) -> 'List[_2720.MassDiscSteadyStateSynchronousResponseOnAShaft]':
        '''List[MassDiscSteadyStateSynchronousResponseOnAShaft]: 'ComponentSteadyStateSynchronousResponseOnAShaftLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseOnAShaftLoadCases, constructor.new(_2720.MassDiscSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def planetaries(self) -> 'List[MassDiscCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[MassDiscCompoundSteadyStateSynchronousResponseOnAShaft]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscCompoundSteadyStateSynchronousResponseOnAShaft))
        return value
