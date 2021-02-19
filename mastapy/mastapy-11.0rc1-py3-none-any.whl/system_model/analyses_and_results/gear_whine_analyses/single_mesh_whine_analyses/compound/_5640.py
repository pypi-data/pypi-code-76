'''_5640.py

CVTCompoundSingleMeshWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _5609
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'CVTCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundSingleMeshWhineAnalysis',)


class CVTCompoundSingleMeshWhineAnalysis(_5609.BeltDriveCompoundSingleMeshWhineAnalysis):
    '''CVTCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
