'''_5548.py

PulleyCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2261, _2258
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5419
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5499
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'PulleyCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundHarmonicAnalysisOfSingleExcitation',)


class PulleyCompoundHarmonicAnalysisOfSingleExcitation(_5499.CouplingHalfCompoundHarmonicAnalysisOfSingleExcitation):
    '''PulleyCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _PULLEY_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2261.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2261.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5419.PulleyHarmonicAnalysisOfSingleExcitation]':
        '''List[PulleyHarmonicAnalysisOfSingleExcitation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5419.PulleyHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def component_harmonic_analysis_of_single_excitation_load_cases(self) -> 'List[_5419.PulleyHarmonicAnalysisOfSingleExcitation]':
        '''List[PulleyHarmonicAnalysisOfSingleExcitation]: 'ComponentHarmonicAnalysisOfSingleExcitationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisOfSingleExcitationLoadCases, constructor.new(_5419.PulleyHarmonicAnalysisOfSingleExcitation))
        return value
