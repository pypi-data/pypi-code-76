'''_3500.py

KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis
'''


from mastapy.system_model.part_model.gears import _2211
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6547
from mastapy.system_model.analyses_and_results.stability_analyses import _3494
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis(_3494.KlingelnbergCycloPalloidConicalGearStabilityAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2211.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2211.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6547.KlingelnbergCycloPalloidSpiralBevelGearLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6547.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
