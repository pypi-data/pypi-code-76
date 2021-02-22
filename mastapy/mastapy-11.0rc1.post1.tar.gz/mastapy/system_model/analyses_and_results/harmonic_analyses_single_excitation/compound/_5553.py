'''_5553.py

RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1968
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5423
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5525
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation',)


class RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation(_5525.InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation):
    '''RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1968.RollingRingConnection':
        '''RollingRingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.RollingRingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1968.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5423.RollingRingConnectionHarmonicAnalysisOfSingleExcitation]':
        '''List[RollingRingConnectionHarmonicAnalysisOfSingleExcitation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5423.RollingRingConnectionHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def connection_harmonic_analysis_of_single_excitation_load_cases(self) -> 'List[_5423.RollingRingConnectionHarmonicAnalysisOfSingleExcitation]':
        '''List[RollingRingConnectionHarmonicAnalysisOfSingleExcitation]: 'ConnectionHarmonicAnalysisOfSingleExcitationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionHarmonicAnalysisOfSingleExcitationLoadCases, constructor.new(_5423.RollingRingConnectionHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation))
        return value
