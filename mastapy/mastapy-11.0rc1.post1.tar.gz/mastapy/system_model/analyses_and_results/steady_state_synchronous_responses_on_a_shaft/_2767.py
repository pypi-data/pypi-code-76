'''_2767.py

UnbalancedMassSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model import _2150
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6612
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2768
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'UnbalancedMassSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassSteadyStateSynchronousResponseOnAShaft',)


class UnbalancedMassSteadyStateSynchronousResponseOnAShaft(_2768.VirtualComponentSteadyStateSynchronousResponseOnAShaft):
    '''UnbalancedMassSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassSteadyStateSynchronousResponseOnAShaft.TYPE'):
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
    def component_load_case(self) -> '_6612.UnbalancedMassLoadCase':
        '''UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6612.UnbalancedMassLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
