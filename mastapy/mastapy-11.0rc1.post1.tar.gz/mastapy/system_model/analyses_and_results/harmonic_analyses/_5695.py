'''_5695.py

PartToPartShearCouplingHalfHarmonicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2260
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6559
from mastapy.system_model.analyses_and_results.system_deflections import _2449
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5629
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_HALF_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'PartToPartShearCouplingHalfHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingHalfHarmonicAnalysis',)


class PartToPartShearCouplingHalfHarmonicAnalysis(_5629.CouplingHalfHarmonicAnalysis):
    '''PartToPartShearCouplingHalfHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_HALF_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingHalfHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2260.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2260.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6559.PartToPartShearCouplingHalfLoadCase':
        '''PartToPartShearCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6559.PartToPartShearCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2449.PartToPartShearCouplingHalfSystemDeflection':
        '''PartToPartShearCouplingHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2449.PartToPartShearCouplingHalfSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
