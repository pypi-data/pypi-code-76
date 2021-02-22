'''_5715.py

VirtualComponentCompoundSingleMeshWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _5672
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'VirtualComponentCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponentCompoundSingleMeshWhineAnalysis',)


class VirtualComponentCompoundSingleMeshWhineAnalysis(_5672.MountableComponentCompoundSingleMeshWhineAnalysis):
    '''VirtualComponentCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VirtualComponentCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
