'''_3095.py

GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _2128
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2965
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3059
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed',)


class GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed(_3059.ComponentCompoundSteadyStateSynchronousResponseAtASpeed):
    '''GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2128.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2128.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2965.GuideDxfModelSteadyStateSynchronousResponseAtASpeed]':
        '''List[GuideDxfModelSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2965.GuideDxfModelSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def component_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_2965.GuideDxfModelSteadyStateSynchronousResponseAtASpeed]':
        '''List[GuideDxfModelSteadyStateSynchronousResponseAtASpeed]: 'ComponentSteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_2965.GuideDxfModelSteadyStateSynchronousResponseAtASpeed))
        return value
