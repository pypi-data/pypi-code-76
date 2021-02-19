'''_5753.py

FESurfaceResultSelection
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses.results import _5760
from mastapy._internal.python_net import python_net_import

_FE_SURFACE_RESULT_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results', 'FESurfaceResultSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('FESurfaceResultSelection',)


class FESurfaceResultSelection(_5760.ResultNodeSelection):
    '''FESurfaceResultSelection

    This is a mastapy class.
    '''

    TYPE = _FE_SURFACE_RESULT_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FESurfaceResultSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
