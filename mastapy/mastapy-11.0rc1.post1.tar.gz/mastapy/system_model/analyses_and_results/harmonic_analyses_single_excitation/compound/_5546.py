'''_5546.py

PointLoadCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model import _2144
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5417
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5582
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'PointLoadCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundHarmonicAnalysisOfSingleExcitation',)


class PointLoadCompoundHarmonicAnalysisOfSingleExcitation(_5582.VirtualComponentCompoundHarmonicAnalysisOfSingleExcitation):
    '''PointLoadCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_5417.PointLoadHarmonicAnalysisOfSingleExcitation]':
        '''List[PointLoadHarmonicAnalysisOfSingleExcitation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5417.PointLoadHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def component_harmonic_analysis_of_single_excitation_load_cases(self) -> 'List[_5417.PointLoadHarmonicAnalysisOfSingleExcitation]':
        '''List[PointLoadHarmonicAnalysisOfSingleExcitation]: 'ComponentHarmonicAnalysisOfSingleExcitationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisOfSingleExcitationLoadCases, constructor.new(_5417.PointLoadHarmonicAnalysisOfSingleExcitation))
        return value
