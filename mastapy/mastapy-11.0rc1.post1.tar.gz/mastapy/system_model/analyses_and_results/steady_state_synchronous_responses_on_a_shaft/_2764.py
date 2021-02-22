'''_2764.py

TorqueConverterPumpSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.couplings import _2279
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6606
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2683
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'TorqueConverterPumpSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpSteadyStateSynchronousResponseOnAShaft',)


class TorqueConverterPumpSteadyStateSynchronousResponseOnAShaft(_2683.CouplingHalfSteadyStateSynchronousResponseOnAShaft):
    '''TorqueConverterPumpSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2279.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2279.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6606.TorqueConverterPumpLoadCase':
        '''TorqueConverterPumpLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6606.TorqueConverterPumpLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
