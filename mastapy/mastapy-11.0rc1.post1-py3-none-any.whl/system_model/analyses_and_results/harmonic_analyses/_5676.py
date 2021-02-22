'''_5676.py

HypoidGearHarmonicAnalysis
'''


from mastapy.system_model.part_model.gears import _2205
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6535
from mastapy.system_model.analyses_and_results.system_deflections import _2427
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5594
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'HypoidGearHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearHarmonicAnalysis',)


class HypoidGearHarmonicAnalysis(_5594.AGMAGleasonConicalGearHarmonicAnalysis):
    '''HypoidGearHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearHarmonicAnalysis.TYPE'):
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

    @property
    def system_deflection_results(self) -> '_2427.HypoidGearSystemDeflection':
        '''HypoidGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2427.HypoidGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
