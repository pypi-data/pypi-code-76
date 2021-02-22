'''_5853.py

PartCompoundHarmonicAnalysis
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7176
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'PartCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundHarmonicAnalysis',)


class PartCompoundHarmonicAnalysis(_7176.PartCompoundAnalysis):
    '''PartCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
