'''_5791.py

BevelGearMeshCompoundHarmonicAnalysis
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5779
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'BevelGearMeshCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearMeshCompoundHarmonicAnalysis',)


class BevelGearMeshCompoundHarmonicAnalysis(_5779.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis):
    '''BevelGearMeshCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearMeshCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
