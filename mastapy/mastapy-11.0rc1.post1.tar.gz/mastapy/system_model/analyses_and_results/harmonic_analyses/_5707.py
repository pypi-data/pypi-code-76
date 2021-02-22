'''_5707.py

RollingRingConnectionHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1968
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6575
from mastapy.system_model.analyses_and_results.system_deflections import _2460
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5679
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'RollingRingConnectionHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionHarmonicAnalysis',)


class RollingRingConnectionHarmonicAnalysis(_5679.InterMountableComponentConnectionHarmonicAnalysis):
    '''RollingRingConnectionHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1968.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6575.RollingRingConnectionLoadCase':
        '''RollingRingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6575.RollingRingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2460.RollingRingConnectionSystemDeflection':
        '''RollingRingConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2460.RollingRingConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[RollingRingConnectionHarmonicAnalysis]':
        '''List[RollingRingConnectionHarmonicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionHarmonicAnalysis))
        return value
