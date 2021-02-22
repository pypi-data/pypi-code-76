'''_3265.py

SpiralBevelGearSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.gears import _2214
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6583
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3181
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'SpiralBevelGearSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSteadyStateSynchronousResponse',)


class SpiralBevelGearSteadyStateSynchronousResponse(_3181.BevelGearSteadyStateSynchronousResponse):
    '''SpiralBevelGearSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2214.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2214.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6583.SpiralBevelGearLoadCase':
        '''SpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6583.SpiralBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
