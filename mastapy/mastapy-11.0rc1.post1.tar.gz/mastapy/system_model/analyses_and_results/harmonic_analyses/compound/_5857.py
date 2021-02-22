'''_5857.py

PlanetaryConnectionCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1963
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5698
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5871
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'PlanetaryConnectionCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionCompoundHarmonicAnalysis',)


class PlanetaryConnectionCompoundHarmonicAnalysis(_5871.ShaftToMountableComponentConnectionCompoundHarmonicAnalysis):
    '''PlanetaryConnectionCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1963.PlanetaryConnection':
        '''PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1963.PlanetaryConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1963.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1963.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5698.PlanetaryConnectionHarmonicAnalysis]':
        '''List[PlanetaryConnectionHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5698.PlanetaryConnectionHarmonicAnalysis))
        return value

    @property
    def connection_harmonic_analysis_load_cases(self) -> 'List[_5698.PlanetaryConnectionHarmonicAnalysis]':
        '''List[PlanetaryConnectionHarmonicAnalysis]: 'ConnectionHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionHarmonicAnalysisLoadCases, constructor.new(_5698.PlanetaryConnectionHarmonicAnalysis))
        return value
