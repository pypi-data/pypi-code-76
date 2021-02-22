'''_5519.py

GearMeshCompoundHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5525
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'GearMeshCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshCompoundHarmonicAnalysisOfSingleExcitation',)


class GearMeshCompoundHarmonicAnalysisOfSingleExcitation(_5525.InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation):
    '''GearMeshCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
