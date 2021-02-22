'''_5552.py

RollingRingCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2267
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5424
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5499
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'RollingRingCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundHarmonicAnalysisOfSingleExcitation',)


class RollingRingCompoundHarmonicAnalysisOfSingleExcitation(_5499.CouplingHalfCompoundHarmonicAnalysisOfSingleExcitation):
    '''RollingRingCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2267.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2267.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5424.RollingRingHarmonicAnalysisOfSingleExcitation]':
        '''List[RollingRingHarmonicAnalysisOfSingleExcitation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5424.RollingRingHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def component_harmonic_analysis_of_single_excitation_load_cases(self) -> 'List[_5424.RollingRingHarmonicAnalysisOfSingleExcitation]':
        '''List[RollingRingHarmonicAnalysisOfSingleExcitation]: 'ComponentHarmonicAnalysisOfSingleExcitationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisOfSingleExcitationLoadCases, constructor.new(_5424.RollingRingHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[RollingRingCompoundHarmonicAnalysisOfSingleExcitation]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingCompoundHarmonicAnalysisOfSingleExcitation))
        return value
