'''_5351.py

ClutchConnectionHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.connections_and_sockets.couplings import _2018
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6464
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5367
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'ClutchConnectionHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionHarmonicAnalysisOfSingleExcitation',)


class ClutchConnectionHarmonicAnalysisOfSingleExcitation(_5367.CouplingConnectionHarmonicAnalysisOfSingleExcitation):
    '''ClutchConnectionHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2018.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6464.ClutchConnectionLoadCase':
        '''ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6464.ClutchConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
