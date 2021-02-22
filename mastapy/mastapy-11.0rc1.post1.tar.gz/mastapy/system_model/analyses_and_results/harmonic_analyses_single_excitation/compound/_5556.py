'''_5556.py

ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2269
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5427
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5496
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation',)


class ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation(_5496.ConnectorCompoundHarmonicAnalysisOfSingleExcitation):
    '''ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2269.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2269.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5427.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation]':
        '''List[ShaftHubConnectionHarmonicAnalysisOfSingleExcitation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5427.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def component_harmonic_analysis_of_single_excitation_load_cases(self) -> 'List[_5427.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation]':
        '''List[ShaftHubConnectionHarmonicAnalysisOfSingleExcitation]: 'ComponentHarmonicAnalysisOfSingleExcitationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisOfSingleExcitationLoadCases, constructor.new(_5427.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation))
        return value
