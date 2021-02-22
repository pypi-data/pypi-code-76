'''_6704.py

HypoidGearAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.part_model.gears import _2205
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6535
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6644
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'HypoidGearAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearAdvancedTimeSteppingAnalysisForModulation',)


class HypoidGearAdvancedTimeSteppingAnalysisForModulation(_6644.AGMAGleasonConicalGearAdvancedTimeSteppingAnalysisForModulation):
    '''HypoidGearAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2205.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2205.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6535.HypoidGearLoadCase':
        '''HypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6535.HypoidGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
