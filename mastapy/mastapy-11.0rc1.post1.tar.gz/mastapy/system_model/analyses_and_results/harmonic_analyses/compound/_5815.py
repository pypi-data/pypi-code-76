'''_5815.py

CVTCompoundHarmonicAnalysis
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5784
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'CVTCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundHarmonicAnalysis',)


class CVTCompoundHarmonicAnalysis(_5784.BeltDriveCompoundHarmonicAnalysis):
    '''CVTCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
