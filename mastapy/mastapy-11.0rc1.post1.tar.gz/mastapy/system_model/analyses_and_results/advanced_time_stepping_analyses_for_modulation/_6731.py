'''_6731.py

RingPinsAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.part_model.cycloidal import _2241
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6572
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6719
from mastapy._internal.python_net import python_net_import

_RING_PINS_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'RingPinsAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsAdvancedTimeSteppingAnalysisForModulation',)


class RingPinsAdvancedTimeSteppingAnalysisForModulation(_6719.MountableComponentAdvancedTimeSteppingAnalysisForModulation):
    '''RingPinsAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2241.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2241.RingPins)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6572.RingPinsLoadCase':
        '''RingPinsLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6572.RingPinsLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
