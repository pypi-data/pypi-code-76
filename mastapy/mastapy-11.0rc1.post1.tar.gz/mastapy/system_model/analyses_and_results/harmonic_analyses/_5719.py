'''_5719.py

SpringDamperConnectionHarmonicAnalysis
'''


from mastapy.system_model.connections_and_sockets.couplings import _2026
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6586
from mastapy.system_model.analyses_and_results.system_deflections import _2472
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5628
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'SpringDamperConnectionHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperConnectionHarmonicAnalysis',)


class SpringDamperConnectionHarmonicAnalysis(_5628.CouplingConnectionHarmonicAnalysis):
    '''SpringDamperConnectionHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_CONNECTION_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperConnectionHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2026.SpringDamperConnection':
        '''SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2026.SpringDamperConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6586.SpringDamperConnectionLoadCase':
        '''SpringDamperConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6586.SpringDamperConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2472.SpringDamperConnectionSystemDeflection':
        '''SpringDamperConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2472.SpringDamperConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
