'''_5780.py

AGMAGleasonConicalGearSetCompoundHarmonicAnalysis
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5808
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'AGMAGleasonConicalGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearSetCompoundHarmonicAnalysis',)


class AGMAGleasonConicalGearSetCompoundHarmonicAnalysis(_5808.ConicalGearSetCompoundHarmonicAnalysis):
    '''AGMAGleasonConicalGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearSetCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
