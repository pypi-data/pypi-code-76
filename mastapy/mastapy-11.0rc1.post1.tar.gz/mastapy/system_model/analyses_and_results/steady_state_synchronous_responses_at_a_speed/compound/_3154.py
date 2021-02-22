'''_3154.py

TorqueConverterTurbineCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2281
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3025
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3073
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'TorqueConverterTurbineCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineCompoundSteadyStateSynchronousResponseAtASpeed',)


class TorqueConverterTurbineCompoundSteadyStateSynchronousResponseAtASpeed(_3073.CouplingHalfCompoundSteadyStateSynchronousResponseAtASpeed):
    '''TorqueConverterTurbineCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2281.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2281.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3025.TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed]':
        '''List[TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3025.TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def component_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_3025.TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed]':
        '''List[TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed]: 'ComponentSteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_3025.TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed))
        return value
