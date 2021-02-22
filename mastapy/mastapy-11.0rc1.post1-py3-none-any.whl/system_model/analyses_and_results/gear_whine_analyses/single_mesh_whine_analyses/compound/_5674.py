'''_5674.py

PartCompoundSingleMeshWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _6562
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'PartCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundSingleMeshWhineAnalysis',)


class PartCompoundSingleMeshWhineAnalysis(_6562.PartCompoundAnalysis):
    '''PartCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
