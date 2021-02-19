'''_5654.py

GearSetCompoundSingleMeshWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _5691
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'GearSetCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetCompoundSingleMeshWhineAnalysis',)


class GearSetCompoundSingleMeshWhineAnalysis(_5691.SpecialisedAssemblyCompoundSingleMeshWhineAnalysis):
    '''GearSetCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
