'''_5777.py

AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5809
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis',)


class AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis(_5809.ConnectionCompoundHarmonicAnalysis):
    '''AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
