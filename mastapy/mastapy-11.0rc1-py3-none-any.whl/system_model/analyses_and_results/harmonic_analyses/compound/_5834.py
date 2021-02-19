'''_5834.py

GearSetCompoundHarmonicAnalysis
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5872
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'GearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetCompoundHarmonicAnalysis',)


class GearSetCompoundHarmonicAnalysis(_5872.SpecialisedAssemblyCompoundHarmonicAnalysis):
    '''GearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
