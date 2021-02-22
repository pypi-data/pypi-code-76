'''_5798.py

CoaxialConnectionCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1945
from mastapy._internal import constructor, conversion
from mastapy.system_model.connections_and_sockets.cycloidal import _2011
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5614
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5871
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'CoaxialConnectionCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionCompoundHarmonicAnalysis',)


class CoaxialConnectionCompoundHarmonicAnalysis(_5871.ShaftToMountableComponentConnectionCompoundHarmonicAnalysis):
    '''CoaxialConnectionCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1945.CoaxialConnection':
        '''CoaxialConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1945.CoaxialConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CoaxialConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1945.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1945.CoaxialConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CoaxialConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5614.CoaxialConnectionHarmonicAnalysis]':
        '''List[CoaxialConnectionHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5614.CoaxialConnectionHarmonicAnalysis))
        return value

    @property
    def connection_harmonic_analysis_load_cases(self) -> 'List[_5614.CoaxialConnectionHarmonicAnalysis]':
        '''List[CoaxialConnectionHarmonicAnalysis]: 'ConnectionHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionHarmonicAnalysisLoadCases, constructor.new(_5614.CoaxialConnectionHarmonicAnalysis))
        return value
