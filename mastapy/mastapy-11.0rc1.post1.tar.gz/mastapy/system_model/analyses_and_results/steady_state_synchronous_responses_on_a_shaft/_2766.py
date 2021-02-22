'''_2766.py

TorqueConverterTurbineSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.couplings import _2281
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6607
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2683
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'TorqueConverterTurbineSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineSteadyStateSynchronousResponseOnAShaft',)


class TorqueConverterTurbineSteadyStateSynchronousResponseOnAShaft(_2683.CouplingHalfSteadyStateSynchronousResponseOnAShaft):
    '''TorqueConverterTurbineSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineSteadyStateSynchronousResponseOnAShaft.TYPE'):
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
    def component_load_case(self) -> '_6607.TorqueConverterTurbineLoadCase':
        '''TorqueConverterTurbineLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6607.TorqueConverterTurbineLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
