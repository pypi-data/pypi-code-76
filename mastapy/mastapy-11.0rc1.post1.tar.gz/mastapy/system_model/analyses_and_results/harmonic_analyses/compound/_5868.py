'''_5868.py

RootAssemblyCompoundHarmonicAnalysis
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5781
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'RootAssemblyCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyCompoundHarmonicAnalysis',)


class RootAssemblyCompoundHarmonicAnalysis(_5781.AssemblyCompoundHarmonicAnalysis):
    '''RootAssemblyCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
