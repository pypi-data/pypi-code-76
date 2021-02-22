'''_5716.py

SpiralBevelGearHarmonicAnalysis
'''


from mastapy.system_model.part_model.gears import _2214
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6583
from mastapy.system_model.analyses_and_results.system_deflections import _2471
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5606
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'SpiralBevelGearHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearHarmonicAnalysis',)


class SpiralBevelGearHarmonicAnalysis(_5606.BevelGearHarmonicAnalysis):
    '''SpiralBevelGearHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearHarmonicAnalysis.TYPE'):
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

    @property
    def system_deflection_results(self) -> '_2471.SpiralBevelGearSystemDeflection':
        '''SpiralBevelGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2471.SpiralBevelGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
