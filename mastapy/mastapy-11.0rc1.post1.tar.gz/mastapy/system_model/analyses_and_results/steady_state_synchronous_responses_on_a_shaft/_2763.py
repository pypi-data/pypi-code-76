'''_2763.py

TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.connections_and_sockets.couplings import _2028
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6604
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2682
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft',)


class TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft(_2682.CouplingConnectionSteadyStateSynchronousResponseOnAShaft):
    '''TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2028.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6604.TorqueConverterConnectionLoadCase':
        '''TorqueConverterConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6604.TorqueConverterConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
