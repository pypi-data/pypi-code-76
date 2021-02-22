'''_5860.py

PointLoadCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2144
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5701
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5896
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'PointLoadCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundHarmonicAnalysis',)


class PointLoadCompoundHarmonicAnalysis(_5896.VirtualComponentCompoundHarmonicAnalysis):
    '''PointLoadCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2144.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2144.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5701.PointLoadHarmonicAnalysis]':
        '''List[PointLoadHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5701.PointLoadHarmonicAnalysis))
        return value

    @property
    def component_harmonic_analysis_load_cases(self) -> 'List[_5701.PointLoadHarmonicAnalysis]':
        '''List[PointLoadHarmonicAnalysis]: 'ComponentHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisLoadCases, constructor.new(_5701.PointLoadHarmonicAnalysis))
        return value
