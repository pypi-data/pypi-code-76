'''_6040.py

GearMeshCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6047
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'GearMeshCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshCompoundDynamicAnalysis',)


class GearMeshCompoundDynamicAnalysis(_6047.InterMountableComponentConnectionCompoundDynamicAnalysis):
    '''GearMeshCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
