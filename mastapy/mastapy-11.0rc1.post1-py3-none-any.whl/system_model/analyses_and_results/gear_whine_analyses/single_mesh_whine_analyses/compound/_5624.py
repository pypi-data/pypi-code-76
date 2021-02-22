'''_5624.py

ComponentCompoundSingleMeshWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _5674
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'ComponentCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentCompoundSingleMeshWhineAnalysis',)


class ComponentCompoundSingleMeshWhineAnalysis(_5674.PartCompoundSingleMeshWhineAnalysis):
    '''ComponentCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
