'''_5839.py

InterMountableComponentConnectionCompoundHarmonicAnalysis
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5809
from mastapy._internal.python_net import python_net_import

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'InterMountableComponentConnectionCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('InterMountableComponentConnectionCompoundHarmonicAnalysis',)


class InterMountableComponentConnectionCompoundHarmonicAnalysis(_5809.ConnectionCompoundHarmonicAnalysis):
    '''InterMountableComponentConnectionCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'InterMountableComponentConnectionCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
