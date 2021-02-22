'''_2438.py

KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection
'''


from mastapy.system_model.part_model.gears import _2211
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6547
from mastapy.system_model.analyses_and_results.power_flows import _3766
from mastapy.gears.rating.klingelnberg_spiral_bevel import _366
from mastapy.system_model.analyses_and_results.system_deflections import _2432
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection',)


class KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection(_2432.KlingelnbergCycloPalloidConicalGearSystemDeflection):
    '''KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection.TYPE'):
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

    @property
    def power_flow_results(self) -> '_3766.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow':
        '''KlingelnbergCycloPalloidSpiralBevelGearPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3766.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def component_detailed_analysis(self) -> '_366.KlingelnbergCycloPalloidSpiralBevelGearRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_366.KlingelnbergCycloPalloidSpiralBevelGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
