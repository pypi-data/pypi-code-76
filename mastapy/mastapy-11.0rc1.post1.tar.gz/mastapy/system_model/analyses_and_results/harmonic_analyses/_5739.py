'''_5739.py

UnbalancedMassHarmonicAnalysis
'''


from mastapy.system_model.part_model import _2150
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6612
from mastapy.system_model.analyses_and_results.system_deflections import _2496
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5740
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'UnbalancedMassHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassHarmonicAnalysis',)


class UnbalancedMassHarmonicAnalysis(_5740.VirtualComponentHarmonicAnalysis):
    '''UnbalancedMassHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassHarmonicAnalysis.TYPE'):
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

    @property
    def system_deflection_results(self) -> '_2496.UnbalancedMassSystemDeflection':
        '''UnbalancedMassSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2496.UnbalancedMassSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
