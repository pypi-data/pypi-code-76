'''_3152.py

TorqueConverterConnectionCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2028
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3022
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3072
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'TorqueConverterConnectionCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionCompoundSteadyStateSynchronousResponseAtASpeed',)


class TorqueConverterConnectionCompoundSteadyStateSynchronousResponseAtASpeed(_3072.CouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed):
    '''TorqueConverterConnectionCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2028.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.TorqueConverterConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2028.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3022.TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed]':
        '''List[TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3022.TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def connection_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_3022.TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed]':
        '''List[TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed]: 'ConnectionSteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_3022.TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed))
        return value
