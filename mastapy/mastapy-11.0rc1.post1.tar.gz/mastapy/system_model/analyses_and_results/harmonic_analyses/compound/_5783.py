'''_5783.py

BeltConnectionCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1944, _1949
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5599
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5839
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'BeltConnectionCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionCompoundHarmonicAnalysis',)


class BeltConnectionCompoundHarmonicAnalysis(_5839.InterMountableComponentConnectionCompoundHarmonicAnalysis):
    '''BeltConnectionCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1944.BeltConnection':
        '''BeltConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1944.BeltConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BeltConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1944.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1944.BeltConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BeltConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5599.BeltConnectionHarmonicAnalysis]':
        '''List[BeltConnectionHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5599.BeltConnectionHarmonicAnalysis))
        return value

    @property
    def connection_harmonic_analysis_load_cases(self) -> 'List[_5599.BeltConnectionHarmonicAnalysis]':
        '''List[BeltConnectionHarmonicAnalysis]: 'ConnectionHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionHarmonicAnalysisLoadCases, constructor.new(_5599.BeltConnectionHarmonicAnalysis))
        return value
