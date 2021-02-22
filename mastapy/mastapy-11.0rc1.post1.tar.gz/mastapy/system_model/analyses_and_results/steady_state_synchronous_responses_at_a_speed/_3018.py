'''_3018.py

SynchroniserHalfSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.part_model.couplings import _2275
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6598
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3019
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'SynchroniserHalfSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfSteadyStateSynchronousResponseAtASpeed',)


class SynchroniserHalfSteadyStateSynchronousResponseAtASpeed(_3019.SynchroniserPartSteadyStateSynchronousResponseAtASpeed):
    '''SynchroniserHalfSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2275.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2275.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6598.SynchroniserHalfLoadCase':
        '''SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6598.SynchroniserHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
